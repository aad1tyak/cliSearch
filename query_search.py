import json
import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()

search_url = "https://google.serper.dev/search"
queryList_File = "QueryList.txt"

search_results = [] #the input portion provided for training

start = 0
end = 500

headers = {
  'X-API-KEY': os.environ.get("SERPER_DEV"),
  'Content-Type': 'application/json'
}
counter = 0
def runScript(query):
    counter += 1
    payload = json.dumps({
        "q": query,
        "num": 4
    })

    try:
        response = requests.post(search_url, headers=headers, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        search_items = response.json().get('organic', [])
        clean_items = []
        for item in search_items:
            clean_items.append(f"Title: {item.get('title')}\n Snippet: {item.get('snippet')}\n Website Address:  {item.get('link')}\n \n \n")
        search_results.append({"Id: ": counter, Query": query.strip(), "Search Items": clean_items})
    except requests.exceptions.RequestException as e:
        print(f"Error during API request for query '{query.strip()}': {e}")

#Go through the QueryList file and perfrom search for all of the query
with open(queryList_File, "r", encoding='utf-8', errors="ignore") as f:
    for i, line in enumerate(f):
        if i < start:
            continue
        if i >= end:
            break
        runScript(line)

with open('query_response.csv', 'w', encoding='utf-8', newline='') as f:
    if search_results:
        writer = csv.DictWriter(f, fieldnames=search_results[0].keys())
        writer.writeheader()
        writer.writerows(search_results)

