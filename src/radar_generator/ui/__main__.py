import sys

import pyqtgraph as pg

from . import RadarGeneratorApp


if __name__ == "__main__":
    app = pg.mkQApp()
    ui = RadarGeneratorApp()
    ui.show()
    sys.exit(app.exec())
#endif
