import random
from itertools import cycle
from typing import Generator, TypeAlias, overload
Parameter: TypeAlias = Generator[float, None, None]


@overload
def init(value: float, *, std: float | None = None) -> Parameter: ...
@overload
def init(value: list[float], *, std: float | None = None) -> Parameter: ...
@overload
def init(value: list[float], *, std: float | None = None, group_size: int) -> Parameter: ...
@overload
def init(value: float, *, jitter_rate: float) -> Parameter: ...
@overload
def init(value: list[float], *, std: float | None = None, group_size: int | None = None, random: bool = True) -> Parameter: ...
def init(
    value: float | list[float],
    *,
    std: float | None = None,
    group_size: int | None = None,
    jitter_rate: float | None = None,
    random: bool = False
) -> Parameter:
    """initialize a parameter generator.

    @param value: base value to generator
    @param std: std of value
    @param group_size: specific for grouped change parameter
    @param jitter_rate: jitter rate for jitter change parameter
    @param random: if random choose value or not
    @return: a parameter generator
    """

    if isinstance(value, (float, int)):
        if jitter_rate is None:
            return _init_fixed_value(value, std)
        #endif
        return _init_jitter_value(value, jitter_rate)
    elif isinstance(value, list):
        if random:
            return _init_random_value(value, group_size, std)
        #endif
        if group_size is not None:
            value = [v for v in value for _ in range(group_size)]
        #endif
        return _init_list_value(value, std)
    else:
        raise ValueError(f"`float` or `list[float]` is needed, but `{type(value)}` got")
    #endif
#enddef


def _init_fixed_value(value: float, std: float | None) -> Parameter:
    while True:
        yield (
            value if std is None
            else random.gauss(value, std)
        )
    #endwhile
#enddef


def _init_list_value(value: list[float], std: float | None) -> Parameter:
    it = cycle(value)
    while True:
        v = next(it)
        if std is not None:
            v = random.gauss(v, std)
        #endif
        yield v
    #endwhile
#enddef


def _init_jitter_value(value: float, jitter_rate: float) -> Parameter:
    bound = value * jitter_rate
    while True:
        yield value + random.uniform(-bound, bound)
    #endwhile
#enddef


def _init_random_value(
    value: list[float],
    group_size: int | None,
    std: float | None,
) -> Parameter:
    group_size = group_size or 1
    while True:
        v = random.choice(value)
        for _ in range(group_size):
            if std is not None:
                v = random.gauss(v, std)
            #endif
            yield v
        #endfor
    #endwhile
#enddef
