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

# ELECTRIC MIGRATION

# 0003 (deletion ended up ok, but maybe more safe to answer 'no' then manually drop unnecessary tables)
# 0004 add FK fields

UPDATE `electric-summary` SET `panel_id`=(SELECT `id` FROM `electric_panel` WHERE `electric_panel`.`veris_id`=CONVERT(SUBSTRING_INDEX(`electric-summary`.`panel`,"Panel ", -1), UNSIGNED INT));
UPDATE `electric-circuits` SET `circuit`=(SELECT `id` FROM `electric_circuit` WHERE `electric_circuit`.`panel_id`=-1+CONVERT(SUBSTRING_INDEX(`electric-circuits`.`panel`,"Panel ", -1), UNSIGNED INT) AND `electric_circuit`.`name`=`electric-circuits`.`channel`);
# ^  354250 rows affected (26.75 sec)

# 0005 remove old string fields, update uniqueness constraints