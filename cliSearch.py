import request
import json 
import argparse
#Define the Arguement Parser object instance 
parser = argparse.ArgumentParser('cliSearch', 'Let the user to make search query through terminal.')

#attach arguements for task 
parser.add_argument('query', nargs=1)

args = parser.parse_args()
print(args.query)

#google api key and cxid 
API_KEY = os.environ.get("API_KEY")
CX_ID = os.environ.get("CUSTOM_SEARCH_CX_ID")
#url for search 
url = "https://www.googleapis.com/customsearch/v1"

params = {
        'key': API_KEY,
        'cx': CX_ID,
        'q': args.query,
        'num': 5  # Request up to 5 results for simplicity
    }

response = requests.get(url, params)

print(rresponse.json())
