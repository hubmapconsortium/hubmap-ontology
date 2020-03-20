#!/usr/bin/env python3
from collections import deque
import json, csv
import networkx as nx
from constants import CCF_PARTONOMY_JSONLD, CCF_PARTONOMY_CSV


def dfs_nodes(G, root_node, sort_key = 'order'):
  q = deque()
  q.extend([(root_node, 0)])
  sorter = lambda x: G.nodes[x].get(sort_key, 0)
  while len(q) > 0:
    n, depth = q.popleft()
    for child in sorted(G.successors(n), key=sorter):
      q.appendleft((child, depth + 1))
    yield n, depth

def get_nodes(input_json):
  nodes = json.load(open(input_json))
  for n in nodes:
    data = {
      'iri': n['@id'],
      'synonyms': map(lambda s: s['@value'], n['http://www.geneontology.org/formats/oboInOwl#hasExactSynonym']),
      'label': n['http://www.w3.org/2000/01/rdf-schema#label'][0]['@value'],
      'id': n['http://www.geneontology.org/formats/oboInOwl#id'][0]['@value'],
      'parent': None if not n['parent'] else n['parent'][0]['@id'],
      'order': n['order']
    }
    yield data['iri'], data

def write_partonomy_report(input_json, output_csv, root_node='http://purl.obolibrary.org/obo/UBERON_0013702'):
  G = nx.DiGraph()
  for n, data in get_nodes(input_json):
    G.add_node(n, **data)
  for child, parent in G.nodes.data('parent'):
    if parent is not None:
      G.add_edge(parent, child, weight=G.nodes[child]['order'])

  with open(output_csv, 'w') as out_f:
    out = csv.writer(out_f)
    out.writerow(['Label (indented)', 'ID', 'Synonyms'])
    for n, depth in dfs_nodes(G, root_node):
      row = [ str('    ' * depth) + str(G.nodes[n]['label']), G.nodes[n]['id'] ]
      row.extend(G.nodes[n]['synonyms'])
      out.writerow(row)

if __name__ == "__main__":
  from sys import argv
  if len(argv) == 2:
    write_partonomy_report(CCF_PARTONOMY_JSONLD, argv[1])
  elif len(argv) == 3:
    write_partonomy_report(CCF_PARTONOMY_JSONLD, argv[1], argv[2])
  else:
    write_partonomy_report(CCF_PARTONOMY_JSONLD, CCF_PARTONOMY_CSV)
