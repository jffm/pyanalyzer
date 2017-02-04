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

"""This module implements a light NameResolver for an AST

It first starts by creating a symbol table with the modules, classes and functions
Then it analyses the following relationships
    import -> search in list of defined modules
    inheritance -> search inside the classes inside the current unit
                -> search in list of imported modules
                   and in list of classes inside a given module
    call -> search inside the classes inside the unit
         -> search inside the functions inside the unit
         -> search inside the methods of the current class
         -> search in list of imported modules and in list of classes
         -> search in list of imported modules and in list of methods of the classes
    except
    raise
    getattr
"""

__author__ = "Frederic F. MONFILS"
__version__ = "$Revision: $".split()[1]
__revision__ = __version__
# $Source: $
__date__ = "$Date: $"
__copyright__ = "Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS"
__license__ = "GPLv3"
__contact__ = "ffm at cetic.be"

import sys, compiler, os, itertools
from core.visitor import Visitor
from core.extractor.symboltableextractor import SymbolTableExtractor, SymbolTable, Symbol

__all__ = ["NameResolver"]

def get_symbols_for_filename(symboltable, filename):
    definitions = {}
    for (name, entities) in symboltable.iteritems():
        for entity in entities:
            if entity[1] != filename:
                continue
            try:
                definitions[name].append(entity)
            except KeyError:
                definitions[name] = [entity]
    return definitions

class NameGetter(Visitor):
    result = None
    def __init__(self):
        self.result = []
        Visitor.__init__(self)
    def visitGetattr(self, node, *args):
        self.default(node, *args)
        self.result.append(node.attrname)
    visitAssAttr = visitGetattr
    def visitName(self, node, *args):
        self.result.append(node.name)
    def visitCallFunc(self, node, *args):
        pass
    
class ClassInheritanceResolver(Visitor):

    def __init__(self, symboltable):
        self.symboltable = symboltable

    def visitClass(self, node, *args):
        node.inherits = []
        node.ancestors = None
        for base in node.bases:
            parts = compiler.walk(base, NameGetter()).result
            called = ".%s" % ".".join(parts)
            parents = [
                item.node
                for (name, data) in self.symboltable.iteritems()
                    for item in data
                        if (item.kind == "Class")
                        and called.endswith(".%s" % name)
            ]
            node.inherits.extend(parents)
            for parent in parents:
                try:
                    parent.inheritedby.append(node)
                except AttributeError:
                    parent.inheritedby = [node]
        self.default(node, *args)
        
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
    
class ImportGetter(Visitor):
    def __init__(self, packages, project_path):
        self.packages = packages
        self.project_path = project_path
        self.result = SymbolTable()
    def visitModule(self, node, *args):
        self.filename = node.filename
        self.default(node, node, node, None)
    def visitFrom(self, node, *args):
        (scope, module, class_) = args
        result = self.result
        symbols = scope.symbols
        modname = node.modname
        for (imported, alias) in node.names:
            name = alias or imported
            ref = Imported(
                "%s.%s" % (modname, imported),
                node.lineno,
                self.filename,
                is_internal_module(modname, self.filename, self.project_path)
            )
            symbol = Symbol(
                "Function|Class|Variable,Imported",
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
                "Module,Imported",
                scope, ref, module, class_
            )
            result[name] = symbols[name] = symbol

class Referrer(object):
    def __init__(self, node, scope, module, class_, possibilities):
        self.node = node
        self.scope = scope
        self.module = module
        self.class_ = class_
        self.possibilities = possibilities

def iternodes(node):
    yield node
    for child in node.getChildNodes():
        iternodes(child)

class NameResolver(Visitor):
    """This class, resolves the calls that exist inside the application.
    The references are stored in the following nodes:
      - Module: list of imported modules inside the application
      - Class: link to base classes and ancestors inside the application
      - CallFunc: link to called element inside the application
    """
    definitions = None
    symboltable = None
    packages = None
    classes = None
    index = 0
    filename = None
    dirname = None
    definitions = None
    imports = None

    def __init__(self, options):
        Visitor.__init__(self)
        self.symboltable = None
        self.packages = SymbolTable()
        self.p = {}
        # Stack to hold the current module
        self.modules = []
        # Stack to hold the current class
        self.classes = []
        # Stack to hold the current method/function
        self.functions = []
        self.log = options.log

    def visitProject(self, node, *args):
        """Resolve the name for the whole project
        """
        # Create the symboltable
        self.symboltable = compiler.walk(node, SymbolTableExtractor()).result
        # Extract the Modules from the symbol table
        for (name, data) in self.symboltable.iteritems():
            module = [item.node for item in data if "Imported" not in item.kind]
            for item in data:
                if ("Imported" in item.kind) and item.node.isinternal:
                    item.node.symbols = module[0].symbols
                if "Module" in item.kind:
                    self.packages[name] = item
                    self.p[item.filename] = item
        compiler.walk(node, ClassInheritanceResolver(self.symboltable))
        self.index = 0
        self.project = node
        #
        # Create the builtins
        #
        self.builtins = builtins = SymbolTable()
        builtin_types = self.packages["__types__"][0]
        builtin_functions = self.packages["__functions__"][0]
        builtin_variables = self.packages["__variables__"][0]
        # builtins["__types__"] = builtin_types
        for (name, symbols) in builtin_types.node.symbols.iteritems():
            builtins[name] = symbols
        for (name, symbols) in builtin_functions.node.symbols.iteritems():
            builtins[name] = symbols
        for (name, symbols) in builtin_variables.node.symbols.iteritems():
            builtins[name] = symbols
        self.default(node, node)

    def visitModule(self, node, *args):
        self.filename = node.filename
        self.definitions = node.symbols
        self.default(node, node, node, None)

    def visitClass(self, node, *args):
        #
        # Create the list of ancestors of the class
        #
        ancestors = node.inherits[:]
        index = 0
        self.index += 1
        while index < len(ancestors):
            parent = ancestors[index]
            ancestors = (
                ancestors[:index+1]
                + parent.inherits
                + ancestors[index+1:]
            )
            index += 1
        # Store the list of ancestors in the node
        node.symbol.ancestors = ancestors
        # Get scope
        (scope, module, class_) = args
        # Analyse the children
        self.default(node, node, module, node)

    def visitFunction(self, node, *args):
        (scope, module, class_) = args
        self.default(node, node, module, class_)
        
    def visitGetattr(self, node, *args):
        (scope, module, class_) = args
        self.default(node, *args)
        if self._symbol and ("Undefined" not in self._symbol.kind):
            node.reference = self._resolve(node, node.attrname, scope, module, class_, self._symbol)
            
    def visitCallFunc(self, node, *args):
        (scope, module, class_) = args
        self.default(node, *args)
        if self._symbol and ("Class" in self._symbol.kind):
            self.log.debug("Trying to continue to __init__ function for class %s" % self._symbol.node.name)
            self._symbol = self._resolve(node, "__init__", self._symbol.node, module, class_, self._symbol)
        
    def _resolve(self, node, name, scope, module, class_, symbol=None):
        self.log.info("resolving %s" % name)
        # result will be the list of found symbols
        res = []
        if symbol:
            symbol.resolve(name, scope.symbols)
            res = symbol.reference.symbols.get(name, [symbol])
        elif name in scope.symbols:
            # check if current scope contains the name
            res = scope.symbols[name]
        else:
            # find the symbol in the upper scope
            current = scope
            while True:
                if not isinstance(scope, compiler.ast.Module):
                    scope = scope.symbol.scope
                if name in scope.symbols:
                    res = scope.symbols[name]
                    break
                if scope == module:
                    if (not res) and (name in self.builtins):
                        res = self.builtins[name]
                    elif not res:
                        self.log.error("Cannot find symbol '%s' in module %s" % (name, module.filename))
                        return Symbol("Undefined", scope, node, module, class_)
                    elif ("Imported" in res[0].kind) and res[0].isinternal:
                        self.log.warn("External symbol '%s' imported in module %s" % (name, module.filename))
                        return Symbol("External,Undefined", scope, node, module, class_) # external import
                    break
            # add symbol to current scope to speed up next research
            if current != scope:
                current.symbols[name] = res

        # set the bidirectional link between referrer and reference
        possibilities = len(res)
        reference = node.reference = res[0]
        referrer = Referrer(node, scope, module, class_, possibilities) # create the referrer
        reference.node.referencedby.append(referrer) # add it to _symbol
        return reference
        
    def visitTuple(self, node, *args):
        self._symbol = None
        
    def visitConstType(self, type, node, *args):
        (scope, module, class_) = args
        self._symbol = self._resolve(node, type, self.project, module, class_)
        
    def visitDict(self, node, *args):
        self.visitConstType("dict", node, *args)
        
    def visitList(self, node, *args):
        self.visitConstType("sequence", node, *args)
        
    def visitConst(self, node, *args):
        self._symbol = None
        if isinstance(node.value, str):
            self.visitConstType("string", node, *args)
        
    def visitName(self, node, *args):
        (scope, module, class_) = args
        node.filename = module.filename
        # Try to resolve the current name
        self._symbol = node.reference = self._resolve(node, node.name, scope, module, class_)
        
    visitAssAttr = visitGetattr