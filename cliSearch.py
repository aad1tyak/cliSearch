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
parser.add_argument('query', nargs=1) #stores the search query 
parser.add_argument('-v', type=int, choices=[1, 2, 3], default=2) #1 -> Quick just breif 2-> Complete search query with no restruction; 3 -> Also include the content from first 3 sites  
parser.add_argument('-n', 'n_query_result' type=int, default=5) #Numb of search result.

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
        'num': args.n_query_result 
    }

search_response = requests.get(search_url, search_params)

#Using gemini to simplify the search query
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

search_results = search_response.json().get('items', [])
query_summaries = []
for item in search_results:
    query_summaries.append(f"Title: {item.get('title')}\nSnippet: {item.get('snippet')}\n")

gemini_params = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"Summarize the key findings from these search results for the query. Answer brefily don't waste token and time. Be very very quick in responding.'{args.query[0]}':\n{''.join(query_summaries)}"
                }
            ],
        }
    ]
}


gemini_response = requests.post(gemini_url, json = gemini_params)

console = Console()
markdown = Markdown(gemini_response.json()['candidates'][0]['content']['parts'][0]['text'])
console.print(markdown)
