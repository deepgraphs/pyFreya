'''
Created on Jul 12, 2014

@author: Me
'''

from Annotation import *
# *
# * representation of Potential Ontology Concept
# *
# * @author danica
# *
# 
class POC(object):
    def __init__(self):
        self._annotation = Annotation()

    def getAnnotation(self):
        return self._annotation

    def setAnnotation(self, annotation):
        self._annotation = annotation

    def getHead(self):
        return self._head

    def setHead(self, head):
        self._head = head

    def getModifiers(self):
        return self._modifiers

    def setModifiers(self, modifiers):
        self._modifiers = modifiers

    def getMainSubject(self):
        return self._mainSubject

    def setMainSubject(self, mainSubject):
        self._mainSubject = mainSubject

    def __str__(self):#toString
        buffer = ""
        buffer+="POC:" + self.getAnnotation().__str__()
        return buffer