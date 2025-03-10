from .radar import Generator as RadarGenerator


def load_n(
    config: str = "radars.toml",
    save_path: str = "data.csv",
    *,
    size: int,
) -> None:
    generator = RadarGenerator.from_toml(config)
    it = iter(generator)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("RadarID,TOA,DOA,RF,PW,PA\n")
        for i in range(size):
            pdw = next(it)
            f.write(f"{pdw.radar_id},{pdw.toa},{pdw.doa},{pdw.rf},{pdw.pw},{pdw.pa}\n")
        #endfor
    #endwith
#enddef


def load_until(
    config: str = "radars.toml",
    save_path: str = "data.csv",
    *,
    end_toa: float
) -> None:
    generator = RadarGenerator.from_toml(config)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("RadarID,TOA,DOA,PW,PA\n")
        for pdw in generator:
            if pdw.toa > end_toa:
                break
            #endif
            f.write(f"{pdw.radar_id},{pdw.toa},{pdw.doa},{pdw.rf},{pdw.pw},{pdw.pa}\n")
        #endfor
    #endwith
#enddef
