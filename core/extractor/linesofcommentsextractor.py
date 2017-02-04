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
"""
linesofcomments is used to extract the lines of comments of a python source file
usage: linesofcomments.py python_file
"""

__author__ = "Frederic F. MONFILS"
__version__ = "$Revision: $".split()[1]
__revision__ = __version__
# $Source: $
__date__ = "$Date: $"
__copyright__ = "Copyright (c) 2008-2009 Junior (Frederic) FLEURIAL MONFILS"
__license__ = "GPLv3"
__contact__ = "ffm at cetic.be"

__all__ = ["LinesOfCommentsExtractor"]

def read(file, lineno, lines=[]):
    """Return next character and increment line number if needed
    """
    char = file.read(1)
    if lines:
        lineno = lines.pop()
    if char == "\n":
        lines.append(lineno+1)
    return char, lineno

class LinesOfCommentsExtractor(object):

    def __init__(self, filename):
        self.filename = filename
        
    def extract(self):
        """Return the ordered list of line numbers of commented lines
        [int, int, ...]
        """

        lines_of_comments = []
        
        f = open(self.filename)
        c = lineno = 1

        while c:
            c, lineno = read(f, lineno)
            if c in ('"', "'"):
                # String
                c0, lineno = read(f, lineno)
                if c0 == c:
                    c1, lineno = read(f, lineno)
                    if c1 == c:
                        # Triple quote string
                        # Record the value of the triple quoted string
                        q = 0
                        e = 0
                        s = c * 3 # s will hold the value of the string
                        while q != 3: # until we found 3 successive quotes
                            cs, lineno = read(f, lineno)
                            s += cs
                            if cs == c:
                                if not (e%2): # not escaped quote
                                    q += 1
                            elif cs == "\\":
                                e += 1
                                q = 0
                            else:
                                e = 0
                                q = 0
                    else:
                        # Empty quoted string
                        s = c*2
                else:
                    # Record value of the string
                    s = "%s%s" % (c, c0)
                    e = (c0 == "\\") and 1 or 0
                    while True:
                        c0, lineno = read(f, lineno)
                        s += c0
                        if c0 == c and not (e%2): # not escaped quote
                            break
                        elif c0 == "\\":
                            e += 1
                        else: # and c0 != "\\"
                            e = 0
            elif c == "#":
                # we are sure that this is a real comment indicator
                # because we are sure that we are not inside a string
                lines_of_comments.append(lineno)
                s = ""
                while c and (c != "\n"):
                    c, lineno = read(f, lineno)
                    s += c                        

        del f, c, lineno # clean up used variables

        return lines_of_comments

if __name__ == "__main__":
    import sys
    print LinesOfCommentsExtractor(sys.argv[1]).extract()
