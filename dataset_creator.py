from Dataset_creation.auto_dataset_creator import auto
from Extraction.extract_pdf import extract_pdf

import os
import time
import json

start = time.time()

folder_path = "Resumes"
output_file = "resume_dataset.jsonl"

with open(output_file, "w", encoding="utf-8") as jsonl_file:

    with os.scandir(folder_path) as entries:

        for entry in entries:

            if not entry.is_file():
                continue

            print(f"Processing: {entry.name}")

            try:

                resume_text = extract_pdf(entry.path)

                raw_output = auto(resume_text)

                try:
                    labels = json.loads(raw_output)

                    record = {
                        "id": entry.name,
                        "file_name": entry.name,
                        "file_path": entry.path,
                        "text": resume_text,
                        "labels": labels,
                        "valid_json": True
                    }

                except json.JSONDecodeError:

                    record = {
                        "id": entry.name,
                        "file_name": entry.name,
                        "file_path": entry.path,
                        "text": resume_text,
                        "raw_output": raw_output,
                        "valid_json": False
                    }

                    print(f"[JSON ERROR] {entry.name}")

                jsonl_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )

            except Exception as e:

                print(f"[FAILED] {entry.name}: {e}")

                record = {
                    "id": entry.name,
                    "file_name": entry.name,
                    "file_path": entry.path,
                    "error": str(e)
                }

                jsonl_file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )

end = time.time()

print(f"\nTime taken: {end - start:.2f} seconds")
