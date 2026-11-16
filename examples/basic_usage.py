"""lasercalc 基础示例：一个完整的激光打孔工艺参数推算。

运行方式（任选其一）：
    pip install -e .          # 先安装本地包
    python examples/basic_usage.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lasercalc import gaussian, energy, pulse  # noqa: E402

# 场景：光纤激光 1064nm，聚焦后腰斑半径 20um，M²=1.3
W0 = 20          # um
WL = 1064e-9     # m
M2 = 1.3

print("=== 光束质量 ===")
zr = gaussian.rayleigh_length(W0, WL, M2, unit="um")
b = gaussian.confocal_parameter(W0, WL, M2, unit="um")
theta = gaussian.divergence_half_angle(W0, WL, M2, unit="um")
print(f"瑞利长度 z_R   : {zr:.1f} um")
print(f"焦深 b = 2 z_R : {b:.1f} um")
print(f"发散半角       : {theta*1e3:.2f} mrad")

print("\n=== 离焦影响（离焦 ±0.3mm）===")
for z in (-0.3, 0, 0.3):
    wz = gaussian.beam_radius(W0, z * 1e3, WL, M2, unit="um")
    print(f"z={z:+.1f}mm -> w={wz:.1f} um  (放大 {wz/W0:.2f}x)")

print("\n=== 能量密度（单脉冲 0.5mJ）===")
E = 0.5e-3
f0 = energy.peak_fluence(E, W0, unit="um")
print(f"峰值能量密度 F0 : {f0/1e4:.2f} J/cm²")
f_avg = energy.average_fluence(E, W0, unit="um")
print(f"面积平均        : {f_avg/1e4:.2f} J/cm²")

print("\n=== 脉冲与扫描参数（50W, 100kHz, 脉宽 200ns, 扫描 500mm/s）===")
P_AVG, F_REP, TAU, V = 50, 100e3, 200e-9, 500e-3
ep = pulse.pulse_energy(P_AVG, F_REP)
pp = pulse.peak_power(ep, TAU)
duty = pulse.duty_cycle(F_REP, TAU, percent=True)
ov = energy.pulse_overlap(2 * W0, F_REP, V,
                          spot_unit="um", speed_unit="m/s")
print(f"单脉冲能量 E    : {ep*1e3:.3f} mJ")
print(f"峰值功率        : {pp/1e3:.1f} kW")
print(f"占空比          : {duty:.2f} %")
print(f"脉冲重叠率      : {ov*100:.1f} %")
