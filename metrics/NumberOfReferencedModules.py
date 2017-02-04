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

import compiler

from core.metric import Metric

KIND, FILE, LINE, REF, MODULE, CLASS = range(6)

class NumberOfReferencedModules(Metric):
    """Number of classes created by a (Module, Class, Function)
    
    This is an approximation of the EfferentCoupling metric
    """
    resolve = True # Name resolving needed
    requires = ('ClassReferences', 'FunctionReferences')
    def visitModule(self, node, *args):
        node.NumberOfReferencedModules = len(
            set(
                imported.module
                for imports in node.symbols.values()
                    for imported in imports
                        if ("Imported" in imported.kind) and (imported.module != node)
            )
        )
    def visitClass(self, node, *args):
        references = list(node.ClassReferences)
        references.extend(node.FunctionReferences)
        node.NumberOfReferencedModules = len(
            set(
                reference.module
                for reference in references 
                    if (reference.module != node.module)
            )
        )
    visitFunction = visitClass