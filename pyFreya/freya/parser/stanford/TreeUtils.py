from freya.model.POC import *
import freya.util.FreyaConstants as FreyaConstants
#@Component
class TreeUtils(object):
	#    static org.apache.commons.logging.Log logger =
	#                    org.apache.commons.logging.LogFactory.getLog(TreeUtils.class);
	#@Value("${org.freya.parser.preterminal.pocs}") String preterminalPOCs;
	def getAnswerType(self, tree):
		mainSubjectTree = self.findTheHeadOfTheNounPhrase(tree)
		return mainSubjectTree

	# *
	# * @param tree
	# * @return
	#
	def getMainSubjectTree(self, tree):
		pocs = self.findPocs(tree)
		if pocs != None and pocs.size() > 0:
			return pocs.get(0)
		else:
			return None

	# *
	# * finds the first NP/NN* (main subject/answer type/focus);
	# *
	# * @param tree
	# * @return
	#
	def findTheFirstNounPhraseOld(self, tree):
		value = None
		# treeLabel is the pos tag: NP, VP, etc.
		treeLabel = tree.label().value()
		if treeLabel != None and (treeLabel.startsWith("NP") or treeLabel.startsWith("NN")) and not (treeLabel.startsWith("PRP")):
			# || treeLabel.startsWith("WHNP")
			return tree
		elif treeLabel != None and (treeLabel.startsWith("WHADVP") or treeLabel.startsWith("WHNP") or treeLabel.startsWith("WHADJP")): # this is to support how long,
			# how
			# large, how big, etc.
			children = tree.getChildrenAsList()
			if children != None and children.size() <= 2: # we always expect
				# one or two
				firstChild = children.get(0)
				secondChild = None
				if children.size() > 1:
					secondChild = children.get(1)
				# this is to support where what etc
				if secondChild == None and (firstChild.label().value().startsWith("WRB")):
					# || firstChild.label().value().startsWith("WP"))) {
					return tree
				elif secondChild != None:
					if firstChild.label().value().startsWith("WRB") and ((secondChild.label().value().startsWith("JJ")) or secondChild.label().value().startsWith("ADJP")) or secondChild.label().value().startsWith("NN") or secondChild.label().value().startsWith("NP") or firstChild.label().value().startsWith("NN") or firstChild.label().value().startsWith("NP"):
						# return secondChild;// well?
						return tree
			elif children != None:
				it = children.iterator()
				while it.hasNext():
					something = it.next()
					if something.label().value().startsWith("NP") or (something.label().value().startsWith("NN")):
						return something
		else:
			listOfChildren = tree.getChildrenAsList()
			# put them in reverse order
			# Collections.reverse(listOfChildren);
			indexus = 0
			while indexus < listOfChildren.length():
				currentTree = listOfChildren[indexus]
				mainSubjectTree = self.getMainSubjectTree(currentTree)
				if mainSubjectTree != None:
					value = mainSubjectTree
					break
				indexus += 1
		return value

	# *
	# * fins preterminals
	# *
	# * @param tree
	# * @return
	#
	def findPrePreTerminals(self, tree):
		pocs = ArrayList[Tree]()
		value = None
		# treeLabel is the pos tag: NP, VP, etc.
		treeLabel = tree.label().value()
		# logger.info("label is:"+treeLabel);
		if tree.isPrePreTerminal():
			pocs.add(tree)
			logger.debug(treeLabel + " is prepreterminal so adding it to the list of POCs.")
			return pocs
		else:
			listOfChildren = tree.getChildrenAsList()
			# put them in reverse order
			# Collections.reverse(listOfChildren);
			# logger.info("now listing children...");
			indexus = 0
			while indexus < listOfChildren.length():
				currentTree = listOfChildren[indexus]
				# logger.info("child..."+currentTree.label().value());
				if currentTree.isPrePreTerminal():
					pocs.add(currentTree)
				else:
					pocs.addAll(self.findPrePreTerminals(currentTree))
				indexus += 1
		# logger.info("currently total pocs are:"+pocs.size());
		return pocs

	# *
	# * lucene split poc which contains adjective into two pocs: adjective and the rest
	# *
	# * @param pocs
	# * @param root
	# * @param stanfordSentence
	# * @return
	#
	def generateSeparatePOCForAdjectives(self, pocs, root):
		# if there is no JJ* generate a new poc and update the current
		adjectives = ArrayList[Tree]()
		toRemove = ArrayList[POC]()
		logger.debug("before checking jjs...pocs:" + pocs.toString())
		indexus = 0
		while indexus < pocs.length():
			pocElement = pocs[indexus]
			trees = pocElement.getAnnotation().getSyntaxTree()
			splitTrees = ArrayList[Tree]()
			indexus = 0
			while indexus < trees.length():
				eachTree = trees[indexus]
				if eachTree.isPrePreTerminal():
					# split into preterminals
					splitTrees.addAll(eachTree.getChildrenAsList())
				else:
					splitTrees.add(eachTree)
				indexus += 1
			remainingList = ArrayList[Tree]()
			indexus = 0
			while indexus < splitTrees.length():
				pocTree = splitTrees[indexus]
				if self.isDescriptive(pocTree) and splitTrees.size() > 1:
					# so that if JJs are already split we do not generate
					# duplicates
					adjectives.add(pocTree)
				else:
					if not remainingList.contains(pocTree):
						remainingList.add(pocTree)
				indexus += 1
			# //////////////////////////////////////update
			if remainingList != None and remainingList.size() > 0:
				pocElement = self.updatePOCAnnotation(remainingList, root, pocElement)
			else:
				# mark the poc for removal
				toRemove.add(pocElement)
			indexus += 1
		logger.debug("before splitting jjs...pocs:" + pocs.toString())
		# //////////////////////////////////////////
		# generate poc from the adjective
		# ////////////////////////////////////////
		if adjectives.size() > 0:
			indexus = 0
			while indexus < adjectives.length():
				adjective = adjectives[indexus]
				newPoc = POC()
				adjectiveTree = ArrayList[Tree]()
				adjectiveTree.add(adjective)
				newPoc = self.updatePOCAnnotation(adjectiveTree, root, newPoc)
				pocs.add(newPoc)
				indexus += 1
		logger.debug("after adding jjs...:" + pocs.toString())
		if toRemove.size() > 0:
			pocs.removeAll(toRemove)
		return pocs

	# *
	# * checks whether the tree is ajdective, adverb superlative or verb, past participle (as this verb is always part of
	# * the NP we assume it has the function of adjective such as 'populated state')
	# *
	# * @param tree
	# * @return
	#
	def isDescriptive(self, tree):
		isDescriptive = False
		if tree.label().value().startsWith(FreyaConstants.JJ_TAG_TREEBANK) or tree.label().value().startsWith(FreyaConstants.VBN_TAG_TREEBANK) or tree.label().value().startsWith(FreyaConstants.RBS_TAG_TREEBANK) or tree.label().value().startsWith("ADJP"):
			isDescriptive = True
		return isDescriptive

	# *
	# * checks whether there are any JJ* or ADJP inside poc
	# *
	# * @param poc
	# * @return
	#
	def pocContainsJJs(self, poc):
		containsJJs = False
		indexus = 0
		while indexus < poc.getAnnotation().getSyntaxTree().length():
			tree = poc.getAnnotation().getSyntaxTree()[indexus]
			treeLabel = tree.label().value()
			# logger.info("Checking whether "+treeLabel+ " is JJ");
			if self.isDescriptive(tree):
				containsJJs = True
				break
			else:
				children = tree.getChildrenAsList()
				indexus = 0
				while indexus < children.length():
					child = children[indexus]
					# String childLabel = child.label().value();
					if self.isDescriptive(child):
						containsJJs = True
						break
					indexus += 1
			indexus += 1
		return containsJJs

	# *
	# * if pocs are prepreterminals then split their tree into children
	# *
	# * @param pocs
	# * @return
	#
	def splitPocs(self, pocs):
		toRemove = ArrayList[POC]()
		indexus = 0
		while indexus < pocs.length():
			poc = pocs[indexus]
			trees = poc.getAnnotation().getSyntaxTree()
			if trees != None and trees.size() == 1:
				# check if they are prepreterminals
				tree = trees.get(0)
				if tree.isPrePreTerminal():
					# split into preterminals
					newTree = ArrayList[Tree]()
					indexus = 0
					while indexus < tree.getChildrenAsList().length():
						child = tree.getChildrenAsList()[indexus]
						newTree.add(child)
						indexus += 1
					poc.getAnnotation().setSyntaxTree(newTree)
			indexus += 1
		return pocs

	# *
	# * update the poc with new syntax tree and also update it's annotation start and end offsets and the text
	# *
	# * @param treeList
	# * @param root
	# * @param stanfordSentence
	# * @param poc
	# * @return poc updated with the syntax tree; null if the tree is empty
	#
	def updatePOCAnnotation(self, treeList, root, poc):
		if treeList == None or treeList.size() == 0:
			return None
		firstTree = treeList.get(0)
		parserStartOffset = Trees.leftEdge(firstTree, root)
		lastTree = treeList.get(treeList.size() - 1)
		parserEndOffset = Trees.rightEdge(lastTree, root)
		poc.getAnnotation().setStartOffset(parserStartOffset)
		poc.getAnnotation().setEndOffset(parserEndOffset)
		poc.getAnnotation().setText(self.getNiceString(treeList))
		poc.getAnnotation().setSyntaxTree(treeList)
		return poc

	# *
	# * independent of stanfordSentence remove DT from pocs: if poc has DT then transform it to the list of its children
	# * but remove DT now poc can be a list of trees which are on the same level, not only one tree
	# *
	# * @param pocs
	# * @return
	#
	def removeDTFromPOCs(self, pocs, root):
		# if there is no DT leave pocs as they are (one Tree in the list)
		indexus = 0
		while indexus < pocs.length():
			pocElement = pocs[indexus]
			# before executing this method all pocs are stored in list each
			# list having only one element
			pocTree = pocElement.getAnnotation().getSyntaxTree().get(0)
			list = ArrayList[Tree]()
			children = pocTree.getChildrenAsList()
			indexus = 0
			while indexus < children.length():
				child = children[indexus]
				if FreyaConstants.DT_TAG_TREEBANK.equals(child.label().value()):
					withoutDT = ArrayList[Tree]()
					withoutDT.addAll(children)
					withoutDT.remove(child)
					logger.debug("Removing DT from POC.")
					list = withoutDT
					break
				else:
					if not list.contains(pocTree):
						list.add(pocTree)
				indexus += 1
			pocElement = self.updatePOCAnnotation(list, root, pocElement)
			indexus += 1
		return pocs

	# *
	# * finds pocs: CURRENTLY these are NN* and NP*
	# *
	# * @param tree
	# * @return
	#
	def findPocs(self, tree):
        print "Received tree is: "+ str(tree)
		pocs = ArrayList[Tree]()
		prePreTerminals = self.findPrePreTerminals(tree)
		indexus = 0
		while indexus < prePreTerminals.length():
			node = prePreTerminals[indexus]
			nodeLabel = node.label().value()
			nodeChildLabel = node.getChildrenAsList().get(0).label().value()
			# NPs and NNs
			if nodeLabel != None and (nodeLabel.startsWith(FreyaConstants.NP_TAG_TREEBANK) or nodeLabel.startsWith(FreyaConstants.NN_TAG_TREEBANK) or nodeLabel.startsWith(FreyaConstants.NX_TAG_TREEBANK) or (nodeLabel.startsWith(FreyaConstants.ADJP_TAG_TREEBANK))) and not (nodeChildLabel.startsWith(FreyaConstants.PRP_TAG_TREEBANK)) and not (nodeChildLabel.startsWith(FreyaConstants.EX_TAG_TREEBANK)):
				pocs.add(node)
			elif 			# //////////////////////////////////////////////////////////////////
			# this is to support how long, //////
			# how //////
			# large, how big, etc. //////
			# //////////////////////////////////////////////////////////////////
            nodeLabel != None and (nodeLabel.startsWith(FreyaConstants.WHADVP_TAG_TREEBANK) or nodeLabel.startsWith(FreyaConstants.WHNP_TAG_TREEBANK) or 			# added because of high high: high is prepreterminal but
			# the whole how high is not
            nodeLabel.startsWith(FreyaConstants.WHADJP_TAG_TREEBANK)):
				children = node.getChildrenAsList()
				if children != None and children.size() <= 2: # we always
					# expect
					# one or two
					firstChild = children.get(0)
					secondChild = None
					if children.size() > 1:
						secondChild = children.get(1)
					# this is to support where what etc
					if secondChild == None and (firstChild.label().value().startsWith(FreyaConstants.WRB_TAG_TREEBANK) or firstChild.label().value().startsWith(FreyaConstants.WP_TAG_TREEBANK)):
						# || firstChild.label().value().startsWith("WP"))) {
						leaves = firstChild.getLeaves()
						indexus = 0
						while indexus < leaves.length():
							leaf = leaves[indexus]
							if leaf.label().value().ToLower().equals("where") or leaf.label().value().ToLower().equals("when") or leaf.label().value().ToLower().equals("who"):
								logger.info("Found WH-")
								# logger.info("leaf.label().value():" + leaf.label().value());
								pocs.add(node)
							indexus += 1
					elif secondChild != None:
						if firstChild.label().value().startsWith(FreyaConstants.WRB_TAG_TREEBANK) and ((secondChild.label().value().startsWith(FreyaConstants.JJ_TAG_TREEBANK)) or secondChild.label().value().startsWith(FreyaConstants.ADJP_TAG_TREEBANK)) or secondChild.label().value().startsWith(FreyaConstants.NN_TAG_TREEBANK) or secondChild.label().value().startsWith(FreyaConstants.NP_TAG_TREEBANK) or firstChild.label().value().startsWith(FreyaConstants.NN_TAG_TREEBANK) or firstChild.label().value().startsWith(FreyaConstants.NP_TAG_TREEBANK) or firstChild.label().value().startsWith(FreyaConstants.RB_TAG_TREEBANK):
							# return secondChild;// well?
							# this is to remove WRB in 'how long' how many etc
							pocs.add(node)
				elif children != None:
					it = children.iterator()
					while it.hasNext():
						something = it.next()
						if something.label().value().startsWith("NP") or (something.label().value().startsWith("NN")):
							pocs.add(something)
			indexus += 1 # if prepreterminal is WHNP, WHADJP or WHADVP
		# now also add those that are preterminals and NNs but were missed in
		# findPocs method
		logger.info("Number of pocs as prepreterminals:" + pocs.size())
		pocs.addAll(self.findPreTerminalsThatAreNNOrINs(tree, pocs))
		logger.info("Number of pocs as preterminals and prepreterminals (final num of pocs):" + pocs.size())
		return pocs

	# *
	# * find those preterminals that are NNs as they were missed due to the way sp parses tree
	# *
	# * @param root
	# * @param pocs
	# * @return
	#
	def findPreTerminalsThatAreNNOrINs(self, root, pocs):
		numberOfTokens = root.getLeaves().size()
		newList = ArrayList[Tree]()
		skipList = HashSet()
		indexus = 0
		while indexus < pocs.length():
			poc = pocs[indexus]
			logger.debug("Checking poc:" + poc.toString())
			start = Trees.leftEdge(poc, root)
			end = Trees.rightEdge(poc, root)
			logger.debug("Start poc:" + start)
			logger.debug("End poc:" + end)
			j = start
			while j < end:
				skipList.add(System.Nullable[Int64](j))
				logger.debug("Adding element to skip list:" + j)
				j += 1
			indexus += 1
		listToConsider = HashSet[Nullable]()
		i = 0
		while i < numberOfTokens:
			iFound = False
			indexus = 0
			while indexus < skipList.length():
				toSkip = skipList[indexus]
				if toSkip.longValue() == i:
					iFound = True
					break
				else:
				indexus += 1
			if not iFound:
				listToConsider.add(i)
			i += 1
		indexus = 0
		while indexus < listToConsider.length():
			element = listToConsider[indexus]
			preTerminal = None
			preTerminal = Trees.getPreTerminal(root, element.intValue())
			logger.debug("checking now:" + element.intValue() + " and its preterminal:" + preTerminal)
			if preTerminal != None and self.startsWithTagsToConsider(preTerminal.label().value()):
				newList.add(preTerminal)
				logger.info("Found preTerminal:" + preTerminal.toString())
			indexus += 1
		return newList

	# *
	# * reads pocs to consider form properties file and checks whether it should be considered or not; this applies to
	# * preterminal pocs only
	# *
	# * @param preterminalLabelValue
	# * @return
	#
	def startsWithTagsToConsider(self, preterminalLabelValue):
		consider = False
		# InputStream is = this.getClass().getResourceAsStream("/Service.properties");
		# Properties ps = new Properties();
		# try {
		# ps.load(is);
		# } catch(IOException e1) {
		# // TODO Auto-generated catch block
		# e1.printStackTrace();
		# }
		# String preterminalPOCs = new String(ps.getProperty("preterminalPOCs"));
		tagsToConsider = preterminalPOCs.split(",")
		indexus = 0
		while indexus < tagsToConsider.length():
			tag = tagsToConsider[indexus]
			if preterminalLabelValue.startsWith(tag):
				consider = True
				break
			indexus += 1
		return consider

	# *
	# * this method finds the head of the phrase
	# *
	# * @param tree
	# * @return
	#
	def findTheHeadOfTheNounPhrase(self, tree):
		toReturn = None
		if tree != None:
			hf = ModCollinsHeadFinder()
			head = tree.headTerminal(hf)
			if head.label().value() != None and not (head.label().value().startsWith("PRP")):
				toReturn = head
		return toReturn

	# System.out.println("the head is:" + head.toString());
	# *
	# * this method finds the head of the phrase
	# *
	# * @param tree
	# * @return
	#
	def findModifiersOfTheNounPhrase(self, tree, head):
		if tree == None or head == None:
			return None
		hf = ModCollinsHeadFinder()
		# Tree head = tree.headTerminal(hf);
		toReturn = ArrayList[TreeGraphNode]()
		tlp = PennTreebankLanguagePack()
		gsf = tlp.grammaticalStructureFactory()
		gs = gsf.newGrammaticalStructure(tree)
		#Collection tdl = gs.typedDependenciesCollapsed();
		tdl = gs.typedDependenciesCCprocessed()
		it = tdl.iterator()
		while it.hasNext():
			td = it.next()
			depName = td.reln().getShortName()
			if (depName.equals("amod") or depName.equals("dep") or depName.equals("advmod")) and td.gov().value() == head.value():
				toReturn.add(td.dep())
		tp = TreePrint("penn,typedDependenciesCollapsed")
		#tp.printTree(head);
		return toReturn

	# System.out.println("the head is:" + head.toString());
	# *
	# * generates a nice string from the tree
	# *
	# * @param firstNPorNN
	# * @return
	#
	def getNiceString(self, trees):
		niceString = ""
		indexus = 0
		while indexus < trees.length():
			tree = trees[indexus]
			indexus = 0
			while indexus < tree.getLeaves().length():
				leaf = tree.getLeaves()[indexus]
				if leaf.isLeaf():
					niceString = niceString + " " + leaf.value()
				else:
					leafs = ArrayList[Tree]()
					leafs.add(leaf)
					niceString = niceString + " " + self.getNiceString(leafs)
				indexus += 1
			indexus += 1
		return niceString.trim()

	# *
	# * returns the distance from one node to the other.
	# *
	# * @param tree1
	# * @param tree2
	# * @return
	#
	def getDistance(self, tree1List, tree2List, root):
		tree1 = None
		tree2 = None
		if tree1List != None and tree1List.size() > 0:
			tree1 = tree1List.get(0)
		if tree2List != None and tree2List.size() > 0:
			tree2 = tree2List.get(0)
		nodes = root.pathNodeToNode(tree1, tree2)
		if tree1 != None and tree2 != None and nodes != None:
			logger.debug("Distance btw" + tree1.toString() + "and " + tree2.toString() + " is:" + nodes.size())
		else:
			logger.debug("Distance btw tree1:" + tree1 + "and tree2 " + tree2 + " is:" + nodes)
		nodeSize = 0
		if nodes != None:
			nodeSize = nodes.size()
		return nodeSize

	# *
	# * get closest oc to the given poc
	# *
	# * @param poc
	# * @param ocs
	# * @param root
	# * @return
	#
	def getClosestOc(self, poc, ocs, root):
		min = 0
		indexus = 0
		while indexus < ocs.length():
			oc = ocs[indexus]
			dist = self.getDistance(poc, oc, root)
			if dist < min:
				min = dist
			indexus += 1
		return min
