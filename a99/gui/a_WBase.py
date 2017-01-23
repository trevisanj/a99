from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from .a_XLogDialog import XLogDialog
from .a_XLogMainWindow import XLogMainWindow


class WBase(QWidget):
    """Widget with 'edited' signal, keep_ref(), logging tools"""
    # Emitted whenever any value changes
    edited = pyqtSignal()

    def __init__(self, parent):
        assert isinstance(parent, (XLogMainWindow, XLogDialog))
        QWidget.__init__(self, parent)
        self._refs = []
        self.parent_form = parent


    # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * #
    # Interface

    def keep_ref(self, obj):
        """Adds obj to internal list to keep a reference to it.

        WHen using PyQt, it happens that the Python object gets garbage-collected even
        when a C++ Qt object still exists, causing a mess
        """
        self._refs.append(obj)
        return obj


    def add_log_error(self, x, flag_also_show=False):
        """Delegates to parent form"""
        self.parent_form.add_log_error(x, flag_also_show)

    def add_log(self, x, flag_also_show=False):
        """Delegates to parent form"""
        self.parent_form.add_log(x, flag_also_show)

    def update_gui_label_fn(self):
        pass