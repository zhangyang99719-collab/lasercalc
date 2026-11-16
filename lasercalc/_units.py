"""内部单位换算工具（相对 SI 的倍率）。"""

# 长度 -> m
LENGTH = {
    "m": 1.0,
    "mm": 1e-3,
    "um": 1e-6, "µm": 1e-6, "micron": 1e-6,
    "nm": 1e-9,
    "cm": 1e-2,
}

# 时间 -> s
TIME = {
    "s": 1.0,
    "ms": 1e-3,
    "us": 1e-6, "µs": 1e-6, "ns": 1e-9,
    "ps": 1e-12, "fs": 1e-15,
}

# 功率 -> W
POWER = {"W": 1.0, "kW": 1e3, "mW": 1e-3, "MW": 1e6}

# 能量 -> J
ENERGY = {"J": 1.0, "mJ": 1e-3, "uJ": 1e-6, "µJ": 1e-6, "nJ": 1e-9}

# 频率 -> Hz
FREQ = {"Hz": 1.0, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}


def factor(table: dict, unit: str, kind: str) -> float:
    """返回单位换算倍率，未知单位抛出 ValueError 并给出可用选项。"""
    try:
        return table[unit]
    except KeyError:
        raise ValueError(
            f"未知{kind}单位 {unit!r}；可用: {', '.join(table)}"
        ) from None
