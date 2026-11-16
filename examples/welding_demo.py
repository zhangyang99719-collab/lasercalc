"""实战示例：光纤激光焊接/打孔工艺参数推算。

场景：光纤激光器 λ=1064nm，聚焦腰斑半径 50um，光束质量 M²=1.3，
平均功率 200W，重频 50kHz，脉宽 100ns，扫描速度 500mm/s。
"""

from lasercalc import gaussian, energy, pulse

# --- 已知工艺参数 ---
W0 = 50          # 束腰半径 um（1/e²）
M2 = 1.3         # 光束质量因子
WL = 1064e-9     # 波长 m
P_AVG = 200      # 平均功率 W
FREQ = 50        # 重频 kHz
WIDTH = 100      # 脉宽 ns
SPEED = 500      # 扫描速度 mm/s

print("=" * 44)
print(" 1. 光束质量 / 离焦")
zr = gaussian.rayleigh_length(W0, WL, M2, unit="um")
w_05 = gaussian.beam_radius(W0, 500, WL, M2, unit="um")  # 离焦 0.5mm=500um
theta = gaussian.divergence_half_angle(W0, WL, M2, unit="um")
print(f"  瑞利长度 z_R      : {zr/1000:8.3f} mm")
print(f"  离焦 0.5mm 光斑   : {w_05:8.2f} um")
print(f"  远场发散半角      : {theta*1e3:8.3f} mrad")

print("=" * 44)
print(" 2. 脉冲参数")
e_p = pulse.pulse_energy(P_AVG, FREQ, freq_unit="kHz")       # J
p_peak = pulse.peak_power(e_p, WIDTH, time_unit="ns", shape="gauss")
duty = pulse.duty_cycle(FREQ, WIDTH, freq_unit="kHz", time_unit="ns", percent=True)
print(f"  单脉冲能量        : {e_p*1e3:8.3f} mJ")
print(f"  峰值功率(高斯)    : {p_peak/1e3:8.2f} kW")
print(f"  占空比            : {duty:8.3f} %")

print("=" * 44)
print(" 3. 能量密度")
f0 = energy.peak_fluence(e_p, W0, unit="um")                 # J/m²
print(f"  峰值能量密度 F0   : {f0/1e4:8.2f} J/cm²")
print(f"  平均能量密度      : {energy.average_fluence(e_p, W0, unit='um')/1e4:8.2f} J/cm²")

print("=" * 44)
print(" 4. 扫描工艺")
led = energy.line_energy_density(P_AVG, SPEED, speed_unit="mm/s")  # J/m
ovl = energy.pulse_overlap(2 * W0, FREQ, SPEED, spot_unit="um",
                           speed_unit="mm/s", freq_unit="kHz")
print(f"  线能量密度        : {led:8.1f} J/m  ({led/1000:.3f} J/mm)")
print(f"  脉冲重叠率        : {ovl*100:8.1f} %")
print("=" * 44)
