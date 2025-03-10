from dataclasses import dataclass
from loguru import logger

from .types import RadarParameter


@dataclass(eq=False, order=False)
class RF(RadarParameter):
    """ RF parameter."""

    value: float | list[float]
    std: float | None = None
    group_size: int | None = None
    random: bool = False

    def _field_check(self) -> None:
        if isinstance(self.value, (int, float)) and self.random:
            logger.warning("`float` value get, `randome` will be ignored")
        #endif
    #enddef
#endclass
