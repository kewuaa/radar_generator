from dataclasses import dataclass

from .types import RadarParameter


@dataclass(eq=False, order=False)
class PA(RadarParameter):
    """ PA parameter."""

    value: float = -1
#endclass
