__author__ = 'root'
# A placeholder of definitions until a python alternative to openrdf is selected
class OWL(object):
    DATATYPEPROPERTY="http://www.w3.org/2002/07/owl#DatatypeProperty"
    OBJECTPROPERTY="http://www.w3.org/2002/07/owl#ObjectProperty"
    CLASS="http://www.w3.org/2002/07/owl#Class"
class RDFS(object):
    SUBCLASSOF="http://www.w3.org/2000/01/rdf-schema#subClassOf"
    DOMAIN="http://www.w3.org/2000/01/rdf-schema#domain"
    CLASS="http://www.w3.org/2000/01/rdf-schema#Class"
    RANGE="http://www.w3.org/2000/01/rdf-schema#range"
    PREFIX="rdfs"
class RDF(object):
    PROPERTY="http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
if __name__=='__main__':
    print OWL.CLASS