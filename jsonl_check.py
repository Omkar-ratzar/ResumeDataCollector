import json
import re
from collections import Counter

import spacy
from spacy.tokens import DocBin

INPUT_FILE = "resume_dataset_reviewed.jsonl"
OUTPUT_FILE = "train.spacy"

nlp = spacy.blank("en")
doc_bin = DocBin()

stats = {
    "documents": 0,
    "successful": 0,
    "missing_entities": 0,
    "multiple_matches": 0,
    "overlapping_spans_removed": 0,
}

entity_counts = Counter()
problems = []


def find_all_occurrences(text, entity_text):
    return [
        (m.start(), m.end())
        for m in re.finditer(
            re.escape(entity_text),
            text,
            flags=re.IGNORECASE
        )
    ]


def remove_overlaps(spans):
    """
    Keep longest spans first.
    spaCy does not allow overlapping entities.
    """
    spans = sorted(
        spans,
        key=lambda x: (
            -(x[1] - x[0]),  # longest first
            x[0]
        )
    )

    accepted = []

    for span in spans:
        start, end, label = span

        overlap = False

        for a_start, a_end, _ in accepted:
            if start < a_end and end > a_start:
                overlap = True
                break

        if overlap:
            stats["overlapping_spans_removed"] += 1
        else:
            accepted.append(span)

    return sorted(accepted, key=lambda x: x[0])


with open(INPUT_FILE, "r", encoding="utf-8") as f:

    for line in f:

        stats["documents"] += 1

        record = json.loads(line)

        text = record["text"]
        labels = record["labels"]

        spans = []

        for label, values in labels.items():

            if not values:
                continue

            for value in values:

                if not value:
                    continue

                value = value.strip()

                if not value:
                    continue

                matches = find_all_occurrences(
                    text,
                    value
                )

                if len(matches) == 0:

                    stats["missing_entities"] += 1

                    problems.append({
                        "id": record["id"],
                        "type": "NOT_FOUND",
                        "label": label,
                        "value": value
                    })

                    continue

                if len(matches) > 1:

                    stats["multiple_matches"] += 1

                    problems.append({
                        "id": record["id"],
                        "type": "MULTIPLE_MATCHES",
                        "label": label,
                        "value": value,
                        "count": len(matches)
                    })

                # add ALL occurrences
                for start, end in matches:
                    spans.append(
                        (start, end, label)
                    )

        spans = remove_overlaps(spans)

        doc = nlp.make_doc(text)

        ents = []

        for start, end, label in spans:

            span = doc.char_span(
                start,
                end,
                label=label,
                alignment_mode="contract"
            )

            if span is not None:
                ents.append(span)
                entity_counts[label] += 1

        try:
            doc.ents = ents
        except ValueError:

            problems.append({
                "id": record["id"],
                "type": "SPACY_ENTITY_ERROR"
            })

            continue

        doc_bin.add(doc)
        stats["successful"] += 1

doc_bin.to_disk(OUTPUT_FILE)

print("\n=== DATASET REPORT ===")

for k, v in stats.items():
    print(f"{k}: {v}")

print("\n=== ENTITY COUNTS ===")

for label, count in sorted(entity_counts.items()):
    print(f"{label}: {count}")

print(f"\nSaved spaCy file: {OUTPUT_FILE}")

if problems:

    with open(
        "span_problems.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            problems,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Saved {len(problems)} issues to span_problems.json"
    )
