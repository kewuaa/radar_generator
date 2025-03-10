from enum import IntEnum

from .base import ParameterBox
from ..radar.pa import PA


class PAMode(IntEnum):
    """ doc."""

    Fixed = 0
#endclass


class PABox(ParameterBox):
    """ PA GroupBox."""

    def __init__(self) -> None:
        super().__init__("PA")
        self._mode_combo.addItems(PAMode._member_names_)
        self._std_input.setEnabled(False)
    #enddef

    def parse_snapshot(self, snapshot: dict) -> PA:
        return PA(float(snapshot["value"]))
    #enddef
#endclass
