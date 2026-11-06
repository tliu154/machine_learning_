"""
np02 练习：广播与向量化
──────────────────────────────────────────────────
铁律：每个 for 循环都要问自己"能不能消掉"
"""

import numpy as np


# ---------- 1. 加法表（广播经典题） ----------
def addition_table(n, m):
    """
    返回 n×m 数组，元素 = 行号 + 列号。
    不许用 for —— 广播：列向量 + 行向量。
    提示：np.arange(n).reshape(-1, 1) + np.arange(m)
    """
    # TODO
    return None


# ---------- 2. 沿轴聚合 ----------
def col_means(m):
    """返回每列的均值（一维，长度=列数）"""
    # TODO
    return None


def row_max(m):
    """返回每行的最大值（一维，长度=行数）"""
    # TODO
    return None


# ---------- 3. 标准化 ----------
def normalize(a):
    """
    返回 (a - 均值) / 标准差 的数组。
    一维输入返回一维；不许用 for。
    标准差用 a.std()（总体标准差）。
    """
    # TODO
    return None


# ---------- 4. 归一化 ----------
def scale_to_01(a):
    """线性缩放到 [0, 1]：最小值→0，最大值→1。全相等时返回全 0"""
    # TODO
    return None


# ---------- 5. 距离与范数 ----------
def distance(u, v):
    """返回两个向量的欧氏距离（float）。用 np.linalg.norm"""
    # TODO
    return None


# ---------- 6. 外积（不用 np.outer） ----------
def outer_product(u, v):
    """返回 u 和 v 的外积矩阵 (i,j) 处 = u[i]*v[j]。用广播，不许用 np.outer"""
    # TODO
    return None


# ---------- 7. 加权平均 ----------
def weighted_average(values, weights):
    """返回加权平均（float）：sum(v*w)/sum(w)。用向量化，不许 for"""
    # TODO
    return None


# ---------- 8. 可复现随机 ----------
def reproducible_random(seed, n):
    """
    每次调用都返回【同样的】n 个 [0,1) 随机数（float 数组）。
    要求：多次调用结果 bit 级一致。
    提示：函数内部新建 np.random.default_rng(seed)
    """
    # TODO
    return None


# ---------- 9. 直线拟合 ----------
def fit_line(x, y):
    """
    最小二乘拟合 y = k*x + b，返回 (k, b) 浮点元组。
    提示：np.polyfit(x, y, 1)
    """
    # TODO
    return None


# ---------- 10. 批量旋转 ----------
def rotate_points(pts, degrees):
    """
    pts 是 (N, 2) 数组，绕原点逆时针旋转 degrees 度，返回新数组 (N, 2)。
    一行矩阵乘法搞定：pts @ R.T
    提示：np.deg2rad / cos / sin
    """
    # TODO
    return None


# ---------- 11. 消灭 for 循环 ----------
def signal_stats(signals):
    """
    signals 是 (N, M) 数组：N 个信号，每个 M 个采样点。
    返回 dict: {"mean": 每个信号的均值数组, "max": 每个信号的最大值数组,
                "argmax": 每个信号最大值位置数组}
    全部 axis 向量化，不许 for。
    """
    # TODO
    return None


# ---------- 12. 拼接与堆叠 ----------
def combine(a, b):
    """
    a, b 是同形状的二维数组。
    返回元组 (vertical, stacked)：
      vertical = 上下拼接（行数翻倍）
      stacked  = np.stack 出三维（形状前面多一维 2）
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    t = addition_table(3, 4)
    assert t.shape == (3, 4)
    assert t[0].tolist() == [0, 1, 2, 3]
    assert t[2, 3] == 5
    assert addition_table(1, 1).tolist() == [[0]]

    m = np.arange(12).reshape(3, 4).astype(float)
    assert np.allclose(col_means(m), [4, 5, 6, 7])
    assert row_max(m).tolist() == [3, 7, 11]

    a = np.array([1.0, 2.0, 3.0])
    z = normalize(a)
    assert np.allclose(z.mean(), 0)
    assert np.allclose(z.std(), 1)
    assert abs(z[2] - 1.2247448) < 1e-6

    assert np.allclose(scale_to_01(np.array([2, 4, 6])), [0, 0.5, 1])
    assert scale_to_01(np.array([5, 5, 5])).tolist() == [0, 0, 0]

    assert abs(distance(np.array([0, 0]), np.array([3, 4])) - 5) < 1e-9
    assert abs(distance(np.array([1, 1]), np.array([1, 1]))) < 1e-9

    op = outer_product(np.array([1, 2]), np.array([10, 20, 30]))
    assert op.shape == (2, 3)
    assert op.tolist() == [[10, 20, 30], [20, 40, 60]]

    assert abs(weighted_average(np.array([80, 90]), np.array([1, 3])) - 87.5) < 1e-9

    r1 = reproducible_random(42, 5)
    r2 = reproducible_random(42, 5)
    assert r1.shape == (5,)
    assert np.array_equal(r1, r2), "同样的 seed 必须产出完全一致的数组"
    assert not np.array_equal(reproducible_random(7, 5), reproducible_random(8, 5))

    x = np.array([0, 1, 2, 3, 4])
    y = np.array([1.1, 2.0, 3.2, 3.9, 5.1])
    k, b = fit_line(x, y)
    assert abs(k - 1.0) < 0.05
    assert abs(b - 1.0) < 0.1

    pts = np.array([[1, 0], [0, 1], [2, 2]])
    rot = rotate_points(pts, 90)
    assert np.allclose(rot, [[0, 1], [-1, 0], [-2, 2]])
    back = rotate_points(rotate_points(pts, 30), -30)
    assert np.allclose(back, pts)

    sig = np.array([[1, 5, 3], [9, 2, 8]])
    stats = signal_stats(sig)
    assert np.allclose(stats["mean"], [3, 6.33333333])
    assert stats["max"].tolist() == [5, 9]
    assert stats["argmax"].tolist() == [1, 0]

    a2 = np.ones((2, 3))
    b2 = np.zeros((2, 3))
    vertical, stacked = combine(a2, b2)
    assert vertical.shape == (4, 3)
    assert vertical[:2].tolist() == a2.tolist()
    assert stacked.shape == (2, 2, 3)
    assert stacked[0].tolist() == a2.tolist()

    print("np02 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def addition_table(n, m):
    return np.arange(n).reshape(-1, 1) + np.arange(m)

def col_means(m):
    return m.mean(axis=0)

def row_max(m):
    return m.max(axis=1)

def normalize(a):
    return (a - a.mean()) / a.std()

def scale_to_01(a):
    lo, hi = a.min(), a.max()
    if hi == lo:
        return np.zeros_like(a, dtype=float)
    return (a - lo) / (hi - lo)

def distance(u, v):
    return float(np.linalg.norm(u - v))

def outer_product(u, v):
    return u.reshape(-1, 1) * v.reshape(1, -1)

def weighted_average(values, weights):
    return float((values * weights).sum() / weights.sum())

def reproducible_random(seed, n):
    rng = np.random.default_rng(seed)
    return rng.random(n)

def fit_line(x, y):
    k, b = np.polyfit(x, y, 1)
    return (float(k), float(b))

def rotate_points(pts, degrees):
    theta = np.deg2rad(degrees)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return pts @ R.T

def signal_stats(signals):
    return {
        "mean": signals.mean(axis=1),
        "max": signals.max(axis=1),
        "argmax": signals.argmax(axis=1),
    }

def combine(a, b):
    vertical = np.vstack([a, b])
    stacked = np.stack([a, b])
    return (vertical, stacked)
"""
# endregion
