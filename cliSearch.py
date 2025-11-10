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
parser.add_argument('query', nargs=1, help="Ask for search query") #stores the search query 
parser.add_argument('-v', '--verbose', type=int, choices=[1, 2, 3], default=2, help="Increases output's verbosity") #1 -> Quick just breif 2-> Complete search query with no restruction; 3 -> Also include the content from first 3 sites  
parser.add_argument('-n', '--numItems', type=int, help="Number of search results (Default is 5)") #Numb of search result.

args = parser.parse_args()

#google api key and cxid 
API_KEY = os.environ.get("API_KEY")
CX_ID = os.environ.get("CUSTOM_SEARCH_CX_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
#url for search 
search_url = "https://www.googleapis.com/customsearch/v1"

num_of_pages = 5 #default number of page
if args.verbose == 1:
    num_of_pages = 2
elif args.verbose == 3:
    num_of_pages = 10

search_params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': args.query,
        'num': args.numItems or num_of_pages
    }

search_response = requests.get(search_url, search_params)

#Using gemini to simplify the search query
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

search_results = search_response.json().get('items', [])
query_summaries = []
for item in search_results:
    if args.verbose == 2:
        query_summaries.append(f"Title: {item.get('title')}\nSnippet: {item.get('snippet')}\n")
    if args.verbose == 3:
        query_summaries.append(f"Title: {item.get('title')}\nSnippet: {item.get('snippet')}\nLink: {item.get('displayLink')}\n")
    else:
        query_summaries.append(f"Snippet: {item.get('snippet')}")
       

gemini_params = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"Summarize the key findings from these search results for the query. Length of your response depends on verbosity [1 -> Breif, 2-> Indepth and complete detail, 3-> Be as indepth as possible. The user requested verbosity: {args.verbose} Be very very quick in responding. Query: {args.query[0]}':\n{''.join(query_summaries)}"
                }
            ],
        }
    ]
}


gemini_response = requests.post(gemini_url, json = gemini_params)

console = Console()
markdown = Markdown(gemini_response.json()['candidates'][0]['content']['parts'][0]['text'])
console.print(markdown)
