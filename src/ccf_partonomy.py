from environment import CCF_NAMESPACE, CCF_PARTONOMY_TERMS, CCF_PARTONOMY_RDF

from owlready2 import *
from rdflib import Graph, Namespace, URIRef
from csv import DictReader


default_world.set_backend(filename='source_ontologies/cache.sqlite')

# Source: https://bioportal.bioontology.org/ontologies/UO
uo = get_ontology('file://source_ontologies/uo.owl').load()

# From https://bioportal.bioontology.org/ontologies/DC
dc = get_ontology('file://source_ontologies/dublincore.owl').load()

# From https://bioportal.bioontology.org/ontologies/FMA
fma = get_ontology('file://source_ontologies/fma.owl').load()

# From https://bioportal.bioontology.org/ontologies/LUNGMAP-HUMAN
lmha = get_ontology('file://source_ontologies/LMHA_20190728.owl').load()

# From http://ontologies.berkeleybop.org/uberon/subsets/human-view.owl
uberon = get_ontology('file://source_ontologies/uberon-human-view.owl').load()

# From CCF_NAMESPACE
ccf = get_ontology('file://docs/ccf-model.owl').load()

# OBO Namespace
obo = uberon.get_namespace('http://purl.obolibrary.org/obo/')

# Dublic core Namespace
dc = dc.get_namespace('http://purl.org/dc/elements/1.1/', name='dc')

default_world.save()

def get_term(term_str):
  if term_str.startswith('FMAID'):
    term_str = term_str.split(':')[-1].strip()
    term = fma.search(iri=f'http://purl.org/sig/ont/fma/fma{term_str}')
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
