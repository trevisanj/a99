"""Routines that somehow look into the package itself"""


import os
import glob
import imp
import inspect
import a99


__all__ = ["ExeInfo", "get_exe_info", "collect_doc",
           "get_classes_in_module"]


class ExeInfo(object):
    """Information about an executable file"""
    def __init__(self, filename, description, flag_error=False, flag_gui=False):
        self.filename = filename
        # First line of script docstring
        self.description = description
        # Error importing script as module?
        self.flag_error = flag_error
        # Script is a graphical application?
        self.flag_gui = flag_gui


def get_exe_info(dir_, flag_protected=False):
    """
    Returns a list of ExeInfo objects, which represent Python scripts within dir_

    Args:
        dir_: string, path to directory
        flag_protected: whether or not to include files starting with a '_'

    Returns:
        list of ExeInfo objects

    The ExeInfo objects represent the ".py" files in directory dir_,
    """

    ret = []
    # gets all scripts in script directory
    ff = glob.glob(os.path.join(dir_, "*.py"))
    # discards scripts whose file name starts with a "_"
    ff = [f for f in ff if flag_protected or not os.path.basename(f).startswith("_")]
    ff.sort()

    for f in ff:
        _, filename = os.path.split(f)
        flag_error = False
        flag_gui = None
        try:
            # Checks if it is a graphical application

            with open(f, "r") as h:
                flag_gui = "QApplication" in h.read()

            script_ = imp.load_source('script_', f)  # module object
            descr = script_.__doc__.strip()
            descr = descr.split("\n")[0]  # first line of docstring
        except Exception as e:
            flag_error = True
            descr = "*{0!s}*: {1!s}".format(e.__class__.__name__, str(e))

        ret.append(ExeInfo(filename, descr, flag_error, flag_gui))

    # Sorts command-line and graphical applications by name separately
    sisi_gra = [si for si in ret if si.flag_gui]
    sisi_cmd = [si for si in ret if not si.flag_gui]
    sisi_gra = sorted(sisi_gra, key=lambda x: x.filename)
    sisi_cmd = sorted(sisi_cmd, key=lambda x: x.filename)
    ret = sisi_cmd+sisi_gra

    return ret


def collect_doc(module, base_class=None, prefix="", flag_exclude_prefix=False):
    """
    Collects class names and docstrings in module for classes starting with prefix

    Arguments:
        module -- Python module
        prefix -- argument for str.startswith(); if not passed, does not filter
        base_class -- filters only descendants of this class
        flag_exclude_prefix -- whether or not to exclude prefix from class name in result

    Returns: [(classname0, signature, docstring0), ...]
    """

    ret = []
    for attrname in module.__all__:
        if prefix and not attrname.startswith(prefix):
            continue

        attr = module.__getattribute__(attrname)

        if base_class is not None and not issubclass(attr, base_class):
            continue

        spec = inspect.signature(attr)

        ret.append((attrname if not flag_exclude_prefix else attrname[len(prefix):], spec, attr.__doc__))

    return ret


def get_classes_in_module(module, superclass=object):
    """
    Returns a list with all classes in module that descend from parent

    Args:
        module: builtins.module
        superclass: a class

    Returns: list
    """

    ret = []
    for classname in dir(module):
        attr = module.__getattribute__(classname)
        try:
            if issubclass(attr, superclass) and (attr != superclass):
                ret.append(attr)
        except TypeError:
            # "issubclass() arg 1 must be a class"
            pass
        except RuntimeError:
            # a99.get_python_logger().exception("Failed probing attribute '{}'".format(classname))
            # raise
            pass
    return ret


def get_class_package(class_):
    """
    Returns package that class belongs to
    """
    root_pkg_name = class_.__module__.split(".")[0]
    if root_pkg_name == a99.__name__:
        return a99
    if root_pkg_name not in __collaborators:
        raise RuntimeError("Class '{}' belongs to package '{}', "
                           "but the latter is not among hypydrive collaborators".
                           format(class_.__name__, root_pkg_name))
    return __collaborators[root_pkg_name]
