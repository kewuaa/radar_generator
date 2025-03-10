import re
from enum import IntEnum

from PySide6.QtWidgets import (
    QCheckBox,
    QVBoxLayout,
)

from . import utils
from ..radar.rf import RF
from .base import ParameterBox


class RFMode(IntEnum):
    """ doc."""

    Fixed = 0
    GroupAgile = 1
#endclass


class RFBox(ParameterBox):
    """ doc."""

    _group_size_input: utils.InputLayout | None = None
    _random_checkbox: QCheckBox | None = None

    def __init__(self) -> None:
        super().__init__("RF")
        self._mode_combo.addItems(RFMode._member_names_)

        switchable_layout = QVBoxLayout()
        self._layout.addLayout(switchable_layout)
        def switch_layout(index: int) -> None:
            utils.clear_layout(switchable_layout)
            self._value_input.setEnabled(True)
            self._value_input.set("")
            self._std_input.setEnabled(True)
            self._std_input.set("")
            self._group_size_input = None
            self._random_checkbox = None

            if index == RFMode.GroupAgile:
                self._setup_agile_group(switchable_layout)
            #endif
        #enddef
        self._mode_combo.currentIndexChanged.connect(switch_layout)
    #enddef

    def _setup_agile_group(self, layout: QVBoxLayout) -> None:
        self._group_size_input = input = utils.InputLayout("group size")
        layout.addLayout(input)
        self._random_checkbox = checkbox = QCheckBox("random")
        layout.addWidget(checkbox)
    #enddef

    def snapshot(self) -> dict:
        snapshot = super().snapshot()
        if self._group_size_input is not None:
            snapshot["group_size"] = self._group_size_input.get()
        #endif
        if self._random_checkbox is not None:
            snapshot["random"] = self._random_checkbox.isChecked()
        #endif
        return snapshot
    #enddef

    def load_snapshot(self, snapshot: dict) -> None:
        super().load_snapshot(snapshot)
        if self._group_size_input is not None:
            self._group_size_input.set(snapshot.get("group_size", ""))
        #endif
        if self._random_checkbox is not None:
            self._random_checkbox.setChecked(snapshot.get("random", False))
        #endif
    #enddef

    def parse_snapshot(self, snapshot: dict) -> RF:
        mode = snapshot["mode"]
        std = None
        if snapshot.get("std"):
            std = float(snapshot["std"])
        #endif
        if mode == RFMode.Fixed:
            return RF(float(snapshot["value"]), std=std)
        #endif
        values = [float(v) for v in re.split(r"\s+", snapshot["value"])]
        group_size = None
        if snapshot.get("group_size"):
            group_size = int(snapshot["group_size"])
        #endif
        return RF(
            values,
            std=std,
            group_size=group_size,
            random=snapshot.get("random", False)
        )
    #enddef
#endclass
