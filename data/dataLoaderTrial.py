import json

with open("data/output/final_output/2024.json","r") as readFile:
    data = json.load(readFile)
with open("data/output/final_output/2022A.json","r") as readFile:
    data1 = json.load(readFile)
with open("data/output/final_output/2022B.json","r") as readFile:
    data2 = json.load(readFile)


print(len(data), len(data1), len(data2))