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

import os
import sys
import compiler
import csv

from core.utils import extract
from core.writer.textwriter import TextWriter
from core.writer.sqlwriter import SqlWriter
from core.writer.csvwriter import CsvWriter

class RulesReporter(object):
    """This class reports the result of the rules.
    
    It can export the result to various formats: text, sql or csv
    @see TextWriter
    @see SqlWriter
    @see CsvWriter
    """
    def __init__(self, options):
        """Creates a RulesReporter instance based on the provided @options
        
        @param options.rules_to_file - if False, output will be stderr
            if True, output to a predefined file located at
            <options.output>/<options.name>_metrics.<options.rules_format>
        @param options.name - name of the project
        @param options.output - directory where to output the file
        @param options.rules_format - format for the output ('csv', 'txt' or 'sql')
        """
        
        if options.rules_to_file: # output to a file
            # check that output directory exists
            if not os.path.isdir(options.output):
                os.makedirs(options.output)
            # open the file for writing
            output = open(
                os.path.join(
                    options.output,
                    "%s_rules.%s" % (options.name, options.rules_format)
                ),
                "wb"
            )
        else: # output to standard error
            output = sys.stderr
            
        fields = (
            ("filename", str),
            ("lineno", int),
            ("severity", str),
            ("code", str),
            ("kind", str),
            ("name", str),
            ("message", str)
        )
        format = options.rules_format
        if format == "csv":
            self.writer = CsvWriter(output, fields)
        elif format == "sql":
            self.writer = SqlWriter(output, fields, "rules")
        else: # options.format_rule == "text":
            template = "%(filename)s:%(lineno)s: [%(code)s, %(kind)s %(name)s] - %(message)s\n"
            self.writer = TextWriter(output, fields, template)
        self.rules = [
            getattr(
                __import__("rules.%s" % rule, globals(), locals(), rule),
                rule
            )
            for rule in extract(options.rules, ",")
        ]
        self.log = options.log
    def report(self, node):
        """Report all rules that were violated
        """
        self.log.info("Reporting violated rules...")
        walk = compiler.walk
        writer = self.writer
        for rule in self.rules:
            walk(node, rule(writer))