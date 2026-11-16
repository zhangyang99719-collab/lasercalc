"""脉冲激光参数计算：平均功率、峰值功率、单脉冲能量、占空比。

基本关系：E = P_avg / f，P_peak ≈ E / τ（矩形脉冲近似）。
若按高斯时间脉冲，峰值功率需乘形状系数 ≈ 0.94（FWHM 定义）。
"""

from ._units import ENERGY, FREQ, POWER, TIME, factor


def average_power(pulse_energy, rep_rate, energy_unit="J", freq_unit="Hz"):
    """平均功率 P_avg（W）= E · f。"""
    e = pulse_energy * factor(ENERGY, energy_unit, "能量")
    f = rep_rate * factor(FREQ, freq_unit, "频率")
    if e < 0 or f <= 0:
        raise ValueError("pulse_energy 非负，rep_rate 必须为正")
    return e * f


def pulse_energy(average_power, rep_rate, power_unit="W", freq_unit="Hz"):
    """单脉冲能量 E（J）= P_avg / f。"""
    p = average_power * factor(POWER, power_unit, "功率")
    f = rep_rate * factor(FREQ, freq_unit, "频率")
    if p <= 0 or f <= 0:
        raise ValueError("average_power、rep_rate 必须为正")
    return p / f


def peak_power(pulse_energy, pulse_width, energy_unit="J",
               time_unit="s", shape="rect"):
    """峰值功率 P_peak（W）。

    shape="rect"  -> E / τ
    shape="gauss" -> 0.94 · E / τ  （τ 为 FWHM 脉宽）
    """
    e = pulse_energy * factor(ENERGY, energy_unit, "能量")
    t = pulse_width * factor(TIME, time_unit, "时间")
    if t <= 0:
        raise ValueError("pulse_width 必须为正数")
    k = {"rect": 1.0, "gauss": 0.94}.get(shape)
    if k is None:
        raise ValueError("shape 只能是 'rect' 或 'gauss'")
    return k * e / t


def duty_cycle(rep_rate, pulse_width, freq_unit="Hz", time_unit="s", percent=False):
    """占空比 = f · τ，默认返回 0~1 的小数；percent=True 返回百分数。"""
    f = rep_rate * factor(FREQ, freq_unit, "频率")
    t = pulse_width * factor(TIME, time_unit, "时间")
    d = f * t
    if d > 1:
        raise ValueError("占空比大于 1：脉宽与重频不匹配")
    return d * 100 if percent else d


def rep_rate_from_duty(duty, pulse_width, time_unit="s", percent=False):
    """由占空比与脉宽反求重复频率（Hz）。"""
    t = pulse_width * factor(TIME, time_unit, "时间")
    d = duty / 100 if percent else duty
    if t <= 0 or d <= 0:
        raise ValueError("duty、pulse_width 必须为正")
    return d / t
