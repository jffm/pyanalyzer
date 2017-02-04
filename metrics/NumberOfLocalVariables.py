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

class CountDeclaredVariables(Visitor):
    result = 0
    def __init__(self, parameters):
        self.parameters = parameters
    def visitAssName(self, node, *args):
        if node.name not in self.parameters:
            self.result += 1

class NumberOfLocalVariables(Metric):
    """Number of local variables used in a (Function)
    
    Count the number of variables declared inside the body of a function
    such variables are simply assignments to names not present in the
    parameters list of the function
    """
    def visitFunction(self, node, *args):
        node.NumberOfLocalVariables = compiler.walk(node, CountDeclaredVariables(node.argnames)).result
