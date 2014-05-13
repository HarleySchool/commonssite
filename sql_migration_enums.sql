# HVAC MIGRATION
# BACKUP! BACKUP! BACKUP!
# 0004 handled by fixtures
# 0005
UPDATE `hvac-vrf` SET NameIndex_id=(SELECT id FROM hvac_rooms where hvac_rooms.name=`hvac-vrf`.name),
AirDirectionIndex_id=(SELECT id from hvac_fandirections where hvac_fandirections.value=`hvac-vrf`.`air direction`),
FanSpeedIndex_id=(SELECT id from hvac_fanspeeds where hvac_fanspeeds.value=`hvac-vrf`.`fan speed`),
ModeIndex_id=(SELECT id from hvac_modes where hvac_modes.value=`hvac-vrf`.`mode`);

UPDATE `hvac-erv` SET NameIndex_id=(SELECT id FROM hvac_rooms where hvac_rooms.name=`hvac-erv`.name),
AirDirectionIndex_id=(SELECT id from hvac_fandirections where hvac_fandirections.value=`hvac-erv`.`air direction`),
FanSpeedIndex_id=(SELECT id from hvac_fanspeeds where hvac_fanspeeds.value=`hvac-erv`.`fan speed`),
ModeIndex_id=(SELECT id from hvac_modes where hvac_modes.value=`hvac-erv`.`mode`);

# these next two do the name swapping
# 0006
# 0007

