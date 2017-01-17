USE `borhandw`;

ALTER TABLE borhandw.`dwh_hourly_partner_usage`
ADD COLUMN billable_storage_mb DECIMAL(19,4);
