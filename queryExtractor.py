import re

input_file = "AOL_query.csv"     # path to your file
output_file = "clean_queries.txt"  # where to save 1000 unique queries

unique_queries = set()
cleaned_queries = []

# regex pattern to match: everything between "Query:" and first "["
pattern = re.compile(r"Query:\s*(.*?)\[")

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            query = match.group(1).strip()  # remove spaces
            # remove duplicate and weird empty ones
            if query and query not in unique_queries:
                unique_queries.add(query)
                cleaned_queries.append(query)
                if len(cleaned_queries) >= 1000:
                    break

# save them
with open(output_file, "w", encoding="utf-8") as f:
    for q in cleaned_queries:
        f.write(q + "\n")

print(f"✅ Saved {len(cleaned_queries)} unique queries to {output_file}")
