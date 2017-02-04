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

"""This module provides the Visitor class for computing metrics and checking rules
"""

import compiler

from core.visitor import Visitor

class Metric(Visitor):
    """A Metric computes its result during the walk. This result is then printed to stdout.
    usage: result = compiler.walk(ast, Metric()).result
        @field requires: the list of metrics that should be computed before this metric
        @field result: the result of the run of this metric
    """
    requires = () # contains the list of metric names that should be computed before this metric
    result = None # contains the result of the metric if needed
    report = True # if the metric should not be reported, it should be set to False
    resolve = False # if the metric requires name reolving, it should be set to True
    execute = True # if the metric should not be executed, it should be set to False
    def __init__(self, node):
        pass
        # Don't compute this metric if it has already been computed
        # value = getattr(node, self.__class__.__name__, None)
        # if value is not None:
            # return
        # Test if the computation of this metric needs additional metrics
        # for required in self.requires:
            # if getattr(node, required, None) is None:
                # metric = getattr(
                    # __import__("metrics.%s" % required, globals(), locals(), required), 
                    # required
                # )
                # compiler.walk(node, metric(node))
