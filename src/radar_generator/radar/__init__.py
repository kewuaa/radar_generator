import heapq
from typing import Iterator

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
#endclass
