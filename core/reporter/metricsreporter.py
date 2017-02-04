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

"""MetricsReporter reports the metrics to a file with the provided format
"""

__author__ = "Frederic F. MONFILS"
__version__ = "$Revision: $".split()[1]
__revision__ = __version__
# $Source: $
__date__ = "$Date: $"
__copyright__ = "Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS"
__license__ = "GPLv3"
__contact__ = "ffm at cetic.be"

import os
import sys

import csv
import compiler

from core.utils import extract
from core.visitor import Visitor
from core.writer.sqlwriter import SqlWriter
from core.writer.csvwriter import CsvWriter

class MetricsReporter(Visitor):
    """This class is used to report the list of code elements and their metrics
    It uses the following options defined at command line
        - metrics-format: export format (csv, xml, text)
        - metrics-to-file
        - output: directory where to create the file with the exported content
    """
    def __init__(self, options):
        self.format = options.metrics_format
        if options.metrics_to_file:
            if not os.path.isdir(options.output):
                os.makedirs(options.output)
            try:
                self.output = open(
                    os.path.join(
                        options.output,
                        "%s_metrics.%s" % (options.name, options.metrics_format)
                    ),
                    "wb"
                )
            except IOError, e:
                options.log.error(e)
                sys.exit("Please check that this file is not already in use")
        else:
            self.output = sys.stdout
        metrics = self.metrics = []
        # only report metrics that were declared as 'reportable'
        # when defining the metric, the field report should be set to True
        for metric in extract(options.metrics, ","):
            metric_computer = getattr(
                __import__("metrics.%s" % metric, globals(), locals(), metric),
                metric
            )
            if metric_computer.report and metric_computer.execute:
                metrics.append(metric)
        self.fields = ["id", "kind", "name", "file", "start", "end", "lower", "upper", "parent", "childof", "level"] + self.metrics
        self.types = zip(self.fields, [int] + [str]*3 + [int]*6 + [str] + [float]*len(self.metrics))
        self.result = []
        self.log = options.log
    def visitProject(self, node, *args):
        self.log.info("Collecting metrics...")
        fields = self.fields
        if self.format == "sql":
            self.log.info("Writing SQL queries...")
            writer = SqlWriter(self.output, self.types, "metrics")
        else: # self.format == "csv"
            self.log.info("Writing CSV rows...")
            writer = CsvWriter(self.output, self.types)
        # Report metrics for the project
        self.reportNode(node, *args)
        # Report metrics for the rest of the AST
        self.default(node, *args)
        # Write the metrics to the desired output stream
        writer.writerows([dict(zip(self.fields, row)) for row in self.result])
    def reportNode(self, node, *args):
        if not args:
            parent_id = childof = None
        else:
            parent, = args
            parent_id = parent.index
            childof = parent.__class__.__name__
        row = [node.index, node.__class__.__name__, node.name, node.relname, node.lineno, node.endline, node.lower, node.upper, parent_id, childof, node.level]
        row.extend(getattr(node, metric, None) for metric in self.metrics)
        self.result.append(row)
    # visitFunction = reportNode
    def visitModule(self, node, *args):
        self.reportNode(node, *args)
        self.default(node, node)
    visitClass = visitFunction = visitModule