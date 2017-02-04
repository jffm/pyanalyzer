"""This module contains only declarations of builtin types in Python
Source: 3.11.1 Types and members
"""

class object:
    __dict__ = None
    __methods__ = None
    __members__ = None
    __class__ = None
    __bases__ = None
    __name__ = None
    __slots__ = None
    __metaclass__ = None
    def __init__(self, *args): pass
    def __new__(cls, *args): pass
    def __del__(self): pass
    def __repr__(self): pass
    def __str__(self): pass
    def __lt__(self): pass
    def __le__(self): pass
    def __eq__(self): pass
    def __ne__(self): pass
    def __gt__(self): pass
    def __ge__(self): pass
    def __cmp__(self): pass
    def __rcmp__(self): pass
    def __hash__(self): pass
    def __nonzero__(self): pass
    def __unicode__(self): pass
    def __call__(self, *args): pass
    # accessor
    def __getattr__(self, name): pass
    def __setattr__(self, name, value): pass
    def __delattr__(self, name): pass
    def __getattribute__(self, name): pass
    # descriptor
    def __get__(self, instance, owner): pass
    def __set__(self, instance, value): pass
    def __delete__(self, instance): pass
    # container
    def __len__(self): pass
    def __getitem__(self, key): pass
    def __setitem__(self, key, value): pass
    def __delitem__(self, key): pass
    def __iter__(self): pass
    def __contains__(self, item): pass
    # sequence
    def __getslice__(self, i, j): pass
    def __setslice__(self, i, j, sequence): pass
    def __delslice__(self, i, j): pass
    # numeric
    def __add__(self, other): pass
    def __sub__(self, other): pass
    def __mul__(self, other): pass
    def __floordiv__(self, other): pass
    def __mod__(self, other): pass
    def __divmod__(self, other): pass
    def __pow__(self, other): pass
    def __lshift__(self, other): pass
    def __rshift__(self, other): pass
    def __and__(self, other): pass
    def __xor__(self, other): pass
    def __or__(self, other): pass
    def __div__(self, other): pass
    def __truediv__(self, other): pass
    def __radd__(self, other): pass
    def __rsub__(self, other): pass
    def __rmul__(self, other): pass
    def __rdiv__(self, other): pass
    def __rtruediv__(self, other): pass
    def __rfloordiv__(self, other): pass
    def __rmod__(self, other): pass
    def __rdivmod__(self, other): pass
    def __rpow__(self, other): pass
    def __rlshift__(self, other): pass
    def __rrshift__(self, other): pass
    def __rand__(self, other): pass
    def __rxor__(self, other): pass
    def __ror__(self, other): pass
    def __iadd__(self, other): pass
    def __isub__(self, other): pass
    def __imul__(self, other): pass
    def __idiv__(self, other): pass
    def __itruediv__(self, other): pass
    def __ifloordiv__(self, other): pass
    def __imod__(self, other): pass
    def __ipow__(self, other): pass
    def __ilshift__(self, other): pass
    def __irshift__(self, other): pass
    def __iand__(self, other): pass
    def __ixor__(self, other): pass
    def __ior__(self, other): pass
    def __neg__(self): pass
    def __pos__(self): pass
    def __abs__(self): pass
    def __invert__(self): pass
    def __complex__(self): pass
    def __int__(self): pass
    def __long__(self): pass
    def __float__(self): pass
    def __oct__(self): pass
    def __hex__(self): pass
    def __coerce__(self, other): pass
    
    
class complex(object):
    def conjugate(self): pass
    
class dict(object):
    def clear(self): pass
    def copy(self): pass
    def has_key(self, key): pass
    def items(self): pass
    def keys(self): pass
    def update(self, dict=None): pass
    def fromkeys(self, seq, value=None): pass
    def values(self): pass
    def get(self, key, x=None): pass
    def setdefault(self, key, x=None): pass
    def pop(self, key, x=None): pass
    def popitem(self): pass
    def iteritems(self): pass
    def iterkeys(self): pass
    def itervalues(self): pass

class iterator(object):
    def next(self): pass
    
class sequence(object):
    def append(self, x): pass
    def extend(self, x): pass
    def count(self, x): pass
    def index(self, x, i=None, j=None): pass
    def insert(self, i, x): pass
    def pop(self, i=None): pass
    def remove(self, x): pass
    def reverse(self): pass
    def sort(self, cmp=None, key=None, reverse=None): pass
    
class string(object):
    def capitalize(self): pass
    def center(self, fillchar=None): pass
    def count(self, sub, start=None, end=None): pass
    def decode(self, encoding=None, errors=None): pass
    def encode(self, encoding=None, errors=None): pass
    def endswith(self, suffix, start=None, end=None): pass
    def expandtabs(self, tabsize=None): pass
    def find(self, sub, start=None, end=None): pass
    def index(self, sub, start=None, end=None): pass
    def isalnum(self): pass
    def isalpha(self): pass
    def isdigit(self): pass
    def islower(self): pass
    def isspace(self): pass
    def istitle(self): pass
    def isuper(self): pass
    def join(self, seq): pass
    def ljust(self, width, fillchar=None): pass
    def lower(self): pass
    def lstrip(self, chars=None): pass
    def replace(self, old, new, count=None): pass
    def rfind(self, sub, start=None, end=None): pass
    def rindex(self, sub, start=None, end=None): pass
    def rjust(self, width, fillchar=None): pass
    def rsplit(self, sep=None, maxsplit=None): pass
    def rstrip(self, chars=None): pass
    def split(self, sep, maxsplit=None): pass
    def splitlines(self, keepends=None): pass
    def startswith(self, prefix, start=None, end=None): pass
    def strip(self, chars=None): pass
    def swapcase(self): pass
    def title(self): pass
    def translate(self, table, deletechars=None): pass
    def upper(self): pass
    def zfill(self, width=None): pass
    
class frozenset(object):
    def issubset(self, t): pass
    def issuperset(self, t): pass
    def union(self, t): pass
    def intersection(self, t): pass
    def difference(self, t): pass
    def symmetric_difference(self, t): pass
    def copy(self, t): pass
    
class set(frozenset):
    def update(self, t): pass
    def intersection_update(self, t): pass
    def difference_update(self, t): pass
    def symmetric_difference_update(self, t): pass
    def add(self, x): pass
    def remove(self, x): pass
    def discard(self, x): pass
    def pop(self): pass
    def clear(self): pass
    
class file(object):
    closed=None
    encoding=None
    mode=None
    name=None
    newlines=None
    softspace=None
    def close(self): pass
    def flush(self): pass
    def fileno(self): pass
    def isatty(self): pass
    def next(self): pass
    def read(self, size=None): pass
    def readline(self, size=None): pass
    def readlines(self, sizehint=None): pass
    def xreadlines(self): pass
    def seek(self, offset, whence=None): pass
    def tell(self): pass
    def truncate(self, size=None): pass
    def write(self, str): pass
    def writelines(self, sequence): pass
    
class module(object):
    __doc__ = None
    __file__ = None
    
class class_(object):
    __doc__ = None
    __module__ = None
    
class method(object):
    __doc__ = None
    __name__ = None
    im_class = None
    im_func = None
    im_self = None
    
class function(object):
    __doc__ = None
    __name__ = None
    func_code = None
    func_defaults = None
    func_doc = None
    func_globals = None
    func_name = None
    
class traceback(object):
    tb_frame = None
    tb_lasti = None
    tb_lineno = None
    tb_next = None
    
class frame(object):
    f_back = None
    f_builtins = None
    f_code = None
    f_exc_traceback = None
    f_exc_type = None
    f_exc_value = None
    f_globals = None
    f_lasti = None
    f_lineno = None
    f_locals = None
    f_restricted = None
    f_trace = None
    
class code(object):
    co_argcount = None
    co_code = None
    co_const = None
    co_filename = None
    co_firstlineno = None
    co_flags = None
    co_lnotab = None
    co_name = None
    co_names = None
    co_nlocals = None
    co_stacksize = None
    co_varnames = None
    
class builtin(object): 
    __doc__ = None
    __name__ = None
    __self__ = None
    