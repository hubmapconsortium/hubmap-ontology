import bz2, glob
from csv import DictReader
from owlready2 import *
from rdflib import Graph, Namespace, URIRef
from constants import CCF_NAMESPACE, CCF_PARTONOMY_TERMS, CCF_PARTONOMY_RDF


set_log_level(1)

def load_ontology(bzFile):
  return get_ontology(f'file://{bzFile}'.replace('.bz2', '')).load(fileobj=bz2.open(bzFile, 'r'))

def load_ontologies():
  for bzFile in glob.glob('source_ontologies/*.owl.bz2'):
    load_ontology(bzFile)

load_ontologies()

def get_term(term_str):
  if term_str.startswith('FMAID'):
    term_str = term_str.split(':')[-1].strip()
    term = default_world.search(iri=f'http://purl.org/sig/ont/fma/fma{term_str}')
  else:
    term = default_world.search(id=term_str)

  return term[0] if len(term) > 0 else None

with open(CCF_PARTONOMY_TERMS) as in_f:
  ccf_ns = Namespace(f'{CCF_NAMESPACE}#')
  ccf_part_of = ccf_ns.ccf_part_of
  g = Graph()
  g.namespace_manager.bind('ccf', ccf_ns, override=False)

  for row in DictReader(in_f):
    parent = row['Parent ID']
    child = row['Ontology ID']

    child_term = get_term(child)
    parent_term = get_term(parent)

    if child_term and parent_term:
      g.add( (URIRef(child_term.iri), ccf_part_of, URIRef(parent_term.iri)) )

    elif len(parent+child.strip()) > 0:
      print(f'Parent: {parent}, Child: {child}')

  g.serialize(CCF_PARTONOMY_RDF, format='xml')
