DROP TABLE IF EXISTS `borhandw`.dwh_dim_api_actions;

CREATE TABLE `borhandw`.`dwh_dim_api_actions` (
  `action_id` INT(11) NOT NULL AUTO_INCREMENT,
  `action_name` VARCHAR(166) NOT NULL DEFAULT '',
  `service_name` VARCHAR(166) NOT NULL DEFAULT '',
  `dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`action_id`),
   UNIQUE KEY (`action_name`, `service_name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `borhandw`.`dwh_dim_api_actions_setcreationtime_oninsert` BEFORE INSERT
    ON `borhandw`.`dwh_dim_api_actions`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
