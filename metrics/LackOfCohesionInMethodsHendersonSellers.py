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

class LackOfCohesionInMethodsHendersonSellers(Metric):
    """Lack Of Cohesion in Methods [Henderson Sellers] of a (Class)
    Henderson-Sellers defines Lack of Cohesion in Methods as follows.
    Let:
        M	be the set of methods defined by the class
        F	be the set of fields defined by the class
        r(f)	be the number of methods that access field f, where f is a member of F
        <r>	be the mean of r(f) over F.
        
    Then:
        Lack of Cohesion in Methods = (<r> - |M|) / (1 - |M|)
    """
    requires = ('Methods', 'InternalFieldAccesses')
    def visitClass(self, node, *args):
        methods = node.Methods
                
        number_of_methods = len(methods)
        if number_of_methods <= 1:
            value = -1 # cannot compute LOCM, too few methods
        else:
            field_accesses = node.InternalFieldAccesses
            number_of_fields = len(field_accesses)
            if number_of_fields == 0:
                value = -1
            else:
                sum_field_accesses = sum(len(m) for (f, m) in field_accesses.items())
                mean_field_accesses = float(sum_field_accesses)/number_of_fields
                value = (mean_field_accesses - number_of_methods) / (1.0 - number_of_methods)

        node.LackOfCohesionInMethodsHendersonSellers = value
