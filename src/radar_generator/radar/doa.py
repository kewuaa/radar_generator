from dataclasses import dataclass

from .types import RadarParameter


@dataclass(eq=False, order=False)
class DOA(RadarParameter):
    """ DOA parameter."""

    value: float
    std: float | None = None
#endclass
