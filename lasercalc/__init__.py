"""lasercalc - 激光加工常用参数计算库.

子模块:
    gaussian : 高斯光束（腰斑、瑞利长度、离焦光斑、峰值光强）
    energy   : 能量密度（高斯面能量密度、线能量密度、脉冲重叠率）
    pulse    : 脉冲参数（平均/峰值功率、重频、占空比、单脉冲能量）

所有函数只依赖 Python 标准库。长度默认单位 m，功率 W，能量 J，时间 s，
角度 rad。函数均提供 unit= 参数以切换常用工程单位。
"""

from . import gaussian, energy, pulse
from .gaussian import (
    beam_radius,
    rayleigh_length,
    peak_intensity,
    confocal_parameter,
)
from .energy import (
    peak_fluence,
    average_fluence,
    line_energy_density,
    pulse_overlap,
)
from .pulse import (
    average_power,
    peak_power,
    pulse_energy,
    duty_cycle,
)

__version__ = "0.1.0"
__all__ = [
    "gaussian", "energy", "pulse",
    "beam_radius", "rayleigh_length", "peak_intensity", "confocal_parameter",
    "peak_fluence", "average_fluence", "line_energy_density", "pulse_overlap",
    "average_power", "peak_power", "pulse_energy", "duty_cycle",
]
