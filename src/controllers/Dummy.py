from pathlib import Path
import csv
dir = Path.cwd()

table = "Cool_stuff"
filename = dir.joinpath(f"{table}.csv")
result = "Happy days"

with open(filename, "w", encoding="utf-8") as file:
    csv.writer(file).writerows(result)