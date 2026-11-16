# lasercalc

激光加工常用参数计算库 —— 高斯光束、能量密度、脉冲参数。

纯 Python 标准库实现，无第三方依赖。面向激光焊接、切割、打孔、熔覆、表面处理等工艺场景，以及激光光学光路设计。

## 完整版：LIMA-Tools 微信小程序

本库是 **LIMA-Tools 激光智造工程计算器** 的核心计算内核（开源版）。完整版本已作为微信小程序上线，包含 10 个工程计算器，覆盖从光路设计到工艺参数的全流程，支持原理图实时渲染、能量密度云图、扫描轨迹可视化。

![LIMA-Tools 微信小程序：10 个工程计算器](docs/lima-tools-miniprogram.jpg)

**小程序功能覆盖**：

| 模块 | 说明 |
|---|---|
| 光路设计 | 从光纤到聚焦光斑，准直镜 / 扩束镜 / 聚焦镜实时渲染 |
| 能量密度 | 综合仿真与高斯云图（峰值 / 平均值 / 光斑面积） |
| 脉冲特性 | 单脉冲与搭接率（脉宽、重频、占空比、峰值功率） |
| 光斑计算 | 离焦光斑 w(z)、瑞利长度、发散角 |
| 工艺模式 | 连续 / 脉冲工艺参数换算 |
| 扫描轨迹 | 直线 / 圆形 / 8 字 / 正弦摆动与能量沉积 |
| 行业资讯 | 激光智造每日前沿速递 |
| 实时能量监测 | 工艺参数实时推算 |

特性：本地计算（无需联网）、工程级精度（科学可靠）、实时渲染（所见即所得）、随时随地（产线 / 会议 / 出差）。

> 微信搜索小程序「**LIMA-Tools**」或「**激光智造工程计算器**」即可使用；关注公众号「激光智造应用 LIMA」获取更新。

## 安装

```bash
pip install lima-lasercalc
```

或从源码：

```bash
git clone https://github.com/zhangyang99719-collab/lasercalc.git
cd lasercalc
pip install -e .
```

## 快速开始

```python
from lasercalc import gaussian, energy, pulse

# 高斯光束：腰斑 10um，波长 1064nm，离焦 0.5mm 处的光斑半径
zr = gaussian.rayleigh_length(10, 1064e-9, unit="um")     # 295.3 um
wz = gaussian.beam_radius(10, 500, 1064e-9, unit="um")    # 19.67 um

# 能量密度：单脉冲 1mJ，光斑半径 100um
f0 = energy.peak_fluence(1e-3, 100, unit="um")            # 6.37 J/cm²

# 脉冲参数：平均功率 200W，重频 50kHz，脉宽 100ns
e = pulse.pulse_energy(200, 50, freq_unit="kHz")          # 4 mJ
pp = pulse.peak_power(e, 100, time_unit="ns")             # 40 kW
```

命令行：

```bash
lasercalc gaussian --w0 10 --z 0.5 --wl 1064
lasercalc energy --pulse-energy 1 --w0 100
lasercalc pulse --power 200 --rep-rate 50 --width 100
```

## API 与公式

长度类函数统一通过 `unit=` 指定输入输出单位，返回与输入相同的单位。
支持 `m / mm / um / nm / cm`；时间 `s / ms / us / ns / ps / fs`；
功率 `W / kW / mW`；能量 `J / mJ / uJ / nJ`；频率 `Hz / kHz / MHz`。

### gaussian —— 高斯光束

采用 1/e² 强度半径定义（w0 为束腰半径）。

| 函数 | 公式 | 说明 |
|---|---|---|
| `rayleigh_length(w0, wl, m2, unit)` | z_R = π·w0² / (M²·λ) | 瑞利长度 |
| `beam_radius(w0, z, wl, m2, unit)` | w(z) = w0·√(1+(z/z_R)²) | 离焦光斑半径 |
| `peak_intensity(P, w0, unit)` | I0 = 2P/(π·w0²) | 峰值光强 W/m² |
| `average_intensity(P, w0, unit)` | I_avg = P/(π·w0²) | 平均光强 W/m² |
| `confocal_parameter(...)` | b = 2·z_R | 焦深范围 |
| `divergence_half_angle(w0, wl, m2, unit)` | θ = M²·λ/(π·w0) | 远场发散半角 rad |
| `M_squared(w0, θ, wl, unit)` | M² = π·w0·θ/λ | 光束质量因子 |

### energy —— 能量密度

高斯分布 F(r) = F0·exp(-2r²/w0²)，单脉冲能量 E = F0·π·w0²/2。

| 函数 | 公式 | 说明 |
|---|---|---|
| `peak_fluence(E, w0, unit)` | F0 = 2E/(π·w0²) | 峰值能量密度 J/m² |
| `average_fluence(E, w0, unit)` | F_avg = E/(π·w0²) = F0/2 | 面积平均 |
| `pulse_energy_from_fluence(F0, w0, unit)` | E = F0·π·w0²/2 | 反算脉冲能量 |
| `line_energy_density(P, v, ...)` | E_lin = P/v | 线能量密度 J/m |
| `pulse_overlap(D, f, v, ...)` | η = 1 - v/(f·D) | 脉冲重叠率 |
| `spot_area(w0, unit)` | A = π·w0² | 光斑面积 m² |

### pulse —— 脉冲参数

| 函数 | 公式 | 说明 |
|---|---|---|
| `average_power(E, f, ...)` | P_avg = E·f | 平均功率 W |
| `pulse_energy(P, f, ...)` | E = P/f | 单脉冲能量 J |
| `peak_power(E, τ, shape, ...)` | P_peak = E/τ（矩形）或 0.94E/τ（高斯 FWHM） | 峰值功率 W |
| `duty_cycle(f, τ, ...)` | D = f·τ | 占空比 |
| `rep_rate_from_duty(D, τ, ...)` | f = D/τ | 反算重频 |

## 工程注意事项

1. **1/e² 与 FWHM 的区别**：本库光斑半径均按 1/e² 强度定义。若你的测量设备给的是 FWHM 光斑直径，需先换算：w_1/e² ≈ FWHM/1.699。
2. **峰值 vs 平均**：高斯光斑的峰值能量密度是面积平均值的 2 倍，烧蚀阈值判断应使用峰值。
3. **脉宽与峰值功率**：`shape="rect"` 为方波近似；超短脉冲激光建议用 `shape="gauss"`（0.94 系数，τ 取 FWHM）。
4. **单位一致性**：所有 `unit` 参数同时作用于该函数的长度输入与返回值；波长 `wl` 始终以米传入。

## 测试

```bash
pip install -e ".[test]"
pytest tests/ -q
```

17 个单元测试覆盖解析值、单位换算、边界与异常输入。

## 关联项目

- **LIMA-Tools 微信小程序**：本库的完整图形化版本（10 个工程计算器 + 实时原理图 + 能量云图），微信搜索「LIMA-Tools」。
- **激光智造应用 LIMA**：技术公众号，激光制造行业应用资讯与工艺干货。

## License

MIT © 2026 LIMA
