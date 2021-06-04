#!/usr/bin/env python3
import json
from rdflib import Graph
from constants import CCF_CONTEXT, CCF_GENERATED_REFERENCE_ENTITIES, CCF_REFERENCE_ENTITIES, CCF_REFERENCE_ENTITIES_RDF


g = Graph()

context = json.load(open(CCF_CONTEXT))
entities = json.load(open(CCF_REFERENCE_ENTITIES)) + json.load(open(CCF_GENERATED_REFERENCE_ENTITIES))
for entity in entities:
  entity['@context'] = context
  if 'placement' in entity:
    placement = entity['placement']
    if isinstance(placement, list):
      for p in placement:
        p['@context'] = context
    elif placement:
      placement['@context'] = context
  g.parse(data=json.dumps(entity), format='json-ld')

g.serialize(CCF_REFERENCE_ENTITIES_RDF, format='xml')
