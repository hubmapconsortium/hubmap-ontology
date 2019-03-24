# hubmap-ontology
Repository for creating ontologies for HuBMAP

To create these ontologies, we need code as well as original data. Code and data should have an open-source licenses, e.g. MIT for code and CC-BY for data.

Currently, code is licensed under the MIT License and the data is CC-BY 4.0. Eventually, there should be a curated ontology/release version of the ontology that is CC-BY-ND (No derivatives) that will ensure that there are fixed reference forms of the ontology, which should exist side-by-side with an almost identical one so as to permit the ontology to be remixed and reused as need be.

## Release 0.1.0 overview 
The CCF ontology bundles the initial CCF ontology, requested ontology terms, and software necessary to generate the ontology. 

In Release 0.1.0, ... 

Sam, please revise this!

## CCF Development roadmap
We maintain a development and release roadmap for the CCF Ontology and supporting software, available at [https://docs.google.com/document/d/1Sso27-7YI4993LC5a_HTBBMOK6QN83pcgXEg0ggrsWc/edit] (last edited: March 24, 2019).  

## Documentation

[Documentation can be found here](https://docs.google.com/document/d/1X21O5DgGkq9ngPOsBZa-qy1-6Y2MiohJD7Bt-JFyysY/edit#)

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
