"""This module contains only declarations of builtin functions in Python
"""

def __import__(name, globals=None, locals=None, fromlist=None): pass
def abs(x): pass
def basestring(): pass
def bool(x=None): pass
def callable(object): pass
def chr(i):pass
def classmethod(function): pass
def cmp(x, y): pass
def compile(string, filename, kind, flags=None, dont_inherit=None): pass
def complex(real=None, imag=None): pass
def delattr(object, name): pass
def dict(mapping_or_sequence=None): pass
def dir(object=None): pass
def divmod(a, b): pass
def enumerate(iterable): pass
def eval(expression, globals=None, locals=None): pass
def execfile(filename, globals=None, locals=None): pass
def file(filename, mode=None, bufsize=None): pass
def filter(function, list): pass
def float(x=None): pass
def frozenset(iterable=None): pass
def getattr(object, name, default=None): pass
def globals(): pass
def hasattr(object, name): pass
def hash(object): pass
def help(object=None): pass
def hex(x): pass
def id(object): pass
def input(prompt=None): pass
def int(x=None, radix=None): pass
def isinstance(object, classinfo): pass
def issubclass(class_, classinfo): pass
def iter(o, sentinel=None): pass
def len(s): pass
def list(sequence=None): pass
def locals(): pass
def long(x, radix=None): pass
def map(function, *list): pass
def max(s, *args): pass
def min(s, *args): pass
def object(): pass
def oct(x): pass
def open(filename, mode=None, bufsize=None): pass
def ord(c): pass
def pow(x, y, z=None): pass
def property(fget=None, fset=None, fdel=None, doc=None): pass
def range(start=None, stop=None, step=None): pass
def raw_input(prompt=None): pass
def reduce(function, sequence, initializer=None): pass
def reload(module): pass
def repr(object): pass
def reversed(seq): pass
def round(x, n=None): pass
def set(iterable=None): pass
def setattr(object, name, value): pass
def slice(start_or_stop, stop=None, step=None): pass
def sorted(iterable, cmp=None, key=None, reverse=None): pass
def staticmethod(function): pass
def str(object=None): pass
def sum(sequence, start=None): pass
def super(type, object_or_type=None): pass
def tuple(sequence=None): pass
def type(object_or_name, bases=None, dict=None): pass
def unichr(i): pass
def unicode(object=None, encoding=None, errors=None): pass
def vars(object=None): pass
def xrange(start=None, stop=None, step=None): pass
def zip(*iterable): pass

class ArithmeticError(object): pass
class AssertionError(object): pass
class AttributeError(object): pass
class DeprecationWarning(object): pass
class EOFError(object): pass
class Ellipsis(object): pass
class EnvironmentError(object): pass
class Exception(object): pass
class FloatingPointError(object): pass
class FutureWarning(object): pass
class IOError(object): pass
class ImportError(object): pass
class IndentationError(object): pass
class IndexError(object): pass
class KeyError(object): pass
class KeyboardInterrupt(object): pass
class LookupError(object): pass
class MemoryError(object): pass
class NameError(object): pass
class NotImplemented(object): pass
class NotImplementedError(object): pass
class OSError(object): pass
class OverflowError(object): pass
class OverflowWarning(object): pass
class PendingDeprecationWarning(object): pass
class ReferenceError(object): pass
class RuntimeError(object): pass
class RuntimeWarning(object): pass
class StandardError(object): pass
class StopIteration(object): pass
class SyntaxError(object): pass
class SyntaxWarning(object): pass
class SystemError(object): pass
class SystemExit(object): pass
class TabError(object): pass
class TypeError(object): pass
class UnboundLocalError(object): pass
class UnicodeDecodeError(object): pass
class UnicodeEncodeError(object): pass
class UnicodeError(object): pass
class UnicodeTranslateError(object): pass
class UserWarning(object): pass
class ValueError(object): pass
class Warning(object): pass
class WindowsError(object): pass
class ZeroDivisionError(object): pass
