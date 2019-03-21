# hubmap-ontology
Repository for creating ontologies for HuBMAP

To create these ontologies, we need code as well as original data. Code and data should have an open-source licenses, e.g. MIT for code and CC-BY for data.

Currently, code is licensed under the MIT License and the data is CC-BY 4.0. Eventually, there should be a curated ontology/release version of the ontology that is CC-BY-ND (No derivatives) that will ensure that there are fixed reference forms of the ontology, which should exist side-by-side with an almost identical one so as to permit the ontology to be remixed and reused as need be.

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
