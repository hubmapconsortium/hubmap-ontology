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

def partof_subclassof_list(onto_class):
    part_of = rdflib.term.URIRef("http://purl.obolibrary.org/obo/BFO_0000050")
    some_values_from = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#someValuesFrom')
    subclassof_rdf = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')

    subclassof_list = list(onto_class.rdflib_graph.objects(predicate=(subclassof_rdf)))
    ps_list = [] #partof_subclassof_list
    for subclassof in subclassof_list:
        if type(subclassof) == rdflib.term.BNode:
            bnode_objects = list(onto_class.rdflib_graph.objects(subclassof))
            bnode_predicates = list(onto_class.rdflib_graph.predicates(subclassof))
            #print(bnode_predicates)
            if part_of in bnode_objects:
                part_of_node = rdflib.term.URIRef(list(onto_class.rdflib_graph.objects(subclassof,some_values_from))[0])
                
                #g.add_edge(onto_class.locale, ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], type='PartOf')
                ps_list.append((ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], onto_class.locale))
    return ps_list


# Load the ontology
o = ontospy.Ontospy()
o.load_rdf("ext.owl")
#o.build_all()
o.build_classes() # We only use the classes, so no need to build everything

# Use a sample element
kidney_id = "UBERON_0002113"
kidney_class = o.get_class(kidney_id)[0]
rg_id = "UBERON_0000074"
renal_glomerulus = o.get_class(rg_id)
node_ids = ['UBERON_0002015', 'UBERON_0004200', 'UBERON_0001284', 'UBERON_0006171', 'UBERON_0001224', 'UBERON_0001226', 'UBERON_0001227', 'UBERON_0008716', 'UBERON_0001225', 'UBERON_0000362', 'UBERON_0001228', 'UBERON_0001285', 'UBERON_0001288', 'UBERON_0004134', 'UBERON_0004135', 'UBERON_0002335']


# Create the graph
g = nx.DiGraph(IRI="ext.owl")
# Create graph from the ontology
subclassof_string = 'SubClassOf'
partof_string = 'PartOf'
classassertion_string = 'ClassAssertion'
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
# Make a DAG only involving one node, but with all its ancestors and descendants
#g_slim = g.subgraph(networkx.descendants(g, rg_id))
#g_slim = networkx.compose(list(g.subgraph(networkx.descendants(g,rg_id)), g.subgraph(networkx.ancestors(g, rg_id))))                                           

# Add partOf and equivalentClass to the graph
part_of = rdflib.term.URIRef("http://purl.obolibrary.org/obo/BFO_0000050")
some_values_from = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#someValuesFrom')
equivalent_class = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#equivalentClass')
subclassof_rdf = rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')
for onto_class in o.all_classes:
    # Find more complex subClassOf objects that rdflib identifies through BNode elements
    #onto_class.rdflib_graph.subect_objects(predicate=
    subclassof_list = list(onto_class.rdflib_graph.objects(predicate=(subclassof_rdf)))
    # Below needs to be replaced by function that is already defined
    for subclassof in subclassof_list:
        if type(subclassof) == rdflib.term.BNode:
            bnode_objects = list(onto_class.rdflib_graph.objects(subclassof))
            bnode_predicates = list(onto_class.rdflib_graph.predicates(subclassof))
            #print(bnode_predicates)
            if part_of in bnode_objects:
                part_of_node = rdflib.term.URIRef(list(onto_class.rdflib_graph.objects(subclassof,some_values_from))[0])
                
                #g.add_edge(onto_class.locale, ontospy.core.utils.inferURILocalSymbol(part_of_node.toPython())[0], type='PartOf')
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
        edge_weight = 2
    g.get_edge_data(*edge)['weight'] = edge_weight

#Start at kidney and compute shortest path, least cost route to desired node (e.g. renal glomerulus)
#root_node_simple_paths = list(nx.all_simple_paths(g,kidney_id,rg_id))
#rg_ancestors = set(nx.algorithms.shortest_paths.generic.shortest_path(g,kidney_id,rg_id,weight='weight'))

# Make a slim version of the graph
rg_tree_set = nx.descendants(g,rg_id) | nx.ancestors(g,rg_id)
#rg_tree_set = nx.descendants(g,rg_id) | rg_ancestors
rg_tree_set.add(rg_id)
for node_id in node_ids:
    rg_tree_set |= nx.descendants(g,node_id) | nx.ancestors(g,node_id)
    rg_tree_set.add(node_id)
g_slim = g.subgraph(rg_tree_set)

# Make a maximum branching
max_g_slim = nx.maximum_branching(g_slim)
#max_g_slim = nx.DiGraph(g_slim)

# Remove everything coming into the kidney
in_edges_list = list(max_g_slim.in_edges(kidney_id))
max_g_slim.remove_edges_from(in_edges_list)

#g_slim - max_g_slim
removed_edges = nx.difference(g_slim, max_g_slim)

# create labels, nominally for plotting
for node in max_g_slim:                  
    g_slim_labels[node] = id_label(o,node)

# Turn graph back into ontology
o_slim = ontospy.Ontospy()
o_slim_rdf_graph = rdflib.Graph()
onClass = rdflib.term.URIRef('http://www.w3.org/2002/07/owl#onClass')
for node in max_g_slim:
    # Find the appropriate class from the original ontology
    new_o_class = o.get_class(node)[0]
    # Substitue out the triple that was the partof that was problematic
    # First, find pairs that should be added
    ps_list = partof_subclassof_list(new_o_class)
    # Then add in the new subclassof relationship
    for ps_sub in ps_list:
        superclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+ps_sub[0])
        #new_o_class.rdflib_graph.add((ps_sub[1], subclassof_rdf, ps_sub[0]))
        new_o_class.rdflib_graph.add((new_o_class.uri, subclassof_rdf, superclass_rdf))
        #new_o_class.triples = o_slim.sparqlHelper.entityTriples(new_o_class.uri)
    # remove those edges from max_g_slim
    # Needs to be in_edges because of how subClassOf works
    #for edge in removed_edges:
    for removed_edge in removed_edges.in_edges(node):
        # Remove the RDF lib term
        superclass_rdf = rdflib.term.URIRef("http://purl.obolibrary.org/obo/"+removed_edge[0])
        new_o_class.rdflib_graph.remove((new_o_class.uri,subclassof_rdf,superclass_rdf))
    # Remove any equivalentClasses (for now)
    equivalentClass_list = list(new_o_class.rdflib_graph.subject_objects(equivalent_class))
    for equivalentClass_tuple in equivalentClass_list:
        new_o_class.rdflib_graph.remove((equivalentClass_tuple[0], equivalent_class, equivalentClass_tuple[1]))
    # Fixing errors with restrictions
    onClass_list = list(new_o_class.rdflib_graph.subject_objects(onClass))
    for onClass_tuple in onClass_list:
        new_o_class.rdflib_graph.remove((onClass_tuple[0], onClass, onClass_tuple[1]))
    # Now add the class to the ontology
    o_slim.all_classes += [new_o_class]
o_slim.all_classes = sorted(o_slim.all_classes, key=lambda x: x.qname)


# Now generate the string for serialization
s_slim = ""
for o_slim_class in o_slim.all_classes:
    s_slim +=o_slim_class.rdf_source()
for new_o_class in o_slim.all_classes:
    o_slim_rdf_graph += new_o_class.rdflib_graph
osrg = o_slim_rdf_graph.serialize(format="turtle")
if isinstance(osrg, bytes):
    osrg = osrg.decode('utf-8')
s_slim = osrg
# Write the string to a file
slim_file = open("slim.ttl","w")
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
