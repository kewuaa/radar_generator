from abc import abstractmethod

from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
)

from . import utils


class ParameterBox(QGroupBox):
    """ Parameter GroupBox."""

    _layout: QVBoxLayout
    _mode_combo: QComboBox
    _value_input: utils.InputLayout
    _std_input: utils.InputLayout

    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._layout = vbox = QVBoxLayout()
        self.setLayout(vbox)

        self._mode_combo = mode_combo = QComboBox()
        vbox.addWidget(mode_combo)

        self._value_input = utils.InputLayout("value")
        vbox.addLayout(self._value_input)

        self._std_input = utils.InputLayout("std")
        vbox.addLayout(self._std_input)
    #enddef
    @abstractmethod
    def snapshot(self) -> dict:
        return {
            "mode": self._mode_combo.currentIndex(),
            "value": self._value_input.get(),
            "std": self._std_input.get()
        }
    #enddef

    @abstractmethod
    def load_snapshot(self, snapshot: dict) -> None:
        self._mode_combo.setCurrentIndex(snapshot.get("mode", 0))
        self._value_input.set(snapshot.get("value", ""))
        self._std_input.set(snapshot.get("std", ""))
    #enddef
#endclass
