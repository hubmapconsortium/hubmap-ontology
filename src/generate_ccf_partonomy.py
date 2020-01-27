#!/usr/bin/env python3
import bz2, glob, json
from csv import DictReader
from operator import itemgetter
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

def get_term_data(id, label, term, order, parent = None):
  return {
    '@id': term.iri,
    'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym': [
      { '@value': l } for l in term.hasExactSynonym
    ],
    'http://www.w3.org/2000/01/rdf-schema#label': [{
        '@value': label
    }],
    'http://www.geneontology.org/formats/oboInOwl#id': [{
        '@value': id
      }],
    'parent': [{'@id': parent.iri}] if parent else None,
    'order': order
  }

with open(CCF_PARTONOMY_TERMS) as in_f:
  ccf_ns = Namespace(f'{CCF_NAMESPACE}#')
  ccf_part_of = ccf_ns.ccf_part_of
  g = Graph()
  g.namespace_manager.bind('ccf', ccf_ns, override=False)

  body = get_term('UBERON:0005172')
  terms = { body.iri: get_term_data('UBERON:0005172', 'Body', body, 0, None) }

  for order, row in enumerate(DictReader(in_f)):
    parent = row['Parent ID']
    child = row['Ontology ID']

    child_term = get_term(child)
    parent_term = get_term(parent)

    if child_term and parent_term:
      if child_term.iri == parent_term.iri:
        print(f'Removed self-link: ${child}: ${child_term.iri}')
      else:
        g.add( (URIRef(child_term.iri), ccf_part_of, URIRef(parent_term.iri)) )

        child_label = row['HuBMAP Preferred Name'].strip()
        if not child_label:
          child_label = child_term.label

        terms[child_term.iri] = get_term_data(child, child_label, child_term, order, parent_term)
        if parent_term.iri not in terms:
          parent_label = parent_term.label
          terms[parent_term.iri] = get_term_data(parent, parent_label, parent_term, order, body)
    elif len(parent+child.strip()) > 0:
      print(f'Parent: {parent}, Child: {child}')

  term_list = list(sorted(terms.values(), key=itemgetter('order')))
  json.dump(term_list, open('dist/ccf-partonomy.jsonld', 'w'), indent=2)
  g.serialize(CCF_PARTONOMY_RDF, format='xml')
