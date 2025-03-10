from abc import abstractmethod
import random
from dataclasses import dataclass, field, asdict
from typing import Iterator

from loguru import logger

from .. import parameter
from ..parameter import Parameter


@dataclass(eq=True, order=True)
class PDW:
    """ Pulse Describe Word."""

    toa: float = field(compare=True)
    doa: float
    rf: float
    pw: float
    pa: float
    radar_id: int
#endclass


@dataclass(eq=False, order=False)
class RadarParameter:
    """ parameter of radar."""

    def __post_init__(self) -> None:
        self._field_check()
    #enddef

    @abstractmethod
    def _field_check(self) -> None:
        pass
    #enddef

    def get(self) -> Parameter:
        return parameter.init(**asdict(self))
    #enddef
#endclass


@dataclass(eq=False, order=False, repr=True)
class Radar:
    """ Base Radar Object."""

    id: int
    _start: float
    _pri: RadarParameter
    _doa: RadarParameter
    _rf: RadarParameter
    _pw: RadarParameter
    _pa: RadarParameter
    _loss_rate: float | None = None

    def __iter__(self) -> Iterator[PDW]:
        start = self._start
        for (pri, doa, rf, pw, pa) in zip(
            self._pri.get(),
            self._doa.get(),
            self._rf.get(),
            self._pw.get(),
            self._pa.get()
        ):
            start += pri
            if (
                self._loss_rate is not None
                and random.random() < self._loss_rate
            ):
                logger.debug(f"pulse at `{start}` lossed")
                continue
            #endif
            yield PDW(start, doa, rf, pw, pa, self.id)
        #endfor
    #enddef
#endclass
