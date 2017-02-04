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

from core.visitor import Visitor
from core.metric import Metric

class CountAndOr(Visitor):
    result = 0
    def visitAnd(self, node, *args):
        self.result += 1
        self.default(node, *args)
    visitOr = visitAnd

def bool_comp(node, *args):
    if node is None:
        return 0
    return compiler.walk(node, CountAndOr()).result

class CountPath(Visitor):
    
    result = 0
    infunction = False
    
    def __init__(self, function):
        self.function = function
        
    def prod(self, node, *args):
        npath = args[0]
        for child in node.getChildNodes():
            r = self.visit(child, *args) or 1 # visit will be stored by compiler.walk
            npath *= r
        return npath

    # def sum(self, node, *args):
        # npath = args[0]
        # for child in node.getChildNodes():
            # r = self.dispatch(child, *args) or 0 # visit will be stored by compiler.walk
            # npath += r
        # return npath

    def visitFunction(self, node, *args):
        npath = 1
        if (node == self.function):
            npath = self.prod(node, 1);
            self.result = npath
        return npath

    def visitStmt(self, node, *args):
        return self.prod(node, 1);
        
    # def visitSimpleStmt(self, node, *args):
        # return 1
        
    def visitTryExcept(self, node, *args):
        # try:
        #   <try_range>
        # except Error1:
        #   <except_range>
        # except Error2:
        #   <except_range>
        return (
            self.npath(node.body)
            + sum(
                self.npath(handler)
                for (name, variable, handler) in node.handlers
              )
            + self.npath(node.else_)
        )
        
    def visitTryFinally(self, node, *args):
        return (
            self.npath(node.body)
            + self.npath(node.final)
        )
        
    def visitReturn(self, node, *args):
        return bool_comp(node.value) or 1
        
    # visitAssAttr = visitAssList = visitAssName = visitAssTuple \
             # = visitAssert = visitAssign = visitAugAssign = visitBreak \
             # = visitCallFunc = visitClass = visitContinue = visitDecorators \
             # = visitLeftShift = visitListComp = visitPass = visitPrint \
             # = visitPrintnl = visitRaise = visitRightShift = visitExpression \
             # = visitYield = visitSimpleStmt
    def visitAssAttr(self, node, *args):
        return bool_comp(node.expr)
        
    visitDiscard = visitBackquote = visitExec = visitGetattr = visitInvert = visitAssAttr
    
    def visitAssert(self, node, *args):
        return bool_comp(node.test)
        
    def visitAugAssign(self, node, *args):
        return (
            self.npath(node.node)
            + bool_comp(node.expr)
        )
        
    def visitWhile(self, node, *args):
        return (
            bool_comp(node.test)
            + self.npath(node.body)
            + (node.else_ and self.npath(node.else_) or 1)
        )
        
    def visitDiv(self, node, *expr):
        return (
            bool_comp(node.left)
            + bool_comp(node.right)
        )
    visitFloorDiv = visitLeftShift = visitRightShift = visitDiv
    
    def visitListComp(self, node, *expr):
        return bool_comp(node.expr) + sum(self.npath(f) for f in node.quals)
        
    def visitListCompFor(self, node, *expr):
        # [ expr for assign in list if test ]
        #        --------------------------
        # the npath complexity is BoolComp(list) + NP(ifs)
        #
        # TODO: check this assumption
        return bool_comp(node.list) + sum(self.npath(i) for i in node.ifs)
        
    def visitListCompIf(self, node, *expr):
        # [ expr for assign in list if test ]
        #                           -------
        # the npath complexity is NP(test) + 1
        # we add 1 in the case of test is False
        #
        # TODO: check this assumption
        return bool_comp(node.test) + 1
        
    def npath(self, node, *args):
        if node is None:
            return 1
        npath = 1
        for child in node.getChildNodes():
            r = self.visit(child, *args) or 1
            npath *= r
        return npath
    
    def visitFor(self, node, *args):
        return (
            bool_comp(node.list)
            + self.npath(node.body)
            + self.npath(node.else_)
        )

    def visitIf(self, node, *args):
        
        children = node.getChildren()
        complexity = 0
        
        while children:
            expr, if_range, next = children[:3]
            if next is None:
                # We have here: 
                # if expr: 
                #   if_range
                #
                # NPath(if) = NPath(expr) + NPath(if-range) + 1
                complexity += (
                    bool_comp(expr)
                    + self.npath(if_range)
                    + 1
                )
                break
            elif len(children) > 3:
                # Whe have here: 
                # if expr: 
                #   if_range
                # elif else_range:
                #   elif_range
                #
                # NPath(if-elif) = NPath(expr) + NPath(if_range)
                complexity += (
                    bool_comp(expr)
                    + self.npath(if_range)
                )
                children = children[2:]
            else:
                # Whe have here: 
                # if expr: 
                #   if_range
                # else:
                #   else_range
                #
                # NPath(if-else) = NPath(expr) + NPath(if_range) + NPath(else_range)
                complexity += (
                    bool_comp(expr)
                    + self.npath(if_range)
                    + self.npath(next)
                )
                break
        return complexity

class NumberOfPaths(Metric):
    """Number of acyclic execution paths of a (Function)
    """
    def visitFunction(self, node, *args):
        node.NumberOfPaths = compiler.walk(node, CountPath(node)).result