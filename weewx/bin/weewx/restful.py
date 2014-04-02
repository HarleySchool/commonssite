#
#    Copyright (c) 2009, 2012 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
#    $Revision: 1561 $
#    $Author: tkeffer $
#    $Date: 2013-10-21 11:51:51 -0400 (Mon, 21 Oct 2013) $
#
"""Publish weather data to RESTful sites such as the Weather Underground or PWSWeather."""
from __future__ import with_statement
import syslog
import datetime
import threading
import httplib
import urllib
import urllib2
import socket
import time
import platform
import re
import sys

import weewx.archive
import weewx.units
import weeutil.weeutil

site_url = {'Wunderground' : "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?",
            'PWSweather'   : "http://www.pwsweather.com/pwsupdate/pwsupdate.php?",
            'WOW'          : "http://wow.metoffice.gov.uk/automaticreading?"} 

class FailedPost(IOError):
    """Raised when a post fails, usually because of a login problem"""

class SkippedPost(Exception):
    """Raised when a post is skipped."""

#===============================================================================
#                          Abstract base class REST
#===============================================================================

class REST(object):
    """Abstract base class for RESTful protocols."""
    
    # The types to be retrieved from the archive database:
    archive_types = ['dateTime', 'usUnits', 'altimeter', 'barometer', 'outTemp', 'outHumidity', 
                     'windSpeed', 'windDir', 'windGust', 'windGustDir', 'dewpoint', 'radiation', 'UV']
    # A SQL statement to do the retrieval:
    sql_select = "SELECT " + ", ".join(archive_types) + " FROM archive WHERE dateTime=?"  

    def extractRecordFrom(self, archive, time_ts):
        """Get a record from the archive database. 
        
        This is a general version that works for:
          - WeatherUnderground
          - PWSweather
          - CWOP
        It can be overridden and specialized for additional protocols.
        
        archive: An instance of weewx.archive.Archive
        
        time_ts: The record desired as a unix epoch time.
        
        returns: A dictionary of weather values"""
        
        sod_ts = weeutil.weeutil.startOfDay(time_ts)
        
        # Get the data record off the archive database:
        sqlrec = archive.getSql(REST.sql_select, (time_ts,))
        # There is no reason why the record would not be in the database,
        # but check just in case:
        if sqlrec is None:
            raise SkippedPost("Non existent record %s" % (weeutil.weeutil.timestamp_to_string(time_ts),))

        # Make a dictionary out of the types:
        datadict = dict(zip(REST.archive_types, sqlrec))
        
        # CWOP says rain should be "rain that fell in the past hour".  WU says
        # it should be "the accumulated rainfall in the past 60 min".
        # Presumably, this is exclusive of the archive record 60 minutes before,
        # so the SQL statement is exclusive on the left, inclusive on the right.
        datadict['hourRain'] = archive.getSql("SELECT SUM(rain) FROM archive WHERE dateTime>? AND dateTime<=?",
                                         (time_ts - 3600.0, time_ts))[0]

        # Similar issue, except for last 24 hours:
        datadict['rain24'] = archive.getSql("SELECT SUM(rain) FROM archive WHERE dateTime>? AND dateTime<=?",
                                            (time_ts - 24*3600.0, time_ts))[0]

        # NB: The WU considers the archive with time stamp 00:00 (midnight) as
        # (wrongly) belonging to the current day (instead of the previous
        # day). But, it's their site, so we'll do it their way.  That means the
        # SELECT statement is inclusive on both time ends:
        datadict['dayRain'] = archive.getSql("SELECT SUM(rain) FROM archive WHERE dateTime>=? AND dateTime<=?", 
                                              (sod_ts, time_ts))[0]

        # All these online weather sites require US units. 
        if datadict['usUnits'] == weewx.US:
            # It's already in US units.
            return datadict
        else:
            # It's in something else. Perform the conversion
            datadict_us = weewx.units.StdUnitConverters[weewx.US].convertDict(datadict)
            # Add the new unit system
            datadict_us['usUnits'] = weewx.US
            return datadict_us
        
#===============================================================================
#                             class Ambient
#===============================================================================

class Ambient(REST):
    """Upload using the Ambient protocol. 
    
    For details of the Ambient upload protocol,
    see http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
    
    For details on how urllib2 works, see "urllib2 - The Missing Manual"
    at http://www.voidspace.org.uk/python/articles/urllib2.shtml
    """

    # Types and formats of the data to be published:
    _formats = {'dateTime'    : 'dateutc=%s',
                'barometer'   : 'baromin=%.3f',
                'outTemp'     : 'tempf=%.1f',
                'outHumidity' : 'humidity=%03.0f',
                'windSpeed'   : 'windspeedmph=%03.0f',
                'windDir'     : 'winddir=%03.0f',
                'windGust'    : 'windgustmph=%03.0f',
                'dewpoint'    : 'dewptf=%.1f',
                'hourRain'    : 'rainin=%.2f',
                'dayRain'     : 'dailyrainin=%.2f',
                'radiation'   : 'solarradiation=%.2f',
                'UV'          : 'UV=%.2f'}


    def __init__(self, site, **kwargs):
        """Initialize for a given upload site.
        
        site: The upload site ('Wunderground' or 'PWSweather')
        
        station: The name of the station (e.g., "KORHOODR3") 
        as a string [Required]
        
        password: Password for the station [Required]
        
        http_prefix: The URL of the upload point [Optional. If not
        given a prefix will be chosen on the basis of the upload site.
        
        max_tries: Max # of tries before giving up [Optional. Default
        is 3]"""
        
        self.site        = site
        self.station     = kwargs['station']
        self.password    = kwargs['password']
        self.http_prefix = kwargs.get('http_prefix', site_url[site])
        self.max_tries   = int(kwargs.get('max_tries', 3))

    def postData(self, archive, time_ts):
        """Post using the Ambient HTTP protocol

        archive: An instance of weewx.archive.Archive
        
        time_ts: The record desired as a unix epoch time."""
        
        _url = self.getURL(archive, time_ts)

        # Retry up to max_tries times:
        for _count in range(self.max_tries):
            # Now use an HTTP GET to post the data. Wrap in a try block
            # in case there's a network problem.
            try:
                _response = urllib2.urlopen(_url)
            except (urllib2.URLError, socket.error, httplib.BadStatusLine), e:
                # Unsuccessful. Log it and go around again for another try
                syslog.syslog(syslog.LOG_ERR, "restful: Failed attempt #%d to upload to %s" % (_count+1, self.site))
                syslog.syslog(syslog.LOG_ERR, "   ****  Reason: %s" % (e,))
            else:
                # No exception thrown, but we're still not done.
                # We have to also check for a bad station ID or password.
                # It will have the error encoded in the return message:
                for line in _response:
                    # PWSweather signals with 'ERROR', WU with 'INVALID':
                    if line.startswith('ERROR') or line.startswith('INVALID'):
                        # Bad login. No reason to retry. Log it and raise an exception.
                        syslog.syslog(syslog.LOG_ERR, "restful: %s returns %s. Aborting." % (self.site, line))
                        raise FailedPost, line
                # Does not seem to be an error. We're done.
                return
        else:
            # This is executed only if the loop terminates normally, meaning
            # the upload failed max_tries times. Log it.
            syslog.syslog(syslog.LOG_ERR, "restful: Failed to upload to %s" % self.site)
            raise IOError, "Failed upload to site %s after %d tries" % (self.site, self.max_tries)

    def getURL(self, archive, time_ts):

        """Return an URL for posting using the Ambient protocol.
        
        archive: An instance of weewx.archive.Archive
        
        time_ts: The record desired as a unix epoch time.
        """
    
        record = self.extractRecordFrom(archive, time_ts)
        
        _liststr = ["action=updateraw", "ID=%s" % self.station, "PASSWORD=%s" % self.password ]
        
        # Go through each of the supported types, formatting it, then adding to _liststr:
        for _key in Ambient._formats:
            v = record[_key]
            # Check to make sure the type is not null
            if v is not None :
                if _key == 'dateTime':
                    # For dates, convert from time stamp to a string, using what
                    # the Weather Underground calls "MySQL format." I've fiddled
                    # with formatting, and it seems that escaping the colons helps
                    # its reliability. But, I could be imagining things.
                    v = urllib.quote(datetime.datetime.utcfromtimestamp(v).isoformat('+'), '-+')
                # Format the value, and accumulate in _liststr:
                _liststr.append(Ambient._formats[_key] % v)
        # Add the software type and version:
        _liststr.append("softwaretype=weewx-%s" % weewx.__version__)
        # Now stick all the little pieces together with an ampersand between them:
        _urlquery='&'.join(_liststr)
        # This will be the complete URL for the HTTP GET:
        _url=self.http_prefix + _urlquery
        return _url

#===============================================================================
#                             class WOW
#===============================================================================

class WOW(Ambient):

    """Upload using the WOW protocol. 
    
    For details of the WOW upload protocol,
    see http://wow.metoffice.gov.uk/support?category=dataformats#dataFileUpload
    
    For details on how urllib2 works, see "urllib2 - The Missing Manual"
    at http://www.voidspace.org.uk/python/articles/urllib2.shtml
    """

    # Types and formats of the data to be published:
    _formats = {'dateTime'    : 'dateutc=%s',
                'barometer'   : 'baromin=%.1f',
                'outTemp'     : 'tempf=%.1f',
                'outHumidity' : 'humidity=%.0f',
                'windSpeed'   : 'windspeedmph=%.0f',
                'windDir'     : 'winddir=%.0f',
                'windGust'    : 'windgustmph=%.0f',
                'windGustDir' : 'windgustdir=%.0f',
                'dewpoint'    : 'dewptf=%.1f',
                'hourRain'    : 'rainin=%.2f',
                'dayRain'     : 'dailyrainin=%.2f'}

    def postData(self, archive, time_ts):
        """Post using the WOW HTTP protocol

        archive: An instance of weewx.archive.Archive
        
        time_ts: The record desired as a unix epoch time."""
        
        _url = self.getURL(archive, time_ts)

        # Retry up to max_tries times:
        for _count in range(self.max_tries):
            # Now use an HTTP GET to post the data. Wrap in a try block
            # in case there's a network problem.
            try:
                _response = urllib2.urlopen(_url)
            except (urllib2.URLError, socket.error, httplib.BadStatusLine), e:
                # Unsuccessful. Log it and go around again for another try
                syslog.syslog(syslog.LOG_ERR,   "restful: Failed attempt #%d to upload to %s" % (_count+1, self.site))
                syslog.syslog(syslog.LOG_ERR,   "   ****  Reason: %s" % (e,))
                syslog.syslog(syslog.LOG_DEBUG, "url used: %s" % (_url))
            else:
                # No exception thrown, but we're still not done.
                # We have to also check for a bad station ID or password.
                # It will have the error encoded in the return message:
                for line in _response:
                    # WOW signals success with '200'
                    if not line.startswith('200'):
                        # Bad login. No reason to retry. Log it and raise an exception.
                        syslog.syslog(syslog.LOG_ERR, "restful: %s returns %s. Aborting." % (self.site, line))
                        raise FailedPost, line
                # Does not seem to be an error. We're done.
                return
        else:
            # This is executed only if the loop terminates normally, meaning
            # the upload failed max_tries times. Log it.
            syslog.syslog(syslog.LOG_ERR, "restful: Failed to upload to %s" % self.site)
            raise IOError, "Failed upload to site %s after %d tries" % (self.site, self.max_tries)

    def getURL(self, archive, time_ts):

        """Return an URL for posting using the WOW protocol.
        
        archive: An instance of weewx.archive.Archive
        
        time_ts: The record desired as a unix epoch time.
        """
    
        record = self.extractRecordFrom(archive, time_ts)
        
        _liststr = ["siteid=%s" % self.station, "siteAuthenticationKey=%s" % self.password ]
        
        # Go through each of the supported types, formatting it, then adding to _liststr:
        for _key in WOW._formats:
            v = record[_key]
            # Check to make sure the type is not null
            if v is not None :
                if _key == 'dateTime':
                    # For dates, convert from time stamp to a string, using 
                    # the following format: YYYY-mm-DD HH:mm:ss, where ':' 
                    # is encoded as %3A, and the space is encoded as either '+' or %20
                    v = urllib.quote(datetime.datetime.utcfromtimestamp(v).isoformat('+'), '-+')
                # Format the value, and accumulate in _liststr:
                _liststr.append(WOW._formats[_key] % v)
        # Add the software type and version:
        _liststr.append("softwaretype=weewx-%s" % weewx.__version__)
        # Now stick all the little pieces together with an ampersand between them:
        _urlquery='&'.join(_liststr)
        # This will be the complete URL for the HTTP GET:
        _url=self.http_prefix + _urlquery
        return _url

#===============================================================================
#                             class CWOP
#===============================================================================

class CWOP(REST):
    """Upload using the CWOP protocol. """
    
    # Station IDs must start with one of these:
    valid_prefixes = ['CW', 'DW', 'EW']

    def __init__(self, site, **kwargs):
        """Initialize for a post to CWOP.
        
        site: The upload site ("CWOP")
        
        station: The name of the station (e.g., "CW1234") as a string [Required]
        
        server: List of APRS servers and ports in the 
        form cwop.aprs.net:14580 [Required]
         
        latitude: Station latitude [Required]
        
        longitude: Station longitude [Required]

        hardware: Station hardware (eg, "VantagePro") [Required]
        
        passcode: Passcode for your station [Optional. APRS only]
        
        interval: The interval in seconds between posts [Optional. 
        Default is 0 (send every post)]
        
        stale: How old a record can be before it will not be 
        used for a catchup [Optional. Default is 1800]
        
        max_tries: Max # of tries before giving up [Optional. Default is 3]

        CWOP does not like heavy traffic on their servers, so they encourage
        posts roughly every 15 minutes and at most every 5 minutes. So,
        key 'interval' should be set to no less than 300, but preferably 900.
        Setting it to zero will cause every archive record to be posted.
        """
        self.site      = site
        self.station   = kwargs['station'].upper()
        if self.station[0:2] in CWOP.valid_prefixes:
            self.passcode = "-1"
        else:
            self.passcode = kwargs['passcode']
        self.server    = weeutil.weeutil.option_as_list(kwargs['server'])
        self.latitude  = float(kwargs['latitude'])
        self.longitude = float(kwargs['longitude'])
        self.hardware  = kwargs['hardware']
        self.interval  = int(kwargs.get('interval', 0))
        self.stale     = int(kwargs.get('stale', 1800))
        self.max_tries = int(kwargs.get('max_tries', 3))
        
        self._lastpost = None
        
    def postData(self, archive, time_ts):
        """Post data to CWOP, using the CWOP protocol."""
        
        _last_ts = archive.lastGoodStamp()

        # There are a variety of reasons to skip a post to CWOP.

        # 1. They do not allow backfilling, so there is no reason
        # to post anything other than the latest record:
        if time_ts != _last_ts:
            raise SkippedPost, "CWOP: Record %s is not last record" %\
                    (weeutil.weeutil.timestamp_to_string(time_ts), )

        # 2. No reason to post an old out-of-date record.
        _how_old = time.time() - time_ts
        if self.stale and _how_old > self.stale:
            raise SkippedPost, "CWOP: Record %s is stale (%d > %d)." %\
                    (weeutil.weeutil.timestamp_to_string(time_ts), _how_old, self.stale)
        
        # 3. Finally, we don't want to post more often than the interval
        if self._lastpost and time_ts - self._lastpost < self.interval:
            raise SkippedPost, "CWOP: Wait interval (%d) has not passed." %\
                    (self.interval, )
        
        # Get the data record for this time:
        _record = self.extractRecordFrom(archive, time_ts)

        # Send it to its destination:
        self.sendRecord(_record)

        self._lastpost = time_ts

    def sendRecord(self, record):
        """This method sends the record to its destination.
        If you have some exotic setup, such as a ham radio TNC, it
        can be overridden and customized to send the record out whatever
        port it needs to go.
        
        This version sends it out a socket."""
        
        # Get the login and packet strings:
        _login = self.getLoginString()
        _tnc_packet = self.getTNCPacket(record)

        # Get a socket connection:
        _sock = self._get_connect()

        # Send the login:
        self._send(_sock, _login)

        # And now the packet
        self._send(_sock, _tnc_packet)
        
        try:
            _sock.close()
        except:
            pass
    
    def getLoginString(self):
        login = "user %s pass %s vers weewx %s\r\n" % (self.station, self.passcode, weewx.__version__ )
        return login
    
    def getTNCPacket(self, record):
        """Form the TNC2 packet used by CWOP."""
        
        # Preamble to the TNC packet:
        prefix = "%s>APRS,TCPIP*:" % (self.station, )

        # Time:
        time_tt = time.gmtime(record['dateTime'])
        time_str = time.strftime("@%d%H%Mz", time_tt)

        # Position:
        lat_str = weeutil.weeutil.latlon_string(self.latitude, ('N', 'S'), 'lat')
        lon_str = weeutil.weeutil.latlon_string(self.longitude, ('E', 'W'), 'lon')
        latlon_str = '%s%s%s/%s%s%s' % (lat_str + lon_str)

        # Wind and temperature
        wt_list = []
        for obs_type in ('windDir', 'windSpeed', 'windGust', 'outTemp'):
            wt_list.append("%03d" % record[obs_type] if record[obs_type] is not None else '...')
        wt_str = "_%s/%sg%st%s" % tuple(wt_list)

        # Rain
        rain_list = []
        for obs_type in ('hourRain', 'rain24', 'dayRain'):
            rain_list.append("%03d" % (record[obs_type]*100.0) if record[obs_type] is not None else '...')
        rain_str = "r%sp%sP%s" % tuple(rain_list)
        
        # Barometer:
        if record['altimeter'] is None:
            baro_str = "b....."
        else:
            # Figure out what unit type barometric pressure is in for this record:
            (u, g) = weewx.units.getStandardUnitType(record['usUnits'], 'altimeter')
            # Convert to millibars:
            baro = weewx.units.convert((record['altimeter'], u, g), 'mbar')
            baro_str = "b%05d" % (baro[0]*10.0)

        # Humidity:
        humidity = record['outHumidity']
        if humidity is None:
            humid_str = "h.."
        else:
            humid_str = ("h%02d" % humidity) if humidity < 100.0 else "h00"
            
        # Radiation:
        radiation = record['radiation']
        if radiation is None:
            radiation_str = ""
        elif radiation < 1000.0:
            radiation_str = "L%03d" % radiation
        elif radiation < 2000.0:
            radiation_str = "l%03d" % (radiation - 1000)
        else:
            radiation_str = ""

        # Station equipment
        equipment_str = ".weewx-%s-%s" % (weewx.__version__, self.hardware)
        
        tnc_packet = prefix + time_str + latlon_str + wt_str + rain_str +\
                     baro_str + humid_str + radiation_str + equipment_str + "\r\n"

        return tnc_packet

    def _get_connect(self):
        
        # Go through the list of known server:ports, looking for
        # a connection that works:
        for serv_addr_str in self.server:
            server, port = serv_addr_str.split(":")
            port = int(port)
            for _count in range(self.max_tries):
                try:
                    sock = socket.socket()
                    sock.connect((server, port))
                except socket.error, e:
                    # Unsuccessful. Log it and try again
                    syslog.syslog(syslog.LOG_ERR, "restful: Connection attempt #%d failed to %s server %s:%d" % (_count+1, self.site, server, port))
                    syslog.syslog(syslog.LOG_ERR, "   ****  Reason: %s" % (e,))
                else:
                    syslog.syslog(syslog.LOG_DEBUG, "restful: Connected to %s server %s:%d" % (self.site, server, port))
                    return sock
                # Couldn't connect on this attempt. Close it, try again.
                try:
                    sock.close()
                except:
                    pass
            # If we got here, that server didn't work. Log it and go on to the next one.
            syslog.syslog(syslog.LOG_ERR, "restful: Unable to connect to %s server %s:%d" % (self.site, server, port))

        # If we got here. None of the servers worked. Raise an exception
        raise IOError, "Unable to obtain a socket connection to %s" % (self.site,)
     
    def _send(self, sock, msg):
        
        for _count in range(self.max_tries):

            try:
                sock.send(msg)
            except (IOError, socket.error), e:
                # Unsuccessful. Log it and go around again for another try
                syslog.syslog(syslog.LOG_ERR, "restful: Attempt #%d failed to send to %s" % (_count+1, self.site))
                syslog.syslog(syslog.LOG_ERR, "   ****  Reason: %s" % (e,))
            else:
                _resp = sock.recv(1024)
                return _resp
        else:
            # This is executed only if the loop terminates normally, meaning
            # the send failed max_tries times. Log it.
            syslog.syslog(syslog.LOG_ERR, "restful: Failed to upload to %s" % self.site)
            raise IOError, "Failed CWOP upload to site %s after %d tries" % (self.site, self.max_tries)


#==============================================================================
# class StationRegistry
#==============================================================================
# Periodically 'phone home' to register a weewx station.
#
#  This will periodically do a http GET with the following information:
#
#    station_url           should be world-accessible
#    description           description of station
#    latitude, longitude   must be in decimal format
#    station_type          for example Vantage, FineOffsetUSB
#
#  The station_url is the unique key by which a station is identified.
#
#  To enable this module, add the following to weewx.conf:
#
# [StdRESTful]
#     ...
#     [[StationRegistry]]
#         register_this_station = True
#         driver = weewx.register.StationRegistry

WEEWX_SERVER_URL = 'http://weewx.com/register/register.cgi'

class StationRegistry(REST):
    """Class for phoning home to register a weewx station."""

    def __init__(self, site, **kwargs):
        """
        register_this_station: indicates whether to run this service
        [Required]

        station_url: URL of the weather station
        [Required]

        description: description of station
        [Optional]

        latitude: station latitude
        [Required]

        longitude: station longitude
        [Required]

        hardware: station hardware
        [Required]

        server_url - site at which to register
        [Optional.  Default is weewx.com]

        interval: time in seconds between posts
        [Optional.  Default is 604800 (once per week)]

        max_tries: number of attempts to make before giving up
        [Optional.  Default is 5]
        """

        # should this service run?
        optin = weeutil.weeutil.tobool(kwargs.get('register_this_station', 'false'))
        if not optin:
            raise KeyError('register_this_station')

        # this uniquely identifies the station
        self.station_url = kwargs.get('station_url', None)
        if self.station_url is None:
            self.station_url = kwargs['station_url']

        # these are defined by RESTful
        self.latitude = float(kwargs['latitude'])
        self.longitude = float(kwargs['longitude'])
        self.hardware = kwargs['hardware']

        # these are optional
        self.server_url = kwargs.get('server_url', WEEWX_SERVER_URL)
        self.interval = int(kwargs.get('interval', 604800))
        self.max_tries = int(kwargs.get('max_tries', 5))
        self.description = kwargs.get('description', None)
        if self.description is None:
            self.description = kwargs.get('location', None)

        self.weewx_info = weewx.__version__
        self.python_info = platform.python_version()
        self.platform_info = platform.platform()
        self._last_ts = None

        # these two must be defined to keep RESTful happy
        self.site = 'StationRegistry'
        self.station = self.station_url

        # adapted from django URLValidator
        self._urlregex = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        self._validateParameters()

        syslog.syslog(syslog.LOG_INFO, 'restful: station will register with %s' % self.server_url)

    def postData(self, archive, time_ts):
        now = time.time()
        if self._last_ts is not None and now - self._last_ts < self.interval:
            msg = 'Registration interval (%d) has not passed.' % self.interval
            syslog.syslog(syslog.LOG_DEBUG, 'restful: %s' % msg)
            raise weewx.restful.SkippedPost, msg

        url = self.getURL()
        for _count in range(self.max_tries):
            # Use HTTP GET to convey the station data
            try:
                syslog.syslog(syslog.LOG_DEBUG, "restful: Attempting to register using '%s'" % url)
                _response = urllib2.urlopen(url)
            except (urllib2.URLError, socket.error,
                    httplib.BadStatusLine, httplib.IncompleteRead), e:
                # Unsuccessful. Log it and try again
                syslog.syslog(syslog.LOG_ERR, 'restful: Failed attempt %d of %d: %e' % (_count+1, self.max_tries, e))
            else:
                # Check for the server response
                for line in _response:
                    # Registration failed, log it and bail out
                    if line.startswith('FAIL'):
                        syslog.syslog(syslog.LOG_ERR, "restful: Registration server returned %s" % line)
                        raise weewx.restful.FailedPost, line
                # Registration was successful
                syslog.syslog(syslog.LOG_DEBUG, 'restful: Registration successful')
                self._last_ts = time.time()
                return
        else:
            # The upload failed max_tries times. Log it.
            msg = 'Failed to register after %d tries' % self.max_tries
            syslog.syslog(syslog.LOG_ERR, 'restful: %s' % msg)
            raise IOError, msg

    def getURL(self):
        args = {
            'station_url' : self.station_url,
            'latitude' : self.latitude,
            'longitude' : self.longitude,
            'station_type' : self.hardware,
            'weewx_info' : self.weewx_info,
            'python_info' : self.python_info,
            'platform_info' : self.platform_info,
            }
        if self.description is not None:
            args['description'] = self.description
        return '%s?%s' % (self.server_url, urllib.urlencode(args))

    def _checkURL(self, url):
        return self._urlregex.search(url)

    def _validateParameters(self):
        msgs = []

        if self.station_url is None:
            # the station url must be defined
            msgs.append("station_url is not defined")
        elif not self._checkURL(self.station_url):
            # ensure the url does not have problem characters.  do not check
            # to see whether the site actually exists.
            msgs.append("station_url '%s' is not a valid URL" %
                        self.station_url)

        # check server url just in case someone modified the default
        url = self.server_url
        if not self._checkURL(url):
            msgs.append("server_url '%s' is not a valid URL" % self.server_url)

        if msgs:
            errmsg = 'One or more unusable parameters.'
            syslog.syslog(syslog.LOG_ERR, 'restful: %s' % errmsg)
            for m in msgs:
                syslog.syslog(syslog.LOG_ERR, '   **** %s' % m)
            # FIXME: restful depends on a hack - throw a KeyError to indicate
            # that a restful service should not start.  here we should throw
            # a ValueError, but that kills StdRESTful instead of simply
            # indicating that this restful service is not ready to run.
            raise KeyError(errmsg)

#===============================================================================
#                             class RESTThread
#===============================================================================

class RESTThread(threading.Thread):
    """Dedicated thread for publishing weather data using RESTful protocol.
    
    Inherits from threading.Thread.

    Basically, it watches a queue, and if anything appears in it, it publishes it.
    The queue should be populated with the timestamps of the data records to be published.
    """
    def __init__(self, archive_db_dict, queue, protocol_list):
        """Initialize an instance of RESTThread.
        
        archive_db_dict: The database dictionary for the archive database  
        
        queue: An instance of Queue.Queue where the timestamps will appear

        protocol_list: An iterable list of RESTful upload sites.
        """
        threading.Thread.__init__(self, name="RESTThread")

        self.archive_db_dict = archive_db_dict
        self.queue           = queue 
        self.protocol_list   = protocol_list
        # In the strange vocabulary of Python, declaring yourself a "daemon thread"
        # allows the program to exit even if this thread is running:
        self.setDaemon(True)

    def run(self):

        # Open up the archive. This cannot be done in the initializer because
        # then the connection would have been created in a different thread.
        # Also, use a 'with' statement. This will automatically close the
        # archive in the case of an exception:
        with weewx.archive.Archive.open(self.archive_db_dict) as self.archive:

            while True :
                # This will block until something appears in the queue:
                time_ts = self.queue.get()
    
                # A 'None' value appearing in the queue is our signal to exit
                if time_ts is None:
                    break
                
                # This string is just used for logging:
                time_str = weeutil.weeutil.timestamp_to_string(time_ts)
                
                # Cycle through all the RESTful stations in the list:
                for protocol in self.protocol_list:
        
                    # Post the data to the upload site. Be prepared to catch any exceptions:
                    try :
                        protocol.postData(self.archive, time_ts)
                    # The urllib2 library throws exceptions of type urllib2.URLError, a subclass
                    # of IOError. Hence all relevant exceptions are caught by catching IOError.
                    # Starting with Python v2.6, socket.error is a subclass of IOError as well,
                    # but we keep them separate to support V2.5:
                    except (IOError, socket.error), e:
                        syslog.syslog(syslog.LOG_ERR, "restful: Unable to publish record %s to %s station %s" % (time_str, protocol.site, protocol.station))
                        syslog.syslog(syslog.LOG_ERR, "   ****  %s" % e)
                        if hasattr(e, 'reason'):
                            syslog.syslog(syslog.LOG_ERR, "   ****  Failed to reach server. Reason: %s" % e.reason)
                        if hasattr(e, 'code'):
                            syslog.syslog(syslog.LOG_ERR, "   ****  Failed to reach server. Error code: %s" % e.code)
                    except SkippedPost, e:
                        syslog.syslog(syslog.LOG_DEBUG, "restful: Skipped record %s to %s station %s" % (time_str, protocol.site, protocol.station))
                        syslog.syslog(syslog.LOG_DEBUG, "   ****  %s" % (e,))
                    except httplib.HTTPException, e:
                        syslog.syslog(syslog.LOG_ERR, "restful: HTTP error from server. Skipped record %s to %s station %s" % (time_str, protocol.site, protocol.station))
                        syslog.syslog(syslog.LOG_ERR, "   ****  %s" % (e,))
                    except Exception, e:
                        syslog.syslog(syslog.LOG_CRIT, "restful: Unrecoverable error when posting record %s to %s station %s" % (time_str, protocol.site, protocol.station))
                        syslog.syslog(syslog.LOG_CRIT, "   ****  %s" % (e,))
                        weeutil.weeutil.log_traceback("   ****  ")
                        syslog.syslog(syslog.LOG_CRIT, "   ****  Thread terminating.")
                        self.archive.close()
                        raise
                    else:
                        syslog.syslog(syslog.LOG_INFO, "restful: Published record %s to %s station %s" % (time_str, protocol.site, protocol.station))


#===============================================================================
#                                 Testing
#===============================================================================

if __name__ == '__main__':
           
    import configobj
    from optparse import OptionParser
    import Queue
    
    def main():
        usage_string ="""Usage: 
        
        restful.py config_path upload-site [--today] [--last]
        
        Arguments:
        
          config_path: Path to weewx.conf
          
          upload-site: Either "Wunderground", "PWSweather", or "CWOP" 
          
        Options:
        
            --today: Publish all of today's data
            
            --last: Just do the last archive record. [default]
          """
        parser = OptionParser(usage=usage_string)
        parser.add_option("-t", "--today", action="store_true", dest="do_today", help="Publish today\'s records")
        parser.add_option("-l", "--last", action="store_true", dest="do_last", help="Publish the last archive record only")
        (options, args) = parser.parse_args()
        
        if len(args) < 2:
            sys.stderr.write("Missing argument(s).\n")
            sys.stderr.write(parser.parse_args(["--help"]))
            exit()
            
        if options.do_today and options.do_last:
            sys.stderr.write("Choose --today or --last, not both\n")
            sys.stderr.write(parser.parse_args(["--help"]))
            exit()
    
        if not options.do_today and not options.do_last:
            options.do_last = True
            
        config_path = args[0]
        site        = args[1]
        
        weewx.debug = 1
        
        try :
            config_dict = configobj.ConfigObj(config_path, file_error=True)
        except IOError:
            print "Unable to open configuration file ", config_path
            exit()
            
        archive_db_dict = config_dict['Databases'][config_dict['StdArchive']['archive_database']]
        with weewx.archive.Archive.open(archive_db_dict) as archive:
            stop_ts  = archive.lastGoodStamp()
            start_ts = weeutil.weeutil.startOfDay(stop_ts) if options.do_today else stop_ts
            publish(config_dict, site, archive, start_ts, stop_ts )

    def publish(config_dict, site, archive, start_ts, stop_ts):
        """Publishes records to site 'site' from start_ts to stop_ts. 
        Makes a useful test."""
        
        archive_db_dict = config_dict['Databases'][config_dict['StdArchive']['archive_database']]

        site_dict = config_dict['StdRESTful'][site]
        site_dict['latitude']  = config_dict['Station']['latitude']
        site_dict['longitude'] = config_dict['Station']['longitude']
        site_dict['hardware']  = config_dict['Station']['station_type']

        stationName = site_dict['station']
        
        # Instantiate an instance of the class that implements the
        # protocol used by this site:
        try:
            station = weeutil.weeutil._get_object(site_dict['driver'])(site, **site_dict)
        except Exception:
            print "Unable to instantiate %s" % (site_dict['driver'],)
            raise 

        # Create the queue into which we'll put the timestamps of new data
        queue = Queue.Queue()
        # Start up the thread:
        thread = RESTThread(archive_db_dict, queue, [station])
        thread.start()

        for row in archive.genSql("SELECT dateTime FROM archive WHERE dateTime >=? and dateTime <= ?", (start_ts, stop_ts)):
            ts = row[0]
            print "Posting station %s for time %s" % (stationName, weeutil.weeutil.timestamp_to_string(ts))
            queue.put(ts)
            
        # Value 'None' signals to the thread to exit:
        queue.put(None)
        # Wait for exit:
        thread.join()
    
    main()
    
