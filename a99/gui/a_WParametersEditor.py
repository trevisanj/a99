"""Parameters Editor Widget. Mostly used embedded in XParametersEditor"""

__all__ = ["WParametersEditor"]

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .parameter import Parameters

################################################################################

class WParametersEditor(QWidget):
    """
    Parameters editor widget.

    Arguments:
      parent=None
      specs=None -- list as [(name, {...}), ...], which will be passed
       to Parameters constructor. Parameter.FromSpec()
       for full documentation.
      parameters=None -- Parameters instance. If passed, ignores specs and sets
      internal parameters attribute directly
    """

    # Emitted whenever the parameters changes into a valid parameters
    # TODO Not sure if will be used
    ParametersChanged = pyqtSignal(tuple)

    def __init__(self, parent=None, specs=None, parameters=None):
        QWidget.__init__(self, parent)

        if parameters is not None:
            assert isinstance(parameters, Parameters)
            self._parameters = parameters
        else:
            self._parameters = Parameters(specs)

        self._SetupUi()

    def setFocus(self, reason=None):
        """Sets focus to first field. Note: reason is ignored."""
        self.formLayout.itemAt(0, QFormLayout.FieldRole).widget().setFocus()

    def get_kwargs(self):
        self._parameters.UpdateFromWidgets()
        return self._parameters.GetKwargs()

    def validate(self):
        # Currently calling Parameters.GetKwargs() to do the <quote>validation<quote>
        self._parameters.UpdateFromWidgets()

    def set_error_text(self, x):
        self._set_error_text(x)


    ############################################################################
    ############################################################################

    def _set_error_text(self, x):
        """Sets text of labelError."""
        self.labelError.setText(x)

    def _SetupUi(self):
        self.setObjectName("WParametersEditor")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(0)

        self.formLayout = QFormLayout()
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setHorizontalSpacing(5)
        self.verticalLayout.addLayout(self.formLayout)

        self.labelError = QLabel(self)
        self.labelError.setStyleSheet("color: red")
        self.labelError.setText("")
        self.verticalLayout.addWidget(self.labelError)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self._parameters.AddToLayout(self.formLayout)
