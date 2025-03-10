import re
from enum import IntEnum

from PySide6.QtWidgets import (
    QVBoxLayout,
)

from ..radar.pri import PRI
from . import utils
from .base import ParameterBox


class PRIMode(IntEnum):
    """ pri mode."""

    Fixed = 0
    Uneven = 1
    Slip = 2
    Group = 3
    Jitter = 4
#endclass


class PRIBox(ParameterBox):
    """ GroupBox for PRI."""

    _range_layout: utils.RangeLayout | None = None
    _group_size_input: utils.InputLayout | None = None
    _jitter_rate_input: utils.InputLayout | None = None

    def __init__(self) -> None:
        super().__init__("PRI")
        self._mode_combo.addItems(PRIMode._member_names_)

        switchable_layout = QVBoxLayout()
        self._layout.addLayout(switchable_layout)

        def switch_layout(index: int) -> None:
            utils.clear_layout(switchable_layout)
            self._value_input.setEnabled(True)
            self._value_input.set("")
            self._std_input.setEnabled(True)
            self._std_input.set("")
            self._range_layout = None
            self._group_size_input = None
            self._jitter_rate_input = None

            if index == PRIMode.Slip:
                self._setup_slip(switchable_layout)
            elif index == PRIMode.Group:
                self._setup_group(switchable_layout)
            elif index == PRIMode.Jitter:
                self._setup_jitter(switchable_layout)
            #endif
        #enddef
        switch_layout(PRIMode.Fixed)
        self._mode_combo.currentIndexChanged.connect(switch_layout)
    #enddef

    def _setup_slip(self, layout: QVBoxLayout) -> None:
        self._value_input.setEnabled(False)
        self._range_layout = utils.RangeLayout()
        layout.addLayout(self._range_layout)
    #enddef

    def _setup_group(self, layout: QVBoxLayout) -> None:
        self._group_size_input = input = utils.InputLayout("group size")
        layout.addLayout(input)
    #enddef

    def _setup_jitter(self, layout: QVBoxLayout) -> None:
        self._std_input.setEnabled(False)
        self._jitter_rate_input = input = utils.InputLayout("jitter rate")
        layout.addLayout(input)
    #enddef

    def snapshot(self) -> dict:
        snapshot = super().snapshot()
        if self._range_layout is not None:
            snapshot.update(self._range_layout.snapshot())
        #endif
        if self._group_size_input is not None:
            snapshot["group_size"] = self._group_size_input.get()
        #endif
        if self._jitter_rate_input is not None:
            snapshot["jitter_rate"] = self._jitter_rate_input.get()
        #endif
        return snapshot
    #enddef

    def load_snapshot(self, snapshot: dict) -> None:
        super().load_snapshot(snapshot)
        if self._range_layout is not None:
            self._range_layout.load_snapshot(snapshot)
        #endif
        if self._group_size_input is not None:
            self._group_size_input.set(snapshot.get("group_size", ""))
        #endif
        if self._jitter_rate_input is not None:
            self._jitter_rate_input.set(snapshot.get("jitter_rate", ""))
        #endif
    #enddef

    def parse_snapshot(self, snapshot: dict) -> PRI:
        mode = snapshot["mode"]
        std = None
        if snapshot.get("std"):
            std = float(snapshot["std"])
        #endif
        if mode == PRIMode.Fixed:
            return PRI(float(snapshot["value"]), std=std)
        #endif
        if mode == PRIMode.Slip:
            assert self._range_layout is not None
            values = self._range_layout.parse_snapshot(snapshot)
            return PRI(values, std=std)
        #endif
        if mode == PRIMode.Uneven or mode == PRIMode.Group:
            values = [float(v) for v in re.split(r"\s+", snapshot["value"])]
            group_size = None
            if snapshot.get("group_size"):
                group_size = int(snapshot["group_size"])
            #endif
            return PRI(
                values,
                std=std,
                group_size=group_size
            )
        #endif
        if mode == PRIMode.Jitter:
            return PRI(
                float(snapshot["value"]),
                jitter_rate=float(snapshot["jitter_rate"])
            )
        #endif
        raise RuntimeError("unreachable")
    #enddef
#endclass
