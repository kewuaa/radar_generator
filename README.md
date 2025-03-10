# usage

`pip install -e .` to install project to site-packages.

## api

```python
import pandas as pd

from radar_generator import load_n, load_until

# load 1000 pulse
load_n(1000)
# load until time point 10000
load_until(10000)
# default load config from ./radars.toml, and data will be saved to ./data.csv
data = pd.read_csv("data.csv")
```

## ui

```sh
python -m radar_generator.ui
```
