# at time of writing, commonscontrol.harleyschool.org has the IP address '208.99.242.111'
import os
from private import *

################
## SQL SERVER ##
################

# credentials (username and password) are stored on the server in a protected file
sql_credentials = os.path.expanduser("~/code/commonssite/sql_creds.txt")

#####################
## SHARED SETTINGS ##
#####################

datetime_out_format = '%Y-%m-%d %H:%M:%S'
scrapers_settings_sql_table = 'scraper-settings'

###################
## HVAC SETTINGS ##
###################

hvac_host = "10.1.6.200"
hvac_port = 80
hvac_log_interval = 10*60 # 10 minutes
hvac_sql_table_vrf = 'hvac-vrf'
hvac_sql_table_erv = 'hvac-erv'

####################
## SOLAR SETTINGS ##
####################

sma_host = "commonscontrol.harleyschool.org"
sma_port = 80
# NOTE: According to the RPC manual, sma_log_interval cannot be
# less than 30 seconds
sma_log_interval = 10*60 # 10 minutes
sma_sql_table_weather = 'sma-weather'
sma_sql_table_panels = 'sma-panels'
sma_sql_table_overview = 'sma-overview'

#######################
## ELECTRIC SETTINGS ##
#######################

veris_host = "10.1.6.202"
veris_port = 80
veris_uname = "user"
veris_sql_table_channel = 'electric-channel'
veris_sql_table_device = 'electric-summary'
veris_sql_table_map = 'electic-channel-map'

##################
# VPMXP settings #
##################

url2 = 'http://%s/setup/devicexml.cgi?ADDRESS=2&TYPE=DATA' % veris_host
url3 = 'http://%s/setup/devicexml.cgi?ADDRESS=3&TYPE=DATA' % veris_host
url4 = 'http://%s/setup/devicexml.cgi?ADDRESS=4&TYPE=DATA' % veris_host


##############################
## WEATHER STATION SETTINGS ##
##############################

weather_host = "10.1.6.203"
weather_port = 22222
