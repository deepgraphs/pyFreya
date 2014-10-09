
from freya.model.Annotation import *
from freya.model.MainSubject import *
from freya.model.POC import *
from freya.model.Question import *
from freya.util.FreyaConstants import *
import logging
from multiprocessing import Process, Queue
from corenlp import *
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from nltk.tree import Tree
import time
import nltk
from TreeUtils import *
# *
# * This USED TO BE PR is a very simple wrapper for SP: as input it takes documents, and as output it generates
# * edu.stanford.nlp.trees.Tree object and stores it in the default Annotation Set as 'StanfordTree' annotation type with
# * feature 'tree'
# *
# * @author danica
# 
#@Component
class SimpleStanfordParser(object):
    def __init__(self):
        self._serialVersionUID = -3062171258011850283L
        logging.basicConfig(filename='../../index/simplestanfordparser.log', filemode='w', level=logging.DEBUG)
    #static org.apache.commons.logging.Log logging =
    #org.apache.commons.logging.LogFactory.getLog(SimpleStanfordParser.class);
    #
    #@Value("${org.freya.parser.stanford.model}") Resource parserFile;
    #@Autowired TreeUtils treeUtils;
    # *
    # * tries to predice whether it is boolean how many/count or any other question type
    # *
    # * @param question
    # * @return
    #
    def findQuestionType(self, question):
        root = question.getSyntaxTree()
        firstTree = Trees.getPreTerminal(root, 0)
        Console.WriteLine("firstTree:" + firstTree.label().value())
        Console.WriteLine("firstTree children 0:" + firstTree.getChildrenAsList().get(0).label().value())
        if firstTree.label().value().startsWith("VB") and (not firstTree.getChildrenAsList().get(0).label().value().ToLower().equals("show") and not firstTree.children()[0].label().value().ToLower().equals("give") and not firstTree.children()[0].label().value().ToLower().equals("list") and not firstTree.children()[0].label().value().ToLower().equals("count")):
            question.setType(Type.BOOLEAN)
        elif firstTree.getChild(0).label().value().ToLower().startsWith("count"):
            question.setType(Type.LONG)
        elif firstTree.getChild(0).label().value().ToLower().equals("how"):
            secondTree = Trees.getPreTerminal(root, 1)
            if secondTree.getChild(0).label().value().ToLower().equals("much") or secondTree.getChild(0).label().value().ToLower().equals("many"):
                question.setType(Type.LONG)
            else:
                question.setType(Type.UNKNOWN)
        else:
            question.setType(Type.UNKNOWN)
        return question

    # /**
    #  * Parse the current document without making links to GATE annotaitons.
    #  */
    def parseQuestion(self, text):
        question = Question()
        print "RECEIVED DATA IS\n" + text
        wordList = nltk.word_tokenize(text)
        i = 0
        tokens = list()
        for word in wordList:
            print "WORD: "+str(word)
            if not str(word).strip() is "" and not str(word).strip() is "." and not str(word).strip() is "?" and not str(word).strip() is "!" and not str(word).strip() is ",":
                tokens.append(word)
            i+=1
        print tokens
        question.setTokens(tokens)
        result = self.parse(text)
        tree = Tree.parse(result['sentences'][0]['parsetree'])
        print TreeUtils.findPocs(tree)
        # tlp = PennTreebankLanguagePack()
        # extends if IList <  else HasWord > wordList
        # if self._lp != None and text.length() > 0:
        # 	extends if Tokenizer <  else HasWord > toke
        # 	wordList = toke.tokenize()
        # 	tokens = ArrayList[HasWord]()
        # 	i = 0
        # 	while :
        # question.setTokens(tokens)






    def findFocus(self, question):
        # TODO consider an alternative solution
        mainSubject = MainSubject()
        pocs = question.getPocs()
        logger.info("There are " + pocs.size() + " pocs")
        if pocs != None and pocs.size() > 0:
            firstPoc = pocs.get(0)
            mainSubjectString = firstPoc.getAnnotation().getText().ToLower()
            if mainSubjectString.startsWith("how") or mainSubjectString.startsWith("where") or mainSubjectString.startsWith("when") or mainSubjectString.startsWith("since") or mainSubjectString.startsWith("who") or mainSubjectString.startsWith("list") or mainSubjectString.startsWith("show"):
                logging.info("SETTING UP THE PRIORITY FOR THE MAIN SUBJECT AS IT STARTS WITH HOW...")
                mainSubject.setPriority(FreyaConstants.MAIN_SUBJECT_PRIORITY_MAX)
            else:
                mainSubject.setPriority(FreyaConstants.MAIN_SUBJECT_PRIORITY_MIN)
            firstPoc.setMainSubject(mainSubject)
            question.setFocus(firstPoc)
            preservedFocus = self.preserveFocus(question.getFocus(), question.getSyntaxTree())
            question.setFocus(preservedFocus)
        return question

    # *
    # * just copy POC into another POC so that focus can be saved for later even when all pocs are resolved through the
    # * dialog
    # *
    # * @param focus
    # * @return
    #
    def preserveFocus(self, focus, root):
        preservedFocus = POC()
        annotation = Annotation()
        if focus != None:
            annotation.setText(focus.getAnnotation().getText())
            annotation.setEndOffset(focus.getAnnotation().getEndOffset())
            annotation.setStartOffset(focus.getAnnotation().getStartOffset())
            trees = focus.getAnnotation().getSyntaxTree()
            firstTree = trees.get(0)
            toRemove = False
            if firstTree.isPrePreTerminal():
                logging.info("OK:")
                # check whether it starts with which or what and if yes remove it
                toTest = firstTree.getChildrenAsList().get(0).getLeaves().get(0)
                logging.info("totest:" + toTest.label().value())
                if toTest.label().value().ToLower().startsWith("which") or toTest.label().value().ToLower().startsWith("what"):
                    toRemove = True
            else:
                logging.info("Not OK:, firstTree:" + firstTree.toString())
            if toRemove:
                all = firstTree.getChildrenAsList()
                all.remove(0)
                focus.getAnnotation().setSyntaxTree(all)
                focus.getAnnotation().setStartOffset(focus.getAnnotation().getStartOffset() + 1)
                focus.getAnnotation().setText(treeUtils.getNiceString(all))
            logging.info("Focus now looks like this:" + focus.toString())
            annotation.setSyntaxTree(focus.getAnnotation().getSyntaxTree())
            preservedFocus.setMainSubject(focus.getMainSubject())
            preservedFocus.setHead(focus.getHead())
            preservedFocus.setModifiers(focus.getModifiers())
        preservedFocus.setAnnotation(annotation)
        return preservedFocus

    # *
    # * method which 'cleans' pocs and separate jjs into separate ones, deletes wrb if they are followed by something
    # * else, leaves them otherwise e.g. where is...is WHADVP-WRB-where..here we do not want to delete WRB how big
    # * is...is WHADJP-(WRB-JJ), so here we want to get rid of WRB
    # *
    # * @param cleanedPocs
    # * @param root
    # * @param stanfordSentence
    # * @return
    #
    def cleanPocsLucene(self, question):
        cleanedPocs = question.getPocs()
        root = question.getSyntaxTree()
        # remove wrb elements
        # cleanedPocs = treeUtils.removeWRB(cleanedPocs);
        logging.info("Before separating POCs (if they contain WRB) there are " + cleanedPocs.size() + " POCs." + cleanedPocs.toString())
        cleanedPocs = treeUtils.generateSeparatePOCForAdjectives(cleanedPocs, root)
        logging.info("After separating POCs if they contain ajdectives JJ* there are " + cleanedPocs.size() + " POCs." + cleanedPocs.toString())
        return question

    # *
    # * initialisation of stanford parser, loading training data from file
    # *
    # * @throws ResourceInstantiationException
    #
    def instantiateStanfordParser(self): # throws Exception
        try:
            logging.info("Starting Parser Service:")
            self.que = Queue()
            # self._lp = LexicalizedParser.loadModel(parserFile.getFile().getAbsolutePath())
            # self._lp.setOptionFlags(Array[str](("-maxLength", "80", "-retainTmpSubcategories")))
            self.process = Process(target=self.json_server, args=(self.que,))
            self.process.start()
            print self.que.get()
            time.sleep(1)
            print "done loading"
            self.server = ServerProxy(JsonRpc20(),
                          TransportTcpIp(addr=("127.0.0.1", 8080)))
        except Exception as e:
            print e.message
    def parse(self, text):
        return json.loads(self.server.parse(text))
    def __enter__(self):
        return self
    def __exit__(self,a,f,g):
       self.process.terminate()
    def json_server(self,que):
        """The code below starts an JSONRPC server
        """
        parser = optparse.OptionParser(usage="%prog [OPTIONS]")
        parser.add_option('-p', '--port', default='8080', help='Port to serve on (default 8080)')
        parser.add_option('-H', '--host', default='127.0.0.1',help='Host to serve on (default localhost; 0.0.0.0 to make public)')
        options, args = parser.parse_args()
        server = jsonrpc.Server(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=(options.host, int(options.port))))
        nlp = StanfordCoreNLP()
        server.register_function(nlp.parse)
        que.put("About Done!")
        print 'Serving on http://%s:%s' % (options.host, options.port)
        server.serve()
if __name__=="__main__":
    with SimpleStanfordParser() as  p:
        p.instantiateStanfordParser()
        p.parseQuestion("How may albums did Michael Jackson record?.")
        # result = p.parse("How may albums did Michael Jackson record?.")
        # pprint(result)
        # print "__ClientOutput__"
        # tree = Tree.parse(result['sentences'][0]['parsetree'])
        # pprint(tree)
        # p.process.join()
        # text = "How may albums did Michael Jackson record?."
        # try:
        # except Exception as e:#IOException(e):
        # print e.message