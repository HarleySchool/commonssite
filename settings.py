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
sma_log_interval = 1*60 # 10 minutes

#######################
## ELECTRIC SETTINGS ##
#######################

veris_host = "10.1.6.202"
veris_port = 80

##############################
## WEATHER STATION SETTINGS ##
##############################

weather_host = "10.1.6.203"
weather_port = 22222