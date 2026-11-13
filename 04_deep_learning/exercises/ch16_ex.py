"""
ch16 练习：训练深度网络（Training Deep Networks）
──────────────────────────────────────────────────
重点：SGD / Momentum / Adam 的更新式与偏差修正、cosine / step 学习率调度、
      BatchNorm / LayerNorm、running stats、Dropout 的 inverted scaling、
      残差连接的恒等支路，最后用几何平均判断「数值是不是在逐层放大」。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch16_training_dnn.md

说明：本文件是 ML 全局第 16 章。00_foundations/python_basics/exercises/
只到 ch12（基础教程自己的章号），这里没有同名文件，按完整路径打开即可。

本练习只用 numpy，不用 PyTorch / sklearn，不依赖仓库外文件。
教学文档里的所有数字来自同一套固定 seed，注释里标了出处。
"""

import numpy as np


# ---------- 公共工具（已给实现，不是题目） ----------
_H = np.array([1.0, 100.0])          # 病态二次型的曲率：条件数 100


def quad_loss(w):
    """f(w) = 0.5 * (w0^2 + 100 * w1^2)。"""
    return 0.5 * float(np.sum(_H * np.asarray(w, dtype=float) ** 2))


def quad_grad(w):
    """梯度 = H * w。"""
    return _H * np.asarray(w, dtype=float)


# ---------- 第 1 题：SGD 一步 / 锚点 c16-01 ----------
def sgd_step(w, g, lr):
    """返回 w - lr * g（不改原 w）。"""
    # TODO
    return None


# ---------- 第 2 题：Momentum 一步 / 锚点 c16-01 ----------
def momentum_step(w, v, g, lr=0.01, beta=0.9):
    """v_new = beta * v + g；返回 (w - lr * v_new, v_new)。"""
    # TODO
    return None


# ---------- 第 3 题：Adam 一步 / 锚点 c16-01 ----------
def adam_step(w, m, v, g, t, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8):
    """标准 Adam（含偏差修正）。t 从 1 开始计数。
    返回 (w_new, m_new, v_new)。"""
    # TODO
    return None


# ---------- 第 4 题：偏差修正的第一步 / 锚点 c16-01 ----------
def adam_first_step(lr=0.1, correct=True):
    """常数梯度 g=1、初值 w=0 时，Adam 第 1 步的位移绝对值。
    correct=False 表示不做偏差修正（直接 m / sqrt(v)）。"""
    # TODO
    return None


# ---------- 第 5 题：cosine 调度 / 锚点 c16-02 ----------
def cosine_lr(t, total, lr_max, warmup=0):
    """前 warmup 步线性爬升，之后按余弦从 lr_max 降到 0。t 从 0 开始。"""
    # TODO
    return None


# ---------- 第 6 题：step decay / 锚点 c16-02 ----------
def step_lr(t, total, lr_max, drops=(0.5, 0.75)):
    """每越过一个 drops 里的比例就砍到 1/10。t 从 0 开始。"""
    # TODO
    return None


# ---------- 第 7 题：批统计量 / 锚点 c16-03 ----------
def batch_stats(z):
    """沿 batch 维（axis=0）求每个特征的 (均值, 方差)，方差用 ddof=0。"""
    # TODO
    return None


# ---------- 第 8 题：running stats 更新 / 锚点 c16-03 ----------
def update_running(running, batch_value, momentum=0.1):
    """PyTorch 语义：new = (1 - momentum) * running + momentum * batch_value。"""
    # TODO
    return None


# ---------- 第 9 题：LayerNorm / 锚点 c16-03 ----------
def layer_norm(z, gamma, beta, eps=1e-5):
    """沿特征维（axis=1）归一化：每个样本自己算一套均值和方差。"""
    # TODO
    return None


# ---------- 第 10 题：Dropout 掩码 / 锚点 c16-04 ----------
def dropout_mask(shape, p, seed=0):
    """inverted dropout 的掩码：被保留的位置是 1/(1-p)，被丢弃的位置是 0。
    返回与 shape 同形的 float 数组。"""
    # TODO
    return None


# ---------- 第 11 题：残差的恒等支路 / 锚点 c16-04 ----------
def residual_forward(x, W):
    """不加缩放的残差块：y = relu(x @ W) + x。"""
    # TODO
    return None


# ---------- 第 12 题：判断数值是否逐层放大 / 锚点 c16-05 ----------
def per_layer_ratio(stds):
    """给一串逐层统计量（std / 梯度范数 / loss 都行），
    返回相邻两层之间的平均放大倍数（几何平均）。"""
    # TODO
    return None


if __name__ == "__main__":
    # ---- 第 1 题 ----
    w1 = sgd_step(np.array([1.0, 1.0]), np.array([1.0, 100.0]), 0.018)
    assert np.allclose(w1, [0.982, -0.8]), w1

    def run_sgd(lr, steps):
        w = np.array([1.0, 1.0])
        for _ in range(steps):
            w = sgd_step(w, quad_grad(w), lr)
        return quad_loss(w)

    # 文档 16.1：lr=0.018 第 362 步首次 < 1e-6
    assert run_sgd(0.018, 300) > 1e-6
    assert run_sgd(0.018, 362) < 1e-6
    # lr=0.020 踩到稳定上限 2/λmax，600 步后仍在 50 附近
    assert 40 < run_sgd(0.020, 600) < 60

    # ---- 第 2 题 ----
    wn, vn = momentum_step(np.array([1.0, 1.0]), np.zeros(2),
                           np.array([1.0, 100.0]), lr=0.0018, beta=0.9)
    assert np.allclose(vn, [1.0, 100.0])
    assert np.allclose(wn, [1.0 - 0.0018, 1.0 - 0.18])

    def run_momentum(lr, steps):
        w, v = np.array([1.0, 1.0]), np.zeros(2)
        for _ in range(steps):
            w, v = momentum_step(w, v, quad_grad(w), lr=lr, beta=0.9)
        return quad_loss(w)

    # 文档 16.1：Momentum lr=0.0018 第 299 步达标
    assert run_momentum(0.0018, 299) < 1e-6
    assert run_momentum(0.0015, 375) < 1e-6
    assert run_momentum(0.0015, 340) > 1e-6

    # ---- 第 3 题 ----
    w, m, v = adam_step(np.array([0.0]), 0.0, 0.0, np.array([1.0]), t=1, lr=0.1)
    assert np.isclose(abs(w[0]), 0.1), w          # 有修正：第一步恰好 lr
    w, m, v = adam_step(np.array([0.0]), 0.0, 0.0, np.array([1.0]), t=1,
                        lr=0.1, b1=0.9, b2=0.999)
    assert np.isclose(abs(w[0]), 0.1)

    def run_adam(lr, steps):
        w, m, v = np.array([1.0, 1.0]), np.zeros(2), np.zeros(2)
        for t in range(1, steps + 1):
            w, m, v = adam_step(w, m, v, quad_grad(w), t, lr=lr)
        return quad_loss(w)

    # 文档 16.1：Adam lr=0.1 第 82 步达标
    assert run_adam(0.1, 82) < 1e-6
    assert run_adam(0.1, 70) > 1e-6

    # ---- 第 4 题 ----
    assert np.isclose(adam_first_step(0.1, correct=True), 0.1)
    # 无修正：0.1 / sqrt(0.001) * 0.1 = 0.316228
    assert np.isclose(adam_first_step(0.1, correct=False), 0.31622776601, atol=1e-9)
    assert adam_first_step(0.1, correct=False) > 3 * adam_first_step(0.1, correct=True)

    # ---- 第 5 题 ----
    assert np.isclose(cosine_lr(0, 100, 1.0), 1.0)
    assert np.isclose(cosine_lr(50, 100, 1.0), 0.5)
    assert np.isclose(cosine_lr(100, 100, 1.0), 0.0, atol=1e-12)
    # warmup=10：第 0 步只有峰值 1/10
    assert np.isclose(cosine_lr(0, 100, 1.0, warmup=10), 0.1)
    assert np.isclose(cosine_lr(9, 100, 1.0, warmup=10), 1.0)

    # ---- 第 6 题 ----
    assert np.isclose(step_lr(10, 100, 1.0), 1.0)
    assert np.isclose(step_lr(50, 100, 1.0), 0.1)
    assert np.isclose(step_lr(75, 100, 1.0), 0.01)
    assert np.isclose(step_lr(99, 100, 1.0), 0.01)

    # ---- 第 7 题 ----
    z = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    mu, var = batch_stats(z)
    assert np.allclose(mu, [3.0, 4.0])
    assert np.allclose(var, [8.0 / 3.0, 8.0 / 3.0])

    # ---- 第 8 题 ----
    assert np.isclose(update_running(0.0, 3.0, 0.1), 0.3)
    assert np.isclose(update_running(1.0, 3.0, 0.1), 1.2)
    r = 0.0
    for _ in range(50):
        r = update_running(r, 1.0, 0.1)
    assert 0.99 < r <= 1.0, r          # 跑够多步会收敛到批次值

    # ---- 第 9 题 ----
    y = layer_norm(z, np.ones(2), np.zeros(2))
    assert np.allclose(y[0], [-1.0, 1.0], atol=1e-4)
    assert np.allclose(y.mean(axis=1), 0.0, atol=1e-9)      # 每个样本均值为 0
    assert np.allclose(y.std(axis=1), 1.0, atol=1e-4)       # 每个样本 std 为 1

    # ---- 第 10 题 ----
    mask = dropout_mask((1000, 100), 0.5, seed=0)
    assert set(np.unique(mask)) <= {0.0, 2.0}
    assert abs((mask == 0).mean() - 0.5) < 0.01            # 文档 16.4：置零 0.5025
    assert abs(mask.mean() - 1.0) < 0.01                   # 期望保持为 1
    mask2 = dropout_mask((1000, 100), 0.2, seed=0)
    assert abs((mask2 == 0).mean() - 0.2) < 0.01

    # ---- 第 11 题 ----
    x = np.array([[1.0, -2.0], [3.0, 0.5]])
    W0 = np.zeros((2, 2))
    out = residual_forward(x, W0)
    assert np.allclose(out, x)               # W=0 时整块退化成恒等映射
    W = np.array([[1.0, 0.0], [0.0, -1.0]])
    out = residual_forward(x, W)
    assert np.allclose(out, x + np.maximum(x @ W, 0))

    # ---- 第 12 题 ----
    no_bn = [3.292, 15.27, 52.94, 206.6, 1010.0, 4055.0, 20320.0]
    with_bn = [0.586, 0.592, 0.610, 0.598, 0.619, 0.613, 0.635]
    assert np.isclose(per_layer_ratio(no_bn), 4.284, atol=0.01)    # 约 4.3 倍
    assert np.isclose(per_layer_ratio(with_bn), 1.0135, atol=0.001)  # 约 1.01 倍
    assert per_layer_ratio([1.0, 1.0, 1.0]) == 1.0

    print("ch16 全部通过 ✓")


# region 参考答案
"""
def sgd_step(w, g, lr):
    return w - lr * g


def momentum_step(w, v, g, lr=0.01, beta=0.9):
    v = beta * v + g
    return w - lr * v, v


def adam_step(w, m, v, g, t, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8):
    m = b1 * m + (1 - b1) * g
    v = b2 * v + (1 - b2) * g * g
    mh = m / (1 - b1 ** t)
    vh = v / (1 - b2 ** t)
    return w - lr * mh / (np.sqrt(vh) + eps), m, v


def adam_first_step(lr=0.1, correct=True):
    g = 1.0
    m = 0.1 * g
    v = 0.001 * g * g
    if correct:
        mh, vh = m / (1 - 0.9), v / (1 - 0.999)
    else:
        mh, vh = m, v
    return float(abs(lr * mh / np.sqrt(vh)))


def cosine_lr(t, total, lr_max, warmup=0):
    if warmup and t < warmup:
        return lr_max * (t + 1) / warmup
    p = (t - warmup) / max(1, total - warmup)
    return lr_max * 0.5 * (1 + np.cos(np.pi * p))


def step_lr(t, total, lr_max, drops=(0.5, 0.75)):
    k = sum(t >= int(total * d) for d in drops)
    return lr_max * (0.1 ** k)


def batch_stats(z):
    return z.mean(axis=0), z.var(axis=0)


def update_running(running, batch_value, momentum=0.1):
    return (1 - momentum) * running + momentum * batch_value


def layer_norm(z, gamma, beta, eps=1e-5):
    mu = z.mean(axis=1, keepdims=True)
    var = z.var(axis=1, keepdims=True)
    return gamma * (z - mu) / np.sqrt(var + eps) + beta


def dropout_mask(shape, p, seed=0):
    rng = np.random.default_rng(seed)
    return (rng.random(shape) > p) / (1.0 - p)


def residual_forward(x, W):
    return np.maximum(x @ W, 0) + x


def per_layer_ratio(stds):
    stds = np.asarray(stds, dtype=float)
    return float((stds[-1] / stds[0]) ** (1.0 / (len(stds) - 1)))
"""
# endregion
