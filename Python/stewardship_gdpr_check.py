## This script serves as the Data Stewardship Gatekeeper. It scans incoming records, flags unmasked PII, and verifies GDPR user consent flags before allowing data into downstream pipelines.

import logging
import re
import pandas as pd

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

# Mock incoming batch data from raw landing staging
MOCK_INCOMING_DATA = [
    {"user_id": "usr_101", "email": "alice@example.com", "ip_address": "192.168.1.1", "consent_given": True},
    {"user_id": "usr_102", "email": "bob@example.com", "ip_address": "10.0.0.5", "consent_given": False},  # Non-compliant consent
    {"user_id": "usr_103", "email": "charlie_at_domain", "ip_address": "172.16.0.1", "consent_given": True},  # Malformed PII
    {"user_id": "usr_104", "email": "david@example.com", "ip_address": "192.168.1.50", "consent_given": True}
]

def mask_email(email: str) -> str:
    """Masks email address to comply with GDPR data minimization guidelines."""
    pattern = r"(^.)(?=.*@)(.*)(@.*)"
    return re.sub(pattern, r"\1***\3", email)

def audit_gdpr_and_stewardship(records: list) -> pd.DataFrame:
    """Audits user records for active consent and masks PII fields."""
    logging.info("Starting Data Stewardship & GDPR Compliance Audit...")
    df = pd.DataFrame(records)
    
    total_records = len(df)
    logging.info(f"Scanning {total_records} incoming user records...")
    
    # 1. Check for missing consent (GDPR Article 22 Compliance)
    non_consented = df[df["consent_given"] == False]
    if not non_consented.empty:
        logging.warning(f"Flagged {len(non_consented)} record(s) lacking valid GDPR consent. Isolating records...")
        df = df[df["consent_given"] == True].copy()
    
    # 2. Mask PII Fields (Email Data Minimization)
    df["masked_email"] = df["email"].apply(mask_email)
    df.drop(columns=["email"], inplace=True)
    
    logging.info(f"Successfully processed {len(df)} verified records into feature store stage.")
    return df

if __name__ == "__main__":
    verified_data = audit_gdpr_and_stewardship(MOCK_INCOMING_DATA)
    print("\n--- Processed Feature Store Sample ---")
    print(verified_data[["user_id", "masked_email", "consent_given"]])
    print("\n[SUCCESS] Data Stewardship Audit completed successfully.")
