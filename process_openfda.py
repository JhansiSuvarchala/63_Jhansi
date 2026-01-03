import json
import os

INPUT_DIR = "data"
OUTPUT_FILE = "data/openfda_clean.json"

MAX_RECORDS = 2000   # 🔥 LIMIT DATASET SIZE (FAST BUILD)

clean_data = []

def safe_get(record, key):
    """
    Safely extract first element from FDA list fields
    """
    value = record.get(key, [])
    if isinstance(value, list) and len(value) > 0:
        return value[0]
    return ""

def extract_drug_name(record):
    """
    Extract drug name from openfda section
    """
    openfda = record.get("openfda", {})
    for key in ["generic_name", "brand_name", "substance_name"]:
        if key in openfda and len(openfda[key]) > 0:
            return openfda[key][0].lower()
    return None


# =========================================================
# Process all openFDA JSON files
# =========================================================
for file in os.listdir(INPUT_DIR):
    if not file.startswith("drug-label") or not file.endswith(".json"):
        continue

    print(f"Processing {file}")

    with open(os.path.join(INPUT_DIR, file), "r") as f:
        data = json.load(f)

    for record in data.get("results", []):
        if len(clean_data) >= MAX_RECORDS:
            break

        drug_name = extract_drug_name(record)
        if not drug_name:
            continue

        clean_data.append({
            "drug_name": drug_name,
            "uses": safe_get(record, "indications_and_usage"),
            "dosage": safe_get(record, "dosage_and_administration"),
            "warnings": safe_get(record, "warnings_and_cautions") or safe_get(record, "warnings"),
            "side_effects": safe_get(record, "adverse_reactions")
        })

    if len(clean_data) >= MAX_RECORDS:
        break


# =========================================================
# Save cleaned dataset
# =========================================================
with open(OUTPUT_FILE, "w") as f:
    json.dump(clean_data, f, indent=2)

print(f"\n✅ Extracted {len(clean_data)} FDA drug labels")
print(f"📁 Saved to {OUTPUT_FILE}")
