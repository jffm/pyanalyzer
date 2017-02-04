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

import compiler.ast

from core.metric import Metric
from core.visitor import Visitor

class FieldAccessesGetter(Visitor):
    result = None
    def __init__(self):
        self.result = []
        Visitor.__init__(self)
    def visitGetattr(self, node, *args):
        if isinstance(node.expr, compiler.ast.Name):
            self.result.append(".".join([node.expr.name, node.attrname]))
        self.default(node, *args)

class AccessToForeignData(Metric):
    report = False
    def visitClass(self, node, *args):
        node.AccessToForeignData = set(
            field
            for field in compiler.walk(node, FieldAccessesGetter()).result
                if not field.startswith("self")
        )
    visitFunction = visitClass