DELIMITER $$

DROP VIEW IF EXISTS `borhandw`.`dwh_dim_countries`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `borhandw`.`dwh_dim_countries` AS (SELECT `dwh_dim_locations`.`country` AS `country`,`dwh_dim_locations`.`country_id` AS `country_id` FROM `borhandw`.`dwh_dim_locations` WHERE (`dwh_dim_locations`.`location_type_name` = 'country'))$$

DELIMITER ;