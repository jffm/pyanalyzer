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
from core.utils import log2

class HalsteadVolume(Metric):
    """Halstead Volume of a (Project, Module, Function)
    
    The program volume (V) is the information contents of the module/function,
    measured in mathematical bits. It is calculated as the program length times
    the 2-base logarithm of the vocabulary size (n):
        V = N * log2(n)

    Halstead's volume (V) describes the size of the implementation 
    of an algorithm. The computation of V is based on the number of operations
    performed and operands handled in the algorithm. Therefore V is less 
    sensitive to code layout than the lines-of-code measures.

    The volume of a function should be at least 20 and at most 1000. 
    The volume of a parameterless one-line function that is not empty
    is about 20. A volume greater than 1000 tells that the function probably
    does too many things.

    The volume of a file should be at least 100 and at most 8000.
    These limits are based on volumes measured for files whose 
    NumberOfLinesOfCode and CyclomaticComplexity are near their
    recommended limits. The limits of volume can be used for double-checking.
    
    source: http://www.verifysoft.com/en_halstead_metrics.html
    """
    requires = ('HalsteadLength','HalsteadVocabulary')
    def countHalsteadVolume(self, node, *args):
        node.HalsteadVolume = node.HalsteadLength * log2(node.HalsteadVocabulary)
    visitFunction = countHalsteadVolume
    def visitProject(self, node, *args):
        self.countHalsteadVolume(node)
        self.default(node)
    visitModule = visitProject
    
