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

class CountMethodWeights(Visitor):
    result = 0
    def visitFunction(self, node, *args):
        self.result += node.CyclomaticComplexity

class WeightedMethodsPerClass(Metric):
    """Weighted Methods per (Class)
    
    Also known as: WMC
    
    Description:
    The sum of the statical weight of all methods of a class. Here, the
    CyclomaticComplexity is used to quantify the method's weight.
    
        WeightedMethodsPerClass(Class) :=
            Sum(CyclomaticComplexity(Method) forall Method in Class)
    
    Sources:
    CK94. Shyam R. Chidamber and Chris F. Kemerer. A metrics suite for object 
          oriented design. IEEE Transactions on Software Engineering, June 1994
    McC76. T.J. McCabe. A measure of complexity. IEEE Transaction on Software
           Engineering, December 1976
    LM06 Michele Lanza and Radu Marinescu. Object-Oriented Metrics in Practice,
         Springer Verlag, 2006.
    """
    requires = ('CyclomaticComplexity',)
    def visitClass(self, node, *args):
        node.WeightedMethodsPerClass = compiler.walk(node, CountMethodWeights()).result
