'''
Created on Jul 12, 2014

@author: Me
'''
class FreyaConstants(object):
    def __init__(self):
        self._SENTENCE_DELIMITER = "\n "
        self._QUESTION = "processedQuestion"
        self._SEMANTIC_CONCEPTS = "semanticConcepts"
        self._VARIABLE_E = "E"
        self._VARIABLE_L = "L"
        self._VARIABLE_P = "P"
        self._VARIABLE_T = "T"
        self._POC_TYPE = "POC"
        self._OC_TYPE = "OC"
        self._CLASS_FEATURE_LKB = "class"
        self._OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
        self._INST_FEATURE_LKB = "inst"
        self._PROPERTY_FEATURE_LKB = "pred"
        self._FIELD_EXACT_CONTENT = "prec"
        self._FIELD_EXACT_LOWERCASED_CONTENT = "low"
        self._FIELD_STEMMED_CONTENT = "stem"
        self._SCORE = "score"
        self._MAX_FUNCTION = "max"
        self._MIN_FUNCTION = "min"
        self._SUM_FUNCTION = "sum"
        self._NONE_NEIGHBOURING_ONTOLOGY_ELEMENT = "NONENEIGHBOURINGONTOLOGYELEMENT"
        self._INSTANCE_WITHOUT_DIRECT_CLASS = "INSTANCEWITHOUTDIRECTCLASS"
        self._NUMBER_OF_RESULTS = "numberOfResults"
        self._TRIPLE_ELEMENTS = "tripleElements"
        self._RESULTS_GRAPH = "resultsGraph"
        self._ANSWER = "answer"
        self._ELEMENTS = "elements"
        self._TABLE = "table"
        self._GRAPH = "graph"
        self._SPARQL = "sparql"
        self._PRECISE_SPARQL = "preciseSparql"
        self._REPOSITORY_URL = "repositoryUrl"
        self._REPOSITORY_ID = "repositoryId"
        # ///////////////////////////////////////
        # query specific constants ////////////
        # //////////////////////////////////////
        self._NP_TAG_TREEBANK = "NP"
        self._NN_TAG_TREEBANK = "NN"
        self._NX_TAG_TREEBANK = "NX"
        self._PRP_TAG_TREEBANK = "PRP"
        self._EX_TAG_TREEBANK = "EX"
        self._WHADVP_TAG_TREEBANK = "WHADVP"
        self._WHADJP_TAG_TREEBANK = "WHADJP"
        self._WHNP_TAG_TREEBANK = "WHNP"
        self._WRB_TAG_TREEBANK = "WRB"
        self._WP_TAG_TREEBANK = "WP"
        self._RB_TAG_TREEBANK = "RB"
        # * JJ adjective, JJR comparative, JJS superlative
        self._JJ_TAG_TREEBANK = "JJ"
        # * VBN verb, past participle
        self._VBN_TAG_TREEBANK = "VBN"
        # * RBS adverb, superlative
        self._RBS_TAG_TREEBANK = "RBS"
        self._ADJP_TAG_TREEBANK = "ADJP"
        self._DT_TAG_TREEBANK = "DT"
        self._DEBUG_MODE = False
        self._ANNOTATION_FEATURE_TREE = "Tree"
        self._STANFORD_TREE = "StanfordTree"
        self._RESULT_TYPE_GRAPH = "Graph"
        self._RESULT_TYPE_TREE = "Tree"
        self._RESULT_TYPE_STRING = "string"
        self._ANNOTATION_TYPE_ONTORES = "OntoRes"
        self._ANNOTATION_TYPE_ONTORESCHUNK = "OntoResChunk"
        # used when grouping elements to indicate if it is a conjunction element
        self._CONJUNCTION = "and"
        # used when grouping elements to indicate if it is a disjunction element
        self._DISJUNCTION = "or"
        # *
        # * this constant is used to indicate wheather the keyword is from the gazetteer with this name
        # 
        self._LIST_COMMANDS = "listCommands"
        # *
        # * Name of the common logger
        # 
        self._LOGGER_NAME = "CLOnE-QL-logger"
        self._LOGGER_OUPUT_LEVEL = "2000"
        # separator used during formatting of results
        self._TRIPLES_SEPARATOR = " --> "
        # 
        # * flag indicating the output of the result, in this case it is refering to the resource names
        # 
        self._SHOWING_TRIPLES_WITH_RESOURCE_NAMES = "showingTriplesWithResourceNames"
        # 
        # * flag indicating the output of the result, in this case it is refering to the labels
        # 
        self._SHOWING_TRIPLES_WITH_LABELS = "showingTriplesWithLabels"
        self._REGEX_GROUPS_SEPARATED_BY_AND = "i\\d+-and-i\\d+(-and-i\\d+)*"
        self._REGEX_GROUPS_SEPARATED_BY_OR = "i\\d+-or-i\\d+(-or-i\\d+)*"
        self._GROUP_PREFIX = "gs:"
        self._GROUP_SUFFIX = ":ge"
        self._REGEX_PPP = "[i,c,d,g]\\d+-([k,o,p]\\d+-)*[i,c,d,g]\\d+"
        self._REGEX_FIND_JOKER = "[i,c,d,g]\\d+-[i,c,d,g]\\d+"
        self._REGEX_FIND_CLASS_JOKER = "[p]\\d+-[p]\\d+"
        self._POTENTIAL_PROPERTY_POSITION = "-r"
        self._EXACT_PROPERTY = "-ep"
        self._POTENTIAL_RELATED_ELEMENTS = ":"
        self._MAX_SIMILARITY_VALUE = "1"
        # three types of weights - to show the importance of every type of score
        self._SIMILARITY_SCORE_WEIGHT = 3.0
        self._SPECIFICITY_SCORE_WEIGHT = 1.0
        self._DISTANCE_SCORE_WEIGHT = 1.0
        self._SELECT = "select distinct"
        self._WHERE = "where"
        self._FROM = "from"
        self._INVERSE_PROPERTY = "[inverseProperty]"
        self._JOKER = "joker"
        self._LITERAL_VALUE_CONNECTOR = "is"
        # these are used as annotation type names in order to transwer the results
        # from the gate pipeline elsewhere
        self._QUERY = "query"
        self._INTERPRETATIONS_LIST = "interpretationsList"
        self._SELECTED_INTERPRETATION = "selectedInterpretation"
        self._INTERPRETATION_RESULTS = "interpretationResults"
        self._QUERY_INTERPRETATIONS = "queryInterpretations"
        self._MAP_OF_LABELS = "mapOfLabels"
        self._LEVENSHTEIN_THRESHOLD = 0.1
        self._MONGE_THRESHOLD = 0.5
        self._MAX_MONGE_THRESHOLD = 1.0
        self._REINFORCEMENT_REWARD = 1.0
        self._REINFORCEMENT_NULL_STATE = 0
        self._REINFORCEMENT_NEGATIVE_REWARD = -1.0
        self._CLARIFICATION_OPTIONS_NONE = "none"
        self._CLARIFIED_INTERPRETATION_DETAILS = "clarifiedInterpretationDetails"
        self._CIPIN_SEPARATOR = ","
        # priority over ontology annotations
        self._MAIN_SUBJECT_PRIORITY_MAX = 100
        self._MAIN_SUBJECT_PRIORITY_MIN = 0
if __name__=="__main__":
    Constants=FreyaConstants()
    print Constants._QUERY_INTERPRETATIONS #test