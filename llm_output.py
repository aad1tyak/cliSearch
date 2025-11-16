import requests
import time
import csv
import os
import json
import sys
from dotenv import load_dotenv
load_dotenv()

# CONFIG
INPUT_FILE = "query_response.csv"
OUTPUT_FILE = "LLM_trainingData(2.5-flash-lite).jsonl"

START_ROW = 1 # inclusive: 1 = process from the first data row
END_ROW = 2500 # inclusive: set to None to continue until file ends

# API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
gemini_url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-lite:generateContent?key=" + GEMINI_API_KEY
)

def run_llm(input_text):
    gemini_params = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "You will be given noisy, unstructured text. "
                            "Your task is to extract ONLY information directly relevant to the query.\n\n"
                            "Rules:\n"
                            "- Do NOT add new information.\n"
                            "- Do NOT infer missing information.\n"
                            "- Do NOT rewrite or paraphrase unless necessary.\n"
                            "- Keep relevant text as-is.\n"
                            "- Remove irrelevant, repetitive, or off-topic content.\n"
                        )
                    }
                ],
            },
            {
                "role": "user",
                "parts": [{"text": input_text}]
            }
        ]
    }

    r = requests.post(gemini_url, json=gemini_params)
    time.sleep(4)
    if r.status_code != 200:
        print("❌ Request failed:", r.status_code)
        sys.exit(1)

    try:
        response_json = r.json()
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("❌ Failed to parse Gemini output:", e)
        sys.exit(1)


# MAIN PROCESSING
current_row = 0

with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile, \
     open(OUTPUT_FILE, "a", encoding='utf-8') as out:

    reader = csv.DictReader(csvfile)

    for row in reader:
        current_row += 1

        # Skip until start row
        if current_row < START_ROW:
            continue
        
        # Stop after end row
        if END_ROW is not None and current_row > END_ROW:
            print("Reached END_ROW. Stopping.")
            break

        try:
            row_id = row.get("Id: ", "").strip()
            query = row.get("Query", "").strip()
            search_items = row.get("Search Items", "").strip()
        except:
            continue

        if not query or not search_items:
            continue

        llm_input = (
            f"### Query:\n{query}\n\n"
            f"### SearchItems:\n{search_items}"
        )

        llm_output = run_llm(llm_input)

        entry = {
            "instruction": "Extract only the relevant parts of SearchItems that answer the Query.",
            "input": llm_input,
            "output": llm_output
        }

        out.write(json.dumps(entry) + "\n")

        print(f"✔ Completed row {current_row} (ID: {row_id})")
