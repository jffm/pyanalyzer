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

"""Implements a MetricsComputer
"""

import sys

import compiler
import operator

from core.utils import extract
from core.visitor import Visitor

def get_metric(name, cache={}):
    try:
        return cache[name]
    except KeyError:
        cache[name] = getattr(
            __import__("metrics.%s" % name, globals(), locals(), name),
            name
        )
        return cache[name]

def ordered(dependencies):
    """return an ordered sequence of the items in the dependencies
    
    @param dependencies: dictionary with the dependencies
        { 'item': ('depends on other item', ...) }
    """
    res = {}
    names = {}
    order = 0
    seq = dependencies.copy()
    # set order=0 to elements that have no dependencies
    for (m, reqs) in seq.items():
        if not len(reqs):
            res[m] = order
            names[m.__name__] = order
            del seq[m]
    done = (len(seq) == 0)
    # increment order
    while not done:
        order += 1
        changes = 0
        # set order for elements for wich all their
        # dependencies have received their order
        for (m, reqs) in seq.items():
            max_order = max(names.get(req, order) for req in reqs)
            if max_order < order:
                res[m] = order
                names[m.__name__] = order
                changes += 1
                del seq[m]
        done = (changes == 0)
    if len(seq):
        # if the sequence is not empty, the remaining
        # items have cycles in their dependencies
        return False, seq
    else:
        # otherwise, we return the items sorted by their order
        return True, sorted(res.items(), key=operator.itemgetter(1))
        
class MetricsComputer(Visitor):
    def __init__(self, options):
        options.log.info("Extracting metrics to compute...")
        # Order the list of metrics to compute
        metrics = [
            get_metric(metric)
            for metric in extract(options.metrics, ",")
        ]
        options.log.info("Checking that no cyclic dependencies exist...")
        dependencies = dict(
            (metric, tuple(metric.requires))
            for metric in metrics
        )
        nocycle, seq = ordered(dependencies)
        if nocycle:
            self.metrics = metrics_to_compute = []
            for (metric, order) in seq:
                if metric.resolve:
                    metric.execute = options.resolve
                if metric.execute:
                    metrics_to_compute.append(metric)
        else:
            fatal = (
                "Cannot compute metrics, cyclic dependencies between: %s"
                % seq
            )
            options.log.fatal(fatal)
            sys.exit(fatal)
        self.log = options.log
    def visitProject(self, node, *args):
        for metric in self.metrics:
            self.log.debug(
                "    Computing metric %s" % metric.__name__
            )
            compiler.walk(node, metric(node))
