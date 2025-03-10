from dataclasses import dataclass

from .types import RadarParameter


@dataclass(eq=False, order=False)
class PW(RadarParameter):
    """ PW parameter."""

    value: float | list[float]
    std: float | None
    group_size: int | None = None
#endclass
