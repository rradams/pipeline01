import csv
import json
import pathlib

RAW_DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'
PROCESSED_DATA_DIR = pathlib.Path(__file__).parent / 'processed_data'

with open(
    RAW_DATA_DIR / 'census_population_2020.json',
    'r', encoding='utf-8',
) as infile:
    data = json.load(infile)

with open(
    PROCESSED_DATA_DIR / 'census_population_2020.csv',
    'w', encoding='utf-8',
) as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)
