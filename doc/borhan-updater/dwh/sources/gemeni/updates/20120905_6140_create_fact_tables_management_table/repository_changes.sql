DROP TABLE IF EXISTS borhandw_ds.fact_tables;
CREATE TABLE borhandw_ds.fact_tables
	(fact_table_id INT NOT NULL,
	fact_table_name VARCHAR(50),
	UNIQUE KEY (fact_table_id));
INSERT INTO borhandw_ds.fact_tables VALUES (1,'borhandw.dwh_fact_events'), 
				(2,'borhandw.dwh_fact_bandwidth_usage'),
				(3,'borhandw.dwh_fact_fms_session_events'),
				(4,'borhandw.dwh_fact_api_calls'),
				(5,'borhandw.dwh_fact_incomplete_api_calls'),
				(6,'borhandw.dwh_fact_errors');
ALTER TABLE borhandw_ds.staging_areas
		ADD COLUMN target_table_id INT AFTER target_table;

UPDATE borhandw_ds.staging_areas s, borhandw_ds.fact_tables f
SET s.target_table_id = f.fact_table_id
WHERE s.target_table = f.fact_table_name;

ALTER TABLE borhandw_ds.staging_areas
	CHANGE COLUMN target_table_id target_table_id INT NOT NULL,
	DROP COLUMN target_table;
