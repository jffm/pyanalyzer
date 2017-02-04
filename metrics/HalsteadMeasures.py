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

"""
This module computes the Halstead measures

OPERANDS:
Identifiers: Identifier
Literals: Number, String

OPERATORS:
Reserved: and, del, for, is, raise, assert, elif, from, lambda, return, break, else, global, not, try, class, except, if, or, while, continue, exec, import, pass, yield, def, finally, in, print
Punctuation: >>= [] not and or + - * / . , < > >>= |= &= ^ = == () {}
"""

import compiler
import tokenize

from core.metric import Metric

keywords = ('and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'yield')
operands = (tokenize.NAME, tokenize.NUMBER, tokenize.STRING)
operators = (
    tokenize.LPAR,              #  7: (
    tokenize.RPAR,              #  8: )
    tokenize.LSQB,              #  9: [
    tokenize.RSQB,              # 10: ]
    tokenize.COLON,             # 11: :
    tokenize.COMMA,             # 12: ,
    tokenize.SEMI,              # 13: ;
    tokenize.PLUS,              # 14: +
    tokenize.MINUS,             # 15: -
    tokenize.STAR,              # 16: *
    tokenize.SLASH,             # 17: /
    tokenize.VBAR,              # 18: |
    tokenize.AMPER,             # 19: &
    tokenize.LESS,              # 20: <
    tokenize.GREATER,           # 21: >
    tokenize.EQUAL,             # 22: =
    tokenize.DOT,               # 23: .
    tokenize.PERCENT,           # 24: %
    tokenize.BACKQUOTE,         # 25: `
    tokenize.LBRACE,            # 26: {
    tokenize.RBRACE,            # 27: }
    tokenize.EQEQUAL,           # 28: ==
    tokenize.NOTEQUAL,          # 29: !=
    tokenize.LESSEQUAL,         # 30: <=
    tokenize.GREATEREQUAL,      # 31: >=
    tokenize.TILDE,             # 32: ~
    tokenize.CIRCUMFLEX,        # 33: ^
    tokenize.LEFTSHIFT,         # 34: <<
    tokenize.RIGHTSHIFT,        # 35: >>
    tokenize.DOUBLESTAR,        # 36: **
    tokenize.PLUSEQUAL,         # 37: +=
    tokenize.MINEQUAL,          # 38: -=
    tokenize.STAREQUAL,         # 39: *=
    tokenize.SLASHEQUAL,        # 40: /=
    tokenize.PERCENTEQUAL,      # 41: %=
    tokenize.AMPEREQUAL,        # 42: &=
    tokenize.VBAREQUAL,         # 43: |=
    tokenize.CIRCUMFLEXEQUAL,   # 44: ^=
    tokenize.LEFTSHIFTEQUAL,    # 45: <<=
    tokenize.RIGHTSHIFTEQUAL,   # 46: >>=
    tokenize.DOUBLESTAREQUAL,   # 47: **=
    tokenize.DOUBLESLASH,       # 48: //
    tokenize.DOUBLESLASHEQUAL,  # 49: //=
    tokenize.AT,                # 50: @
    tokenize.OP,                # 51: punctuation
)

class Container(object):
    def __init__(self):
        self.n1 = {}
        self.n2 = {}
        self.N1 = 0
        self.N2 = 0


class HalsteadMeasures(Metric):
    """Halstead measures of a (Module)
    
    These metrics are based on interpreting the source code as a sequence
    of tokens and classifying each token to be an operator or an operand.

    Then is counted:
        * number of unique (distinct) operators (n1)
        * number of unique (distinct) operands (n2)
        * total number of operators (N1)
        * total number of operands (N2). 

    The number of unique operators and operands (n1 and n2) as well as
    the total number of operators and operands (N1 and N2) are calculated
    by collecting the frequencies of each operator and operand token
    of the source program.

    Other Halstead measures are derived from these four quantities
    with certain fixed formulas as described later.

    The classificaton rules applied are determined so that frequent language
    constructs give intuitively sensible operator and operand counts. 
    
    source: http://www.verifysoft.com/en_halstead_metrics.html
    """
    report = False
    def countHalsteadMeasures(self, node, *args):
        filename = self.filename = node.filename
        n1 = {}
        n2 = {}
        N1 = 0
        N2 = 0
        openfile = file(filename)
        for token in tokenize.generate_tokens(openfile.readline):
            (token_type, token_text, (start_line, start_column), (end_line, end_column), line) = token
            if (start_line < node.lineno):
                continue
            elif (end_line > node.endline):
                break
            if token_type in operators:
                # an operator has been found
                n1[token_text] = 1
                N1 += 1
            elif token_type in operands:
                if token_text in keywords:
                    # a keyword has been found, this is an operator
                    n1[token_text] = 1
                    N1 += 1
                else:
                    # an operand has been found
                    n2[token_text] = 1
                    N2 += 1
        if args:
            container, = args
            container.n1.update(n1)
            container.n2.update(n2)
            container.N1 += N1
            container.N2 += N2
        node.HalsteadMeasures = len(n1), len(n2), N1, N2
    visitFunction = countHalsteadMeasures
    def visitModule(self, node, *args):
        container, = args
        this = Container()
        self.default(node, this)
        if not this.N1:
            self.countHalsteadMeasures(node, this)
        container.n1.update(this.n1)
        container.n2.update(this.n2)
        container.N1 += this.N1
        container.N2 += this.N2
        node.HalsteadMeasures = len(this.n1), len(this.n2), this.N1, this.N2
    def visitProject(self, node, *args):
        this = Container()
        self.default(node, this)
        node.HalsteadMeasures = len(this.n1), len(this.n2), this.N1, this.N2
