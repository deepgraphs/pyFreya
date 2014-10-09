class MainSubject(object):
	# def __init__(self):
        #    pass

    #    Annotation annotation = new Annotation();
	#	List<Tree> tree;
	#
	#	public List<Tree> getTree() {
	#		return tree;
	#	}
	#
	#	public void setTree(List<Tree> tree) {
	#		this.tree = tree;
	#	}
	#
	#	public Annotation getAnnotation() {
	#		return annotation;
	#	}
	#
	#	public void setAnnotation(Annotation annotation) {
	#		this.annotation = annotation;
	#	}
	# 
	# * defines the priority for the main subject: for example, if we want to
	# * give priority to the main subject wrt the ontology concepts e.g. in cases
	# * of 'how long' when long is a mountain
	# 
	def getPriority(self):
		return self._priority

	def setPriority(self, priority):
		self._priority = priority