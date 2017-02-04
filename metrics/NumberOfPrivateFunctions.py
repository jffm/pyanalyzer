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

class PrivateFunctionsCounter(Visitor):
    result = 0
    def visitFunction(self, node, *args):
        if node.name.startswith("_"):
            self.result += 1

class NumberOfPrivateFunctions(Metric):
    """Number of private functions of a (Project, Module, Class)
    
    There is no real private method in Python. The convention is that a method
    starting with '_' is private.
    
    - If the method name starts with a single '_', it is still accessible 
      outside the defining class.
      
    - If the method name starts with two '_', it is not accessible outside the 
      defining class. If, at the same time, the method name ends with two '_'
      this should only be for Python's special functions like:
        __init__, __call__, __getitem__, __setitem__, __iter__, ...
    """
    def countFunctions(self, node, *args):
        node.NumberOfPrivateFunctions = compiler.walk(node, PrivateFunctionsCounter()).result
    def visitProject(self, node, *args):
        self.countFunctions(node, *args)
        self.default(node, *args)
    visitModule = visitClass = visitProject
