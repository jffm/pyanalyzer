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
import compiler.ast
import compiler.visitor

from core.metric import Metric

class LackOfCohesionInMethodsChidamberKemerer(Metric):
    """Lack Of Cohesion in Methods [Chidamber Kemerer] of a (Class)
    For Chidamber and Kemerer the Lack of Cohesion in Methods is calculated by subtracting
    from the number of method pairs that don't share a field access the number of method
    pairs that do share a field access.
    Lack of Cohesion in Methods is zero when the substraction results in a negative number
    """
    requires = ('Methods','InternalFieldAccesses')
    def visitClass(self, node, *args):
        methods = node.Methods
                
        number_of_methods = len(methods)
        if number_of_methods < 2:
            value = 0 # cannot compute LOCM, too few methods
        else:            
            method_accesses = {}
            for (field, client_methods) in node.InternalFieldAccesses.iteritems():
                for client_method in client_methods:
                    try:
                        method_accesses[client_method].add(field)
                    except KeyError:
                        method_accesses[client_method] = set([field])
            similar_methods = []
            add_similar_methods = similar_methods.append
            dissimilar_methods = []
            add_dissimilar_methods = dissimilar_methods.append
            empty = set([])
            for i in range(number_of_methods):
                firstmethod = methods[i]
                try:
                    fields = method_accesses[firstmethod]
                except KeyError:
                    fields = empty
                intersects = fields.intersection
                for j in range(i+1, number_of_methods):
                    secondmethod = methods[j]
                    try:
                        secondfields = method_accesses[secondmethod]
                    except KeyError:
                        secondfields = empty
                    if intersects(secondfields):
                        add_similar_methods((firstmethod, secondmethod))
                    else:
                        add_dissimilar_methods((firstmethod, secondmethod))
            number_of_similar_methods = len(similar_methods)
            number_of_dissimilar_methods = len(dissimilar_methods)
            
            if number_of_similar_methods > number_of_dissimilar_methods:
                value = 0
            else:
                value = number_of_dissimilar_methods-number_of_similar_methods
        
        node.LackOfCohesionInMethodsChidamberKemerer = value
