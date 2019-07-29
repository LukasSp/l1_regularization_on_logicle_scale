# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.4
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_Logicle')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_Logicle')
    _Logicle = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_Logicle', [dirname(__file__)])
        except ImportError:
            import _Logicle
            return _Logicle
        try:
            _mod = imp.load_module('_Logicle', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _Logicle = swig_import_helper()
    del swig_import_helper
else:
    import _Logicle
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
     import __builtins__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class Logicle(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Logicle, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Logicle, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _Logicle.new_Logicle(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _Logicle.delete_Logicle
    __del__ = lambda self: None

    def T(self):
        return _Logicle.Logicle_T(self)

    def W(self):
        return _Logicle.Logicle_W(self)

    def M(self):
        return _Logicle.Logicle_M(self)

    def A(self):
        return _Logicle.Logicle_A(self)

    def a(self):
        return _Logicle.Logicle_a(self)

    def b(self):
        return _Logicle.Logicle_b(self)

    def c(self):
        return _Logicle.Logicle_c(self)

    def d(self):
        return _Logicle.Logicle_d(self)

    def f(self):
        return _Logicle.Logicle_f(self)

    def w(self):
        return _Logicle.Logicle_w(self)

    def x0(self):
        return _Logicle.Logicle_x0(self)

    def x1(self):
        return _Logicle.Logicle_x1(self)

    def x2(self):
        return _Logicle.Logicle_x2(self)

    def scale(self, value):
        return _Logicle.Logicle_scale(self, value)

    def inverse(self, scale):
        return _Logicle.Logicle_inverse(self, scale)

    def dynamicRange(self):
        return _Logicle.Logicle_dynamicRange(self)

    def axisLabels(self, label):
        return _Logicle.Logicle_axisLabels(self, label)
Logicle_swigregister = _Logicle.Logicle_swigregister
Logicle_swigregister(Logicle)
cvar = _Logicle.cvar
Logicle.DEFAULT_DECADES = _Logicle.cvar.Logicle_DEFAULT_DECADES

class FastLogicle(Logicle):
    __swig_setmethods__ = {}
    for _s in [Logicle]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, FastLogicle, name, value)
    __swig_getmethods__ = {}
    for _s in [Logicle]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, FastLogicle, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _Logicle.new_FastLogicle(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _Logicle.delete_FastLogicle
    __del__ = lambda self: None

    def scale(self, value):
        return _Logicle.FastLogicle_scale(self, value)

    def bins(self):
        return _Logicle.FastLogicle_bins(self)

    def intScale(self, value):
        return _Logicle.FastLogicle_intScale(self, value)

    def inverse(self, *args):
        return _Logicle.FastLogicle_inverse(self, *args)
FastLogicle_swigregister = _Logicle.FastLogicle_swigregister
FastLogicle_swigregister(FastLogicle)
FastLogicle.DEFAULT_BINS = _Logicle.cvar.FastLogicle_DEFAULT_BINS

# This file is compatible with both classic and new-style classes.