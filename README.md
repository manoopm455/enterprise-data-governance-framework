# Enterprise Data Governance & Metadata Management Framework

An automated data governance toolkit for mapping data lineage, maintaining metadata catalogs, enforcing GDPR stewardship checks, and preventing schema drift across ML feature pipelines.

---

## 📌 Business Context & Problem

In enterprise personalization platforms, unmonitored feature pipelines introduce significant legal and operational risks:
* **Regulatory Compliance (GDPR Art. 5/22):** Unverified customer consent flags or unmasked PII reaching feature stores leads to compliance violations.
* **Pipeline Integrity:** Unannounced schema drift or missing attributes silently degrade machine learning model performance.
* **Data Lineage Gaps:** Lack of automated metadata documentation makes auditing data origin and transformation flow difficult.

This framework provides an automated governance layer between raw data ingestion and model production feature stores.

---

## 🏗️ Architecture & Governance Flow

+---------------------+
|  Raw Staging Data   |
+---------------------+
           │
           ▼
+-------------------------------------+
| SQL Lineage & Metadata Extraction   | ──► Populates Metadata Catalog & Lineage
+-------------------------------------+
           │
           ▼
+-------------------------------------+
| Python GDPR & Stewardship Gatekeeper| ──► Filters Unverified Consent & PII
+-------------------------------------+
           │
           ▼
+-------------------------------------+
| Schema Drift & Quality Validator    | ──► Flags Missing Features & Drift
+-------------------------------------+
           │
           ▼
+---------------------+
| Verified Feature    |
|       Store         |
+---------------------+

---

## 🛠️ Repository Components

| Directory | Component | Purpose |
| :--- | :--- | :--- |
| sql/ | 01_schema_definitions.sql | DDL definitions for raw staging, feature stores, and lineage tracking. |
| sql/ | 02_lineage_metadata_query.sql | SQL scripts to trace column-level lineage and construct metadata records. |
| python/ | stewardship_gdpr_check.py | Audits ingestion data for PII compliance and active GDPR user consent. |
| python/ | schema_drift_validator.py | Automatically detects missing attributes, type mismatches, and data drift. |
| docs/ | governance_policy.md | Enterprise rules defining PII handling, data ownership, and retention rules. |

---

## 🚀 Quickstart & Verification

### Prerequisites
* Python 3.9+
* SQL-compatible environment (PostgreSQL / SQLite / BigQuery syntax)

### 1. Run Data Stewardship & GDPR Compliance Verification

Command to run:
python python/stewardship_gdpr_check.py

Expected Output:
[INFO] Scanning 10,000 incoming user records...
[PASSED] User consent flags verified (consent_given = TRUE).
[WARNING] 12 records flagged for unmasked IP addresses — redirected to isolation pipeline.
[SUCCESS] Data Stewardship Audit completed successfully.

### 2. Run Pipeline Schema Drift & Quality Audit

Command to run:
python python/schema_drift_validator.py

Expected Output:
[INFO] Validating production feature store schema against metadata catalog...
[PASSED] No missing attributes detected.
[PASSED] Schema alignment verified across 15 features.
[SUCCESS] Pipeline clear for ML model retraining.

---

## 🛡️ Key Governance Outcomes
* **Automated Enforcement:** Blocks non-compliant records before they enter production feature stores.
* **Audit Readiness:** Maintains clean, traceable lineage mapping from raw ingestion to model input.
* **Standardized Metadata:** Provides clear data ownership and column definitions across engineering and governance teams.
