"""
np03 练习：线性代数与图像
──────────────────────────────────────────────────
图像约定：uint8，灰度 (H, W)，彩色 (H, W, 3)，下标 [y, x]
每题都按"视觉组日常"来设计
"""

import numpy as np


# ---------- 1. 灰度化 ----------
def to_grayscale(color):
    """
    (H, W, 3) uint8 彩图 → (H, W) uint8 灰度图。
    权重（BGR 顺序）：B=0.114, G=0.587, R=0.299
    提示：color @ np.array([0.114, 0.587, 0.299])，注意转 uint8
    """
    # TODO
    return None


# ---------- 2. 反色 ----------
def invert(img):
    """黑变白、白变黑：255 - 值。返回同 dtype 的 uint8 数组"""
    # TODO
    return None


# ---------- 3. 二值化 ----------
def binarize(gray, threshold=127):
    """大于 threshold → 255，否则 → 0。返回 uint8"""
    # TODO
    return None


# ---------- 4. 裁剪 ROI ----------
def crop_roi(img, y1, y2, x1, x2):
    """返回行 [y1, y2)、列 [x1, x2) 的子区域（切片，视图即可）"""
    # TODO
    return None


# ---------- 5. 翻转 ----------
def flip_horizontal(img):
    """水平翻转（左右镜像）。返回新数组，不改原图"""
    # TODO
    return None


def flip_vertical(img):
    """垂直翻转（上下镜像）"""
    # TODO
    return None


# ---------- 6. 调亮（防溢出版） ----------
def brighten(img, delta):
    """
    每个像素加 delta（可为负），必须【不回绕】：uint8 溢出要截断到 [0, 255]。
    提示：astype 升位 → 加 → clip → 转回 uint8
    """
    # TODO
    return None


# ---------- 7. 下采样 ----------
def downsample2(img):
    """隔行隔列取样，高宽各减半"""
    # TODO
    return None


# ---------- 8. 通道统计 ----------
def channel_means(color):
    """返回 (B均值, G均值, R均值) 的浮点元组"""
    # TODO
    return None


# ---------- 9. 行投影 ----------
def row_projection(gray, threshold=127):
    """返回一维 int 数组：每行有多少像素 > threshold（找目标在哪些行时超好用）"""
    # TODO
    return None


# ---------- 10. 解线性方程组 ----------
def solve_linear(A, b):
    """解 Ax = b 返回解向量。用 np.linalg.solve"""
    # TODO
    return None


# ---------- 11. 最小二乘（不许用 polyfit） ----------
def least_squares_line(x, y):
    """
    用正规方程解最小二乘拟合 y = kx + b：
        A = [[x_0, 1], [x_1, 1], ...]
        解 A^T A [k, b]^T = A^T y
    返回 (k, b) 浮点元组。
    """
    # TODO: 拼出 A，然后 np.linalg.solve
    return None


# ---------- 12. 归一化 ----------
def normalize01(img):
    """uint8 → float32，值域压到 [0, 1]（喂网络前的标准操作）"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    color = np.array([
        [[100, 150, 200], [0, 0, 0]],
        [[255, 255, 255], [10, 20, 30]],
    ], dtype=np.uint8)          # (2, 2, 3)

    gray = to_grayscale(color)
    assert gray.shape == (2, 2)
    assert gray.dtype == np.uint8
    w = np.array([0.114, 0.587, 0.299])
    expected = (color.astype(np.float64) @ w).astype(np.uint8)
    assert gray.tolist() == expected.tolist()
    assert gray[1, 0] == 255

    g = np.array([[0, 128, 255]], dtype=np.uint8)
    assert invert(g).tolist() == [[255, 127, 0]]
    assert invert(g).dtype == np.uint8

    assert binarize(np.array([[10, 200]], dtype=np.uint8)).tolist() == [[0, 255]]
    assert binarize(np.array([[128]], dtype=np.uint8), 100).tolist() == [[255]]
    assert binarize(np.array([[100]], dtype=np.uint8), 100).tolist() == [[0]]

    m = np.arange(16).reshape(4, 4)
    assert crop_roi(m, 1, 3, 1, 3).tolist() == [[5, 6], [9, 10]]

    img = np.array([[1, 2], [3, 4]], dtype=np.uint8)
    assert flip_horizontal(img).tolist() == [[2, 1], [4, 3]]
    assert flip_vertical(img).tolist() == [[3, 4], [1, 2]]
    assert img.tolist() == [[1, 2], [3, 4]], "不允许修改原图"

    bright = brighten(np.array([[200, 10]], dtype=np.uint8), 100)
    assert bright.tolist() == [[255, 110]], "uint8 回绕了！"
    dark = brighten(np.array([[200, 10]], dtype=np.uint8), -100)
    assert dark.tolist() == [[100, 0]]

    big = np.arange(16).reshape(4, 4)
    assert downsample2(big).shape == (2, 2)
    assert downsample2(big).tolist() == [[0, 2], [8, 10]]

    means = channel_means(color)
    assert isinstance(means, tuple) and len(means) == 3
    assert np.allclose(means, color.mean(axis=(0, 1)))

    proj = row_projection(np.array([[200, 10, 200], [0, 0, 0]], dtype=np.uint8))
    assert proj.tolist() == [2, 0]

    x = solve_linear(np.array([[3.0, 1], [1, 2]]), np.array([9, 8]))
    assert np.allclose(x, [2, 3])
    assert np.allclose(np.array([[3, 1], [1, 2]]) @ x, [9, 8])

    xs = np.array([0.0, 1, 2, 3, 4])
    ys = np.array([1.1, 2.0, 3.2, 3.9, 5.1])
    k, b = least_squares_line(xs, ys)
    assert abs(k - 1.0) < 0.05
    assert abs(b - 1.0) < 0.1
    # 对照 polyfit 验证
    k2, b2 = np.polyfit(xs, ys, 1)
    assert abs(k - k2) < 1e-9 and abs(b - b2) < 1e-9

    n = normalize01(np.array([[0, 128, 255]], dtype=np.uint8))
    assert n.dtype == np.float32
    assert np.allclose(n, [[0, 128 / 255, 1]], atol=1e-6)

    print("np03 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def to_grayscale(color):
    weights = np.array([0.114, 0.587, 0.299])      # B G R
    return (color.astype(np.float64) @ weights).astype(np.uint8)

def invert(img):
    return 255 - img            # uint8 直接整体减，不会越界

def binarize(gray, threshold=127):
    return np.where(gray > threshold, 255, 0).astype(np.uint8)

def crop_roi(img, y1, y2, x1, x2):
    return img[y1:y2, x1:x2]

def flip_horizontal(img):
    return img[:, ::-1].copy()

def flip_vertical(img):
    return img[::-1, :].copy()

def brighten(img, delta):
    out = img.astype(np.int32) + delta
    return np.clip(out, 0, 255).astype(np.uint8)

def downsample2(img):
    return img[::2, ::2]

def channel_means(color):
    b, g, r = color[:, :, 0], color[:, :, 1], color[:, :, 2]
    return (float(b.mean()), float(g.mean()), float(r.mean()))

def row_projection(gray, threshold=127):
    return (gray > threshold).sum(axis=1).astype(int)

def solve_linear(A, b):
    return np.linalg.solve(np.asarray(A, dtype=float), np.asarray(b, dtype=float))

def least_squares_line(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    A = np.column_stack([x, np.ones_like(x)])   # 每行 [x_i, 1]
    k, b = np.linalg.solve(A.T @ A, A.T @ y)
    return (float(k), float(b))

def normalize01(img):
    return img.astype(np.float32) / 255.0
"""
# endregion
