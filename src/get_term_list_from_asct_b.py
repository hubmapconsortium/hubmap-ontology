import csv, json, re
from collections import namedtuple, defaultdict
from os import listdir, path

ASCT_RELEASE_DIR='../ccf-releases/v1.1/asct-b/'
ASCTB_JSON='dist/ccf-asctb.json'
OUTPUT_CSV='source_data/ccf-term-list.csv'
GOOD_ONTOLOGIES = set(['CL', 'UBERON', 'FMA', 'FMAID'])

AS = namedtuple('AnatomicalStructure', ['id', 'name', 'rdfs_label'])

# Fix IDs from ASCT+B Tables. Ideally, these changes are made up stream for next release and no transformation is necessary
def fix_id(idstr):
  if idstr.startswith('fma') and idstr[3].isdigit():
    idstr = 'fma:'+idstr[3:]
  idstr = idstr.replace('_', ':').replace('::', ':').replace(': ', ':').replace('FMA:', 'FMAID:').replace('fma:', 'FMAID:').split(' ')[0].upper()
  idstr = ':'.join(map(lambda s: s.strip(), idstr.split(':')))
  return idstr

# Fix names. Ideally this is not needed when changes are made up stream.
def fix_name(name):
  if name == 'thoracic thymus':
    return 'thymus'
  return name

def good_node(node):
  onto_val = node.id.split(':', 1)
  return node.id and onto_val[0] in GOOD_ONTOLOGIES and len(onto_val) == 2 and len(onto_val[1]) > 0

def as_temp_node(node):
  suffix = re.sub(r'[^a-z0-9-]+', '', re.sub(r'\W+', '-', node.name.lower().strip()))
  ontologyId = f'ASCTB-TEMP:{suffix}'
  return AS(ontologyId, node.name, node.name)

def asct_rows(in_f):
  text = open(in_f, 'rb').read().decode('ISO-8859-1').split('\n')
  rows = csv.reader(text)
  print(in_f)
  header = False
  lookup = {}
  max_as = 1
  for row in rows:
    if len(row) > 0 and row[0] == 'AS/1':
      header = row
      for index, column in enumerate(header):
        if column.startswith('AS/'):
          colspec = column.split('/')
          as_index = int(colspec[1])
          if len(colspec) == 2:
            prop = '_NAME_'
          elif len(colspec) == 3:
            prop = colspec[2]
          lookup[index] = (as_index - 1, prop)
          max_as = max(as_index, max_as)
    elif header != False:
      datum = [ {} for _ in range(max_as) ]
      for index, (as_index, prop) in lookup.items():
        if index < len(row):
          datum[as_index][prop] = row[index].strip()
      yield [ AS(fix_id(d.get('ID', '')), fix_name(d.get('_NAME_')), fix_name(d.get('LABEL'))) for d in datum ]

def asct_rows2():
  data = json.load(open(ASCTB_JSON))['data']
  seen = set()
  for row in data:
    as_tuple = tuple([ AS(fix_id(a['id']), fix_name(a['name']), fix_name(a['rdfs_label'])) for a in row['anatomical_structures'] ])
    if as_tuple not in seen:
      seen.add(as_tuple)
      yield as_tuple

with open(OUTPUT_CSV, 'w') as out_f:
  out = csv.writer(out_f)
  out.writerow('Name,HuBMAP Preferred Name,Ontology ID,Parent name,Parent ID,Cell-Type,Curator'.split(','))
  body = AS('UBERON:0013702', 'body', 'body')

  # Patches for use the EUI
  out.writerow(['left kidney', 'left kidney', 'UBERON:0004538', 'kidney', 'UBERON:0002113', 'N', '0000-0001-7655-4833'])
  out.writerow(['right kidney', 'right kidney', 'UBERON:0004539', 'kidney', 'UBERON:0002113', 'N', '0000-0001-7655-4833'])
  out.writerow(['pelvis', 'pelvis', 'UBERON:0001270', body.rdfs_label, body.id, 'N', '0000-0001-7655-4833'])
  out.writerow(['bone marrow', 'bone marrow', 'UBERON:0002371', 'pelvis', 'UBERON:0001270', 'N', '0000-0001-7655-4833'])
  out.writerow(['blood', 'blood', 'UBERON:0000178', 'pelvis', 'UBERON:0001270', 'N', '0000-0001-7655-4833'])
  out.writerow(['blood vasculature', 'blood vasculature', 'UBERON:0004537', body.rdfs_label, body.id, 'N', '0000-0001-7655-4833'])
  out.writerow(['lung', 'lung', 'UBERON:0002048', body.rdfs_label, body.id, 'N', '0000-0001-7655-4833'])
  out.writerow(['respiratory system', 'respiratory system', 'UBERON:0001004', 'lung', 'UBERON:0002048', 'N', '0000-0001-7655-4833'])
  out.writerow(['mesenteric lymph node', 'mesenteric lymph node', 'UBERON:0002509', 'lymph node', 'UBERON:0000029', 'N', '0000-0001-7655-4833'])
  out.writerow(['left eye', 'left eye', 'UBERON:0004548', 'eye', 'UBERON:0000970', 'N', '0000-0001-7655-4833'])
  out.writerow(['right eye', 'right eye', 'FMAID:54449', 'eye', 'UBERON:0000970', 'N', '0000-0001-7655-4833'])
  out.writerow(['left fallopian tube', 'left fallopian tube', 'UBERON:0001303', 'fallopian tube', 'UBERON:0003889', 'N', '0000-0001-7655-4833'])
  out.writerow(['right fallopian tube', 'right fallopian tube', 'UBERON:0001302', 'fallopian tube', 'UBERON:0003889', 'N', '0000-0001-7655-4833'])
  out.writerow(['left knee', 'left knee', 'FMAID:24978', 'knee', 'UBERON:0001465', 'N', '0000-0001-7655-4833'])
  out.writerow(['right knee', 'right knee', 'FMAID:24977', 'knee', 'UBERON:0001465', 'N', '0000-0001-7655-4833'])
  out.writerow(['left ovary', 'left ovary', 'FMAID:7214', 'ovary', 'UBERON:0000992', 'N', '0000-0001-7655-4833'])
  out.writerow(['right ovary', 'right ovary', 'FMAID:7213', 'ovary', 'UBERON:0000992', 'N', '0000-0001-7655-4833'])
  out.writerow(['left ureter', 'left ureter', 'UBERON:0001223', 'ureter', 'UBERON:0000056', 'N', '0000-0001-7655-4833'])
  out.writerow(['right ureter', 'right ureter', 'UBERON:0001222', 'ureter', 'UBERON:0000056', 'N', '0000-0001-7655-4833'])

  seen = defaultdict(dict)
  # for in_f in listdir(ASCT_RELEASE_DIR):
  #   if in_f.endswith('.csv'):
  #     for row in asct_rows(path.join(ASCT_RELEASE_DIR, in_f)):
  for row in asct_rows2():
    for i, node in enumerate(row):
      if not good_node(node):
        node = as_temp_node(node)
      if i == 0:
        if (node.id, None) not in seen:
          out.writerow([node.rdfs_label, node.name, node.id, body.rdfs_label, body.id, 'N', '0000-0001-7655-4833'])
      elif good_node(row[i-1]):
        parent = row[i-1]
        if node.id != parent.id and (node.id, parent.id) not in seen:
          out.writerow([node.rdfs_label, node.name, node.id, parent.rdfs_label, parent.id, 'N', '0000-0001-7655-4833'])
