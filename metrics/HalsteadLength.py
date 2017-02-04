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

from core.metric import Metric

class HalsteadLength(Metric):
    """Halstead Lenght of a (Project, Module, Function)
    
    The program length (N) is the sum of the total number of operators
    and operands in the module or function: 
        N = N1 + N2
    
    source: http://www.verifysoft.com/en_halstead_metrics.html
    """
    requires = ('HalsteadMeasures',)
    def countHalsteadLength(self, node, *args):
        n1, n2, N1, N2 = node.HalsteadMeasures
        node.HalsteadLength = N1 + N2
    visitFunction = countHalsteadLength
    def visitProject(self, node, *args):
        self.countHalsteadLength(node)
        self.default(node)
    visitModule = visitProject
