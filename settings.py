# at time of writing, commonscontrol.harleyschool.org has the IP address '208.99.242.111'

################
## SQL SERVER ##
################

# credentials (username and password) are stored on the server in a protected file
sql_credentials = "/home/dataupload/sql_creds.txt"

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

sma_host = "10.1.6.201"
sma_port = 80
# NOTE: According to the RPC manual, sma_log_interval cannot be
# less than 30 seconds
sma_log_interval = 10*60 # 10 minutes

#######################
## ELECTRIC SETTINGS ##
#######################

veris_host = "10.1.6.202"
veris_port = 80
veris_uname = "user"

##################
# VPMXP settings #
##################

url3 = 'http://commonscontrol.harleyschool.org/electric/setup/devicexml.cgi?ADDRESS=3&TYPE=DATA' #TODO use harley intranet ip's here
url4 = 'http://commonscontrol.harleyschool.org/electric/setup/devicexml.cgi?ADDRESS=4&TYPE=DATA'

##############################
## WEATHER STATION SETTINGS ##
##############################

weather_host = "10.1.6.203"
weather_port = 22222
