import requests
import os
import json 
import argparse
from dotenv import load_dotenv
load_dotenv()
#Define the Arguement Parser object instance 
parser = argparse.ArgumentParser('cliSearch', 'Let the user to make search query through terminal.')

#attach arguements for task 
parser.add_argument('query', nargs=1)

args = parser.parse_args()
print(args.query)

#google api key and cxid 
API_KEY = os.environ.get("API_KEY")
CX_ID = os.environ.get("CUSTOM_SEARCH_CX_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
#url for search 
search_url = "https://www.googleapis.com/customsearch/v1"

serach_params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': args.query,
        'num': 5  # Request up to 5 results for simplicity
    }

search_response = requests.get(search_url, search_params)

#Using gemini to simplify the search query
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

gemini_params = {
    'key' = GEMINI_API_KEY
}

gemini_response = requests.get(gemini_url, gemini_params)

print(response.json())

print(API_KEY, CX_ID)
