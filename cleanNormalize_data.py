# clean_dataset.py
import json
import re
from pathlib import Path

INPUT = "LLM_trainingData(2.5-flash-lite).jsonl"
OUTPUT = "LLM_trainingData(2.5-flash-lite).clean.jsonl"

skip_pattern = re.compile(r"\[SKIPPED", re.IGNORECASE)

def normalize_output(text):
    # If empty, return empty string
    if not text or not text.strip():
        return ""
    # Replace Windows newlines etc
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    # If already has bullets (- or •), keep but normalize to "- "
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # remove leading bullets and whitespace
        if re.match(r"^[-•\*\u2022]\s+", line):
            line = re.sub(r"^[-•\*\u2022]\s+", "", line)
        # collapse excessive whitespace
        line = re.sub(r"\s+", " ", line)
        lines.append("- " + line)
    # join with newline
    return "\n".join(lines)

total = 0
kept = 0
skipped = 0

with open(INPUT, "r", encoding="utf-8") as inf, open(OUTPUT, "w", encoding="utf-8") as outf:
    for raw in inf:
        total += 1
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception as e:
            print("bad json on line", total, e)
            continue
        out_text = obj.get("output", "")
        if isinstance(out_text, str) and skip_pattern.search(out_text):
            skipped += 1
            continue
        # normalize
        normalized = normalize_output(out_text)
        if not normalized:
            # optionally skip empty outputs too
            skipped += 1
            continue
        obj["output"] = normalized
        outf.write(json.dumps(obj, ensure_ascii=False) + "\n")
        kept += 1

print(f"Done. total={total}, kept={kept}, skipped={skipped}. Clean file -> {OUTPUT}")
