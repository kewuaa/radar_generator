from enum import IntEnum

from .base import ParameterBox
from ..radar.doa import DOA


class DOAMode(IntEnum):
    """ doc."""

    Fixed = 0
#endclass


class DOABox(ParameterBox):
    """ DOA GroupBox."""

    def __init__(self) -> None:
        super().__init__("DOA")
        self._mode_combo.addItems(DOAMode._member_names_)
    #enddef

    def parse_snapshot(self, snapshot: dict) -> DOA:
        std = None
        if snapshot.get("std"):
            std = float(snapshot["std"])
        #endif
        return DOA(float(snapshot["value"]), std=std)
    #enddef
#endclass
