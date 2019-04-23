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

import networkx as nx
import ontospy
from urllib.parse import urldefrag
import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_digraph, rdflib_to_networkx_multidigraph
import copy
import pandas as pd
import pydot
import yaml
import re
import numpy as np

# Take ontology class and get its label
def class_label(onto_class):
    label_info = list(onto_class.rdflib_graph.subject_objects(predicate=rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label')))
    #print(onto_class.locale)
    if len(label_info) != 0:
        #print(label_info, )
        return label_info[0][1].value
    else:
        return onto_class.locale

# Take the ontology ID and get its label
#def node_label(g,o, id):
#    return class_label(o.get_class(list(g.nodes)
def id_label(o, ont_id):
    return class_label(o.get_class(ont_id)[0])

def partof_subclassof_list(onto_class_rdflib_graph, onto_class_locale):
    part_of = rdflib.term.URIRef("http://purl.obolibrary.org/obo/BFO_0000050")
    some_values_from = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#someValuesFrom')
    subclassof_rdf = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')

    subclassof_list = list(onto_class_rdflib_graph.objects(predicate=(subclassof_rdf)))
    ps_list = [] #partof_subclassof_list
    for subclassof in subclassof_list:
        if type(subclassof) == rdflib.term.BNode:
            bnode_objects = list(onto_class_rdflib_graph.objects(subclassof))
            bnode_predicates = list(onto_class_rdflib_graph.predicates(subclassof))
            #print(bnode_predicates)
            if part_of in bnode_objects:
                part_of_node = rdflib.term.URIRef(list(onto_class_rdflib_graph.objects(subclassof,some_values_from))[0])
                
                #g.add_edge(onto_class.locale, ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], type='PartOf')
                ps_list.append((ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], onto_class_locale))
    return ps_list

def load_ontology(filename):
    # Load the ontology
    o = ontospy.Ontospy()
    o.load_rdf(filename)
    #o.build_all()
    o.build_classes() # We only use the classes, so no need to build everything
    return o

owl_settings = open("owl_settings.yml","r").read()
owl_settings_dict = yaml.load(owl_settings)
ontologies_string = "ontologies"

o = load_ontology(owl_settings_dict["ontologies"]["UBERON_filename"])
#o_cl = load_ontology(owl_settings_dict["ontologies"]["CL_filename"]) # Load CL
# Use a sample element
anatomical_system_id = "UBERON_0000467"
# Load nodes and root nodes
ccf_df = pd.read_csv("ccf_input_terms.csv")
ccf_df = ccf_df[ccf_df['Ontology ID'].notnull()] # Filter out nulls
ccf_df = ccf_df[~ccf_df['Ontology ID'].str.startswith("fma")] # Filter out fma only terms
node_ids = list(ccf_df['Ontology ID'])
ancestor_nodes = list(ccf_df['Parent ID'])
descendants = list(ccf_df['Descendants'])
root_nodes = set(ccf_df['Parent ID'])

# Create the graph
subclassof_string = 'SubClassOf'
partof_string = 'PartOf'
classassertion_string = 'ClassAssertion'
part_of = rdflib.term.URIRef("http://purl.obolibrary.org/obo/BFO_0000050")
some_values_from = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#someValuesFrom')
equivalent_class = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#equivalentClass')
subclassof_rdf = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')

# Create graph from the ontology
g = nx.DiGraph(IRI="hubmap.owl")
for onto_class in o.all_classes:
    g.add_node(onto_class.locale, type='Class')

    for parent in onto_class.parents():
        # This works for UBERON at least
        g.add_edge(onto_class.locale, parent.locale, type=subclassof_string)

        for instance in onto_class.instances:
            start_url, fragment = urldefrag(instance)
            g.add_edge(fragment, onto_class.locale, type=classassertion_string)

# Check later if reversal is still necessary
g = g.reverse(copy=False)
g_orig = nx.DiGraph(g)
g = nx.DiGraph(g)

# Add partOf and equivalentClass to the graph
for onto_class in o.all_classes:
    # Find more complex subClassOf objects that rdflib identifies through BNode elements
    subclassof_list = list(onto_class.rdflib_graph.objects(predicate=(subclassof_rdf)))
    # Below needs to be replaced by function that is already defined
    for subclassof in subclassof_list:
        if type(subclassof) == rdflib.term.BNode:
            bnode_objects = list(onto_class.rdflib_graph.objects(subclassof))
            bnode_predicates = list(onto_class.rdflib_graph.predicates(subclassof))
            #print(bnode_predicates)
            if part_of in bnode_objects:
                part_of_node = rdflib.term.URIRef(list(onto_class.rdflib_graph.objects(subclassof,some_values_from))[0])
                g.add_edge(ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], onto_class.locale, type=partof_string)
    # Handle equivalentClass 
    equivalentClass_list = list(onto_class.rdflib_graph.objects(predicate=equivalent_class))
    

# Add weights to the graph
for edge in g.edges:
    edge_type = g.get_edge_data(*edge)['type']
    edge_weight = 0
    if edge_type == subclassof_string:
        edge_weight = 1
    elif edge_type == partof_string:
        edge_weight = 20
    g.get_edge_data(*edge)['weight'] = edge_weight
# Boost weights to nodes
for root_node in root_nodes:
    for edge in g.out_edges(root_node):
        g.get_edge_data(*edge)['weight'] += 100
node_ancestor_pairs = list(zip(ancestor_nodes,node_ids))
for root_node, node in node_ancestor_pairs:
    if root_node == node:
        continue
    root_node_simple_paths = list(nx.all_simple_paths(g,root_node,node))
    if len(root_node_simple_paths) == 0: # Error reporting from CSV file
        print(root_node, node, id_label(o,root_node), id_label(o,node))
    for path in root_node_simple_paths:
        for i in range(len(path)-1):
            g.get_edge_data(path[i],path[i+1])['weight'] += 500
for root_node in root_nodes:                
    # Boost weights from anatomical system to root nodes
    # Find the shortest path between the root node and anatomical system
    root_node_simple_paths = list(nx.all_simple_paths(g,anatomical_system_id,root_node))
    if len(root_node_simple_paths) > 0: # Only do this if there's a path to anatomical system
        lengths_of_simple_paths = [len(path) for path in root_node_simple_paths]
        shortest_path_index = np.argmin(lengths_of_simple_paths)
        path = root_node_simple_paths[shortest_path_index]
        # Weight that path heavily (this should become a function call)
        for i in range(len(path)-1):
            g.get_edge_data(path[i],path[i+1])['weight'] += 5000

#Start at key/root node (e.g. kidney) and compute shortest path, least cost route to desired node (e.g. renal glomerulus)
#root_node_simple_paths = list(nx.all_simple_paths(g,kidney_id,rg_id))
#rg_ancestors = set(nx.algorithms.shortest_paths.generic.shortest_path(g,kidney_id,rg_id,weight='weight'))

# Make a slim version of the graph
node_tree_set = set()
for node_id, check_descendants in zip(node_ids,descendants):
    # Only add descendants if desired
    if check_descendants:
        node_tree_set |= nx.descendants(g,node_id)
    node_tree_set |= nx.ancestors(g,node_id)
    node_tree_set.add(node_id)
g_slim = g.subgraph(node_tree_set)

# Make a maximum branching
max_g_slim_large = nx.maximum_branching(g_slim)

# Remove everything coming into the kidney
in_edges_list = []
cutting_nodes = []
root_node_cut = False # This needs to become a settings parameter
if root_node_cut == True:
    cutting_nodes = root_nodes
else:
    cutting_nodes = [anatomical_system_id]
for cut_node in cutting_nodes:
    in_edges_list.extend(list(max_g_slim_large.in_edges(cut_node)))
max_g_slim_large.remove_edges_from(in_edges_list)

# Remove nodes and edges that do not contribute to supporting the input nodes
# The input nodes support all their descandant nodes
max_slim_nodes_support = set()
for node_id, check_descendants in zip(node_ids,descendants):
    if check_descendants:
        max_slim_nodes_support |= nx.descendants(max_g_slim_large, node_id)
    max_slim_nodes_support |= nx.ancestors(max_g_slim_large, node_id)
    max_slim_nodes_support |= set([node_id])
# Find the nodes that are not supported
max_g_slim_large_nodes = set(max_g_slim_large.nodes())
unsupported_max_g_slim_large_nodes = max_g_slim_large_nodes - max_slim_nodes_support
# Remove edges from unsupported nodes
unsupported_edges = set(max_g_slim_large.out_edges(unsupported_max_g_slim_large_nodes)) | set(max_g_slim_large.in_edges(unsupported_max_g_slim_large_nodes))
max_g_slim_large.remove_edges_from(unsupported_edges)

# Only work with components that have at least one edge:
list_of_components = list(max_g_slim_large.subgraph(c) for c in nx.weakly_connected_components(max_g_slim_large))
num_component_edges = np.array([len(component.edges()) for component in list_of_components])
max_g_slim_tree_indices = np.where(num_component_edges > 0)[0]
actual_trees_list = [list_of_components[i] for i in max_g_slim_tree_indices]
max_g_slim = nx.compose_all(actual_trees_list)

#g_slim - max_g_slim
removed_edges_list = list(set(g_slim.in_edges()) - set(max_g_slim.in_edges()))
removed_edges_dict = dict(removed_edges_list)
removed_edges = nx.difference(g_slim, max_g_slim_large)
#Remove nodes without edges

# create labels, nominally for plotting
g_slim_labels = {}
for node in max_g_slim:
    # Check for uberon
    if re.match(node,"UBERON") != None :
        g_slim_labels[node] = id_label(o,node)
    else: # Must be in CL
        g_slim_labels[node] = id_label(o_cl,node)

max_g_slim_relabeled = nx.relabel_nodes(max_g_slim,g_slim_labels,copy=True)
list_of_components = list(max_g_slim_relabeled.subgraph(c) for c in nx.weakly_connected_components(max_g_slim_relabeled))
dot_files = "dot_files"
re_whitespace = re.compile("\s+")
# Writing dot files
if dot_files in owl_settings_dict:
    dot_files_dict = owl_settings_dict[dot_files]
    if "entire_ontology" in dot_files_dict and dot_files_dict["entire_ontology"]:
        nx.drawing.nx_pydot.write_dot(max_g_slim_relabeled,"dot/slim.dot")
    # find the kidney component
    if "root_nodes" in dot_files_dict and dot_files_dict["root_nodes"]:
        list2_of_components = [list(list_of_components[i]) for i in range(len(list_of_components))]
        for root_node in root_nodes:
            root_node_name = id_label(o,root_node)
            root_node_name_finds = np.where(np.array([root_node_name in component for component in list2_of_components]))[0]
            if len(root_node_name_finds) > 0:
                root_node_index = root_node_name_finds[0]
                root_node_graph = list_of_components[root_node_index]
                root_node_name_snakecase = re_whitespace.sub("_",root_node_name)
                nx.drawing.nx_pydot.write_dot(root_node_graph,"dot/roots/"+root_node_name_snakecase+".dot")
    if "non_leaf_nodes" in dot_files_dict and dot_files_dict["non_leaf_nodes"]:
        for node in list(max_g_slim_relabeled.nodes):
            node_out_edges = max_g_slim_relabeled.out_edges(node)
            if len(node_out_edges) > 0:
                node_graph = max_g_slim_relabeled.edge_subgraph(node_out_edges)
                node_name_snakecase = re_whitespace.sub("_",node)
                nx.drawing.nx_pydot.write_dot(node_graph,"dot/non_leafs/"+node_name_snakecase+".dot")

# Turn graph back into ontology
#o_slim = ontospy.Ontospy()
o_slim_rdf_graph = rdflib.Graph()
onClass = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#onClass')
for node in max_g_slim:
    # Find the appropriate class from the original ontology
    new_o_class_rdflib_graph = copy.deepcopy(o.get_class(node)[0].rdflib_graph)
    # Substitue out the triple that was the partof that was problematic
    # First, find pairs that should be added
    ps_list = partof_subclassof_list(new_o_class_rdflib_graph, node)
    # Then add in the new subclassof relationship
    for ps_sub in ps_list:
        superclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+ps_sub[0])
        subclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+ps_sub[1])
        new_o_class_rdflib_graph.add((subclass_rdf, subclassof_rdf, superclass_rdf))
    # remove those edges from max_g_slim
    # Needs to be in_edges because of how subClassOf works
    #for edge in removed_edges:
    for removed_edge in removed_edges.in_edges(node):
        # Remove the RDF lib term
        superclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+removed_edge[0])
        subclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+removed_edge[1])
        new_o_class_rdflib_graph.remove((subclass_rdf,subclassof_rdf,superclass_rdf))
    # Remove any equivalentClasses (for now)
    equivalentClass_list = list(new_o_class_rdflib_graph.subject_objects(equivalent_class))
    for equivalentClass_tuple in equivalentClass_list:
        new_o_class_rdflib_graph.remove((equivalentClass_tuple[0], equivalent_class, equivalentClass_tuple[1]))
    # Fixing errors with restrictions
    onClass_list = list(new_o_class_rdflib_graph.subject_objects(onClass))
    for onClass_tuple in onClass_list:
        new_o_class_rdflib_graph.remove((onClass_tuple[0], onClass, onClass_tuple[1]))
    # Removing triples that have a triple with a predicate referencing a term
    # not present in the slim ontology
    # Get the list of subject predicates for a wildcard match
    #new_o_class_rdflib_graph.subject_predicates(rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_"))
    # Now add the class to the ontology
    o_slim_rdf_graph += new_o_class_rdflib_graph

# Now generate the string for serialization
s_slim = ""
owl_filetype = "owl_filetype"
if owl_filetype in owl_settings_dict:
    serialization_format = owl_settings_dict[owl_filetype]
else:
    serialization_format = "turtle"
osrg = o_slim_rdf_graph.serialize(format=serialization_format)
if isinstance(osrg, bytes):
    osrg = osrg.decode('utf-8')
s_slim = osrg
# Write the string to a file
owl_filename = "owl_filename"
if owl_filename in owl_settings_dict:
    slim_filename = owl_settings_dict[owl_filename]
else:
    slim_filename = "slim.ttl"
slim_file = open(slim_filename,"w")
slim_file.write(s_slim)
slim_file.close()

##############################
# IGNORE BELOW
##############################
#
## Add treeview edges
#for onto_class in renal_glomerulus:
#    # Find more complex subClassOf objects that rdflib identifies through BNode elements
#    #onto_class.rdflib_graph.subect_objects(predicate=
#    subclassof_list = list(onto_class.rdflib_graph.objects(predicate=(rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'))))
#    for subclassof in subclassof_list:
#        if type(subclassof) == rdflib.term.BNode:
#            bnode_objects = list(onto_class.rdflib_graph.objects(subclassof))
#            bnode_predicates = list(onto_class.rdflib_graph.predicates(subclassof))
#            print(bnode_predicates)
#            if part_of in bnode_objects:
#                part_of_node = rdflib.term.URIRef(list(onto_class.rdflib_graph.objects(subclassof,some_values_from))[0])
#                
#                g.add_edge(onto_class.locale, ontospy.core.utils.inferURILocalSymbol(part.toPython())[0], type='PartOf')
## Add treeview edges
#for onto_class in renal_glomerulus:
#    # Find more complex subClassOf objects that rdflib identifies through BNode elements
#    #onto_class.rdflib_graph.subect_objects(predicate=
#    subclassof_list = list(onto_class.rdflib_graph.objects(predicate=(rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'))))
#    for subclassof in subclassof_list:
#        if type(subclassof) == rdflib.term.BNode:
#            bnode_objects = list(onto_class.rdflib_graph.objects(subclassof))
#            bnode_predicates = list(onto_class.rdflib_graph.predicates(subclassof))
#            #print(bnode_predicates)
#            if part_of in bnode_objects:
#                part_of_node = rdflib.term.URIRef(list(onto_class.rdflib_graph.objects(subclassof,some_values_from))[0])
