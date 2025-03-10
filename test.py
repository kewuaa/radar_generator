from itertools import accumulate, cycle

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from scipy.stats import gaussian_kde

from radar_generator import parameter


def norm(arr: np.ndarray) -> np.ndarray:
    return (arr - arr.min()) / np.ptp(arr)
#enddef


def fixed_rf() -> None:
    p = parameter.init(1000, std=1)
    params = np.array([next(p) for _ in range(100)])
    # plt.grid(visible=True)
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.ylim(985, 1015)
    plt.scatter(range(params.size), params)
    plt.show()
#enddef

def slip_rf_rand() -> None:
    B = 10
    p = parameter.init(1000)
    params = np.array([next(p) for _ in range(100)])
    params = params + B*(np.random.random(params.size)*2 - 1)
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.ylim(980, 1020)
    plt.scatter(range(params.size), params)
    plt.hlines(1010, xmin=0, xmax=params.size, linestyles="dotted")
    plt.hlines(990, xmin=0, xmax=params.size, linestyles="dotted")
    plt.show()
#enddef


def slip_rf_step() -> None:
    T = 5
    step = 10
    size = 100
    p = parameter.init([i*step + 1000 for i in range(T)])
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*T for i in range(size//T+1)])
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def slip_rf_sin() -> None:
    B = 10
    T = 10
    size = 100
    p = parameter.init(1000)
    params = np.array([next(p) for _ in range(size)])
    bias = cycle(range(T))
    params = params + B*np.sin(2*np.pi * np.array([next(bias) for _ in range(size)]) / T)
    plt.grid(axis="x")
    plt.xticks([0+i*T for i in range(size//T+1)])
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def random_rf() -> None:
    size = 100
    p = parameter.init([1000, 2000, 1500, 500], random=True)
    params = np.array([next(p) for _ in range(size)])
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def group_rf() -> None:
    size = 100
    p = parameter.init([1000, 2000, 3000, 4000], group_size=5)
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*4*5 for i in range(size//(4*5)+1)])
    plt.xlabel("index")
    plt.ylabel("RF(MHz)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def fixed_pri() -> None:
    size = 50
    p = parameter.init(10)
    params = np.array([next(p) for _ in range(size)])
    plt.xlabel("index")
    plt.ylabel("PRI(μs)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def slip_pri() -> None:
    size = 30
    fig, axes = plt.subplots(2, 1, sharex=True, sharey=True)
    p = parameter.init([10, 20, 30, 40, 50])
    params = np.array([next(p) for _ in range(size)])
    axes[0].grid(axis="x")
    # axes[0].set_xlabel("index")
    axes[0].set_ylabel("PRI(μs)")
    axes[0].scatter(range(params.size), params)

    p = parameter.init([v for v in reversed([10, 20, 30, 40, 50])])
    params = np.array([next(p) for _ in range(size)])
    axes[1].grid(axis="x")
    axes[1].set_xlabel("index")
    axes[1].set_ylabel("PRI(μs)")
    axes[1].scatter(range(params.size), params)
    plt.show()
#enddef


def uneven_pri() -> None:
    size = 15
    p = parameter.init([10, 30, 20])
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*3 for i in range(size//3+1)])
    plt.xlabel("index")
    plt.ylabel("PRI(μs)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def group_pri() -> None:
    size = 15 * 3
    p = parameter.init([10, 30, 20], group_size=3)
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*9 for i in range(size//9+1)])
    plt.xlabel("index")
    plt.ylabel("PRI(μs)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def jitter_pri() -> None:
    size = 50
    p = parameter.init(10, jitter_rate=0.1)
    params = np.array([next(p) for _ in range(size)])
    plt.ylim(7, 13)
    plt.hlines(9, xmin=0, xmax=params.size, linestyles="dotted")
    plt.hlines(11, xmin=0, xmax=params.size, linestyles="dotted")
    plt.xlabel("index")
    plt.ylabel("PRI(μs)")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def slip_params() -> None:
    size = 20
    p = parameter.init([10, 20, 30, 40])
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*4 for i in range(size//4+1)])
    plt.xlabel("index")
    plt.ylabel("value")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def uneven_params() -> None:
    size = 20
    p = parameter.init([10, 30, 40, 20])
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*4 for i in range(size//4+1)])
    plt.xlabel("index")
    plt.ylabel("value")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef


def group_params() -> None:
    size = 40
    p = parameter.init([10, 30, 40, 20], std=0.1, group_size=5)
    params = np.array([next(p) for _ in range(size)])
    plt.grid(axis="x")
    plt.xticks([0+i*4*5 for i in range(size//(4*5)+1)])
    plt.xlabel("index")
    plt.ylabel("value")
    plt.scatter(range(params.size), params)
    plt.show()
#enddef
 

if __name__ == "__main__":
    group_rf()
#endif
