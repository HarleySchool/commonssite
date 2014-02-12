#####################
## GLOBAL SETTINGS ##
#####################

global_max_log_interval = 30*60; # all logs may only be *more frequent* than this limit. This is to prevent accidentally not logging data for long periods of time
global_min_log_interval = 10; # all logs may only be less frequent than this. prevents overly taxing the server and queries

################
## SQL SERVER ##
################

sql_server = "commonscontrol.harleyschool.org/mysql"
sql_user = ""

###################
## HVAC SETTINGS ##
###################

hvac_host = "10.1.6.200"
hvac_port = 80
hvac_log_interval = 10*60 # 10 minutes

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

##############################
## WEATHER STATION SETTINGS ##
##############################

weather_host = "10.1.6.203"
weather_port = 22222