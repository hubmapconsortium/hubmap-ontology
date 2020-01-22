#!/usr/bin/env python3
import json
from rdflib import Graph
from constants import CCF_CONTEXT, HUBMAP_ENTITIES, HUBMAP_ENTITIES_RDF


g = Graph()

context = json.load(open(CCF_CONTEXT))
for entity in json.load(open(HUBMAP_ENTITIES)):
  entity['@context'] = context
  g.parse(data=json.dumps(entity), format='json-ld')

g.serialize(HUBMAP_ENTITIES_RDF, format='xml')
