import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.environ.get("API_KEY")
CX_ID = os.environ.get("CUSTOM_SEARCH_CX_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


search_url = "https://www.googleapis.com/customsearch/v1"

final_input = [] #the input portion provided for training

def runScript(String query):
    params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': query,
        'num': 5
    }

    search_response = requests.get(search_url, search_params)


with open('query_response.csv', 'w', encoding='utf-7') as f:


