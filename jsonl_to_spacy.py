import json
import re
from collections import Counter

import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("en")


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
    spans = sorted(
        spans,
        key=lambda x: (
            -(x[1] - x[0]),
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

        if not overlap:
            accepted.append(span)

    return sorted(accepted, key=lambda x: x[0])


def jsonl_to_spacy(input_file, output_file):

    doc_bin = DocBin()
    entity_counts = Counter()

    docs_created = 0

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:

            record = json.loads(line)

            text = record["text"]
            labels = record["labels"]

            spans = []

            for label, values in labels.items():

                for value in values:

                    if not value:
                        continue

                    matches = find_all_occurrences(
                        text,
                        value.strip()
                    )

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

            doc.ents = ents

            doc_bin.add(doc)
            docs_created += 1

    doc_bin.to_disk(output_file)

    print(f"\nCreated {output_file}")
    print(f"Documents: {docs_created}")

    for label, count in sorted(entity_counts.items()):
        print(f"{label}: {count}")


jsonl_to_spacy(
    "train.jsonl",
    "train.spacy"
)

jsonl_to_spacy(
    "dev.jsonl",
    "dev.spacy"
)

jsonl_to_spacy(
    "test.jsonl",
    "test.spacy"
)
