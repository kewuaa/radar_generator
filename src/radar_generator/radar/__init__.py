import heapq
from pathlib import Path
from typing import Iterator

import tomli

from .doa import DOA
from .pa import PA
from .pri import PRI
from .pw import PW
from .rf import RF
from .types import PDW, Radar


class Generator:
    """ radar Generator."""

    _radars: list[Radar]

    def __init__(self) -> None:
        self._radars = []
    #enddef

    def __iter__(self) -> Iterator[PDW]:
        iters = [iter(radar) for radar in self._radars]
        qq = [next(radar) for radar in iters]
        heapq.heapify(qq)
        while True:
            pdw = heapq.heappop(qq)
            yield pdw
            next_pdw = next(iters[pdw.radar_id])
            heapq.heappush(qq, next_pdw)
        #endwhile
    #enddef

    def add(self, radar: Radar) -> None:
        self._radars.append(radar)
    #enddef

    def clear(self) -> None:
        self._radars.clear()
    #enddef

    @classmethod
    def from_toml(cls, path: str | Path) -> "Generator":
        path = Path(path).absolute()
        if not path.exists():
            raise RuntimeError(f"`{path}` not exists")
        #endif
        with open(path, "rb") as f:
            config = tomli.load(f)
        #endwith
        if not isinstance(config, dict):
            raise RuntimeError("load config failed")
        #endif
        radars: list[dict] | None = config.get("radar", None)
        if radars is None:
            raise RuntimeError("`radar` field not found")
        #endif

        generator = cls()
        for i, radar in enumerate(radars):
            start: float = radar.get("start_toa", 0)
            pri_config: dict | None = radar.get("pri")
            doa_config: dict | None = radar.get("doa")
            rf_config: dict | None = radar.get("rf")
            pw_config: dict | None = radar.get("pw")
            if (
                pri_config is None
                or doa_config is None
                or rf_config is None
                or pw_config is None
            ):
                raise RuntimeError("loss radar field")
            #endif
            generator._radars.append(
                Radar(
                    i,
                    start,
                    PRI(**pri_config),
                    DOA(**doa_config),
                    RF(**rf_config),
                    PW(**pw_config),
                    PA(),
                    radar.get("loss_rate")
                )
            )
        #endfor
        return generator
    #enddef
#endclass
