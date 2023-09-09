import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def sph_irrep(l: int, char=None, rel=False, group: str = "Oh"):
    config = str(Path(".") / "config/charactors.yaml")
    chars, times = charactors(config=config, rel=rel, group=group)
    num = times.sum()
    if char is None:
        sph_char = char_spherical_harm(l=l)

        orthogonalize = ((chars * times) @ sph_char).apply(rounding)
    else:
        orthogonalize = ((chars * times) @ char).apply(rounding)
    return orthogonalize / num


def charactors(group: str = "Oh", rel: bool = True, config="config/charactors.yaml"):
    arg = get_args(config)[group]
    char = arg[f"relativistic {rel}"]
    char = pd.DataFrame.from_dict(char)
    num_times = pd.Series(arg["times"])
    return char.T, num_times


def get_args(config_name):
    # yamlファイルからパラメータの取得
    parser = argparse.ArgumentParser(description="YAMLありの例")
    parser.add_argument("-c", "--config", type=str, help="設定ファイル(.yaml)")
    args = parser.parse_args([f"-c={config_name}"])

    with open(args.config, "r") as f:
        print(f)
        config = yaml.safe_load(f)

    return config


def exp(theta, nrot) -> np.ndarray:
    return np.cos(theta / nrot)


def rounding(x: int, digit: int = 0):
    f, i = math.modf(x * 10 ** (-digit))
    if f >= 0.5:
        return (i + 1) * 10 ** (digit)
    else:
        return i * 10 ** (digit)


def char_spherical_harm(l: float):
    m = np.arange(-l, l + 1, 1)
    theta = m * 2 * np.pi
    # ---
    D_C4 = exp(theta, 4)
    D_C4_2 = exp(theta, 2)
    D_C2_p = D_C4_2
    D_C3 = exp(theta, 3)
    D_I = np.ones(shape=(m.size))
    D_E = D_I
    D_sigma_h = D_I * D_C2_p
    D_sigma_d = D_sigma_h
    D_IC4 = D_C4
    D_IC3 = D_C3
    char = {
        "E": D_E.sum(),
        "6C4": D_C4.sum(),
        "3C4^2": D_C4_2.sum(),
        "6C2'": D_C2_p.sum(),
        "8C^3": D_C3.sum(),
        "I": D_I.sum(),
        "6IC4": D_IC4.sum(),
        "3sigma": D_sigma_h.sum(),
        "6sigmad": D_sigma_d.sum(),
        "8IC^3": D_IC3.sum(),
    }
    return pd.Series(char)
