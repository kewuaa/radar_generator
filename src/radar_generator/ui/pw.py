import re
from enum import IntEnum

from PySide6.QtWidgets import QVBoxLayout

from . import utils
from .base import ParameterBox
from ..radar.pw import PW


class PWMode(IntEnum):
    """ doc."""

    Fixed = 0
    Uneven = 1
    Group = 2
#endclass


class PWBox(ParameterBox):
    """ PW GroupBox."""

    _group_size_input: utils.InputLayout | None = None

    def __init__(self) -> None:
        super().__init__("PW")
        self._mode_combo.addItems(PWMode._member_names_)

        switchable_layout = QVBoxLayout()
        self._layout.addLayout(switchable_layout)

        def switch_layout(index: int) -> None:
            utils.clear_layout(switchable_layout)
            self._value_input.setEnabled(True)
            self._value_input.set("")
            self._std_input.setEnabled(True)
            self._std_input.set("")
            self._group_size_input = None

            if index == PWMode.Group:
                self._setup_group(switchable_layout)
            #endif
        #enddef
        switch_layout(PWMode.Fixed)
        self._mode_combo.currentIndexChanged.connect(switch_layout)
    #enddef

    def _setup_group(self, layout: QVBoxLayout) -> None:
        self._group_size_input = input = utils.InputLayout("group size")
        layout.addLayout(input)
    #enddef

    def snapshot(self) -> dict:
        snapshot = super().snapshot()
        if self._group_size_input is not None:
            snapshot["group_size"] = self._group_size_input.get()
        #endif
        return snapshot
    #enddef

    def load_snapshot(self, snapshot: dict) -> None:
        super().load_snapshot(snapshot)
        if self._group_size_input is not None:
            self._group_size_input.set(snapshot.get("group_size", ""))
        #endif
    #enddef

    def parse_snapshot(self, snapshot: dict) -> PW:
        mode = snapshot["mode"]
        std = None
        if snapshot.get("std"):
            std = float(snapshot["std"])
        #endif
        if mode == PWMode.Fixed:
            return PW(float(snapshot["value"]), std=std)
        #endif
        if mode == PWMode.Uneven or mode == PWMode.Group:
            values = [float(v) for v in re.split(r"\s+", snapshot["value"])]
            group_size = None
            if snapshot.get("group_size"):
                group_size = int(snapshot["group_size"])
            #endif
            return PW(
                values,
                std=std,
                group_size=group_size
            )
        #endif
        raise RuntimeError("unreachable")
    #enddef
#endclass
