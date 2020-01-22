from constants import CCF_FULL_ONTOLOGY, CCF_MODEL, CCF_PARTONOMY_RDF, CCF_REFERENCE_ENTITIES_RDF

from rdflib import Graph
import json


g = Graph()
g.parse(CCF_MODEL, format='xml')
g.parse(CCF_PARTONOMY_RDF, format='xml')
g.parse(CCF_REFERENCE_ENTITIES_RDF, format='xml')
g.serialize(CCF_FULL_ONTOLOGY, format='xml')
