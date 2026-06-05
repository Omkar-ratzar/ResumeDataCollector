import pandas as pd
df = pd.read_json(
    "resume_dataset.jsonl",
    lines=True
)

review_df = pd.DataFrame({
    "id": df["id"],
    "person": df["labels"].apply(
        lambda x: x.get("PERSON", [])
        if isinstance(x, dict)
        else []
    ),
    "company": df["labels"].apply(
        lambda x: x.get("COMPANY", [])
        if isinstance(x, dict)
        else []
    ),
    "college": df["labels"].apply(
        lambda x: x.get("COLLEGE", [])
        if isinstance(x, dict)
        else []
    ),
    "position": df["labels"].apply(
        lambda x: x.get("POSITION", [])
        if isinstance(x, dict)
        else []
    )
})

review_df.to_excel(
    "resume_review.xlsx",
    index=False
)
