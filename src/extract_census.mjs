import fetch from 'node-fetch';
import fs from 'fs';

const __dirname = new URL('.', import.meta.url).pathname;
const RAW_DATA_DIR = `${__dirname}raw_data/`;

const url = 'https://api.census.gov/data/2020/dec/pl?get=NAME,GEO_ID,P1_001N&for=block%20group:*&in=state:42%20county:*';
const resp = await fetch(url);
const data = await resp.json();

const jsonData = JSON.stringify(data);
fs.writeFileSync(
  RAW_DATA_DIR + 'census_population_2020.json',
  jsonData,
  { encoding: 'utf8' },
);