"""能量密度计算。

约定：激光加工中"能量密度"通常指峰值能量密度（脉冲能量/1/e² 光斑面积）。
本模块同时提供峰值与面积平均值，避免混淆。

高斯能量密度分布：F(r) = F0·exp(-2r²/w0²)
单脉冲能量 E = ∫F dA = F0·(π·w0²/2)  =>  F0 = 2E / (π·w0²)
"""

import math

from ._units import LENGTH, POWER, factor

_DEF_WAVELENGTH = 1064e-9


def peak_fluence(pulse_energy, w0, unit="m"):
    """峰值能量密度 F0（J/m²）= 2E / (π·w0²)。

    pulse_energy 单脉冲能量（J），w0 为 1/e² 光斑半径。
    """
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return 2 * pulse_energy / (math.pi * w0m ** 2)


def average_fluence(pulse_energy, w0, unit="m"):
    """面积平均能量密度（J/m²）= E / (π·w0²) = F0/2。"""
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return pulse_energy / (math.pi * w0m ** 2)


def pulse_energy_from_fluence(fluence, w0, unit="m"):
    """由峰值能量密度 F0 反求单脉冲能量 E（J）= F0·π·w0²/2。"""
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return fluence * math.pi * w0m ** 2 / 2


def line_energy_density(power, speed, power_unit="W", speed_unit="m/s"):
    """线能量密度（J/m）= P / v。典型用于激光焊接/切割/熔覆。

    speed 可为扫描速度（m/s、mm/s 等）。
    """
    p = power * factor(POWER, power_unit, "功率")
    SPEED = {"m/s": 1.0, "mm/s": 1e-3, "cm/s": 1e-2, "m/min": 1 / 60}
    v = speed * factor(SPEED, speed_unit, "速度")
    if v <= 0:
        raise ValueError("speed 必须为正数")
    return p / v


def pulse_overlap(spot_diameter, rep_rate, speed,
                  spot_unit="m", speed_unit="m/s", freq_unit="Hz"):
    """相邻脉冲重叠率 = 1 - v / (f·D)。

    其中 D 为光斑直径（2·w0），f 为重复频率，v 为扫描速度。
    speed >= f·D 时返回 0（无重叠）。返回值 0~1。
    """
    SPEED = {"m/s": 1.0, "mm/s": 1e-3, "cm/s": 1e-2, "m/min": 1 / 60}
    d = spot_diameter * factor(LENGTH, spot_unit, "长度")
    v = speed * factor(SPEED, speed_unit, "速度")
    f = rep_rate * factor({"Hz": 1.0, "kHz": 1e3, "MHz": 1e6}, freq_unit, "频率")
    if d <= 0 or f <= 0 or v < 0:
        raise ValueError("spot_diameter、rep_rate 必须为正，speed 非负")
    pitch = v / f
    return max(0.0, 1.0 - pitch / d)


def spot_area(w0, unit="m"):
    """1/e² 光斑圆面积（m²）= π·w0²。"""
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return math.pi * w0m ** 2
