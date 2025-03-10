import sys
import pandas as pd
import seaborn as sns
import pyqtgraph as pg
from matplotlib import pyplot as plt

from radar_generator import load_n
from radar_generator.ui import RadarGeneratorApp


if __name__ == "__main__":
    # load_n(size=3000)
    data = pd.read_csv("data.csv").head(716)
    print(data.groupby("RadarID").count())
    plt.subplot(121)
    sns.scatterplot(data, x="TOA", y="RF", hue="RadarID", palette="tab10")
    plt.subplot(122)
    sns.scatterplot(data, x="RF", y="PW", hue="RadarID", palette="tab10")
    plt.show()
    # app = pg.mkQApp()
    # ui = RadarGeneratorApp()
    # ui.show()
    # sys.exit(app.exec())
#endif
