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
from math import sin, sqrt

from core.metric import Metric

class MaintainabilityIndexCommentWeight(Metric):
    """Maintainability index comment weight of a (Project, Module, Function)
    
        MIcw = 50 * sin(sqrt(2.4 * perCM))
        where:
            perCM = average percent of lines of comments per module
    
    source: http://www.verifysoft.com/en_maintainability.html
    """
    requires = ('RatioCommentToCode',)
    def countMaintainabilityIndexCommentWeight(self, node, *args):
        perCM = node.RatioCommentToCode
        node.MaintainabilityIndexCommentWeight = 50 * sin(sqrt(2.4 * perCM))
    visitFunction = countMaintainabilityIndexCommentWeight
    def visitProject(self, node, *args):
        self.countMaintainabilityIndexCommentWeight(node, *args)
        self.default(node, *args)
    visitModule = visitProject
