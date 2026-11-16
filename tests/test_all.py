"""lasercalc 单元测试（标准库 unittest，零依赖）。"""

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lasercalc import gaussian, energy, pulse  # noqa: E402


class TestGaussian(unittest.TestCase):
    def test_rayleigh_length_ideal(self):
        # w0=10um, λ=1064nm, M²=1 -> z_R = π*(1e-5)^2/1.064e-6 ≈ 0.2953mm = 295.3um
        zr_um = gaussian.rayleigh_length(10, 1064e-9, 1.0, unit="um")
        self.assertAlmostEqual(zr_um, 295.3, places=0)
        self.assertAlmostEqual(zr_um * 1e-6, math.pi * (10e-6) ** 2 / 1064e-9, places=9)
        zr_m = gaussian.rayleigh_length(10e-6, 1064e-9, 1.0, unit="m")
        self.assertAlmostEqual(zr_m, 0.0002953, places=6)

    def test_rayleigh_scales_inverse_m2(self):
        z1 = gaussian.rayleigh_length(10, 1064e-9, 1.0, unit="um")
        z2 = gaussian.rayleigh_length(10, 1064e-9, 2.0, unit="um")
        self.assertAlmostEqual(z1, 2 * z2, places=9)

    def test_beam_radius_at_rayleigh(self):
        # z = z_R 时 w = sqrt(2)·w0
        w0 = 10  # um
        zr_um = gaussian.rayleigh_length(w0, 1064e-9, unit="um")
        wz = gaussian.beam_radius(w0, zr_um, 1064e-9, unit="um")
        self.assertAlmostEqual(wz, w0 * math.sqrt(2), places=6)

    def test_beam_radius_zero_defocus(self):
        self.assertAlmostEqual(
            gaussian.beam_radius(15, 0, 1064e-9, unit="um"), 15, places=9)

    def test_peak_average_intensity_ratio(self):
        i0 = gaussian.peak_intensity(100, 20, unit="um")
        iavg = gaussian.average_intensity(100, 20, unit="um")
        self.assertAlmostEqual(i0, 2 * iavg, places=3)
        # 光斑内积分应等于总功率
        self.assertAlmostEqual(iavg * math.pi * (20e-6) ** 2, 100, places=6)

    def test_divergence_m2(self):
        th = gaussian.divergence_half_angle(10, 1064e-9, unit="um")
        m2 = gaussian.M_squared(10, th, 1064e-9, unit="um")
        self.assertAlmostEqual(m2, 1.0, places=9)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            gaussian.rayleigh_length(0)


class TestEnergy(unittest.TestCase):
    def test_peak_fluence(self):
        # E=1mJ, w0=100um -> F0 = 2e-3 / (π·(1e-4)^2) ≈ 63662 J/m² = 6.366 J/cm²
        f0 = energy.peak_fluence(1e-3, 100, unit="um")
        self.assertAlmostEqual(f0 / 1e4, 6.3662, places=3)
        self.assertAlmostEqual(f0, 2 * energy.average_fluence(1e-3, 100, unit="um"))

    def test_fluence_roundtrip(self):
        e = 0.5e-3
        f0 = energy.peak_fluence(e, 50, unit="um")
        self.assertAlmostEqual(energy.pulse_energy_from_fluence(f0, 50, unit="um"), e)

    def test_line_energy_density(self):
        # P=200W, v=100mm/s -> 200 / 0.1 = 2000 J/m = 2 J/mm
        led = energy.line_energy_density(200, 100, power_unit="W", speed_unit="mm/s")
        self.assertAlmostEqual(led, 2000, places=6)
        led2 = energy.line_energy_density(200, 6, power_unit="W", speed_unit="m/min")
        self.assertAlmostEqual(led2, 2000, places=6)

    def test_pulse_overlap(self):
        # D=100um, f=100kHz, v=500mm/s -> pitch=5um, overlap=0.95
        ov = energy.pulse_overlap(100, 100, 500,
                                  spot_unit="um", speed_unit="mm/s", freq_unit="kHz")
        self.assertAlmostEqual(ov, 0.95, places=9)
        # 无重叠情况
        ov0 = energy.pulse_overlap(10, 1, 100,
                                   spot_unit="um", speed_unit="mm/s", freq_unit="kHz")
        self.assertEqual(ov0, 0.0)

    def test_spot_area(self):
        self.assertAlmostEqual(energy.spot_area(1, unit="mm"), math.pi * 1e-6)


class TestPulse(unittest.TestCase):
    def test_average_power(self):
        # 1mJ @ 20kHz = 20W
        self.assertAlmostEqual(
            pulse.average_power(1, 20, energy_unit="mJ", freq_unit="kHz"), 20)

    def test_pulse_energy_roundtrip(self):
        p = pulse.average_power(2.5, 100, energy_unit="mJ", freq_unit="kHz")
        self.assertAlmostEqual(pulse.pulse_energy(p, 100, freq_unit="kHz"), 2.5e-3)

    def test_peak_power(self):
        # 1mJ / 100ns = 10kW
        self.assertAlmostEqual(
            pulse.peak_power(1, 100, energy_unit="mJ", time_unit="ns"), 1e4)
        # 高斯形状系数 0.94
        self.assertAlmostEqual(
            pulse.peak_power(1, 100, energy_unit="mJ", time_unit="ns", shape="gauss"),
            0.94e4)

    def test_duty_cycle(self):
        # 100kHz × 100ns = 0.01 = 1%
        d = pulse.duty_cycle(100, 100, freq_unit="kHz", time_unit="ns")
        self.assertAlmostEqual(d, 0.01, places=9)
        d2 = pulse.duty_cycle(100, 100, freq_unit="kHz", time_unit="ns", percent=True)
        self.assertAlmostEqual(d2, 1.0, places=9)
        f = pulse.rep_rate_from_duty(0.01, 100, time_unit="ns")
        self.assertAlmostEqual(f, 1e5, places=6)

    def test_invalid_shape(self):
        with self.assertRaises(ValueError):
            pulse.peak_power(1e-3, 1e-9, shape="triangle")


if __name__ == "__main__":
    unittest.main()
