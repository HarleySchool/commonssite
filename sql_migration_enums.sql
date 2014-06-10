# HVAC MIGRATION
# BACKUP! BACKUP! BACKUP!
# Also update the modelregistry channel=>circuit
# 0004 handled by fixtures
# 0005
UPDATE `hvac-vrf` SET NameIndex_id=(SELECT id FROM hvac_rooms where hvac_rooms.name=`hvac-vrf`.name),
AirDirectionIndex_id=(SELECT id from hvac_fandirections where hvac_fandirections.value=`hvac-vrf`.`air direction`),
FanSpeedIndex_id=(SELECT id from hvac_fanspeeds where hvac_fanspeeds.value=`hvac-vrf`.`fan speed`),
ModeIndex_id=(SELECT id from hvac_modes where hvac_modes.value=`hvac-vrf`.`mode`);
-- THIS WAS WAY FASTER THAN EXPECTED WHEN DONE ON THE PRODUCTION SERVER!
-- OUTPUT:
-- Query OK, 162643 rows affected, 15980 warnings (6.05 sec)
-- Rows matched: 162643  Changed: 162643  Warnings: 15980

UPDATE `hvac-erv` SET NameIndex_id=(SELECT id FROM hvac_rooms where hvac_rooms.name=`hvac-erv`.name),
AirDirectionIndex_id=(SELECT id from hvac_fandirections where hvac_fandirections.value=`hvac-erv`.`air direction`),
FanSpeedIndex_id=(SELECT id from hvac_fanspeeds where hvac_fanspeeds.value=`hvac-erv`.`fan speed`),
ModeIndex_id=(SELECT id from hvac_modes where hvac_modes.value=`hvac-erv`.`mode`);
-- OUTPUT:
-- Query OK, 61585 rows affected, 9975 warnings (2.37 sec)
-- Rows matched: 61585  Changed: 61585  Warnings: 9975

# these next two do the name swapping
# 0006
# 0007

# ELECTRIC MIGRATION

# 0003 (deletion ended up ok, but maybe more safe to answer 'no' then manually drop unnecessary tables)
# 0004 add FK fields

UPDATE `electric-summary` SET `panel_id`=(SELECT `id` FROM `electric_panel` WHERE `electric_panel`.`veris_id`=CONVERT(SUBSTRING_INDEX(`electric-summary`.`panel`,"Panel ", -1), UNSIGNED INT));
-- OUTPUT:
-- Query OK, 35223 rows affected (0.59 sec)
-- Rows matched: 35223  Changed: 35223  Warnings: 0
UPDATE `electric-circuits` SET `circuit`=(SELECT `id` FROM `electric_circuit` WHERE `electric_circuit`.`panel_id`=-1+CONVERT(SUBSTRING_INDEX(`electric-circuits`.`panel`,"Panel ", -1), UNSIGNED INT) AND `electric_circuit`.`name`=`electric-circuits`.`channel`);
-- OUTPUT:
-- Query OK, 1484018 rows affected (2 min 27.38 sec)
-- Rows matched: 1495890  Changed: 1484018  Warnings: 0

# 0005 remove old string fields, update uniqueness constraints
# 0006 add calculatedstats