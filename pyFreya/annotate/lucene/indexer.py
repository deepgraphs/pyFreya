__author__ = 'root'
import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, FieldType
if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    indexDir = "../pyFreya/freya/index/actual"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(dir, config)
    with open("data",'r') as f:
        for doc in f.read().split("newDocSep"):
            docr = Document()
            for field in doc.split("csvSep"):
                fieldData = field.split("||")
                try:docr.add(Field(fieldData[1], fieldData[2], Field.Store.YES, Field.Index.ANALYZED))
                except:print "ups"
            print "\n"
            writer.addDocument(docr)
    print >> sys.stderr, "Indexed lines from stdin (%d documents in index)" % (writer.numDocs())
    print >> sys.stderr, "About to optimize index of %d documents..." % writer.numDocs()
    writer.commit()
    print >> sys.stderr, "...done optimizing index of %d documents" % writer.numDocs()
    print >> sys.stderr, "Closing index of %d documents..." % writer.numDocs()
    print >> sys.stderr, "...done closing index of %d documents" % writer.numDocs()
    writer.close()