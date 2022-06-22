import csv, json, re
from collections import namedtuple, defaultdict

ASCTB_JSON='dist/ccf-asctb.json'
OUTPUT_CSV='source_data/ccf-term-list.csv'
GOOD_ONTOLOGIES = set(['CL', 'UBERON', 'FMA', 'FMAID'])

Node = namedtuple('OntologyNode', ['type', 'id', 'name', 'rdfs_label'])

# Fix IDs from ASCT+B Tables. Ideally, these changes are made up stream for next release and no transformation is necessary
def fix_id(idstr):
  if idstr.startswith('fma') and idstr[3].isdigit():
    idstr = 'fma:'+idstr[3:]
  idstr = idstr.replace('_', ':').replace('::', ':').replace(': ', ':').replace('FMA:', 'FMAID:').replace('fma:', 'FMAID:').split(' ')[0].upper()
  idstr = ':'.join(map(lambda s: s.strip(), idstr.split(':')))
  return idstr.strip()

# Fix names. Ideally this is not needed when changes are made up stream.
def fix_name(name):
  if name == 'thoracic thymus':
    return 'thymus'
  return name.strip()

def good_node(node):
  onto_val = node.id.split(':', 1)
  return node.id and onto_val[0] in GOOD_ONTOLOGIES and len(onto_val) == 2 and len(onto_val[1]) > 0

def temp_node(node):
  suffix = re.sub(r'[^a-z0-9-]+', '', re.sub(r'\W+', '-', node.name.lower().strip()))
  ontologyId = f'ASCTB-TEMP:{suffix}'
  return Node(node.type, ontologyId, node.name, node.name)

def asct_rows():
  data = json.load(open(ASCTB_JSON))['data']
  seen = set()
  for row in data:
    as_tuple = tuple([ Node('AS', fix_id(a['id']), fix_name(a['name']), fix_name(a['rdfs_label'])) for a in row['anatomical_structures'] ])
    ct_tuple = tuple([ Node('CT', fix_id(a['id']), fix_name(a['rdfs_label']) or fix_name(a['name']), fix_name(a['rdfs_label'])) for a in row['cell_types'] ])
    if as_tuple not in seen:
      seen.add(as_tuple)
      yield 'AS', as_tuple
    if ct_tuple not in seen:
      seen.add(ct_tuple)
      yield 'CT', ct_tuple
    if len(as_tuple) > 0 and len(ct_tuple) > 0:
      for ct_term in ct_tuple:
        for as_term in as_tuple:
          asct_tuple = tuple([as_term, ct_term])
          if asct_tuple not in seen:
            seen.add(asct_tuple)
            yield 'AS_CT', asct_tuple

with open(OUTPUT_CSV, 'w') as out_f:
  out = csv.writer(out_f)
  out.writerow('EdgeType,Name,HuBMAP Preferred Name,Ontology ID,Parent name,Parent ID'.split(','))
  body = Node('AS', 'UBERON:0013702', 'body', 'body')
  cell = Node('CT', 'CL:0000000', 'cell', 'cell')

  # Patches for use the EUI
  out.writerow(['AS','left kidney', 'left kidney', 'UBERON:0004538', 'kidney', 'UBERON:0002113'])
  out.writerow(['AS','right kidney', 'right kidney', 'UBERON:0004539', 'kidney', 'UBERON:0002113'])
  out.writerow(['AS','pelvis', 'pelvis', 'UBERON:0001270', body.rdfs_label, body.id])
  out.writerow(['AS','bone marrow', 'bone marrow', 'UBERON:0002371', 'pelvis', 'UBERON:0001270'])
  out.writerow(['AS','blood', 'blood', 'UBERON:0000178', 'pelvis', 'UBERON:0001270'])
  out.writerow(['AS','blood vasculature', 'blood vasculature', 'UBERON:0004537', body.rdfs_label, body.id])
  out.writerow(['AS','lung', 'lung', 'UBERON:0002048', body.rdfs_label, body.id])
  out.writerow(['AS','respiratory system', 'respiratory system', 'UBERON:0001004', 'lung', 'UBERON:0002048'])
  out.writerow(['AS','mesenteric lymph node', 'mesenteric lymph node', 'UBERON:0002509', 'lymph node', 'UBERON:0000029'])
  out.writerow(['AS','left eye', 'left eye', 'UBERON:0004548', 'eye', 'UBERON:0000970'])
  out.writerow(['AS','right eye', 'right eye', 'UBERON:0004549', 'eye', 'UBERON:0000970'])
  out.writerow(['AS','left fallopian tube', 'left fallopian tube', 'UBERON:0001303', 'fallopian tube', 'UBERON:0003889'])
  out.writerow(['AS','right fallopian tube', 'right fallopian tube', 'UBERON:0001302', 'fallopian tube', 'UBERON:0003889'])
  out.writerow(['AS','left knee', 'left knee', 'FMAID:24978', 'knee', 'UBERON:0001465'])
  out.writerow(['AS','right knee', 'right knee', 'FMAID:24977', 'knee', 'UBERON:0001465'])
  out.writerow(['AS','left ovary', 'left ovary', 'FMAID:7214', 'ovary', 'UBERON:0000992'])
  out.writerow(['AS','right ovary', 'right ovary', 'FMAID:7213', 'ovary', 'UBERON:0000992'])
  out.writerow(['AS','left ureter', 'left ureter', 'UBERON:0001223', 'ureter', 'UBERON:0000056'])
  out.writerow(['AS','right ureter', 'right ureter', 'UBERON:0001222', 'ureter', 'UBERON:0000056'])
  out.writerow(['AS','spinal cord', 'spinal cord', 'UBERON:0002240', body.rdfs_label, body.id])

  seen = defaultdict(dict)
  for edge_type, row in asct_rows():
    for i, node in enumerate(row):
      if not good_node(node):
        node = temp_node(node)
      if i == 0:
        if edge_type != 'AS_CT' and (node.id, None) not in seen:
          parent = body if node.type == 'AS' else cell
        else:
          parent = None
      elif good_node(row[i-1]):
        parent = row[i-1]

      if parent and node.id != parent.id and (node.id, parent.id) not in seen:
        out.writerow([edge_type,node.rdfs_label, node.name, node.id, parent.rdfs_label, parent.id])
