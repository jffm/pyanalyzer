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

"""This module implements a Rule
"""

import sys
import compiler
from core.metric import Metric
from core.writer.sqlwriter import SqlWriter
from core.writer.textwriter import TextWriter

class Rule(Metric):
    """A Rule is a Metric that is directly printed to stderr
    """
    class config:
        severity = None
        code = 0
        message = None
    def __init__(self, writer):
        self.writer = writer
        self.row = dict(
            (key,value)
            for (key,value) in self.config.__dict__.items()
            if not key.startswith("__"))
        self.row.update(
            code="%s%04d" % (self.config.severity[0].upper(), self.config.code),
            message=self.__doc__.split("\n")[0]
        )
    def report(self, node, mapping):
        self.row.update(
            kind=node.__class__.__name__,
            filename=self.filename,
            name=getattr(node, "name", ""),
            lineno=node.lineno,
            message=self.row["message"] % mapping)
        self.writer.writerow(self.row)
    def visitModule(self, node, *args):
        self.filename = node.filename
        self.default(node, *args)
