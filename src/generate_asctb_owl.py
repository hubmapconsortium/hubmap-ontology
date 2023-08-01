import requests, json
from urllib.parse import quote_plus
from rdflib import Graph

#API_URL = 'https://asctb-api.herokuapp.com/v2/csv?output=jsonld&expanded=true&cache=true&csvUrl={0}'
#API_URL = 'https://asctb-api--staging.herokuapp.com/v2/csv?output=jsonld&expanded=true&cache=true&csvUrl={0}'
#API_URL = 'http://localhost:5000/v2/csv?output=jsonld&expanded=true&csvUrl={0}'
API_URL = 'https://mmpyikxkcp.us-east-2.awsapprunner.com/v2/csv?output=jsonld&expanded=true&cache=true&csvUrl={0}'

API_URL_JSON = 'https://mmpyikxkcp.us-east-2.awsapprunner.com/v2/csv?output=json&expanded=true&cache=true&csvUrl={0}'

GOOGLE_SHEET = 'https://docs.google.com/spreadsheets/d/{0}/export?format=csv&gid={1}'

# ASCTB_SHEET_CONFIGS = 'https://raw.githubusercontent.com/hubmapconsortium/ccf-asct-reporter/develop/projects/v2/src/assets/sheet-config.json'
# ASCTB_SHEET_CONFIGS = 'https://ccf-asct-reporter.netlify.app/assets/sheet-config.json'
ASCTB_SHEET_CONFIGS = 'https://hubmapconsortium.github.io/ccf-asct-reporter/assets/sheet-config.json'

HRA_VERSION = 'v1.4'

config = requests.get(ASCTB_SHEET_CONFIGS).json()

bysheet = {}
asctb_tables = []
for sheet in config:
  if sheet['name'] != 'all':
    table = None
    for version in sheet.get('version', []):
      if HRA_VERSION in version.get('hraVersion', '') and 'sheetId' in version:
        table = quote_plus(GOOGLE_SHEET.format(version['sheetId'], version['gid']))
    if table:
      asctb_tables.append(table)

      data = requests.get(API_URL_JSON.format(table)).json()
      bysheet[sheet['name']] = data

GRAPH_URL=API_URL.format('|'.join(asctb_tables))
JSON_URL=API_URL_JSON.format('|'.join(asctb_tables))

print()
print(GRAPH_URL)
print()

open('dist/ccf-asctb.json', 'w').write(requests.get(JSON_URL).text)
json.dump(bysheet, open('dist/ccf-asctb-all.json', 'w'), indent=2)

graphData = requests.get(GRAPH_URL).text
g = Graph()
g.parse(data=graphData, format='json-ld')
g.serialize('dist/ccf-asctb.owl', format='xml')
