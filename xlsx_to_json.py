import pandas as pd
import ast

# Read original dataset
original_df = pd.read_json(
    "resume_dataset.jsonl",
    lines=True
)

# Read reviewed Excel
review_df = pd.read_excel(
    "resume_review.xlsx"
)

def parse_list(value):
    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    try:
        return ast.literal_eval(str(value))
    except Exception:
        return []

# Rebuild labels dictionary
review_df["labels"] = review_df.apply(
    lambda row: {
        "PERSON": parse_list(row["person"]),
        "COMPANY": parse_list(row["company"]),
        "COLLEGE": parse_list(row["college"]),
        "POSITION": parse_list(row["position"]),
    },
    axis=1,
)

# Create id -> labels mapping
label_map = review_df.set_index("id")["labels"].to_dict()

# Replace labels in original dataframe
original_df["labels"] = original_df["id"].map(label_map)

# Save back to JSONL
original_df.to_json(
    "resume_dataset_reviewed.jsonl",
    orient="records",
    lines=True,
    force_ascii=False
)

print(f"Saved {len(original_df)} records")
