import json
import pathlib
import requests

RAW_DATA_DIR = pathlib.Path(__file__).parent / 'raw_data'

url = 'https://api.census.gov/data/2020/dec/pl?get=NAME,GEO_ID,P1_001N&for=block%20group:*&in=state:42%20county:*'
resp = requests.get(url)
data = resp.json()

json_data = json.dumps(data)
with open(
    RAW_DATA_DIR / 'census_population_2020.json',
    'w', encoding='utf-8',
) as f:
    f.write(json_data)
