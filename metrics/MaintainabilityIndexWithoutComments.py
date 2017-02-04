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
from math import log

from core.metric import Metric

class Container:
    functions = 0
    loc = 0
    v = 0
    g = 0

class MaintainabilityIndexWithoutComments(Metric):
    """Maintainability index without comments for a (Project, Module, Function)
    
        MIwoc = 171 - 5.2 * ln(aveV) -0.23 * aveG -16.2 * ln(aveLOC) 
        
        where:
            aveV = average Halstead Volume per module
            aveG = average extended cyclomatic complexity per module
            aveLOC = average count of (physical) lines per module
            
    source: http://www.verifysoft.com/en_maintainability.html
    """
    requires = ('HalsteadVolume', 'CyclomaticComplexity', 'NumberOfLinesOfCode')
    def visitProject(self, node, *args):
        this = Container()
        self.default(node, this)
        functions = this.functions
        if functions:
            aveG = this.g/functions
            aveV = this.v/functions
            aveLOC = this.loc/functions
        else:
            aveV = aveLOC = 1
            aveG = 0
        node.MaintainabilityIndexWithoutComments = 171 - 5.2 * log(aveV or 1) - 0.23 * aveG - 16.2 * log(aveLOC or 1)
    def visitModule(self, node, *args):
        this = Container()
        self.default(node.node, this)
        functions = this.functions
        if functions:
            aveG = this.g/functions
            aveV = this.v/functions
            aveLOC = this.loc/functions
        else:
            aveV = aveLOC = 1
            aveG = 0
        if args:
            project, = args
            project.g += this.g
            project.v += this.v
            project.loc += this.loc
            project.functions += functions
        node.MaintainabilityIndexWithoutComments = 171 - 5.2 * log(aveV or 1) - 0.23 * aveG - 16.2 * log(aveLOC or 1)

    def visitFunction(self, node, *args):
        loc = node.NumberOfLinesOfCode
        v = node.HalsteadVolume
        g = node.CyclomaticComplexity
        if args:
            module, = args
            module.g += g
            module.v += v
            module.loc += loc
            module.functions += 1
        node.MaintainabilityIndexWithoutComments = 171 - 5.2 * log(v or 1) - 0.23 * g - 16.2 * log(loc or 1)
