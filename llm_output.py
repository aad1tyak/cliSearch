import requests
import os
import json 
from dotenv import load_dotenv
load_dotenv()


INPUT_FILE = "query_response.csv"
OUTPUT_FILE = "LLM_trainingData.csv"

#APi keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

#Gemini request url
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY


def run_llm(input):
    gemini_params = {
    "contents": [
        {
            "role": "Instructor",
            "parts": [
                {
                    "text": f"You will be provided Messy and unstructured Input which a lot of noise and your job is to provide a clean breif output with relevant information from the provided input. So skip all the repetative information, skip all the information thats not useful for a human, also skip anything that is not releavant to the overall theme. Also note that Please do not add any new information, please dont alter the text, return the relevant text as it is." #TODO Create a Instruction for llm 
                }
            ],
        },
        {
            "role": "Messy and unstructured Input",
            "parts": [
                {
                        "text": f"{input}" 
                }
            ]
        }
    ]
    }
    
    gemini_response = requests.post(gemini_url, json = gemini_params)
    return f"{input}, {output}"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
         if i < start:
            continue
        if i >= end:
            break
        run_llm(line) #DONT RUN

with open(OUTPUT_FILE, 'a', encoding="utf-8") as f:
    writer = csv.DictWriter(f, )
    
 

