#!/usr/bin/env python3
import json
from rdflib import Graph
from constants import CCF_CONTEXT, CCF_REFERENCE_ENTITIES, CCF_REFERENCE_ENTITIES_RDF


g = Graph()

context = json.load(open(CCF_CONTEXT))
for entity in json.load(open(CCF_REFERENCE_ENTITIES)):
  entity['@context'] = context
  g.parse(data=json.dumps(entity), format='json-ld')

g.serialize(CCF_REFERENCE_ENTITIES_RDF, format='xml')
