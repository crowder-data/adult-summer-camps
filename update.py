import json
import os
import requests

BASE_ID = "appsXJD6hmXyJzYPv"
TABLE_NAME = "Directory"

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_TOKEN']}"
}

records = []
params = {}

while True:
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print("STATUS:", response.status_code)
        print("AIRTABLE RESPONSE:", response.text)
        raise Exception("Airtable API request failed")
    data = response.json()
    records.extend(data.get("records", []))

    if "offset" not in data:
        break

    params["offset"] = data["offset"]

directory = []

for record in records:
    fields = record.get("fields", {})

    directory.append({
        "name": fields.get("Name", ""),
        "location": fields.get("Location", ""),
        "region": fields.get("Region", ""),
        "cost": fields.get("Cost", ""),
        "length": fields.get("Length", ""),
        "website": fields.get("Website", "")
    })

with open("directory.json", "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

print(f"Exported {len(directory)} records.")
