'''
Created on Jul 13, 2014

@author: Me
'''
from System import *
from edu.stanford.nlp.ling.HasWord import *
from edu.stanford.nlp.trees.Tree import *
from System.Collections.Generic import *
from System.Collections import *
from System.Xml import *
#import com.sun.org.apache.bcel.internal.generic.Type;
#@XmlRootElement
class Question(object):
    def __init__(self):
        # *
        # * question type such as boolean, number, classic (all the others);
        # 
        # this is focus
        self._pocs = list()#ArrayList[POC]()
        self._semanticConcepts = list()#ArrayList[IList]()

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def getTokens(self):
        return self._tokens

    def setTokens(self, tokens):
        self._tokens = tokens

    def getAnswerType(self):
        return self._answerType

    def setAnswerType(self, answerType):
        self._answerType = answerType

    def getFocus(self):
        return self._focus

    def setFocus(self, focus):
        self._focus = focus

    def getSyntaxTree(self):
        return self._syntaxTree

    def setSyntaxTree(self, syntaxTree):
        self._syntaxTree = syntaxTree

    def getSemanticConcepts(self):
        return self._semanticConcepts

    def setSemanticConcepts(self, semanticConcepts):
        self._semanticConcepts = semanticConcepts

    def getPocs(self):
        return self._pocs

    def setPocs(self, pocs):
        self._pocs = pocs

    def __str__(self):
        b = ""
        b += "sem concepts:"
        if self._semanticConcepts != None:
            b+=self._semanticConcepts.__str__()
        b+="pocs:"
        if self._pocs != None:
            b+=self._pocs.__str__()
        b+="Tree:"
        if self._syntaxTree != None:
            b+=self._syntaxTree.__str__()
        return b