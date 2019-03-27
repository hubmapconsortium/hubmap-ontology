# hubmap-ontology
Repository for creating ontologies for HuBMAP

To create these ontologies, we need code as well as original data. Code and data should have an open-source licenses, e.g. MIT for code and CC-BY for data.

Currently, code is licensed under the MIT License and the data is CC-BY 4.0. Eventually, there should be a curated ontology/release version of the ontology that is CC-BY-ND (No derivatives) that will ensure that there are fixed reference forms of the ontology, which should exist side-by-side with an almost identical one so as to permit the ontology to be remixed and reused as need be.

These license policies will be revised in coordination with the appropriate HuBMAP working groups as needed. 

## Release 0.1.0 overview 
SAM PLEASE READ AND REVISE 

The CCF ontology bundles the initial CCF ontology, requested ontology terms, and software necessary to generate the ontology. 

Release 0.1.0 introduces the basic scaffolding (inherited from existing ontologies, particularly Uberon) browsing from the whole-body scale to the single-organ scale, including "insertion points" for organ-specific ontologies. 

It also introduces alpha-level ontologies for kidney and heart, based on terms requested by TMCs and in discussions, to prototype technologies to construct slim ontologies from terms selected from multiple existent ontologies. As part of this effort, 0.1.0 developed the software framework to add new terms ot hte ontology via spreadsheet. 

Lastly, 0.1.0 includes a prototype data ontology and data framework. The entire ontology is released as an OWL (W3C Web Ontology Language) file. 

## CCF Development roadmap
We maintain a development and release roadmap for the CCF Ontology and supporting software, available at [https://docs.google.com/document/d/1Sso27-7YI4993LC5a_HTBBMOK6QN83pcgXEg0ggrsWc/edit] (last edited: March 26, 2019).  

## Documentation

[Documentation can be found here](https://docs.google.com/document/d/1X21O5DgGkq9ngPOsBZa-qy1-6Y2MiohJD7Bt-JFyysY/edit#)

## Dependencies

Currently, the code requires the following Python packges:
* Ontospy
* Networkx
* RDFLib
* pandas
* pydot
* PyYAML

## Running the code

To run the code:
```
python3 owl_to_nx.py
```
We recommend running the code though in ipython or Jupyter and running these commands first after the import statements:
```
o = ontospy.Ontospy()
o.load_rdf("ext.owl")
o.build_classes()
```
where ext.owl is the ontology file to be loaded. At the moment, the loading and building of the classes takes an extremely long time (~10-30 minutes). Then the rest of the code can be run quickly to generate the ontology.
