-- ============================================================================
-- Enterprise Data Governance & Metadata Catalog
-- Part 2: Lineage Extraction & Governance Audit Queries
-- ============================================================================

-- 1. Populate/Register Datasets into the Central Metadata Catalog
INSERT INTO metadata_catalog (dataset_id, table_name, data_owner, data_steward, contains_pii, retention_period_days)
VALUES 
    ('ds_001', 'landing_user_events', 'Data Engineering', 'Compliance Office', TRUE, 90),
    ('ds_002', 'user_feature_store', 'ML Platform Team', 'Data Steward Team', FALSE, 365)
ON CONFLICT (dataset_id) DO NOTHING;


-- 2. Lineage Audit Query: Trace transformations from Raw Landing to Feature Store
-- Verifies that raw event logs map correctly to upstream analytics features
SELECT 
    m1.table_name AS source_table,
    m1.contains_pii AS source_contains_pii,
    m2.table_name AS target_table,
    m2.data_owner AS target_owner,
    m1.retention_period_days AS raw_retention_limit
FROM metadata_catalog m1
JOIN metadata_catalog m2 ON m1.dataset_id = 'ds_001' AND m2.dataset_id = 'ds_002';


-- 3. Data Stewardship Check: Identify records missing explicit GDPR consent
SELECT 
    event_id, 
    user_id, 
    event_type, 
    consent_given
FROM landing_user_events
WHERE consent_given = FALSE;
