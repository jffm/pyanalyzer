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

import compiler

from core.visitor import Visitor
from core.metric import Metric

class LinesOfCodeCounter(Visitor):
    result = 0
    lineno = -1
    def default(self, node, *args):
        for child in node.getChildNodes():
            self.visitNode(child)
    def visitNode(self, node, *args):
        if node.lineno and self.lineno < node.lineno:
            self.result += 1
            self.lineno = node.lineno
        self.default(node)
    def visitPass(self, node, *args):
        pass
    visitProject = visitModule = visitClass = visitFunction = visitNode
    

class NumberOfLinesOfCode(Metric):
    """Number of non commenting lines of code of a (Module, Class, Function, Project)
    
    Count all lines from declaration line to last line
    excluding blank lines and comment lines
    """
    def countLinesOfCode(self, node, *args):
        node.NumberOfLinesOfCode = compiler.walk(node, LinesOfCodeCounter()).result
    visitFunction = countLinesOfCode
    def visitProject(self, node, *args):
        self.countLinesOfCode(node)
        self.default(node)
    visitClass = visitModule = visitProject
