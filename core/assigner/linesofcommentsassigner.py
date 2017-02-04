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

"""This modules implements a LinesOfCommentsAssigner
"""

import os

from bisect import bisect

from core.extractor.linesofcommentsextractor import LinesOfCommentsExtractor

__all__ = ["LinesOfCommentsAssigner"]

class LinesOfCommentsAssigner(object):
    """Assign the lines of comments to the code elements Function and Class
    """
    
    def __init__(self, filename):
        self.lines_of_comments = LinesOfCommentsExtractor(filename).extract()
        self.filename = os.path.realpath(filename)

    def default(self, node, *args):
        for child in node.getChildNodes():
            self.visit(child, *args)
            
    def visitModule(self, node, *args):
        node.lineno = 0
        node.name = ""
        self.assignComments(node, *args)
        
    def assignComments(self, node, *args):
        """Get the name and lineno of this function
        """
        self.default(node, *args)
        loc = self.lines_of_comments
        start = bisect(loc, node.lineno) # where to start searching for comment
        end = bisect(loc, node.endline)  # where to end searching for comment
        node.comments = loc[start:end] # comments inside the code element boundaries
        self.lines_of_comments = loc[0:start] + loc[end:] # remove assigned ones
        
    visitFunction = visitClass = assignComments
