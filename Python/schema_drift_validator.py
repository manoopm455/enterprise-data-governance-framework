##This script serves as the Pipeline Schema Drift & Quality Validator. It compares the schema of active feature store feeds against expected metadata contracts to prevent silent model pipeline failures.

import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

# Metadata Contract (Expected baseline schema definition)
EXPECTED_SCHEMA = {
    "user_id": "string",
    "engagement_score": "float",
    "purchase_frequency_30d": "int",
    "preferred_category": "string",
    "consent_given": "bool"
}

# Mock incoming batch data stream
MOCK_PIPELINE_BATCH = {
    "user_id": "usr_101",
    "engagement_score": 88.5,
    "purchase_frequency_30d": 4,
    "preferred_category": "Electronics",
    "consent_given": True
}

def validate_schema_drift(data_batch: Dict[str, Any], schema_contract: Dict[str, str]) -> bool:
    """Validates incoming batch structure against expected metadata contract."""
    logging.info("Validating production feature store schema against metadata catalog...")
    
    batch_keys = set(data_batch.keys())
    expected_keys = set(schema_contract.keys())
    
    # 1. Detect Missing Attributes
    missing_fields = expected_keys - batch_keys
    if missing_fields:
        logging.error(f"SCHEMA DRIFT DETECTED: Missing required fields: {missing_fields}")
        return False
        
    # 2. Detect Unexpected Extra Attributes
    extra_fields = batch_keys - expected_keys
    if extra_fields:
        logging.warning(f"UNREGISTERED FIELDS DETECTED: New fields present in batch: {extra_fields}")

    # 3. Type Checking
    type_mappings = {"string": str, "float": float, "int": int, "bool": bool}
    for field, expected_type_str in schema_contract.items():
        expected_type = type_mappings.get(expected_type_str)
        actual_val = data_batch.get(field)
        if expected_type and not isinstance(actual_val, expected_type):
             logging.error(f"TYPE MISMATCH: Field '{field}' expected {expected_type_str}, got {type(actual_val).__name__}")
             return False

    logging.info(f"[PASSED] Schema alignment verified across {len(schema_contract)} features.")
    return True

if __name__ == "__main__":
    is_valid = validate_schema_drift(MOCK_PIPELINE_BATCH, EXPECTED_SCHEMA)
    if is_valid:
        print("\n[SUCCESS] Pipeline clear for ML model retraining.")
    else:
        print("\n[FAIL] Pipeline execution halted due to schema violations.")
