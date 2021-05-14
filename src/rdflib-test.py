from rdflib import Graph, Namespace
from rdflib.extras.infixowl import OWL_NS, Class, Restriction, Property
from rdflib.namespace import NamespaceManager

ccf = Namespace('http://purl.org/ccf/')
namespace_manager = NamespaceManager(Graph())
namespace_manager.bind('ccf', ccf, override=False)
namespace_manager.bind('owl', OWL_NS, override=False)

g = Graph()
g.namespace_manager = namespace_manager

part_of = Property(ccf.part_of, graph=g)

organ = Class(ccf.Organ, graph=g, subClassOf=[Restriction(part_of, graph=g, someValuesFrom=ccf.Body)])

organ_part = Class(ccf.OrganPart, graph=g)
organ_part.subClassOf = [Restriction(part_of, graph=g, someValuesFrom=organ)]

kidney_capsule = Class(ccf.KidneyCapsule, graph=g)
kidney_capsule.subClassOf = [ccf.OrganPart, Restriction(part_of, graph=g, someValuesFrom=ccf.Kidney)]

kidney = Class(ccf.Kidney, graph=g, subClassOf=[organ])

left_kidney = Class(ccf.LeftKidney, graph=g, subClassOf=[kidney])
right_kidney = Class(ccf.RightKidney, graph=g, subClassOf=[kidney])

kidney_calyx = Class(ccf.KidneyCalyx, graph=g, subClassOf=[organ_part])
kidney_calyx.subClassOf = [Restriction(part_of, graph=g, someValuesFrom=kidney)]

major_calyx = Class(ccf.MajorCalyx, graph=g, subClassOf=[kidney_calyx])
minor_calyx = Class(ccf.MinorCalyx, graph=g, subClassOf=[kidney_calyx])

g.serialize(format='turtle', destination="rdflib_test.ttl")