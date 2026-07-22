-- ============================================================================
-- ENTERPRISE DATA WAREHOUSE DDL SCHEMAS
-- System: E-Commerce Personalization & Recommendation Engine
-- Purpose: Simulates Multi-Tier Data Lineage for Governance Auditing
-- ============================================================================

-- TIER 1: RAW INGESTION LAYER (Untrusted, Raw Customer Logs)
CREATE TABLE raw_layer.customer_clickstream (
    event_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64),
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_type VARCHAR(32),
    viewed_category VARCHAR(64),
    dwell_time_seconds INT,
    consent_marketing_flag VARCHAR(10),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIER 2: STAGING LAYER (Cleansed & Anonymized Data)
CREATE TABLE staging_layer.stg_user_behavior (
    stg_behavior_id VARCHAR(64) PRIMARY KEY,
    hashed_customer_id VARCHAR(64), -- PII Anonymized via SHA-256
    device_type VARCHAR(32),
    viewed_category VARCHAR(64),
    engagement_score DECIMAL(5,2),
    consent_verified BOOLEAN,
    processed_at TIMESTAMP
);

-- TIER 3: FEATURE STORE (Downstream Model Features for Recommendation Engine)
CREATE TABLE feature_store.user_preference_vectors (
    feature_id VARCHAR(64) PRIMARY KEY,
    hashed_customer_id VARCHAR(64),
    primary_interest_category VARCHAR(64),
    avg_dwell_time DECIMAL(7,2),
    high_value_segment_flag INT,
    model_version VARCHAR(16),
    updated_at TIMESTAMP
);
