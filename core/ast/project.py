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

"""This module implements a Project
"""

from compiler.ast import Node, flatten, flatten_nodes

class Project(Node):
    def __init__(self, path, name, nodes, lineno=0):
        self.name = name
        self.filename = path
        self.relname = path
        self.lineno = lineno
        self.nodes = nodes
    
    def getChildren(self):
        return tuple(flatten(self.nodes))

    def getChildNodes(self):
        nodelist = []
        nodelist.extend(flatten_nodes(self.nodes))
        return tuple(nodelist)
        
    def __repr__(self):
        return "Project(%s, %s)" % (self.name, repr(self.nodes))