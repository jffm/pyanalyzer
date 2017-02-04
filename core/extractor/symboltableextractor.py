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

import re, os
import compiler.ast

from core.visitor import Visitor
from core.ast.variable import Variable

__all__ = [
    "SymbolTableExtractor",
    "Symbol",
    "SymbolTable"
]

class SymbolTable(dict):
    def __setitem__(self, name, symbols):
        if isinstance(symbols, list) or isinstance(symbols, tuple):      
            try:
                dict.__getitem__(self, name).extend(list(symbols))
            except KeyError:
                dict.__setitem__(self, name, list(symbols))
        else:
            try:
                dict.__getitem__(self, name).append(symbols)
            except KeyError:
                dict.__setitem__(self, name, [symbols])

class AnySymbolTable(SymbolTable):
    def __init__(self, *args, **kwargs):
        SymbolTable.__init__(self, *args, **kwargs)
    def __contains__(self, name):
        if not dict.__contains__(self, name):
            symbol = [Symbol(
                "Function|Class|Variable|Module,Undefined",
                None, Member(name), None, None
            )]
            SymbolTable.__setitem__(self, name, symbol)
        else:
            symbol = dict.__getitem__(self, name)
        return symbol
    __getitem__ = __contains__
        
class Type(compiler.ast.Class):
    filename = "__type__"
    lineno = 0
    def __init__(self, node=None):
        self.symbols = AnySymbolTable()
        self.referencedby = []
        self.concrete = node and set([node]) or set()
    @property
    def name(self):
        return self.__str__()
    @property
    def isresolved(self):
        return len(self.concrete)
    def resolve(self, name):
        if self.isresolved:
            if name in self.symbols:
                self.concrete = set(
                    ref
                    for ref in self.concrete
                        if name in ref.symbols
                )
    def lookup(self, name, symboltable):
        if name in self.symbols:
            if name not in symboltable:
                return
            self.concrete.update(
                symbol.node
                for symbols in symboltable.itervalues()
                    for symbol in symbols
                        if (
                            (
                                ("Class" in symbol.kind)
                                and ("Imported" not in symbol.kind)
                                and (name in symbol.node.symbols)
                            ) or 
                            (
                                ("Imported" in symbol.kind)
                                and (symbol.node.isinternal)
                                and (name in symbol.node.symbols)
                            )
                        )   
            )
            
    def __str__(self):
        return "%s[%s]<%s>" % (
            self.__class__.__name__, 
            ",".join([
                node.name
                for node in self.concrete
            ]),
            ",".join(
                [
                    value.node.name
                    for values in self.symbols.values()
                        for value in values
                ]
            )
        )
    __repr__ = __str__

class Member(compiler.ast.Class, Variable):
    filename = "__member__"
    lineno = 0
    def __init__(self, name):
        self.symbols = AnySymbolTable()
        self.referencedby = []
        self.name = name
    def __str__(self):
        return "%s<%s>" % (self.__class__.__name__, self.name)
    __repr__ = __str__
    
class Symbol(object):
    kind = None
    def __init__(self, kind, scope, node, module, class_):
        #   kind is Module, Class, Function or Imported
        #   filename is the path to the file where the node is defined
        #   lineno is the linenumber where the node is defined
        #   node is the reference to the node
        #   module is the reference to the unit containing the node or None
        #   class is the reference to the class containing the node or None
        self.kind = kind
        self.scope = scope
        self.node = node
        self.filename = node.filename
        self.lineno = node.lineno
        self.module = module
        self.class_ = class_
        node.symbol = self
        if ("Variable" not in kind):
            self.reference = node
        else:
            self.reference = Type()
    def __str__(self):
        return "Symbol(%s, %s, %s)" % (
            self.kind,
            self.node.name or self.filename,
            self.reference
        )
    __repr__ = __str__
    @property
    def isresolved(self):
        return not isinstance(self.reference, Type) or self.reference.isresolved
    def resolve(self, name, symboltable=None):
        if self.isresolved and isinstance(self.reference, Type):
            self.reference.resolve(name)
        elif ("Variable" in self.kind):
            self.reference.lookup(name, symboltable)
    def asKind(self, keep, kind):
        if isinstance(self.reference, Type):
            self.reference.concrete = set(
                ref
                for ref in self.reference.concrete
                    if isinstance(ref, kind) == keep
            )
    def asFunction(self, keep=True):
        self.asKind(keep, compiler.ast.Function)
    def asClass(self, keep=True):
        self.asKind(keep, compiler.ast.Class)
    def asType(self, keep=True):
        self.asKind(keep, Type)
    def asVariable(self, keep=True):
        self.asKind(keep, core.ast.Variable)
    def asModule(self, keep=True):
        self.asKind(keep, compiler.ast.Module)

class Imported(compiler.ast.Node):
    def __init__(self, name, lineno, filename, isinternal=False):
        self.name = name
        self.lineno = lineno
        self.filename = filename
        self.symbols = AnySymbolTable()
        self.referencedby = []
        self.isinternal = isinternal
    def __str__(self):
        return "%s[%s]<%s>" % (
            self.__class__.__name__, 
            self.name,
            ",".join(
                [
                    value.node.name
                    for values in self.symbols.values()
                        for value in values
                ]
            )
        )
    __repr__ = __str__
    
class Builtin(Imported): pass
                
def is_internal_module(imported_module, module_path, project_dir):
    path_exists = os.path.exists
    path_join = os.path.join
    module_name = imported_module.replace(".", os.path.sep)
    module_dir = os.path.dirname(module_path)
    for path in (module_dir, project_dir):
        if (path_exists(path_join(path, "%s.py" % module_name))
            or path_exists(path_join(path, module_name, "__init__.py"))):
            return True
    return False
                
class SymbolTableExtractor(Visitor):
    def __init__(self):
        # result is a dictionary that contains the list of defined
        # module, classes and functions
        # for each item, the value is the following tuple
        #   (kind, filename, lineno, node, module, class)
        #
        Visitor.__init__(self)
        self.result = None
        self.filename = None
    def visitProject(self, node, *args):
        self.result = node.symbols = SymbolTable()
        self.project_path = node.filename
        self.default(node, node, None, None)
    def visitModule(self, node, *args):
        node.referencedby = []
        node.symbols = SymbolTable()
        # Get scope
        (scope, module, class_) = args
        self.filename = filename = node.filename
        self.isbuiltin = node.isbuiltin = sum(
            1
            for builtin in ("types", "functions", "variables")
                if filename.endswith("__%s__.py" % builtin)
        )
        # Create the Module symbol
        symbol = Symbol(("Module",), scope, node, module, class_)
        # Add it to the symbol table
        # self.result[os.path.realpath(node.filename)] = symbol
        self.result[os.path.basename(node.filename)[:-3]] = symbol
        # Set scope for the remaining of the extraction and continue
        self.default(node, node, node, None)
    def visitFrom(self, node, *args):
        (scope, module, class_) = args
        result = self.result
        symbols = scope.symbols
        modname = node.modname
        for (imported, alias) in node.names:
            pathname = self.filename.replace(os.path.sep, ".")
            name = alias or imported
            isinternal = is_internal_module(modname, self.filename, self.project_path)
            ref = Imported(
                "%s.%s" % (modname, imported),
                node.lineno,
                self.filename,
                isinternal
            )
            symbol = Symbol(
                ("Function","Class","Variable","Imported"),
                scope, ref, module, class_
            )
            result[name] = symbols[name] = symbol
    def visitImport(self, node, *args):
        (scope, module, class_) = args
        result = self.result
        symbols = scope.symbols
        for (imported, alias) in node.names:
            name = alias or imported
            ref = Imported(
                name,
                node.lineno,
                self.filename,
                is_internal_module(imported, self.filename, self.project_path)
            )
            symbol = Symbol(
                ("Module","Imported"),
                scope, ref, module, class_
            )
            result[name] = symbols[name] = symbol
    def visitClass(self, node, *args):
        node.referencedby = []
        node.inheritedby = []
        node.symbols = SymbolTable()
        node.isbuiltin = self.isbuiltin
        # Get scope
        (scope, module, class_) = args
        # Create the Class symbol
        symbol = Symbol(("Class",), scope, node, module, class_)
        # Add it to the symbol table and in the containing scope
        self.result[node.name] = scope.symbols[node.name] = symbol
        for variable in ("cls", "self"):
            node.symbols[variable] = symbol
        # Set scope for the remaining of the extraction and continue
        self.default(node, node, module, node)
    def visitFunction(self, node, *args):
        node.referencedby = []
        node.symbols = SymbolTable()
        node.isbuiltin = self.isbuiltin
        # Get scope
        (scope, module, class_) = args
        # Create the Method or Function symbol
        if isinstance(scope, compiler.ast.Class):
            # Inside a Class scope, it's a method
            kind = ("Function","Method")
        elif isinstance(scope, compiler.ast.Module):
            # Otherwise it's a Function
            kind = ("Function","Global")
        else:
            kind = ("Function","Local")
        symbol = Symbol(kind, scope, node, module, class_)
        # Add it to the symbol table and in the containing scope
        self.result[node.name] = scope.symbols[node.name] = symbol
        # Add its parameters to its symbol table
        for arg in node.argnames:
            var = Variable(arg, self.filename, node.lineno)
            var.referencedby = []
            symbol = Symbol(("Variable","Parameter"), node, var, module, class_)
            self.result[arg] = node.symbols[arg] = symbol
        # Set scope for the remaining of the extraction and continue
        self.default(node, node, module, class_)
    def visitLambda(self, node, *args):
        node.filename = self.filename
        node.referencedby = []
        node.symbols = SymbolTable()
        # Get scope
        (scope, module, class_) = args
        symbol = Symbol(("Function","Local","Anonymous"), scope, node, module, class_)
        # Add it to the symbol table and in the containing scope
        name = node.name = "lambda,%d" % node.lineno
        self.result[name] = scope.symbols[name] = symbol
        # Add its parameters to its symbol table
        for arg in node.argnames:
            var = Variable(arg, self.filename, node.lineno)
            var.referencedby = []
            symbol = Symbol(("Variable","Parameter"), node, var, module, class_)
            node.symbols[arg] = symbol
        # Set scope for the remaining of the extraction and continue
        self.default(node, node, module, class_)
    def visitAssAttr(self, node, *args):
        (scope, module, class_) = args
        if class_: # skip if the attribute is not defined in a function
            if isinstance(scope, compiler.ast.Function):
                selfarg = scope.argnames[0]
                if isinstance(node.expr, compiler.ast.Name) and node.expr.name == selfarg:
                    if node.attrname not in class_.symbols:
                        var = Variable(node.attrname, self.filename, node.lineno)
                        var.referencedby = []
                        symbol = Symbol(("Variable","Attribute"), class_, var, module, class_)
                        self.result[var.name] = class_.symbols[var.name] = symbol
    visitGetattr = visitAssAttr
    def visitAssName(self, node, *args):
        var = Variable(node.name, self.filename, node.lineno)
        var.referencedby = []
        var.isbuiltin = self.isbuiltin
        (scope, module, class_) = args
        if isinstance(scope, compiler.ast.Class):
            kind = ("Variable","Attribute")
        elif isinstance(scope, compiler.ast.Function):
            kind = ("Variable","Local")
        else:
            kind = ("Variable","Global")
        symbol = Symbol(kind, scope, var, module, class_)
        self.result[node.name] = scope.symbols[node.name] = symbol