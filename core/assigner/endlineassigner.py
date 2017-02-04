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

"""This module provides the EndlineAssigner helper class
"""

from bisect import bisect

from core.visitor import Visitor
from core.extractor.codeelementsextractor import CodeElementsExtractor

__all__ = ["EndlineAssigner"]

class EndlineAssigner(Visitor):
    """Assign the start and end lines of code elements (Module, Class, Function)
    """
    def __init__(self, filename, common_prefix_length):
        """Create the visitor with the given code elements
        """
        self.filename = filename
        self.relname = filename[common_prefix_length:]
        code_elements, self.blanklines = CodeElementsExtractor(filename).extract()
        self.boundaries = dict((e.startline, e.endline) for e in code_elements)
        
    def assignBlanklines(self, node, *args):
        """Get the name and lineno of this function
        """
        bk = self.blanklines
        start = bisect(bk, node.lineno) # where to start searching for blank lines
        end = bisect(bk, node.endline)  # where to end searching for blank lines
        node.blanklines = bk[start:end] # blank lines inside the code element boundaries
        self.blanklines = bk[0:start] + bk[end:] # remove assigned ones
        
    def visitModule(self, node, *args):
        """Assign endline and blank lines to the node Module
        """
        node.lineno = 0
        node.name = ""
        node.endline = self.boundaries[0]
        node.filename = self.filename
        node.relname = self.relname
        self.default(node, *args)
        self.assignBlanklines(node, *args)
        
    def visitClass(self, node, *args):
        """Assign endline and blank lines to the node
        """
        node.filename = self.filename
        node.relname = self.relname
        node.endline = self.boundaries[node.lineno]
        self.default(node, *args)
        self.assignBlanklines(node, *args)
        
    visitFunction = visitClass
