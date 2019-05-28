#!/usr/bin/python3
#######################################################################
#
# This code takes an ontospy object and makes a Networkx graph
#
# Copyright, Samuel Friedman, Opto-Knowledge Systems, Inc. (OKSI), 2019
#
# Licensed under the MIT License.
#
# This code is for the NIH HuBMAP Consortium.
#
#######################################################################

import ontospy
import yaml
import ontotree

def load_ontology(filename):
    """Load the onology into memory"""
    # Load the ontology
    o = ontospy.Ontospy()
    o.load_rdf(filename)
    #o.build_all()
    o.build_classes() # We only use the classes, so no need to build everything
    o.build_properties() # We need this to export property names
    return o

def load_settings(owl_settings_filename):
    """Read the settings file"""
    owl_settings = open(owl_settings_filename,"r").read()
    owl_settings_dict = yaml.load(owl_settings)
    return owl_settings_dict

def create_slim_ontology(owl_settings_filename):
    """Create the ontology, compute its slim form, and write it"""
    owl_settings_dict = load_settings(owl_settings_filename)
    o = load_ontology(owl_settings_dict["ontologies"]["UBERON_filename"])
    #o_cl = load_ontology(owl_settings_dict["ontologies"]["CL_filename"]) # Load CL
    o_graph = ontotree.ontotree()
    o_graph.load_terms(owl_settings_dict)
    o_graph.create_graph(o)
    o_graph.write_ont(o,owl_settings_dict, 0) # Write ontology
    o_graph.write_ont(o,owl_settings_dict, 1) # Write partonomy with XML
    o_graph.write_ont(o,owl_settings_dict, 2) # Write partonomy with JSON-LD
    return o, o_graph

if __name__ == "__main__":
    owl_settings_filename = "owl_settings.yml"
    create_slim_ontology(owl_settings_filename)
    

