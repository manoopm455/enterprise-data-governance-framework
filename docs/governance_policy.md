# Enterprise Data Governance Policy & Stewardship Rules

## 1. Objective
This document defines mandatory compliance and data quality standards across all production feature stores and analytics pipelines.

## 2. PII Classification & Data Minimization (GDPR Art. 5)
* **Direct Identifiers:** Customer Name, Email, Phone Number, IP Address, Physical Address.
* **Rule:** Direct identifiers MUST NOT enter production recommendation feature stores without automated hashing or masking.
* **Enforcement:** Ingestion jobs must verify `consent_given = TRUE` before passing records to downstream analytics.

## 3. Metadata & Lineage Standards
* Every production table must have a designated **Data Owner** and **Steward**.
* Schema changes (column additions/deletions/type changes) must pass automated schema validation checks before model retraining.
* Data retention policies strictly limit raw staging data to 90 days.
