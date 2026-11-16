"""命令行入口：python -m lasercalc 或安装后的 lasercalc 命令。"""

import argparse

from . import gaussian, energy, pulse


def build_parser():
    p = argparse.ArgumentParser(
        prog="lasercalc",
        description="激光加工参数计算器（高斯光束 / 能量密度 / 脉冲参数）",
    )
    sub = p.add_subparsers(dest="cmd")

    g = sub.add_parser("gaussian", help="高斯光束计算")
    g.add_argument("--w0", type=float, required=True, help="束腰半径 1/e² (um)")
    g.add_argument("--z", type=float, default=0.0, help="离焦距离 (mm)")
    g.add_argument("--wl", type=float, default=1064, help="波长 (nm)")
    g.add_argument("--m2", type=float, default=1.0, help="光束质量因子 M²")

    e = sub.add_parser("energy", help="能量密度计算")
    e.add_argument("--pulse-energy", type=float, required=True, help="单脉冲能量 (mJ)")
    e.add_argument("--w0", type=float, required=True, help="光斑半径 1/e² (um)")

    q = sub.add_parser("pulse", help="脉冲参数计算")
    q.add_argument("--power", type=float, required=True, help="平均功率 (W)")
    q.add_argument("--rep-rate", type=float, required=True, help="重复频率 (kHz)")
    q.add_argument("--width", type=float, default=0.0, help="脉宽 (ns)，给出则算峰值功率")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "gaussian":
        w0_um, z_mm = args.w0, args.z
        wl = args.wl * 1e-9
        z_um = z_mm * 1e3  # CLI 输入 z 用 mm，内部统一 um
        zr_um = gaussian.rayleigh_length(w0_um, wl, args.m2, unit="um")
        wz = gaussian.beam_radius(w0_um, z_um, wl, args.m2, unit="um") if z_mm else w0_um
        theta = gaussian.divergence_half_angle(w0_um, wl, args.m2, unit="um")
        print(f"瑞利长度 z_R : {zr_um*1e-3:10.3f} mm")
        print(f"离焦光斑 w(z): {wz:10.3f} um  (z={z_mm} mm)")
        print(f"发散半角 θ   : {theta*1e3:10.3f} mrad")
    elif args.cmd == "energy":
        f0 = energy.peak_fluence(args.pulse_energy * 1e-3, args.w0, unit="um")
        favg = energy.average_fluence(args.pulse_energy * 1e-3, args.w0, unit="um")
        print(f"峰值能量密度 F0     : {f0/1e4:10.3f} J/cm²")
        print(f"面积平均能量密度    : {favg/1e4:10.3f} J/cm²")
    elif args.cmd == "pulse":
        ep = pulse.pulse_energy(args.power, args.rep_rate,
                                freq_unit="kHz")
        print(f"单脉冲能量 E  : {ep*1e3:10.4f} mJ")
        if args.width:
            pp = pulse.peak_power(ep, args.width, time_unit="ns")
            print(f"峰值功率 P_peak: {pp/1e3:10.3f} kW  (矩形近似)")
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
