# Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS
# 
# This file is part of PyAnalyzer.
#
# PyAnalyzer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# or see <http://www.opensource.org/licenses/gpl-3.0.html>
# 
# Contact:
#     Junior FLEURIAL MONFILS <frederic dot fleurialmonfils at cetic dot be>

__author__ = "Frederic F. MONFILS"
__version__ = "$Revision: $".split()[1]
__revision__ = __version__
# $Source: $
__date__ = "$Date: $"
__copyright__ = "Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS"
__license__ = "GPLv3"
__contact__ = "ffm at cetic.be"

import compiler.ast

from core.metric import Metric
from core.visitor import Visitor

class CountDecisionNodes(Visitor):
    result = 0
    def __init__(self, function):
        self.function = function
    def visitFunction(self, node, *args):
        if ((node == self.function)
            and (len(node.code.nodes) == 1)
            and isinstance(node.code.nodes[0], compiler.ast.Pass)):
            self.result = -1 # abstract method
        self.default(node, *args)
    def visitTryExcept(self, node, *args):
        if self.result == -1: self.result = 0
        self.result += len(node.handlers)
        self.default(node, *args)
    def countDecisionNode(self, node, *args):
        if self.result == -1: self.result = 0
        self.result += 1
        self.default(node, *args)
    def visitIf(self, node, *args):
        #
        # The if statement is more complicated because it can include
        #   several tests.
        # if_stmt: 
        #     'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
        # 
        # The If node only defines two attributes: tests and else_. 
        # The tests attribute is a sequence of test expression, 
        #   consequent body pairs.
        # 
        # There is one pair for each if/elif clause.
        # The first element of the pair is the test expression. 
        # The second elements is a Stmt node that contains the code to execute
        #   if the test is true.

        # The getChildren() method of If returns a flat list of child nodes.
        # If there are three if/elif clauses and no else clause, then 
        #   getChildren() will return a list of six elements: the first test 
        #   expression, the first Stmt, the second text expression, etc.

        # only add len(tests)-1 to compensate the +1 in countDecisionNode
        self.result += (len(node.tests)-1)
        self.countDecisionNode(node, *args)
    visitAnd = visitOr = visitFor = visitWhile = \
        visitTryFinally = visitListCompFor = visitListCompIf = countDecisionNode

class CyclomaticComplexity(Metric):
    """McCabe cyclomatic complexity of a (Function)
    
    Count the number of: If, And, Or, For, While, Finally, Except
        if test, [(x for x in list) if test]
        a and b
        a or b
        for a in list, [x for x in list]
        while test
        (try: ...) finally:
        (try: ...) except Exception:
    """
    def visitFunction(self, node, *args):
        node.CyclomaticComplexity = compiler.walk(node, CountDecisionNodes(node)).result + 1
        self.default(node)
    visitClass = visitModule = visitProject = visitFunction