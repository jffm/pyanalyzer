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

import re

__all__ = ["CodeElementsExtractor"]

class CodeElement(object):
    """Code element (Module, Class, Function)
    """
    def __init__(self, kind, name, indent, startline, endline=None):
        self.kind = kind
        self.name = name
        self.indent = indent
        self.startline = startline
        self.endline, = endline is None and (startline,) or (endline,)
        
    def __str__(self):
        return "%s(%s, indent=%d, start=%d, end=%d)" % (
            self.kind, self.name, self.indent, self.startline, self.endline)
    __repr__ = __str__

class CodeElementsExtractor(object):

    def __init__(self, filename):
        """Create the extractor for the given @filename
        """
        self.filename = filename

    def extract(self):
        """Return the ordered list of code elements with their indent, start and end
        [Element(kind, name, indent, startline, endline), ...]
        """

        re_class = re.compile(r"^(\s*)class\s+(\w+)\s*(?:\(|:)")
        re_function = re.compile(r"^(\s*)def\s+(\w+)\s*\(")
        re_code = re.compile(r"^(\s*).*")
        re_comment = re.compile(r"^(\s*)#.*")
        re_blank = re.compile(r"^\s+$")

        elements = []
        stack = []
        blanks = []

        module = CodeElement("Module", self.filename, 0, 0)
        stack.append(module)
        elements.append(module)
        
        i = -2 # if the filename is empty

        for i, line in enumerate(open(self.filename)):
            match = re_class.match(line)
            if match:
                # get indent and name of the class, record it and push it on stack
                indent_str, name = match.groups()
                indent = len(indent_str)
                _class = CodeElement("Class", name, indent, i+1)
                if stack and blanks:
                    j = len(blanks)
                    while stack[-1].endline == blanks[j-1]:
                        stack[-1].endline -= 1
                        j -= 1
                if (stack[-1] != module) and (stack[-1].indent >= _class.indent):
                    stack.pop()
                stack.append(_class)
                elements.append(_class)
                continue
            match = re_function.match(line)
            if match:
                # get indent and name of the function, record it and push it on stack
                indent_str, name = match.groups()
                indent = len(indent_str)
                function = CodeElement("Function", name, indent, i+1)
                if stack and blanks:
                    j = len(blanks)
                    while stack[-1].endline == blanks[j-1]:
                        stack[-1].endline -= 1
                        j -= 1
                if (stack[-1] != module) and (stack[-1].indent >= function.indent):
                    stack.pop()
                stack.append(function)
                elements.append(function)
                continue
            match = re_blank.match(line)
            if match:
                # store the blank line
                blanks.append(i+1)
                stack[-1].endline = i+1
                continue
            match = re_comment.match(line)
            if match:
                # store the commented line
                stack[-1].endline = i+1
                continue
            match = re_code.match(line)
            if match:
                # get the indent of the line of code
                indent_str, = match.groups()
                indent = len(indent_str)
                while True and stack:
                    element = stack.pop()
                    element.endline = i+1
                    if element.indent < indent:
                        break
                stack.append(element)
                continue

        j = len(blanks)
        while stack:
            element = stack.pop()
            element.endline = i+2
            if blanks:
                while element.endline == blanks[j-1]: # last line is blank line
                    element.endline -= 1
                    j -= 1

        element.endline = i+2 # set last line of Module
        
        del stack, re_class, re_function, re_code

        return elements, blanks

if __name__ == "__main__":
    import sys
    print CodeElementsExtractor(sys.argv[1]).extract()
