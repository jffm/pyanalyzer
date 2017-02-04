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

from core.writer.textwriter import TextWriter

class SqlWriter(TextWriter):
    types = {int:"int(11)", str:"varchar(255)", float:"double"}
    wildcard = "%%(%s)s"
    def __init__(self, fileobject, fields, table):
        self.output = fileobject
        self.fields = fields
        self.table = table
        print ",".join([field for (field, type) in fields])
        self.format = "INSERT INTO %s (%s) VALUES (%s);\n" % (
            table,
            ",".join([field for (field, type) in fields]),
            ",".join([((type==int) and "%s" or "'%s'" % (self.wildcard % field)) for (field, type) in fields])
        )
        print fields
        fileobject.write(
            "create table `%s` (\n\t%s\n);\n\n" %
            (
                table,
                ",\n\t".join([
                    ("%s %s" % (field, self.types[type]))
                    for (field, type) in fields
                ])
            )
        )
    def writerow(self, row):
        print row
        print "_"*30
        print self.format
        print "-"*60;
        print dict(
                (key, isinstance(value, str) and value.replace("'", "''") or value)
                for (key, value) in row.items()
            )
        self.output.write(
            self.format %
            dict(
                (key, isinstance(value, str) and value.replace("'", "''") or value)
                for (key, value) in row.items()
            )
        )
