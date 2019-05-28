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

import sys
sys.path.append("../src")
from owl_to_nx import *

owl_settings_filename = "owl_settings_ktao.yml"
create_slim_ontology(owl_settings_filename)
