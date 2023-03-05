import * as csv from 'csv/sync';
import fs from 'fs/promises';

const __dirname = new URL('.', import.meta.url).pathname;
const RAW_DATA_DIR = `${__dirname}raw_data/`;
const PROCESSED_DATA_DIR = `${__dirname}processed_data/`;

const content = await fs.readFile(
  RAW_DATA_DIR + 'census_population_2020.json',
  { encoding: 'utf8' },
);
const data = JSON.parse(content);

const outContent = csv.stringify(data);
await fs.writeFile(
  PROCESSED_DATA_DIR + 'census_population_2020.csv',
  outContent, { encoding: 'utf8' },
);