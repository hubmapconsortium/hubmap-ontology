#!/usr/bin/env python3
import bz2, glob, json
from collections import namedtuple
import networkx as nx
from csv import DictReader
from operator import itemgetter
from os import path
from owlready2 import *
from rdflib.extras.infixowl import OWL, Class, Restriction
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, Literal
from constants import CCF_NAMESPACE, CCF_PARTONOMY_TERMS, CCF_PARTONOMY_RDF, CCF_PARTONOMY_JSONLD


ONTO_CACHE='source_ontologies/cache.sqlite'

ASTempTerm = namedtuple('ASCTB_TEMP', ['iri', 'label', 'hasExactSynonym'])

set_log_level(1)

def load_ontology(bzFile):
  return get_ontology(f'file://{bzFile}'.replace('.bz2', '')).load(fileobj=bz2.open(bzFile, 'r'))

def load_ontologies():
  if not path.exists(ONTO_CACHE):
    default_world.set_backend(filename=ONTO_CACHE)
    for bzFile in glob.glob('source_ontologies/*.owl.bz2'):
      load_ontology(bzFile)
    default_world.save()
  else:
    default_world.set_backend(filename=ONTO_CACHE)

load_ontologies()

def get_term(term_str):
  if term_str.startswith('ASCTB-TEMP:'):
    term_str = term_str.split(':')[-1].strip()
    iri = f'https://purl.org/ccf/ASCTB-TEMP_{term_str}'
    term = [ASTempTerm(iri, [term_str.replace('-', ' ')], [])]
  elif term_str.startswith('CL:'):
    term_str = term_str.split(':')[-1].strip()
    term = default_world.search(iri=f'http://purl.obolibrary.org/obo/CL_{term_str}')
  elif term_str.startswith('FMA'):
    term_str = term_str.split(':')[-1].strip()
    term = default_world.search(iri=f'http://purl.org/sig/ont/fma/fma{term_str}')
    #term = default_world.search(iri=f'http://purl.obolibrary.org/obo/FMA_{term_str}')
  else:
    term = default_world.search(id=term_str)

  return term[0] if len(term) > 0 else None

def get_term_data(id, label, term, order, parent = None):
  return {
    '@id': term.iri,
    'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym': [
      { '@value': l } for l in term.hasExactSynonym
    ],
    'http://www.w3.org/2000/01/rdf-schema#label': [{
      '@value': label.lower()
    }],
    'http://www.geneontology.org/formats/oboInOwl#id': [{
      '@value': id
    }],
    'parent': [{'@id': parent.iri}] if parent else None,
    'order': order
  }

TERMS = [
  'http://purl.obolibrary.org/obo/UBERON_0000955', # Brain
  'http://purl.obolibrary.org/obo/UBERON_0000029', # Lymph Node
  # 'http://purl.obolibrary.org/obo/UBERON_0002509', # Mesenteric Lymph Node
  'http://purl.obolibrary.org/obo/UBERON_0000970', # Eye
  # 'http://purl.obolibrary.org/obo/UBERON_0004548', # Eye, L
  # 'http://purl.obolibrary.org/obo/FMA_54449', # Eye, R
  'http://purl.obolibrary.org/obo/UBERON_0003889', # Fallopian Tube
  # 'http://purl.obolibrary.org/obo/UBERON_0001303', # Fallopian Tube, L
  # 'http://purl.obolibrary.org/obo/UBERON_0001302', # Fallopian Tube, R
  'http://purl.obolibrary.org/obo/UBERON_0000948', # Heart
  'http://purl.obolibrary.org/obo/UBERON_0002113', # Kidney
  # 'http://purl.obolibrary.org/obo/UBERON_0004538', # Kidney, L
  # 'http://purl.obolibrary.org/obo/UBERON_0004539', # Kidney, R
  'http://purl.obolibrary.org/obo/UBERON_0001465', # Knee
  # 'http://purl.obolibrary.org/obo/FMA_24978', # Knee, L
  # 'http://purl.obolibrary.org/obo/FMA_24977', # Knee, R
  'http://purl.obolibrary.org/obo/UBERON_0002107', # Liver
  'http://purl.obolibrary.org/obo/UBERON_0002048', # Lungs
  'http://purl.obolibrary.org/obo/UBERON_0000992', # Ovary
  # 'http://purl.obolibrary.org/obo/FMA_7214', # Ovary, L
  # 'http://purl.obolibrary.org/obo/FMA_7213', # Ovary, R
  'http://purl.obolibrary.org/obo/UBERON_0001264', # Pancreas
  'http://purl.obolibrary.org/obo/UBERON_0001270', # Pelvis
  'http://purl.obolibrary.org/obo/UBERON_0002367', # Prostate Gland
  'http://purl.obolibrary.org/obo/UBERON_0002097', # Skin
  'http://purl.obolibrary.org/obo/UBERON_0002108', # Small Intestine
  'http://purl.obolibrary.org/obo/UBERON_0000059', # Large Intestine
  'http://purl.obolibrary.org/obo/UBERON_0002106', # Spleen
  'http://purl.obolibrary.org/obo/UBERON_0002370', # Thymus
  'http://purl.obolibrary.org/obo/UBERON_0000056', # Ureter
  # 'http://purl.obolibrary.org/obo/UBERON_0001223', # Ureter, L
  # 'http://purl.obolibrary.org/obo/UBERON_0001222', # Ureter, R
  'http://purl.obolibrary.org/obo/UBERON_0001255', # Urinary Bladder
  'http://purl.obolibrary.org/obo/UBERON_0000995', # Uterus
  'http://purl.obolibrary.org/obo/UBERON_0004537' # Blood Vasculature
]

with open(CCF_PARTONOMY_TERMS) as in_f:
  ccf_ns = Namespace(f'{CCF_NAMESPACE}#')
  ccf_part_of = ccf_ns.ccf_part_of
  g = Graph()
  g.namespace_manager.bind('ccf', ccf_ns, override=False)
  g.namespace_manager.bind('owl', OWL, override=False)
  classes = {}
  tree = nx.DiGraph()

  body = get_term('UBERON:0013702')
  terms = { body.iri: get_term_data('UBERON:0013702', 'body', body, 0, None) }

  for order, row in enumerate(DictReader(in_f)):
    if row['Cell-Type'] == 'Y':
      continue
    parent = row['Parent ID']
    child = row['Ontology ID']

    child_term = get_term(child)
    parent_term = get_term(parent)

    if child_term and parent_term:
      if child_term.iri == parent_term.iri:
        print(f'Removed self-link: {child}: {child_term.iri}')
      else:
        tree.add_edge(parent_term.iri, child_term.iri)

        child_label = row['HuBMAP Preferred Name'].strip()
        if not child_label:
          child_label = child_term.label[0]

        terms[child_term.iri] = get_term_data(child, child_label, child_term, order, parent_term)
        if parent_term.iri not in terms:
          parent_label = parent_term.label[0]
          terms[parent_term.iri] = get_term_data(parent, parent_label, parent_term, order, body)
    elif len(parent+child.strip()) > 0:
      print(f'Parent: {parent} ({ "Null" if parent_term is None else "Not null" }), Child: {child} ({"Null" if child_term is None else "Not null"})')
  
  for term in TERMS:
    tree.add_edge('root', term)

  tree = nx.bfs_tree(tree, 'root')
  for (parent_iri, child_iri) in tree.edges:
    if parent_iri == 'root':
      parent_iri = body.iri
    g.add( (URIRef(child_iri), ccf_part_of, URIRef(parent_iri)) )

    if parent_iri not in classes:
      classes[parent_iri] = Class(URIRef(parent_iri), graph=g)
    if child_iri not in classes:
      classes[child_iri] = Class(URIRef(child_iri), graph=g)

    parent_class = classes[parent_iri]
    child_class = classes[child_iri]
    child_class.subClassOf = [parent_class, Restriction(ccf_part_of, graph=g, someValuesFrom=parent_class)]

  for t in terms.values():
    term = URIRef(t['@id'])
    label = Literal(t['http://www.w3.org/2000/01/rdf-schema#label'][0]['@value'])
    id = Literal(t['http://www.geneontology.org/formats/oboInOwl#id'][0]['@value'])

    g.add( (term, RDFS.label, label) )
    g.add( (term, ccf_ns.ccf_preferred_label, label) )
    g.add( (term, ccf_ns.ccf_part_of_rank, Literal(t['order'])) )
    g.add( (term, URIRef('http://www.geneontology.org/formats/oboInOwl#id'), id) )

    for synonym in t['http://www.geneontology.org/formats/oboInOwl#hasExactSynonym']:
      g.add( (term, URIRef('http://www.geneontology.org/formats/oboInOwl#hasExactSynonym'), Literal(synonym['@value'])) )

  term_list = list(sorted(terms.values(), key=itemgetter('order')))
  json.dump(term_list, open(CCF_PARTONOMY_JSONLD, 'w'), indent=2)
  g.serialize(CCF_PARTONOMY_RDF, format='xml')
