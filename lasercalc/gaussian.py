"""高斯光束计算（基于 1/e² 强度半径定义）。

约定：
* w0 为束腰半径（1/e² 强度处），单位由 ``unit`` 指定，默认 m。
* 波长 wavelength 默认 1064 nm（Nd:YAG / 光纤激光常用）。
* M² = 1 表示理想基模高斯光束；实际光束 M² > 1。
* 瑞利长度 z_R = π·w0² / (M²·λ)；离焦光斑 w(z) = w0·sqrt(1+(z/z_R)²)。
"""

import math

from ._units import LENGTH, factor

_DEF_WAVELENGTH = 1064e-9  # m


def rayleigh_length(w0, wavelength=_DEF_WAVELENGTH, m2=1.0, unit="m"):
    """瑞利长度 z_R，返回与 ``unit`` 相同的单位。z_R = π·w0² / (M²·λ)。"""
    f = factor(LENGTH, unit, "长度")
    w0m = w0 * f
    if w0m <= 0 or wavelength <= 0 or m2 <= 0:
        raise ValueError("w0、wavelength、m2 必须为正数")
    return math.pi * w0m ** 2 / (m2 * wavelength) / f


def beam_radius(w0, z, wavelength=_DEF_WAVELENGTH, m2=1.0, unit="m"):
    """离焦 z 处的 1/e² 光斑半径，返回与输入相同的单位。

    w(z) = w0·sqrt(1 + (z/z_R)²)
    """
    f = factor(LENGTH, unit, "长度")
    w0m, zm = w0 * f, z * f
    if w0m <= 0 or wavelength <= 0 or m2 <= 0:
        raise ValueError("w0、wavelength、m2 必须为正数")
    zr = math.pi * w0m ** 2 / (m2 * wavelength)
    return (w0m * math.sqrt(1 + (zm / zr) ** 2)) / f


def peak_intensity(power, w0, unit="m"):
    """束腰处峰值光强 I0（W/m²）—— I(r)=I0·exp(-2r²/w0²)。

    I0 = 2P / (π·w0²)
    """
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return 2 * power / (math.pi * w0m ** 2)


def average_intensity(power, w0, unit="m"):
    """光斑圆形面积（π·w0²）上的平均光强 I_avg（W/m²）= P / (π·w0²)。

    注意：因高斯分布，I_avg = I0 / 2。
    """
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0:
        raise ValueError("w0 必须为正数")
    return power / (math.pi * w0m ** 2)


def confocal_parameter(w0, wavelength=_DEF_WAVELENGTH, m2=1.0, unit="m"):
    """共焦参数 b = 2·z_R（m），即焦深范围。"""
    return 2 * rayleigh_length(w0, wavelength, m2, unit)


def divergence_half_angle(w0, wavelength=_DEF_WAVELENGTH, m2=1.0, unit="m"):
    """远场发散半角 θ（rad）= M²·λ / (π·w0)。"""
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0 or wavelength <= 0 or m2 <= 0:
        raise ValueError("w0、wavelength、m2 必须为正数")
    return m2 * wavelength / (math.pi * w0m)


def M_squared(w0, divergence, wavelength=_DEF_WAVELENGTH, unit="m"):
    """由束腰半径和远场发散半角反求光束质量因子 M²。"""
    w0m = w0 * factor(LENGTH, unit, "长度")
    if w0m <= 0 or divergence <= 0 or wavelength <= 0:
        raise ValueError("w0、divergence、wavelength 必须为正数")
    return math.pi * w0m * divergence / wavelength
