__author__ = 'root'
#
# * Licensed to the Apache Software Foundation (ASF) under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The ASF licenses this file to You under the Apache License, Version 2.0
# * (the "License"); you may not use this file except in compliance with
# * the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
#
# * A clause in a BooleanQuery.
from freya.util.pyJavaSmooth import isset

class BooleanClause(object):
	# * Specifies how clauses are to occur in matching documents.
	#public static enum Occur {
	# * Use this operator for clauses that <i>must</i> appear in the matching documents.
	# MUST     { @Override public String toString() { return "+"; } },
	# * Use this operator for clauses that <i>should</i> appear in the
	# * matching documents. For a BooleanQuery with no <code>MUST</code>
	# * clauses one or more <code>SHOULD</code> clauses must match a document
	# * for the BooleanQuery to match.
	# * @see BooleanQuery#setMinimumNumberShouldMatch
	#
	#  SHOULD   { @Override public String toString() { return "";  } },
	# * Use this operator for clauses that <i>must not</i> appear in the matching documents.
	# * Note that it is not possible to search for queries that only consist
	# * of a <code>MUST_NOT</code> clause.
	#   MUST_NOT { @Override public String toString() { return "-"; } };
	# }
	# * The query whose matching documents are combined by the boolean query.
	#
	# * Constructs a BooleanClause.
	#
    class Occur(object):
        MUST = "+"
        SHOULD = ""
        MUST_NOT = "-"
	def __init__(self, query, occur):
		# self._query = query  Implements clonable?...
		self._occur = self.Occur()

	def getOccur(self):
		return self._occur

	def setOccur(self, occur):
		self._occur = occur

	def getQuery(self):
		return self._query

	def setQuery(self, query):
		self._query = query

	def isProhibited(self):
		return self._occur.MUST_NOT == self._occur

	def isRequired(self):
		return self._occur.MUST == self._occur

	# * Returns true if <code>o</code> is equal to this.
	def equals(self, o):
		if not isset(o) or not (o):
			return False
		return self._query.equals(o.query) and self._occur == o.occur

	# * Returns a hash code value for this object.
	def hashCode(self):
		return self._query.hashCode() ^ (1 if self._occur.MUST == self._occur else 0) ^ (2 if self._occur.MUST_NOT == self._occur else 0)

	def toString(self):
		return self._occur.toString() + self._query.toString()