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

class InternalFieldAccessesGetter(Visitor):
    """Getter used to get the list of field accesses of a (Class)
    not recording the field accesses to inner/local classes
    """
    def __init__(self, node, methods):
        self.methods = methods
        self.result = {}
        self.stack = [node]
        self.iscall = False # used for called methods
    def visitFunction(self, node, *args):
        parent = self.stack[-1]
        if not isinstance(parent, compiler.ast.Function):
            # only push methods
            self.stack.append(node)
            self.default(node)
            _method = self.stack.pop()
        else:
            self.default(node)
    def visitClass(self, node, *args):
        pass # dont go further to classes
    def visitAssAttr(self, node, *args):
        if isinstance(node.expr, compiler.ast.Name):
            method = self.stack[-1] # Get the parent method
            if node.expr.name == "self":
                if node.attrname not in [m.name for m in self.methods]:
                    try:
                        self.result[node.attrname].add(method)
                    except KeyError:
                        self.result[node.attrname] = set([method])
        self.default(node)
    def visitCallFunc(self, node, *args):
        if (isinstance(node.node, compiler.ast.Getattr)
            and isinstance(node.node.expr, compiler.ast.Name)
            and node.node.expr.name == "self"):
            self.iscall = True
        self.default(node)
        self.iscall = False
    def visitGetattr(self, node, *args):
        if isinstance(node.expr, compiler.ast.Name) and self.iscall:
            # Getattr for a name from a CallFunc --> method call
            self.iscall = False
        elif isinstance(node.expr, compiler.ast.Name):
            method = self.stack[-1] # Get the parent method
            if node.expr.name == "self":
                if node.attrname not in [m.name for m in self.methods]:
                    try:
                        self.result[node.attrname].add(method)
                    except KeyError:
                        self.result[node.attrname] = set([method])
        self.default(node)
        
class InternalFieldAccesses(Metric):
    report = False
    requires = ('Methods',)
    def visitClass(self, node, *args):
        methods = node.Methods
        node.InternalFieldAccesses = compiler.walk(node.code, InternalFieldAccessesGetter(node, methods)).result
        