'''
Created on Jul 12, 2014

@author: Me
'''

SENTENCE_DELIMITER = "\n "
QUESTION = "processedQuestion"
SEMANTIC_CONCEPTS = "semanticConcepts"
VARIABLE_E = "E"
VARIABLE_L = "L"
VARIABLE_P = "P"
VARIABLE_T = "T"
POC_TYPE = "POC"
OC_TYPE = "OC"
CLASS_FEATURE_LKB = "class"
OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
INST_FEATURE_LKB = "inst"
PROPERTY_FEATURE_LKB = "pred"
FIELD_EXACT_CONTENT = "prec"
FIELD_EXACT_LOWERCASED_CONTENT = "low"
FIELD_STEMMED_CONTENT = "stem"
SCORE = "score"
MAX_FUNCTION = "max"
MIN_FUNCTION = "min"
SUM_FUNCTION = "sum"
NONE_NEIGHBOURING_ONTOLOGY_ELEMENT = "NONENEIGHBOURINGONTOLOGYELEMENT"
INSTANCE_WITHOUT_DIRECT_CLASS = "INSTANCEWITHOUTDIRECTCLASS"
NUMBER_OF_RESULTS = "numberOfResults"
TRIPLE_ELEMENTS = "tripleElements"
RESULTS_GRAPH = "resultsGraph"
ANSWER = "answer"
ELEMENTS = "elements"
TABLE = "table"
GRAPH = "graph"
SPARQL = "sparql"
PRECISE_SPARQL = "preciseSparql"
REPOSITORY_URL = "repositoryUrl"
REPOSITORY_ID = "repositoryId"
# ///////////////////////////////////////
# query specific constants ////////////
# //////////////////////////////////////
NP_TAG_TREEBANK = "NP"
NN_TAG_TREEBANK = "NN"
NX_TAG_TREEBANK = "NX"
PRP_TAG_TREEBANK = "PRP"
EX_TAG_TREEBANK = "EX"
WHADVP_TAG_TREEBANK = "WHADVP"
WHADJP_TAG_TREEBANK = "WHADJP"
WHNP_TAG_TREEBANK = "WHNP"
WRB_TAG_TREEBANK = "WRB"
WP_TAG_TREEBANK = "WP"
RB_TAG_TREEBANK = "RB"
# * JJ adjective, JJR comparative, JJS superlative
JJ_TAG_TREEBANK = "JJ"
# * VBN verb, past participle
VBN_TAG_TREEBANK = "VBN"
# * RBS adverb, superlative
RBS_TAG_TREEBANK = "RBS"
ADJP_TAG_TREEBANK = "ADJP"
DT_TAG_TREEBANK = "DT"
DEBUG_MODE = False
ANNOTATION_FEATURE_TREE = "Tree"
STANFORD_TREE = "StanfordTree"
RESULT_TYPE_GRAPH = "Graph"
RESULT_TYPE_TREE = "Tree"
RESULT_TYPE_STRING = "string"
ANNOTATION_TYPE_ONTORES = "OntoRes"
ANNOTATION_TYPE_ONTORESCHUNK = "OntoResChunk"
# used when grouping elements to indicate if it is a conjunction element
CONJUNCTION = "and"
# used when grouping elements to indicate if it is a disjunction element
DISJUNCTION = "or"
# *
# * this constant is used to indicate wheather the keyword is from the gazetteer with this name
# 
LIST_COMMANDS = "listCommands"
# *
# * Name of the common logger
# 
LOGGER_NAME = "CLOnE-QL-logger"
LOGGER_OUPUT_LEVEL = "2000"
# separator used during formatting of results
TRIPLES_SEPARATOR = " --> "
# 
# * flag indicating the output of the result, in this case it is refering to the resource names
# 
SHOWING_TRIPLES_WITH_RESOURCE_NAMES = "showingTriplesWithResourceNames"
# 
# * flag indicating the output of the result, in this case it is refering to the labels
# 
SHOWING_TRIPLES_WITH_LABELS = "showingTriplesWithLabels"
REGEX_GROUPS_SEPARATED_BY_AND = "i\\d+-and-i\\d+(-and-i\\d+)*"
REGEX_GROUPS_SEPARATED_BY_OR = "i\\d+-or-i\\d+(-or-i\\d+)*"
GROUP_PREFIX = "gs:"
GROUP_SUFFIX = ":ge"
REGEX_PPP = "[i,c,d,g]\\d+-([k,o,p]\\d+-)*[i,c,d,g]\\d+"
REGEX_FIND_JOKER = "[i,c,d,g]\\d+-[i,c,d,g]\\d+"
REGEX_FIND_CLASS_JOKER = "[p]\\d+-[p]\\d+"
POTENTIAL_PROPERTY_POSITION = "-r"
EXACT_PROPERTY = "-ep"
POTENTIAL_RELATED_ELEMENTS = ":"
MAX_SIMILARITY_VALUE = "1"
# three types of weights - to show the importance of every type of score
SIMILARITY_SCORE_WEIGHT = 3.0
SPECIFICITY_SCORE_WEIGHT = 1.0
DISTANCE_SCORE_WEIGHT = 1.0
SELECT = "select distinct"
WHERE = "where"
FROM = "from"
INVERSE_PROPERTY = "[inverseProperty]"
JOKER = "joker"
LITERAL_VALUE_CONNECTOR = "is"
# these are used as annotation type names in order to transwer the results
# from the gate pipeline elsewhere
QUERY = "query"
INTERPRETATIONS_LIST = "interpretationsList"
SELECTED_INTERPRETATION = "selectedInterpretation"
INTERPRETATION_RESULTS = "interpretationResults"
QUERY_INTERPRETATIONS = "queryInterpretations"
MAP_OF_LABELS = "mapOfLabels"
LEVENSHTEIN_THRESHOLD = 0.1
MONGE_THRESHOLD = 0.5
MAX_MONGE_THRESHOLD = 1.0
REINFORCEMENT_REWARD = 1.0
REINFORCEMENT_NULL_STATE = 0
REINFORCEMENT_NEGATIVE_REWARD = -1.0
CLARIFICATION_OPTIONS_NONE = "none"
CLARIFIED_INTERPRETATION_DETAILS = "clarifiedInterpretationDetails"
CIPIN_SEPARATOR = ","
# priority over ontology annotations
MAIN_SUBJECT_PRIORITY_MAX = 100
MAIN_SUBJECT_PRIORITY_MIN = 0
