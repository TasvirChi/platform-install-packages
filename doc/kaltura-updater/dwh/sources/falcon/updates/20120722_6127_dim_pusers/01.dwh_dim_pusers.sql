DROP TABLE IF EXISTS `borhandw`.`dwh_dim_pusers`;

CREATE TABLE `borhandw`.`dwh_dim_pusers` (
  `puser_id` INT AUTO_INCREMENT NOT NULL ,
  `name` VARCHAR(100) DEFAULT 'missing value',
  `partner_id` INT NOT NULL,
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT 0,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `ri_ind` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`puser_id`),
  KEY `partner_name_index` (`partner_id`,`name`)
) ENGINE=MYISAM  DEFAULT CHARSET=utf8;

CREATE TRIGGER `borhandw`.`dwh_dim_pusers_setcreationtime_oninsert` BEFORE INSERT
    ON `borhandw`.`dwh_dim_pusers`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
