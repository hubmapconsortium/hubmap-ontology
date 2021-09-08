import json, requests
from urllib.parse import quote_plus
from rdflib import Graph

API_URL = 'https://asctb-api.herokuapp.com/v2/csv?output=jsonld&expanded=true&csvUrl={0}'
#API_URL = 'https://asctb-api--staging.herokuapp.com/v2/csv?output=jsonld&expanded=true&csvUrl={0}'
#API_URL = 'http://localhost:5000/v2/csv?output=jsonld&expanded=true&csvUrl={0}'

CSV_SHEET = 'https://hubmapconsortium.github.io/ccf-releases/v1.0/asct-b/{0}'
GOOGLE_SHEET = 'https://docs.google.com/spreadsheets/d/1tK916JyG5ZSXW_cXfsyZnzXfjyoN-8B2GXLbYD6_vF0/export?format=csv&gid={0}'

def get_url(sheet):
  formatter = GOOGLE_SHEET
  if sheet.endswith('.csv'):
    formatter = CSV_SHEET
  return quote_plus(formatter.format(sheet))

asctb_tables = list(map(get_url, [
  '1379088218', # Brain
  '1845311048', # Bone Marrow
  '2133445058', # Heart
  '1440276882', # Lymph Nodes
  '2137043090', # Kidney
  '512613979', # Large Intestine
  '1824552484', # Lung
  '1158675184', # Skin
  '984946629', # Spleen
  '1823527529', # Thymus
  '361657182', # Vasculature
  # 'ASCT-B_Allen_Brain.csv',
  # 'ASCT-B_NIH_Lymph_Node.csv',
  # 'ASCT-B_VH_BM_Blood_Pelvis.csv',
  # 'ASCT-B_VH_Heart.csv',
  # 'ASCT-B_VH_Intestine_Large.csv',
  # 'ASCT-B_VH_Kidney.csv',
  # 'ASCT-B_VH_Lung.csv',
  # 'ASCT-B_VH_Skin.csv',
  # 'ASCT-B_VH_Spleen.csv',
  # 'ASCT-B_VH_Thymus.csv',
  # 'ASCT-B_VH_Vasculature.csv'
]))
GRAPH_URL=API_URL.format('|'.join(asctb_tables))

print()
print(GRAPH_URL)
print()

graphData = requests.get(GRAPH_URL).text
g = Graph()
g.parse(data=graphData, format='json-ld')
g.serialize('dist/ccf-asctb.owl', format='xml')
