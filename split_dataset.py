# split_dataset.py
import json, random
from pathlib import Path

CLEAN = "LLM_trainingData(2.5-flash-lite).clean.jsonl"
TRAIN = "train.jsonl"
VAL = "val.jsonl"
TEST = "test.jsonl"

random.seed(42)
lines = [line.strip() for line in open(CLEAN, encoding="utf-8") if line.strip()]
random.shuffle(lines)

n = len(lines)
n_train = int(n * 0.90)
n_val = int(n * 0.05)
n_test = n - n_train - n_val

with open(TRAIN, "w", encoding="utf-8") as f:
    for L in lines[:n_train]: f.write(L + "\n")
with open(VAL, "w", encoding="utf-8") as f:
    for L in lines[n_train:n_train+n_val]: f.write(L + "\n")
with open(TEST, "w", encoding="utf-8") as f:
    for L in lines[n_train+n_val:]: f.write(L + "\n")

print(f"Split: n={n}, train={n_train}, val={n_val}, test={n_test}")
