import requests
import os
import json 
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
#Define the Arguement Parser object instance 
parser = argparse.ArgumentParser('cliSearch', 'Let the user to make search query through terminal.')

#attach arguements for task 
parser.add_argument('query', nargs=1)

args = parser.parse_args()

#google api key and cxid 
API_KEY = os.environ.get("API_KEY")
CX_ID = os.environ.get("CUSTOM_SEARCH_CX_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
#url for search 
search_url = "https://www.googleapis.com/customsearch/v1"

search_params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': args.query,
        'num': 5  # Request up to 5 results for simplicity
    }

search_response = requests.get(search_url, search_params)

#Using gemini to simplify the search query
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

gemini_params = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"Summarize the key findings and main arguments from the following search results related. Present the answer in plain language, and address what the user is primarily seeking. Here is th search query: \n{args.query[0]}\nAnd here is the search result: \n{json.dumps(search_response.json())}"
                }
            ],
        }
    ]
}


gemini_response = requests.post(gemini_url, json = gemini_params)

console = Console()
markdown = Markdown(gemini_response.json()['candidates'][0]['content']['parts'][0]['text'])
console.print(markdown)
