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

class HalsteadBugs(Metric):
    """Halstead estimated number of errors for a (Project, Module, Function)
    
    The number of delivered bugs (B) correlates with the overall complexity
    of the software. Halstead gives the following formula for B:
        B = ( E ** (2/3) ) / 3000         ** stands for "to the exponent"

    Halstead's delivered bugs (B) is an estimate for the number of errors
    in the implementation.
    Delivered bugs in a file should be less than 2. Experiences have shown
    that, when programming with C or C++, a source file almost always contains
    more errors than B suggests.
    The number of defects tends to grow more rapidly than B.

    When dynamic testing is concerned, the most important Halstead metric is
    the number of delivered bugs. The number of delivered bugs approximates the
    number of errors in a module. As a goal at least that many errors should be
    found from the module in its testing. 
    
    source: http://www.verifysoft.com/en_halstead_metrics.html
    """
    requires = ('HalsteadEffort',)
    def countHalsteadBugs(self, node, *args):
        node.HalsteadBugs = (node.HalsteadEffort ** (2.0/3)) / 3000
    visitFunction = countHalsteadBugs
    def visitProject(self, node, *args):
        self.countHalsteadBugs(node)
        self.default(node)
    visitModule = visitProject
