from dataclasses import dataclass
from loguru import logger

from .types import RadarParameter


@dataclass(eq=False, order=False)
class PRI(RadarParameter):
    """ PRI parameter."""

    value: float | list[float]
    std: float | None = None
    jitter_rate: float | None = None
    group_size: int | None = None

    def _field_check(self) -> None:
        if isinstance(self.value, list):
            if self.jitter_rate is not None:
                logger.warning("`list` value got, `jitter_rate` will be ignored")
            #endif
        elif isinstance(self.value, (int, float)):
            if self.jitter_rate is not None and self.std is not None:
                logger.warning("`jitter_rate` got, `std` will be ignored")
            #endif
        #endif
    #enddef
#endclass
