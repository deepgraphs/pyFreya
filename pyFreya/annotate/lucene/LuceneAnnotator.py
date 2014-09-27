'''
Created on Jul 18, 2014

@author: Me
'''
from sys import *
import lucene
import freya.util.FreyaConstants as FreyaConstants
import freya.util.pyJavaSmooth as pyJava
# from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, EnglishAnalyzer, StandardAnalyzer, IndexSearcher, Version,\
#     QueryParser, MultiFieldQueryParser

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.analysis.core import KeywordAnalyzer



import logging
from freya.model.Annotation import Annotation# For the tests
from freya.model.Ontology import OWL
from freya.model.Ontology import RDF
from freya.model.Ontology import RDFS
# from freya.search.BooleanClause import BooleanClause

#@Component
class LuceneAnnotator(object):
    #@Value("${org.freya.lucene.index.dir.search}") Resource luceneIndexDir;
    def __init__(self):
        logging.basicConfig(filename='../../freya/index/annotator.log', filemode='w', level=logging.DEBUG)

    def close(self):
        if self._reader != None:
            try:
                print "closing index Reader"
            except Exception as e:#IOException(e):
                print e.message
                logging.error("Error")
            finally:
                pass
    #private static final Log logger = LogFactory.getLog(LuceneAnnotator.class);
    def getIndex(self):
        return self._index

    def setIndex(self, index):
        self._index = index
    def testSearcher(self):
        query=QueryParser(Version.LUCENE_CURRENT, "class", StandardAnalyzer(Version.LUCENE_CURRENT)).parse(QueryParser.escape('http\://www.mooney.net/geo#River'))
        print query
        hits = self._searcher.search(query, 50)
        for hit in hits.scoreDocs:
            print hit.score, hit.doc, hit.toString()
            doc = self._searcher.doc(hit.doc)
            print doc.get("class").encode("utf-8")
    #public SynonymMap synonymMap;
    def init(self):
        try:
            print 'lucene', lucene.VERSION
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])
            if not hasattr(self,'_index'):
                indexDir = "../../freya/index/actual"
                self._index = File(indexDir)
            if not hasattr(self,'_reader'):
                self._reader = "Not needed"
            if not hasattr(self,'_searcher'):
                try:
                    # lazily instantiate searcher
                    print "Setting searcher to " + str(self._index)
                    self._searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(self._index)))
                except Exception as e:#Exception(e):
                    print e.message
                    print "Searcher Initialisation Error"
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Lucene Error")

    def getSpecificityScores(self):
        # map = Hashtable[str, Nullable]()
        logging.info("Need to implement....")
        return map

    # *
    # * find lucene annotations for this poc specialTreatment is for common nouns so that they are searched with stem not
    # * exact match
    # *
    # * @param annotation
    # * @return
    #
    def searchIndex(self, annotation, specialTreatment):
        if specialTreatment:
            return self.searchStemFirst(annotation)
        annotations = list() #ArrayList[Annotation]()
        try:
            maxSynonyms = 0
            stemAnalyser = EnglishAnalyzer(Version.LUCENE_CURRENT)
            # Analyzer stemmedAnalyser = AnalyzerUtil.getSynonymAnalyzer(AnalyzerUtil
            # .getPorterStemmerAnalyzer(new StandardAnalyzer(Version.LUCENE_CURRENT)),
            # synonymMap, maxSynonyms);
            analyser = StandardAnalyzer(Version.LUCENE_CURRENT)
            parser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_EXACT_CONTENT, analyser)
            pocString = QueryParser.escape(annotation.getText())
            preparePocString = "\"" + pocString + "\""
            preparePocStringLowercase = "\"" + pocString.lower() + "\""
            query = parser.parse(preparePocString)
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            if freq <= 0:
                # search lowercased exact
                lowerCasedParser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_EXACT_LOWERCASED_CONTENT, analyser)
                query = lowerCasedParser.parse(preparePocStringLowercase)
                # logging.info("Searching for: " + query.toString());
                result = self._searcher.search(query, 1)
                freq = result.totalHits
                if freq > 0:
                    result = self._searcher.search(query, freq)
                hits = pyJava.JArray2List(result.scoreDocs)
                logging.debug("For " + str(query) + " : " + str(result.totalHits))
            if len(hits) == 0 and preparePocStringLowercase.index(" ") < 0:
                # search stemmed
                stemParser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_STEMMED_CONTENT, stemAnalyser)
                query = stemParser.parse(preparePocStringLowercase)
                # logging.info("Searching for: " + query.toString());
                result = self._searcher.search(query, 1)
                freq = result.totalHits
                if freq > 0:
                    result = self._searcher.search(query, freq)
                hits = pyJava.JArray2List(result.scoreDocs)
                logging.info("For " + str(query) + " : " + str(result.totalHits))
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                self._searcher.explain(query, hit.doc)
                ann = Annotation()
                features = dict()
                features[FreyaConstants.CLASS_FEATURE_LKB]=doc.get(FreyaConstants.CLASS_FEATURE_LKB)
                features[FreyaConstants.INST_FEATURE_LKB]=doc.get(FreyaConstants.INST_FEATURE_LKB)
                features[FreyaConstants.PROPERTY_FEATURE_LKB]=doc.get(FreyaConstants.PROPERTY_FEATURE_LKB)
                features["string"]=doc.get(FreyaConstants.FIELD_EXACT_CONTENT)
                features[FreyaConstants.SCORE]=hit.score
                ann.setFeatures(features)
                ann.setEndOffset(annotation.getEndOffset())
                ann.setStartOffset(annotation.getStartOffset())
                ann.setSyntaxTree(annotation.getSyntaxTree())
                ann.setText(annotation.getText())
                annotations.append(ann)
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return annotations

    # *
    # * this method now search both stem and lowercase
    # *
    # * @param annotation
    # * @return
    #
    def searchStemFirst(self, annotation):
        annotations = list()
        pocString = QueryParser.escape(annotation.getText())
        preparePocStringOriginal = "\"" + pocString + "\""
        preparePocStringLowercase = "\"" + pocString.lower() + "\""
        try:
            maxSynonyms = 0
            # Analyzer stemmedAnalyser =
            # AnalyzerUtil.getSynonymAnalyzer(AnalyzerUtil
            # .getPorterStemmerAnalyzer(new StandardAnalyzer(Version.LUCENE_CURRENT)),
            # synonymMap, maxSynonyms);
            stemmedAnalyser = EnglishAnalyzer(Version.LUCENE_CURRENT)
            analyser = StandardAnalyzer(Version.LUCENE_CURRENT)
            stemParser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_STEMMED_CONTENT, stemmedAnalyser)
            query = stemParser.parse(preparePocStringLowercase)
            result = self._searcher.search(query, 1)
            logging.info("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            stemHits = result.scoreDocs
            allHits = stemHits
            # if(stemHits.length == 0) {
            # search lowercased exact
            parser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_EXACT_LOWERCASED_CONTENT, analyser)
            query = parser.parse(preparePocStringLowercase)
            result = self._searcher.search(query, 1)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            lowHits = result.scoreDocs
            allHits = pyJava.JArray2List(allHits) + pyJava.JArray2List(lowHits) # ArrayUtils.addAll(allHits, lowHits)
            logging.info("For " + str(query) + " : " + str(result.totalHits))
            # }
            # if(allHits.length == 0) {
            # search exact
            exactParser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.FIELD_EXACT_CONTENT, analyser)
            query = exactParser.parse(preparePocStringLowercase)
            result = self._searcher.search(query, 1)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            allHits = pyJava.JArray2List(allHits) + pyJava.JArray2List(result.scoreDocs) #ArrayUtils.addAll(allHits, result.scoreDocs)
            logging.info("For " + str(query) + " : " + str(result.totalHits))
            # }
            # for (ScoreDoc hit : allHits) {
            indexus = 0
            while indexus < len(allHits):
                hit = allHits[indexus]
                doc = self._searcher.doc(hit.doc)
                self._searcher.explain(query, hit.doc)
                ann = Annotation()
                features = dict()
                features[FreyaConstants.CLASS_FEATURE_LKB] = doc.get(FreyaConstants.CLASS_FEATURE_LKB)
                features[FreyaConstants.INST_FEATURE_LKB] = doc.get(FreyaConstants.INST_FEATURE_LKB)
                features[FreyaConstants.PROPERTY_FEATURE_LKB] = doc.get(FreyaConstants.PROPERTY_FEATURE_LKB)
                features["string"] = doc.get(FreyaConstants.FIELD_EXACT_CONTENT)
                features["score"] = hit.score
                ann.setFeatures(features)
                ann.setEndOffset(annotation.getEndOffset())
                ann.setStartOffset(annotation.getStartOffset())
                ann.setSyntaxTree(annotation.getSyntaxTree())
                ann.setText(annotation.getText())
                annotations.append(ann)
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return annotations

    # *
    # * @return
    #
    def findPropertyURIs(self):
        uris = list()
        uris = uris + self.findPropertyURIs(OWL.DATATYPEPROPERTY, None)
        uris = uris + self.findPropertyURIs(OWL.OBJECTPROPERTY, None)
        uris = uris + self.findRDFPropertyURIs(None)
        return uris

    # *
    # * @param max
    # * @return
    #
    def findPropertyURIs(self, max):
        uris = list()
        uris = uris + self.findPropertyURIs(OWL.DATATYPEPROPERTY, max)
        uris = uris + self.findPropertyURIs(OWL.OBJECTPROPERTY, max)
        uris = uris + self.findRDFPropertyURIs(max)
        return uris

    # *
    # * @return
    #
    def findDatatypePropertyURIs(self):
        uris = list()
        uris = uris + self.findPropertyURIs(OWL.DATATYPEPROPERTY, None)
        return uris

    # *
    # * @return
    #
    def findObjectPropertyURIs(self):
        uris = list()
        uris = uris + self.findPropertyURIs(OWL.OBJECTPROPERTY, None)
        return uris

    # *
    # * @param max
    # * @return
    #
    def findRDFPropertyURIs(self, max):
        uris = list()
        owl = "http://www.w3.org/2002/07/owl"
        rdfProps = self.findPropertyURIs(RDF.PROPERTY, max)
        # for (String prop : rdfProps) {
        indexus = 0
        while indexus < len(rdfProps):
            prop = rdfProps[indexus]
            if prop != None and not prop.startswith(owl):
                uris.append(prop)
            indexus += 1
        return uris

    # *
    # * @return
    #
    def findClassURIs(self):
        uris = list()
        uris = uris + self.findPropertyURIs(OWL.CLASS, None)
        uris = uris + self.findPropertyURIs(RDFS.CLASS, None)
        return uris

    # *
    # * find lucene annotations for this poc
    # *
    # * @param annotation
    # * @return
    #
    def findPropertyURIs(self, propertyType, max):
        uris = list() # list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            parser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.CLASS_FEATURE_LKB, analyzer)
            query = parser.parse("\"" + QueryParser.escape(propertyType) + "\"")
            result = self._searcher.search(query, 1)
            freq = result.totalHits
            if max != None:
                freq = max.intValue()
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            logging.debug("For " + str(query) + " : " + str(result.totalHits) + " max:" + str(max))
            print "For " + str(query) + " : " + str(result.totalHits) + " max:" + str(max)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                self._searcher.explain(query, hit.doc)
                uris.append(doc.get(FreyaConstants.INST_FEATURE_LKB))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return uris

    # *
    # * @param propertyUri
    # * @return
    #
    def findPropertyRange(self, propertyUri):
        rangeUri = "http://www.w3.org/2000/01/rdf-schema#range"
        return self.searchForClass(propertyUri, rangeUri)

    # *
    # * @param propertyUri
    # * @return
    #
    def findPropertyDomain(self, propertyUri):
        rangeUri = "http://www.w3.org/2000/01/rdf-schema#domain"
        return self.searchForClass(propertyUri, rangeUri)

    # *
    # * given classUri search for field class so that pred=subClassOf
    # *
    # * @param classUri
    # * @return
    #
    def findSubClasses(self, classUri): #RESOLVE multifieldqueryparser DOCUMENTATION PROBLEM!!!!
        propertyURI = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
        subClasses = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            fields = [FreyaConstants.CLASS_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
            flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
            subClassUri = "\"" + QueryParser.escape(propertyURI) + "\""
            queries = ["\"" + QueryParser.escape(classUri) + "\"", subClassUri]
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT,queries, fields,flags,analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                subClasses.append(doc.get(FreyaConstants.INST_FEATURE_LKB))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return subClasses

    # *
    # * check whether this is datatype property or not
    # *
    # * @param propertyUri
    # * @return
    #
    def isItDatatypeProperty(self, propertyUri):
        result = self.checkIfItIsDatatypeProperty(propertyUri)
        exists = False
        if result != None and len(result) > 0:
            exists = True
        # logging.info("isItDatatypeProperty for " + propertyUri + " is " + exists);
        return exists

    # *
    # * @param classUri
    # * @return
    #

    def getDefinedPropertiesWhereClassIsADomain(self, classUri):
        properties = self.searchForInstance(classUri, RDFS.DOMAIN)
        return properties

    # Apparently there is no overloading in Python! MUST CHANGE FLOW
    def getDefinedPropertiesWhereClassIsADomain(self, classUri, forceSuperClasses):
        properties = list()
        if forceSuperClasses:
            superClasses = self.findSuperClasses(classUri)
            superClasses.append(classUri)
            # for (String uri : superClasses) {
            indexus = 0
            while indexus < len(superClasses):
                uri = superClasses[indexus]
                for each in self.getDefinedPropertiesWhereClassIsADomain(uri,False):
                    properties.append(each)
                indexus += 1
        else:
            properties = self.searchForInstance(classUri, RDFS.DOMAIN)
        return properties

    def getDefinedPropertiesWhereClassIsARange(self, classUri, forceSuperClasses):
        properties = list()
        if forceSuperClasses:
            superClasses = self.findSuperClasses(classUri)
            superClasses.append(classUri)
            # for (String uri : superClasses) {
            indexus = 0
            while indexus < len(superClasses):
                uri = superClasses[indexus]
                for each in self.getDefinedPropertiesWhereClassIsARange(uri,False):
                    properties.append(each)
                indexus += 1
        else:
            properties = self.searchForInstance(classUri, RDFS.RANGE)
        return properties


    # *
    # * @param classUri
    # * @return
    #
    def getNeighbouringClassesWhereGivenClassIsADomain(self, classUri, forceSuperClasses):
        classes = list()
        if forceSuperClasses:
            # here recursively go and first find all super classes
            feedClasses = self.findSuperClasses(classUri)
            feedClasses.append(classUri)
            # then for each superclass do the same as above
            # for (String uri : feedClasses) {
            indexus = 0
            while indexus < len(feedClasses):
                uri = feedClasses[indexus]
                for each in self.getNeighbouringClassesWhereGivenClassIsADomain(uri, False):
                    classes.append(each)
                indexus += 1
        else:
            properties = self.searchForInstance(classUri, RDFS.DOMAIN)
            # for (String property : properties) {
            indexus = 0
            while indexus < len(properties):
                property = properties[indexus]
                for each in self.searchForClass(property, RDFS.RANGE):
                    classes.append(each)
                indexus += 1
        return classes




    def getNeighbouringClassesWhereGivenClassIsARange(self, classUri, forceSuperClasses):
        classes = list()
        if forceSuperClasses:
            # here recursively go and first find all super classes
            feedClasses = self.findSuperClasses(classUri)
            feedClasses.append(classUri)
            logging.info("found " + str(len(feedClasses)) + " super classes for " + classUri)
            # then for each superclass do the same as above
            # for (String uri : feedClasses) {
            indexus = 0
            while indexus < len(feedClasses):
                uri = feedClasses[indexus]
                for each in self.getNeighbouringClassesWhereGivenClassIsARange(uri,False):
                    classes.append(each)
                logging.info("found " + str(len(classes)) + " elements for " + uri)
                indexus += 1
        else:
            properties = self.searchForInstance(classUri, RDFS.RANGE)
            # for (String property : properties) {
            indexus = 0
            while indexus < len(properties):
                property = properties[indexus]
                for each in self.searchForClass(property, RDFS.DOMAIN):
                    classes.append(each)
                indexus += 1
        return classes


    # *
    # * @param classUri
    # * @return
    #
    def findSuperClasses(self, classUri):
        searchFinished = False
        directSuperClasses = list()
        superClassesToSave = list()
        while not searchFinished:
            directSuperClasses = self.searchForClass(classUri, RDFS.SUBCLASSOF)
            # print str(directSuperClasses) + " list"
            if len(directSuperClasses) == 0 or (len(directSuperClasses) != 0 and pyJava.contains(directSuperClasses,superClassesToSave)):
                searchFinished = True
            else:
                # logging.info("searchFinished for SuperClasses");
                # System.out.println("size:"+directSuperClasses.size());
                for each in directSuperClasses:
                    superClassesToSave.append(each)
                # for (String cUri : directSuperClasses) {
                indexus = 0
                while indexus < len(directSuperClasses):
                    cUri = directSuperClasses[indexus]
                    for each in self.findSuperClasses(cUri):
                        superClassesToSave.append(each)
                    indexus += 1
                searchFinished = True
        logging.info("For " + str(classUri) + " found " + str(len(superClassesToSave)) + " super-classes.")
        return superClassesToSave





    def searchForInstance(self, classUri, pred):
        uris = list()
        fields = [FreyaConstants.CLASS_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
        flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
        queries = ["\"" + QueryParser.escape(classUri) + "\"", "\"" + QueryParser.escape(pred) + "\""]
        try:
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, queries, fields, flags, StandardAnalyzer(Version.LUCENE_CURRENT))
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                uris.append(doc.get(FreyaConstants.INST_FEATURE_LKB))
                indexus += 1
        except Exception as e:#ParseException(e):
            print e.message
            logging.error("Error")
        return uris

    # *
    # *
    # * @param inst
    # * @param className
    # * @return
    #
    def checkIfItIsDatatypeProperty(self, inst):
        classUris = list()
        fields = [FreyaConstants.INST_FEATURE_LKB, FreyaConstants.CLASS_FEATURE_LKB]
        flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
        queries = ["\"" + inst + "\"", "\"" + OWL.DATATYPEPROPERTY + "\""]
        try:
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, queries, fields, flags, StandardAnalyzer(Version.LUCENE_CURRENT))
            result = self._searcher.search(query, 1)
            logging.info("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                classUris.append(doc.get(FreyaConstants.INST_FEATURE_LKB))
                indexus += 1
        except Exception as e:#ParseException(e):
            print e.message
            logging.error("Error")
        return classUris

    # *
    # * @param inst
    # * @param pred
    # * @return
    #
    def searchForClass(self, inst, pred):
        classUris = list()
        fields = [FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
        flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
        queries = ["\"" + QueryParser.escape(inst) + "\"", "\"" + QueryParser.escape(pred) + "\""]
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.info("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                classUris.append(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
                indexus += 1
        except Exception as e:#ParseException(e):
            print e.message
            logging.error("Error")
        return classUris

    # *
    # * @return
    #
    def findTopClasses(self):
        propertyURI = RDFS.SUBCLASSOF
        allClasses = list()
        topClasses = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            parser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.PROPERTY_FEATURE_LKB, analyzer)
            query = parser.parse("\"" + QueryParser.escape(propertyURI) + "\"")
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                allClasses.append(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
                indexus += 1
            # for (String classUri : allClasses) {
            indexus = 0
            while indexus < len(allClasses):
                classUri = allClasses[indexus]
                logging.info("Checking whether " + classUri + " is a top class.")
                # search inst and pred retrieve class
                # if class exists that means it is not top class otherwise add to
                # topClasses
                classes = self.searchForClass(classUri, propertyURI)
                logging.info("top classes:" + str(len(classes)))
                if classes != None or len(classes) > 0:
                    logging.info("This is not a top class...")
                else:
                    topClasses.append(classUri)
                    logging.info("Adding " + classUri + " to top classes.")
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return topClasses

    # *
    # * randomly gets the direct type
    # *
    # * @param instanceUri
    # * @return
    #
    def findOneDirectType(self, instanceUri):
        return self.findDirectTypes(instanceUri, 1)[0]

    def findDirectTypes(self, instanceUri):
        return self.findDirectTypes(instanceUri, None)

    # *
    # * find direct types
    # *
    # * @param annotation
    # * @return
    #
    def findDirectTypes(self, instanceUri, max):
        dTypes = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            parser = QueryParser(Version.LUCENE_CURRENT, "inst", analyzer)
            query = parser.parse("\"" + QueryParser.escape(instanceUri) + "\"")
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = 0
            if max != None:
                freq = max
            else:
                freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                self._searcher.explain(query, hit.doc)
                dTypes.append(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        logging.debug("there are " + str(len(dTypes)) + " unique direct types")
        return dTypes

    # *
    # * find lucene annotations for this poc
    # *
    # * @param annotation
    # * @return
    #
    def findLabels(self, instanceUri):
        labels = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            fields = [FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
            flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
            labelOrTitleUris = "\"http://www.w3.org/2000/01/rdf-schema#label\"" # +
            # " OR http://purl.org/dc/elements/1.1/title";
            queries = ["\"" + QueryParser.escape(instanceUri) + "\"", QueryParser.escape(labelOrTitleUris)]
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                labels.append(doc.get(FreyaConstants.FIELD_EXACT_CONTENT))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return labels

    def findLiteral(self, instanceUri, propertyURI):
        labels = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
            fields = [FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
            flags = [BooleanClause.Occur.MUST, BooleanClause.Occur.MUST]
            labelOrTitleUris = "\"" + propertyURI + "\""
            queries = ["\"" + QueryParser.escape(instanceUri) + "\"", QueryParser.escape(labelOrTitleUris)]
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = pyJava.JArray2List(result.scoreDocs)
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < len(hits):
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                labels.append(doc.get(FreyaConstants.FIELD_EXACT_CONTENT))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return labels


if __name__=="__main__":
    print "Starting"
    an = LuceneAnnotator()
    an.init()
    # an.testSearcher()
    arr= Annotation()
    arr.setStartOffset(4)
    arr.setEndOffset(10)
    arr.setFeatures({'1':'feat1','2':'feat2'})
    arr.setText("river")
    arr.setSyntaxTree("tree")
    print arr
    # for iterator in an.searchIndex(arr, False):
    #     print iterator
    # print an.findClassURIs()
    # print an.findDatatypePropertyURIs()
    # print an.findSubClasses('http://www.mooney.net/geo#City')
    # print an.findSuperClasses('http://www.mooney.net/geo#Capital')
    # print an.searchForClass('http://www.mooney.net/geo#Capital', RDFS.SUBCLASSOF)
    # print an.isItDatatypeProperty('http://www.mooney.net/geo#cityPopulation')
    # print an.getDefinedPropertiesWhereClassIsADomain('http://www.mooney.net/geo#Mountain',False)
    # print an.getDefinedPropertiesWhereClassIsARange('http://www.mooney.net/geo#Mountain',True)
    # print an.getNeighbouringClassesWhereGivenClassIsADomain('http://www.mooney.net/geo#River',False)
    # print an.getNeighbouringClassesWhereGivenClassIsARange('http://www.mooney.net/geo#Mountain',True)
    # print an.findLabels('http://www.mooney.net/geo#Mountain')
    # print an.findLiteral('http://www.mooney.net/geo#City','class')