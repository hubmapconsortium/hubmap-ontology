#!/usr/bin/env python3
import datetime
from owlready2 import *
from constants import CCF_NAMESPACE, CCF_MODEL


onto = get_ontology(CCF_NAMESPACE)

with onto:
  class ccf_part_of(ObjectProperty):
    pass
  class ccf_part_of_rank(ObjectProperty):
    range = [int]
  class ccf_annotation(ObjectProperty):
    pass
  class ccf_freetext_annotation(ObjectProperty):
    range = [str]
  class ccf_same_as(ObjectProperty):
    pass

  class ccf_preferred_label(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_orcid(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_first_name(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_last_name(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creation_date(AnnotationProperty, FunctionalProperty):
    range = [datetime.date]


  class SpatialPlacement(Thing):
    label = 'spatial placement'
  class has_placement_date(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [datetime.date]
  # Scaling
  class has_x_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  # Rotation
  class has_x_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_theta_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_rotation_order(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [str]
  class has_rotation_units(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [str]
  # Translation
  class has_x_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]

  class SpatialObjectReference(Thing):
    label = 'spatial object reference'
  class has_object_file(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # URI
  class has_object_file_format(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # mimetype
  class has_object_file_subpath(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # format specific internal path
  
  class SpatialEntity(Thing):
    label = 'spatial entity'
  class has_x_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_y_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_z_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_dimension_units(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [str]
  class has_object_reference(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialObjectReference]
  class ccf_representation_of(AnnotationProperty):
    domain = [SpatialEntity]

  class has_placement_source(ObjectProperty):
    domain = [SpatialPlacement]
    range = [SpatialEntity, SpatialObjectReference]
  class has_placement_target(ObjectProperty):
    domain = [SpatialPlacement]
    range = [SpatialEntity]

onto.save(file=CCF_MODEL, format='rdfxml')
