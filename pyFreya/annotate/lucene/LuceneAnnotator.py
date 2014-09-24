'''
Created on Jul 18, 2014

@author: Me
'''
from sys import *
import lucene
import freya.util.FreyaConstants as FreyaConstants
import freya.util.pyJavaSmooth as pyJava
from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, EnglishAnalyzer, StandardAnalyzer, IndexSearcher, Version,\
    QueryParser, MultiFieldQueryParser
import logging
from freya.model.Annotation import Annotation# For the tests
from freya.model.Ontology import OWL
from freya.model.Ontology import RDF
from freya.model.Ontology import RDFS

#@Component
class LuceneAnnotator(object):
    #@Value("${org.freya.lucene.index.dir.search}") Resource luceneIndexDir;
    def __init__(self):
        pass

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
        query=QueryParser(Version.LUCENE_30, "class", StandardAnalyzer(Version.LUCENE_30)).parse('http\://www.mooney.net/geo#River')
        print query
        hits = self._searcher.search(query, 1000)
        for hit in hits.scoreDocs:
            print hit.score, hit.doc, hit.toString()
            doc = self._searcher.doc(hit.doc)
            print doc.get("class").encode("utf-8")
    #public SynonymMap synonymMap;
    def init(self):
        try:
            lucene.initVM()
            if not hasattr(self,'_index'):
                indexDir = "/index/test"
                self._index = File(indexDir)
            # if (!index.exists()) IndexTriplesExec.main(new String[0]);
            if not hasattr(self,'_reader') and self._index.exists():
                self._reader = "stupifaction field"
            # true);
            if not hasattr(self,'_searcher') and self._index.exists():
                try:
                    # lazily instantiate searcher
                    self._searcher = IndexSearcher(SimpleFSDirectory(self._index))
                except :#Exception(e):
                    print "Searcher Initialisation Error"
                finally:
                    print "Searcher Initialised"
        except :#CorruptIndexException(e):
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
            stemAnalyser = EnglishAnalyzer(Version.LUCENE_30)
            # Analyzer stemmedAnalyser = AnalyzerUtil.getSynonymAnalyzer(AnalyzerUtil
            # .getPorterStemmerAnalyzer(new StandardAnalyzer(Version.LUCENE_30)),
            # synonymMap, maxSynonyms);
            analyser = StandardAnalyzer(Version.LUCENE_30)
            parser = QueryParser(Version.LUCENE_30, FreyaConstants.FIELD_EXACT_CONTENT, analyser)
            pocString = annotation.getText()
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
                lowerCasedParser = QueryParser(Version.LUCENE_30, FreyaConstants.FIELD_EXACT_LOWERCASED_CONTENT, analyser)
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
                stemParser = QueryParser(Version.LUCENE_30, FreyaConstants.FIELD_STEMMED_CONTENT, stemAnalyser)
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
        pocString = annotation.getText()
        preparePocStringOriginal = "\"" + pocString + "\""
        preparePocStringLowercase = "\"" + pocString.lower() + "\""
        try:
            maxSynonyms = 0
            # Analyzer stemmedAnalyser =
            # AnalyzerUtil.getSynonymAnalyzer(AnalyzerUtil
            # .getPorterStemmerAnalyzer(new StandardAnalyzer(Version.LUCENE_30)),
            # synonymMap, maxSynonyms);
            stemmedAnalyser = EnglishAnalyzer(Version.LUCENE_30)
            analyser = StandardAnalyzer(Version.LUCENE_30)
            stemParser = QueryParser(Version.LUCENE_30, FreyaConstants.FIELD_STEMMED_CONTENT, stemmedAnalyser)
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
        while indexus < rdfProps.length:
            prop = rdfProps[indexus]
            if prop != None and not prop.startsWith(owl):
                uris.add(prop)
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
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            parser = QueryParser(Version.LUCENE_30, FreyaConstants.CLASS_FEATURE_LKB, analyzer)
            query = parser.parse("\"" + propertyType + "\"")
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
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            fields = [FreyaConstants.CLASS_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB]
            flags = [False,False] # FIX THIS!
            subClassUri = "\"" + propertyURI + "\""
            queries = ["\"" + classUri + "\"", subClassUri]
            # qp = MultiFieldQueryParser(Version.LUCENE_30,fields, analyzer)
            # qp.setDefaultOperator(QueryParser.Operator.AND)
            # query = qp.parse(queries)
            query =  MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + str(query) + " : " + str(result.totalHits))
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                subClasses.add(doc.get(FreyaConstants.INST_FEATURE_LKB))
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
        if result != None and result.size() > 0:
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

    def getDefinedPropertiesWhereClassIsADomain(self, classUri, forceSuperClasses):
        properties = list()
        if forceSuperClasses:
            superClasses = self.findSuperClasses(classUri, HashSet())
            superClasses.add(classUri)
            # for (String uri : superClasses) {
            indexus = 0
            while indexus < superClasses.length:
                uri = superClasses[indexus]
                properties.addAll(self.getDefinedPropertiesWhereClassIsADomain(uri))
                indexus += 1
        return properties

    def getDefinedPropertiesWhereClassIsARange(self, classUri, forceSuperClasses):
        properties = list()
        if forceSuperClasses:
            superClasses = self.findSuperClasses(classUri, HashSet())
            superClasses.add(classUri)
            # for (String uri : superClasses) {
            indexus = 0
            while indexus < superClasses.length:
                uri = superClasses[indexus]
                properties.addAll(self.getDefinedPropertiesWhereClassIsARange(uri))
                indexus += 1
        return properties

    # *
    # * @param classUri
    # * @return
    #
    def getDefinedPropertiesWhereClassIsARange(self, classUri):
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
            feedClasses = self.findSuperClasses(classUri, HashSet())
            feedClasses.add(classUri)
            # then for each superclass do the same as above
            # for (String uri : feedClasses) {
            indexus = 0
            while indexus < feedClasses.length:
                uri = feedClasses[indexus]
                classes.addAll(self.getNeighbouringClassesWhereGivenClassIsADomain(uri))
                indexus += 1
        return classes

    def getNeighbouringClassesWhereGivenClassIsARange(self, classUri, forceSuperClasses):
        classes = list()
        if forceSuperClasses:
            # here recursively go and first find all super classes
            feedClasses = self.findSuperClasses(classUri, HashSet())
            feedClasses.add(classUri)
            logging.info("found " + feedClasses.size() + " super classes for " + classUri)
            # then for each superclass do the same as above
            # for (String uri : feedClasses) {
            indexus = 0
            while indexus < feedClasses.length:
                uri = feedClasses[indexus]
                classes.addAll(self.getNeighbouringClassesWhereGivenClassIsARange(uri))
                logging.info("found " + classes.size() + " elements for " + uri)
                indexus += 1
        return classes

    # *
    # * @param classUri
    # * @return
    #
    def findSuperClasses(self, classUri, superClassesToSave):
        searchFinished = False
        while not searchFinished:
            directSuperClasses = self.searchForClass(classUri, RDFS.SUBCLASSOF)
            # System.out.println("SuperClasses for:" + classUri + " are: "
            # + directSuperClasses.toString());
            if directSuperClasses == None or directSuperClasses.size() == 0 or superClassesToSave.containsAll(directSuperClasses):
                searchFinished = True
            else:
                # logging.info("searchFinished for SuperClasses");
                # System.out.println("size:"+directSuperClasses.size());
                superClassesToSave.addAll(directSuperClasses)
                # for (String cUri : directSuperClasses) {
                indexus = 0
                while indexus < directSuperClasses.length:
                    cUri = directSuperClasses[indexus]
                    # System.out.println("Curi:"+cUri);
                    superClassesToSave.addAll(self.findSuperClasses(cUri, superClassesToSave))
                    indexus += 1
                searchFinished = True
        logging.info("For " + classUri + " found " + superClassesToSave.size() + " super-classes.")
        return superClassesToSave

    # *
    # * @param classUri
    # * @return
    #
    def getNeighbouringClassesWhereGivenClassIsADomain(self, classUri):
        classes = list()
        properties = self.searchForInstance(classUri, RDFS.DOMAIN)
        # for (String property : properties) {
        indexus = 0
        while indexus < properties.length:
            property = properties[indexus]
            classes.addAll(self.searchForClass(property, RDFS.RANGE))
            indexus += 1
        return classes

    # *
    # * @param classUri
    # * @return
    #
    def getNeighbouringClassesWhereGivenClassIsARange(self, classUri):
        classes = HashSet()
        properties = self.searchForInstance(classUri, RDFS.RANGE)
        # for (String property : properties) {
        indexus = 0
        while indexus < properties.length:
            property = properties[indexus]
            classes.addAll(self.searchForClass(property, RDFS.DOMAIN))
            indexus += 1
        return classes

    def searchForInstance(self, classUri, pred):
        uris = list()
        fields = Array[str]((FreyaConstants.CLASS_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB))
        flags = [False,False] # FIX THIS!
        queries = Array[str](("\"" + classUri + "\"", "\"" + pred + "\""))
        try:
            query = MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, StandardAnalyzer(Version.LUCENE_30))
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                uris.add(doc.get(FreyaConstants.INST_FEATURE_LKB))
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
        fields = Array[str]((FreyaConstants.INST_FEATURE_LKB, FreyaConstants.CLASS_FEATURE_LKB))
        flags = [False,False] # FIX THIS!
        queries = Array[str](("\"" + inst + "\"", "\"" + OWL.DATATYPEPROPERTY + "\""))
        try:
            query = MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, StandardAnalyzer(Version.LUCENE_30))
            result = self._searcher.search(query, 1)
            logging.info("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                classUris.add(doc.get(FreyaConstants.INST_FEATURE_LKB))
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
        fields = Array[str]((FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB))
        flags = [False,False] # FIX THIS!
        queries = Array[str](("\"" + inst + "\"", "\"" + pred + "\""))
        try:
            query = MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, StandardAnalyzer(Version.LUCENE_30))
            result = self._searcher.search(query, 1)
            logging.info("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                classUris.add(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
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
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            parser = QueryParser(Version.LUCENE_CURRENT, FreyaConstants.PROPERTY_FEATURE_LKB, analyzer)
            query = parser.parse("\"" + propertyURI + "\"")
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                allClasses.add(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
                indexus += 1
            # for (String classUri : allClasses) {
            indexus = 0
            while indexus < allClasses.length:
                classUri = allClasses[indexus]
                logging.info("Checking whether " + classUri + " is a top class.")
                # search inst and pred retrieve class
                # if class exists that means it is not top class otherwise add to
                # topClasses
                classes = self.searchForClass(classUri, propertyURI)
                logging.info("top classes:" + classes.size())
                if classes != None or classes.size() > 0:
                    logging.info("This is not a top class...")
                else:
                    topClasses.add(classUri)
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
        return self.findDirectTypes(instanceUri, 1).get(0)

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
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            parser = QueryParser(Version.LUCENE_CURRENT, "inst", analyzer)
            query = parser.parse("\"" + instanceUri + "\"")
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + result.totalHits)
            freq = 0
            if max != None:
                freq = max
            else:
                freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                self._searcher.explain(query, hit.doc)
                dTypes.add(doc.get(FreyaConstants.CLASS_FEATURE_LKB))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        logging.debug("there are " + dTypes.size() + " unique direct types")
        return ArrayList(dTypes)

    # *
    # * find lucene annotations for this poc
    # *
    # * @param annotation
    # * @return
    #
    def findLabels(self, instanceUri):
        labels = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            fields = Array[str]((FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB))
            flags = [False,False] # FIX THIS!
            labelOrTitleUris = "\"http://www.w3.org/2000/01/rdf-schema#label\"" # +
            # " OR http://purl.org/dc/elements/1.1/title";
            queries = Array[str](("\"" + instanceUri + "\"", labelOrTitleUris))
            query = MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                labels.add(doc.get(FreyaConstants.FIELD_EXACT_CONTENT))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return ArrayList(labels)

    def findLiteral(self, instanceUri, propertyURI):
        labels = list()
        try:
            analyzer = StandardAnalyzer(Version.LUCENE_30)
            fields = Array[str]((FreyaConstants.INST_FEATURE_LKB, FreyaConstants.PROPERTY_FEATURE_LKB))
            flags = [False,False] # FIX THIS!
            labelOrTitleUris = "\"" + propertyURI + "\""
            queries = Array[str](("\"" + instanceUri + "\"", labelOrTitleUris))
            query = MultiFieldQueryParser.parse(Version.LUCENE_30, queries, fields, flags, analyzer)
            result = self._searcher.search(query, 1)
            logging.debug("For " + query.toString() + " : " + result.totalHits)
            freq = result.totalHits
            if freq > 0:
                result = self._searcher.search(query, freq)
            hits = result.scoreDocs
            # for (ScoreDoc hit : hits) {
            indexus = 0
            while indexus < hits.length:
                hit = hits[indexus]
                doc = self._searcher.doc(hit.doc)
                labels.add(doc.get(FreyaConstants.FIELD_EXACT_CONTENT))
                indexus += 1
        except Exception as e:#CorruptIndexException(e):
            print e.message
            logging.error("Error")
        return ArrayList(labels)

    def main(args):
        an = LuceneAnnotator()
        an.init()
        inputStream = None
        try:
            inputStream = FileInputStream("WordNet-3.0/dict/prolog/wn_s.pl")
            # an.synonymMap = new SynonymMap(inputStream);
            an.setIndex(File("/home/danica/freya/mooney/index"))
            classUri = "http://dbpedia.org/ontology/Mountain"
            result = an.findSuperClasses(classUri, HashSet())
            Console.WriteLine("Finished 1: " + result.toString())
            result = an.getDefinedPropertiesWhereClassIsADomain(classUri, True)
            Console.WriteLine("Finished 2: " + result.toString())
            thisPropertyUri = "http://www.mooney.net/geo#cityPopulation"
            isIt = an.isItDatatypeProperty(thisPropertyUri)
            Console.WriteLine("Finished 3: " + isIt)
            # Annotation annotation = new Annotation();
            # annotation.setText("album");
            # System.out.println("started ");
            # Set<Annotation> result = an.searchIndex(annotation);
            # System.out.println("finished "+result.size());
            inputStream.close()
        except Exception as e:#FileNotFoundException(e):
            print e.message
            logging.error("Error")

    main = staticmethod(main)
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
    # print arr
    # for iterator in an.searchIndex(arr, False):
    #     print iterator
    # print an.findClassURIs()
    # print an.findDatatypePropertyURIs()
    print an.findSubClasses('http://www.mooney.net/geo#City')