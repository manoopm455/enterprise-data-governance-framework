-- ============================================================================
-- Enterprise Data Governance & Metadata Catalog
-- Part 1: Schema Definitions (DDL)
-- ============================================================================

-- 1. Raw Landing Table (Staging layer containing user interaction data)
CREATE TABLE IF NOT EXISTS landing_user_events (
    event_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    email VARCHAR(255),                  -- PII Field
    ip_address VARCHAR(45),             -- PII Field
    event_type VARCHAR(50) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    consent_given BOOLEAN DEFAULT FALSE -- GDPR Compliance Flag
);

-- 2. Cleaned Feature Store Table (Production layer for ML models)
CREATE TABLE IF NOT EXISTS user_feature_store (
    user_id VARCHAR(64) PRIMARY KEY,
    engagement_score NUMERIC(5,2),
    purchase_frequency_30d INT,
    preferred_category VARCHAR(100),
    last_active_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Central Metadata Catalog & Lineage Repository
CREATE TABLE IF NOT EXISTS metadata_catalog (
    dataset_id VARCHAR(64) PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    data_owner VARCHAR(100) NOT NULL,
    data_steward VARCHAR(100) NOT NULL,
    contains_pii BOOLEAN DEFAULT FALSE,
    retention_period_days INT DEFAULT 365,
    last_audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
