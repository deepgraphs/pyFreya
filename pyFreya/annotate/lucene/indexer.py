__author__ = 'root'
import lucene
import sys
from sys import stdin
from lucene import   SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexWriter, Version
if __name__ == "__main__":
    lucene.initVM()
    indexDir = "/index/test"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(1024))
    with open("data.txt",'r') as f:
        for doc in f.read().split("newDocSep"):
            docr = Document()
            for field in doc.split("csvSep"):
                fieldData = field.split("||")
                try:docr.add(Field(fieldData[1], fieldData[2], Field.Store.YES, Field.Index.ANALYZED))
                except:print "fuckup"
            print "\n"
            writer.addDocument(docr)
    print >> sys.stderr, "Indexed lines from stdin (%d documents in index)" % (writer.numDocs())
    print >> sys.stderr, "About to optimize index of %d documents..." % writer.numDocs()
    writer.optimize()
    print >> sys.stderr, "...done optimizing index of %d documents" % writer.numDocs()
    print >> sys.stderr, "Closing index of %d documents..." % writer.numDocs()
    print >> sys.stderr, "...done closing index of %d documents" % writer.numDocs()
    writer.close()