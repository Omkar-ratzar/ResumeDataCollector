import json
import random

random.seed(42)

with open(
    "resume_dataset_reviewed.jsonl",
    "r",
    encoding="utf-8"
) as f:
    records = [json.loads(line) for line in f]

random.shuffle(records)

n = len(records)

train_end = int(0.83 * n)  # 80/96
dev_end = train_end + int(0.08 * n)  # 8/96

train = records[:train_end]
dev = records[train_end:dev_end]
test = records[dev_end:]

print(len(train), len(dev), len(test))

for name, data in [
    ("train.jsonl", train),
    ("dev.jsonl", dev),
    ("test.jsonl", test),
]:
    with open(name, "w", encoding="utf-8") as f:
        for row in data:
            f.write(
                json.dumps(
                    row,
                    ensure_ascii=False
                )
                + "\n"
            )
