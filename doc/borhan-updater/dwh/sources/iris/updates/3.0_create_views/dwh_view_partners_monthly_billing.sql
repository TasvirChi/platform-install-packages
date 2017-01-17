DROP VIEW IF EXISTS borhandw.dwh_view_partners_monthly_billing;
CREATE VIEW `borhandw`.`dwh_view_partners_monthly_billing` 
    AS
(
	SELECT max_blling_updated.month_id, billing.* 
	FROM borhandw.dwh_view_partners_monthly_billing_last_updated_at max_blling_updated, 
		borhandw.dwh_dim_partners_billing billing
	WHERE max_blling_updated.partner_id = billing.partner_id
	AND max_blling_updated.updated_at = billing.updated_at
);

