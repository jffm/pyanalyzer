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

from core.visitor import Visitor
from core.metric import Metric

class CountMaximumNestedLevel(Visitor):
    result = 0
    def __init__(self, function):
        self.function = function
        self.levels = []
    def visitFunction(self, node, *args):
        if ((node == self.function)
            and (len(node.code.nodes) == 1)
            and isinstance(node.code.nodes[0], compiler.ast.Pass)):
            self.result = -1 # abstract method
        elif (node == self.function):
            self.default(node, 0)
        #self.default(node, 0)
    # def visitTryExcept(self, node, *args):
        # level = args[0]
        # for child in node.getChildNodes():
            # level = self.visit(node, level+1)
            # if level > self.result:
                # self.result = level
        # return level
    def countMaximumLevel(self, node, *args):
        level = args[0]
        if level > self.result:
            self.result = level
        self.default(node, level+1)
    visitIf = visitFor = visitWhile = visitTryFinally = visitTryExcept = visitListCompFor = visitListCompIf = countMaximumLevel

class MaximumNestedLevel(Metric):
    """McCabe cyclomatic complexity of a (Function)
    """
    def visitFunction(self, node, *args):
        node.MaximumNestedLevel = compiler.walk(node, CountMaximumNestedLevel(node)).result + 1
        self.default(node)