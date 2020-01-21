from environment import CCF_FULL_ONTOLOGY, CCF_MODEL, CCF_PARTONOMY_RDF, CCF_CONTEXT, CCF_REFERENCE_SPATIAL_ENTITIES

from rdflib import Graph
import json


g = Graph()
g.parse(CCF_MODEL, format='xml')
g.parse(CCF_PARTONOMY_RDF, format='xml')

context = json.load(open(CCF_CONTEXT))
for entity in json.load(open(CCF_REFERENCE_SPATIAL_ENTITIES)):
  entity['@context'] = context
  g.parse(data=json.dumps(entity), format='json-ld')

g.serialize(CCF_FULL_ONTOLOGY, format='xml')
