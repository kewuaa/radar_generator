from PySide6.QtWidgets import QHBoxLayout, QLabel, QLayout, QLineEdit


class InputLayout(QHBoxLayout):
    """ layout with input."""

    _input: QLineEdit

    def __init__(self, name: str) -> None:
        super().__init__()
        label = QLabel(name+": ")
        self.addWidget(label)
        self._input = input = QLineEdit()
        self.addWidget(input)
    #enddef

    def setEnabled(self, enabled: bool) -> None:
        self._input.setEnabled(enabled)
    #enddef

    def get(self) -> str:
        return self._input.text()
    #enddef

    def set(self, text: str) -> None:
        self._input.setText(text)
    #enddef
#endclass


class RangeLayout(QHBoxLayout):
    """ layout with start, end and step."""

    _start: InputLayout
    _end: InputLayout
    _step: InputLayout

    def __init__(self) -> None:
        super().__init__()
        self._start = InputLayout("start")
        self.addLayout(self._start)
        self._end = InputLayout("end")
        self.addLayout(self._end)
        self._step = InputLayout("step")
        self.addLayout(self._step)
    #enddef

    def snapshot(self) -> dict:
        return {
            "start": self._start.get(),
            "end": self._end.get(),
            "step": self._step.get()
        }
    #enddef

    def load_snapshot(self, snapshot: dict) -> None:
        self._start.set(snapshot.get("start", ""))
        self._end.set(snapshot.get("end", ""))
        self._step.set(snapshot.get("step", ""))
    #enddef

    def parse_snapshot(self, snapshot: dict) -> list[float]:
        start = float(snapshot["start"])
        end = float(snapshot["end"])
        step_text = snapshot.get("step", "")
        step = (
            1.0 if not step_text
            else float(step_text)
        )

        values: list[float] = []
        value = start
        while value < end:
            values.append(value)
            value += step
        #endwhile
        return values
    #enddef
#endclass


def clear_layout(layout: QLayout):
    while layout.count(): 
        item = layout.takeAt(0)   # 取出第一个子项 
        widget = item.widget() 
        if widget:
            widget.deleteLater()   # 延迟释放控件内存 
        else:
            # 处理子布局或空白项
            sub_layout = item.layout() 
            if sub_layout:
                clear_layout(sub_layout)  # 递归删除子布局 
            else:
                spacer_item = item.spacerItem() 
                if spacer_item:
                    layout.removeItem(spacer_item) 
                #endif
            #endif
        #endif
    #endwhile
#enddef
