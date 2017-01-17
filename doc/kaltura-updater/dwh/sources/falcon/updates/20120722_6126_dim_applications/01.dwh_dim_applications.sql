DROP TABLE IF EXISTS `borhandw`.`dwh_dim_applications`;

CREATE TABLE `borhandw`.`dwh_dim_applications` (
  `application_id` INT AUTO_INCREMENT NOT NULL ,
  `name` VARCHAR(128) DEFAULT 'missing value',
  `partner_id` INT(11) NOT NULL,
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT 0,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `ri_ind` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`application_id`),
  KEY `partner_id_name_index` (`partner_id`,`name`)
) ENGINE=MYISAM  DEFAULT CHARSET=utf8;

CREATE TRIGGER `borhandw`.`dwh_dim_applications_setcreationtime_oninsert` BEFORE INSERT
    ON `borhandw`.`dwh_dim_applications`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
