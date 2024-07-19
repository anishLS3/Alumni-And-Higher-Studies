import csv
import json
import re

final_list = []

with open("data/input/CSV/itdept2024.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=",")
    line_count = 0
    
    for row in csvReader:
        if row[2] != ("Not Found" and "-"): 
            updated_url = row[2].split("?")[0]
            final_list.append({
                "register_num": "".join(row[0].split(" ")),
                "name": row[1],
                "url": updated_url
            })

with open("data/input/JSON/itdept2024.json","w") as writeFile:
    json.dump(final_list, writeFile, indent=4)