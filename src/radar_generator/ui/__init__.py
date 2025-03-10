import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.graphicsItems.PlotDataItem import ScatterPlotItem
from pyqtgraph.Qt.QtCore import QObject, QPoint, QThread, Signal
from pyqtgraph.Qt.QtWidgets import QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from .. import RadarGenerator
from ..radar import Radar
from . import utils
from .doa import DOABox
from .pa import PABox
from .pri import PRIBox
from .pw import PWBox
from .rf import RFBox


class RadarConfigPanel(QFrame):
    """ doc."""

    _start_toa: utils.InputLayout
    _loss_rate: utils.InputLayout
    _pri: PRIBox
    _doa: DOABox
    _rf: RFBox
    _pw: PWBox
    _pa: PABox

    def __init__(self) -> None:
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self._start_toa = start_pri_input = utils.InputLayout("start toa")
        vbox.addLayout(start_pri_input)

        self._loss_rate = loss_rate_input = utils.InputLayout("loss rate")
        vbox.addLayout(loss_rate_input)

        self._pri = pri_box = PRIBox()
        vbox.addWidget(pri_box)

        self._doa = doa_box = DOABox()
        vbox.addWidget(doa_box)

        self._rf = rf_box = RFBox()
        vbox.addWidget(rf_box)

        self._pw = pw_box = PWBox()
        vbox.addWidget(pw_box)

        self._pa = pa_box = PABox()
        vbox.addWidget(pa_box)
    #enddef

    def clear(self) -> None:
        self._start_toa.set("")
        self._loss_rate.set("")
        self._pri.load_snapshot({})
        self._doa.load_snapshot({})
        self._rf.load_snapshot({})
        self._pw.load_snapshot({})
        self._pa.load_snapshot({})
    #enddef

    def snapshot(self) -> dict:
        return {
            "start_pri": self._start_toa.get(),
            "loss_rate": self._loss_rate.get(),
            "pri": self._pri.snapshot(),
            "doa": self._doa.snapshot(),
            "rf": self._rf.snapshot(),
            "pw": self._pw.snapshot(),
            "pa": self._pa.snapshot()
        }
    #enddef

    def load_snapshot(self, snapshot: dict) -> None:
        self._start_toa.set(snapshot.get("start_pri", ""))
        self._loss_rate.set(snapshot.get("loss_rate", ""))
        self._pri.load_snapshot(snapshot.get("pri", {}))
        self._doa.load_snapshot(snapshot.get("doa", {}))
        self._rf.load_snapshot(snapshot.get("rf", {}))
        self._pw.load_snapshot(snapshot.get("pw", {}))
        self._pa.load_snapshot(snapshot.get("pa", {}))
    #enddef

    def parse_snapshot(self, snapshot: dict) -> Radar:
        start_pri = 0
        if snapshot.get("start_pri"):
            start_pri = float(snapshot["start_pri"])
        #endif
        loss_rate = None
        if snapshot.get("loss_rate"):
            loss_rate = float(snapshot["loss_rate"])
        #endif
        return Radar(
            -1,
            start_pri,
            self._pri.parse_snapshot(snapshot["pri"]),
            self._doa.parse_snapshot(snapshot["doa"]),
            self._rf.parse_snapshot(snapshot["rf"]),
            self._pw.parse_snapshot(snapshot["pw"]),
            self._pa.parse_snapshot(snapshot["pa"]),
            loss_rate
        )
    #enddef
#endclass


class GenerateConfigDialog(QDialog):
    """ doc."""

    _pulse_num_input: QLineEdit
    _end_toa_input: QLineEdit
    _status_label: QLabel
    _canceled: bool

    def __init__(self) -> None:
        super().__init__(f=Qt.WindowType.Popup, modal=True)
        self._result = None

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        btn_group = QButtonGroup()

        btn = QRadioButton("pulse number: ")
        hbox.addWidget(btn)
        btn_group.addButton(btn)
        btn.setChecked(True)

        self._pulse_num_input = pulse_num = QLineEdit()
        hbox.addWidget(pulse_num)

        def toggled1(checked: bool) -> None:
            pulse_num.setEnabled(checked)
        #enddef
        btn.toggled.connect(toggled1)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        btn = QRadioButton("end toa: ")
        hbox.addWidget(btn)
        btn_group.addButton(btn)

        self._end_toa_input = end_toa = QLineEdit()
        hbox.addWidget(end_toa)
        end_toa.setEnabled(False)

        def toggled2(checked: bool) -> None:
            end_toa.setEnabled(checked)
        #enddef
        btn.toggled.connect(toggled2)

        self._status_label = status_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("color: red")
        vbox.addWidget(status_label)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        space = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding)
        hbox.addItem(space)

        cancel_button = QPushButton("cancel")
        hbox.addWidget(cancel_button)
        cancel_button.clicked.connect(self.cancel)

        accept_button = QPushButton("ok")
        hbox.addWidget(accept_button)
        accept_button.clicked.connect(self.accept)
    #enddef

    def cancel(self) -> None:
        self._canceled = True
        self.close()
    #enddef

    def canceled(self) -> bool:
        return self._canceled
    #enddef

    def accept(self) -> None:
        if self._pulse_num_input.isEnabled():
            if not self._pulse_num_input.text().isdigit():
                self._status_label.setText("invalid pulse number")
                return
            #endif
        elif self._end_toa_input.isEnabled():
            if not self._end_toa_input.text().replace(".", "").isdigit():
                self._status_label.setText("invalid end toa")
                return
            #endif
        #endif
        self._status_label.setText("")
        self._canceled = False
        self.close()
    #enddef

    def pulse_num(self) -> int | None:
        if self._pulse_num_input.isEnabled():
            return int(self._pulse_num_input.text())
        #endif
    #enddef

    def end_toa(self) -> float | None:
        if self._end_toa_input.isEnabled():
            return float(self._end_toa_input.text())
        #endif
    #enddef
#endclass

class GenerateWorker(QObject):
    """ doc."""

    generator: RadarGenerator
    save_path: str
    pulse_num: int | None
    end_toa: float | None
    done = Signal()

    def __init__(
        self,
        generator: RadarGenerator,
        save_path: str,
        pulse_num: int | None,
        end_toa: float | None,
    ) -> None:
        super().__init__()
        self.generator = generator
        self.save_path = save_path
        self.pulse_num = pulse_num
        self.end_toa = end_toa
    #enddef

    def do_work(self) -> None:
        it = iter(self.generator)
        if self.pulse_num is not None:
            with open(self.save_path, "w") as f:
                f.write("RadarID,TOA,DOA,RF,PW,PA\n")
                for _ in range(self.pulse_num):
                    pdw = next(it)
                    f.write(f"{pdw.radar_id},{pdw.toa},{pdw.doa},{pdw.rf},{pdw.pw},{pdw.pa}\n")
                #endfor
            #endwith
        elif self.end_toa is not None:
            with open(self.save_path, "w") as f:
                f.write("RadarID,TOA,DOA,RF,PW,PA\n")
                while (pdw := next(it)).toa < self.end_toa:
                    f.write(f"{pdw.radar_id},{pdw.toa},{pdw.doa},{pdw.rf},{pdw.pw},{pdw.pa}\n")
                #endwhile
            #endwith
        #endif
        self.done.emit()
        QThread.currentThread().quit()
    #enddef
#endclass


class RadarGeneratorApp(QMainWindow):
    """ doc."""

    _radars: list[dict[str, dict[str, str]]]
    _radar_panel: QListWidget
    _radar_config_panel: RadarConfigPanel
    _plot_widget: pg.GraphicsLayoutWidget

    def __init__(self) -> None:
        super().__init__()
        self._radars = []
        self._setup_ui()
    #enddef

    def _setup_ui(self) -> None:
        widget = QWidget()
        self.setCentralWidget(widget)

        hbox = QHBoxLayout()
        widget.setLayout(hbox)

        self._radar_panel = radar_panel = QListWidget()
        hbox.addWidget(radar_panel, 1)
        self._setup_radar_panel(radar_panel)

        self._radar_config_panel = config_panel = RadarConfigPanel()
        hbox.addWidget(config_panel, 1)

        plot_panel = QFrame()
        hbox.addWidget(plot_panel, 7)
        self._setup_plot_panel(plot_panel)

        config_panel.setEnabled(False)
    #enddef

    def _setup_radar_panel(self, panel: QListWidget) -> None:
        panel.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        radar_id = 0
        def new_radar() -> None:
            if not self._radar_config_panel.isEnabled():
                self._radar_config_panel.setEnabled(True)
            #endif

            self._radars.append({})

            nonlocal radar_id
            radar_id += 1
            self._radar_panel.addItem(f"radar{radar_id}")
            self._radar_panel.setCurrentRow(len(self._radars)-1)

            # clear after setting current row, otherwise previous snapshot will be empty
            self._radar_config_panel.clear()
        #enddef

        def delete_radar() -> None:
            row = panel.currentRow()
            self._radars.pop(row)
            panel.takeItem(row)
            if not self._radars:
                self._radar_config_panel.setEnabled(False)
            #endif
        #enddef

        def clear_radars() -> None:
            self._radars.clear()
            panel.clear()
            self._radar_config_panel.setEnabled(False)
        #enddef

        def show_menu(pos: QPoint) -> None:
            menu = QMenu()

            new_action = menu.addAction("new")
            new_action.triggered.connect(new_radar)
            if panel.itemAt(pos):
                delete_action = menu.addAction("delete")
                delete_action.triggered.connect(delete_radar)
            elif panel.count() > 0:
                clear_action = menu.addAction("clear")
                clear_action.triggered.connect(clear_radars)
            #endif

            menu.exec(panel.mapToGlobal(pos))
        #enddef
        panel.customContextMenuRequested.connect(show_menu)

        previous_row: int = -1
        def switch_config(row: int) -> None:
            nonlocal previous_row
            if previous_row >= 0 and self._radars:
                self._radars[previous_row] = self._radar_config_panel.snapshot()
            #endif
            previous_row = row
            if row < 0:
                return
            #endif
            self._radar_config_panel.load_snapshot(self._radars[row])
        #enddef
        panel.currentRowChanged.connect(switch_config)
    #enddef

    def _setup_plot_panel(self, panel: QFrame) -> None:
        panel.setFrameShape(QFrame.Shape.Box)

        vbox = QVBoxLayout()
        panel.setLayout(vbox)

        self._plot_widget = plot_widget = pg.GraphicsLayoutWidget()
        vbox.addWidget(plot_widget)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding)
        hbox.addItem(spacer)

        preview_button = QPushButton("preview")
        hbox.addWidget(preview_button)

        generate_button = QPushButton("generate")
        hbox.addWidget(generate_button)

        def scatterplot(
            plot: pg.PlotItem,
            data: pd.DataFrame,
            x: str,
            y: str,
            hue: str,
        ) -> None:
            plot.setLabel("left", y)
            plot.setLabel("bottom", x)
            scatter = ScatterPlotItem()
            scatter.setData(
                data[x].to_numpy(),
                data[y].to_numpy(),
                brush=data[hue].to_numpy()
            )
            plot.addItem(scatter)
        #enddef

        def get_generator() -> RadarGenerator:
            g = RadarGenerator()
            try:
                for i, snapshot in enumerate(self._radars):
                    radar = self._radar_config_panel.parse_snapshot(snapshot)
                    radar.id = i
                    g.add(radar)
                #endfor
            except Exception as e:
                raise e
            else:
                return g
        #enddef

        def preview() -> None:
            if not self._radars:
                QMessageBox(text="no radar configuration").exec()
                return
            #endif
            self._radars[self._radar_panel.currentRow()] = self._radar_config_panel.snapshot()
            try:
                g = get_generator()
            #endtry
            except Exception as e:
                QMessageBox(text=f"{type(e)}: {e}").exec()
            else:
                it = iter(g)
                pdws = [next(it) for _ in range(1000)]
                data = pd.DataFrame(pdws)
                plot_widget.clear() # pyright: ignore
                plot = plot_widget.addPlot(row=0, col=0) # pyright: ignore
                scatterplot(plot, data, "rf", "pw", "radar_id")
                plot = plot_widget.addPlot(row=0, col=1) # pyright: ignore
                scatterplot(plot, data, "doa", "rf", "radar_id")
                plot = plot_widget.addPlot(row=1, col=0) # pyright: ignore
                scatterplot(plot, data, "toa", "rf", "radar_id")
                plot = plot_widget.addPlot(row=1, col=1) # pyright: ignore
                plot.setLabel("left", "PRI")
                plot.setLabel("bottom", "index")
                scatter = ScatterPlotItem()
                pri = np.convolve(data["toa"].to_numpy(), [1, -1], "valid")
                scatter.setData(
                    np.array(range(pri.size)),
                    pri
                )
                plot.addItem(scatter)
            #endtry
        #enddef
        preview_button.clicked.connect(preview)

        t: QThread
        def generate() -> None:
            if not self._radars:
                QMessageBox(text="no radar configuration").exec()
                return
            #endif
            self._radars[self._radar_panel.currentRow()] = self._radar_config_panel.snapshot()
            try:
                g = get_generator()
            except Exception as e:
                QMessageBox(text=f"{type(e)}: {e}").exec()
            else:
                dialog = GenerateConfigDialog()
                dialog.show()
                pos = self.mapToGlobal(self.rect().center())
                dialog.move(pos - QPoint(dialog.width()//2, dialog.height()//2))
                dialog.exec()
                if dialog.canceled():
                    return
                #endif

                file_dialog = QFileDialog()
                file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
                file_dialog.setNameFilter("*.csv")
                file_dialog.setDefaultSuffix("csv")
                file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
                file_dialog.setDirectory(".")
                file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
                file_dialog.exec()
                save_path = ""
                if file_dialog.result() == QFileDialog.DialogCode.Accepted:
                    save_path = file_dialog.selectedFiles()[0]
                else:
                    return
                #endif
                nonlocal t
                t = QThread()
                worker = GenerateWorker(g, save_path, dialog.pulse_num(), dialog.end_toa())
                t.started.connect(worker.do_work)
                worker.done.connect(lambda: QMessageBox(text="generate done").exec())
                worker.moveToThread(t)
                t.start()
            #endtry
        #enddef
        generate_button.clicked.connect(generate)
    #enddef
#endclass
