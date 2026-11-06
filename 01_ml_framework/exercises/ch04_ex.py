"""
ch04 练习：训练三步骤（Three Steps of Training）
──────────────────────────────────────────────────
对应章节：docs/ch04_training_steps.md
重点：模型 → 损失 → 梯度下降 → 训练循环；数值梯度检验；学习率发散
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本文件是【ML 第 4 章】的练习，
与 00_foundations/python_basics/exercises/ch04_ex.py（列表与元组）不是同一份。
"""

import numpy as np


# ---------- 1. 模型前向（锚点 c04-01） ----------
def linear_predict(x, w, b):
    """返回 y_hat = w*x + b，x 可以是 list 或 ndarray"""
    # TODO
    return None


# ---------- 2. 损失函数（锚点 c04-02） ----------
def mse_loss(y, y_pred):
    """返回均方误差 MSE = mean((y - y_hat)^2)，float"""
    # TODO
    return None


# ---------- 3. 解析梯度（锚点 c04-03） ----------
def mse_gradients(x, y, w, b):
    """
    返回 (dw, db)：
      dw = -2 * mean(x * (y - y_hat))
      db = -2 * mean(y - y_hat)
    """
    # TODO
    return None


# ---------- 4. 单步梯度下降（锚点 c04-03） ----------
def gradient_step(x, y, w, b, lr):
    """用【旧的】w,b 一次算完两个梯度，再一起更新，返回 (w_new, b_new)"""
    # TODO
    return None


# ---------- 5. 数值梯度（梯度检验用，锚点 c04-03） ----------
def numerical_gradient(x, y, w, b, eps=1e-6):
    """
    用中心差分 (L(p+eps) - L(p-eps)) / (2*eps) 分别算 w 和 b，
    返回 (dw, db)。不要调用 mse_gradients。
    """
    # TODO
    return None


# ---------- 6. 完整训练循环（锚点 c04-04） ----------
def train_linear(x, y, lr=0.1, epochs=500, w0=0.0, b0=0.0):
    """
    返回 (w, b, losses)：losses 长度 = epochs，记录【更新前】的损失。
    """
    # TODO
    return None


# ---------- 7. 收敛判断（锚点 c04-04） ----------
def has_converged(losses, tol=1e-6, window=5):
    """最近 window 个 loss 相邻差都小于 tol 才算收敛；不足 window 个返回 False"""
    # TODO
    return None


# ---------- 8. 标准化（锚点 c04-05） ----------
def standardize(x):
    """
    返回 (z, mean, std)：z = (x - mean) / std，用总体标准差 np.std()。
    全部元素相等时返回 (全 0 数组, 该值, 1.0)，避免除零。
    """
    # TODO
    return None


# ---------- 9. 小批量生成器（锚点 c04-04） ----------
def batch_iterator(x, y, batch_size, shuffle=False, seed=42):
    """
    生成器：逐批产出 (xb, yb)，必须覆盖全部样本、不重复。
    shuffle=True 时用 np.random.default_rng(seed) 打乱（可复现）。
    提示：yield，呼应基础教程 ch08
    """
    # TODO
    return None


# ---------- 10. 发散判定（锚点 c04-03） ----------
def diverges(x, y, lr, epochs=100):
    """
    从 w=b=0 开始用给定 lr 训练，若出现 inf/nan 或损失超过初始值的 10 倍，
    返回 True（发散）；正常收敛返回 False。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    x = np.linspace(0, 1, 50)
    y_clean = 3 * x + 2
    y_noisy = y_clean + rng.normal(0, 0.05, 50)

    # 1. 模型前向
    assert np.allclose(linear_predict(np.array([1, 2]), 3, 2), [5, 8])
    assert np.allclose(linear_predict(x, 0, 0), np.zeros_like(x))

    # 2. 损失
    assert abs(mse_loss([1, 2, 3], [1, 2, 5]) - 4 / 3) < 1e-9
    assert mse_loss(y_clean, y_clean) == 0.0
    assert mse_loss(y_noisy, linear_predict(x, 3, 2)) < 0.01

    # 3. 解析梯度 vs 数值梯度（本章最关键的一验）
    for w, b in [(0.0, 0.0), (1.0, 0.5), (2.7, 1.3)]:
        analytic = mse_gradients(x, y_noisy, w, b)
        numeric = numerical_gradient(x, y_noisy, w, b)
        assert np.allclose(analytic, numeric, atol=1e-5), \
            f"梯度写错了: 解析={analytic}, 数值={numeric}"

    # 4. 单步更新让损失下降
    w1, b1 = gradient_step(x, y_clean, 0.0, 0.0, lr=0.1)
    assert mse_loss(y_clean, linear_predict(x, w1, b1)) < mse_loss(y_clean, 0)

    # 5. 完整训练能拟合出 w≈3, b≈2
    w, b, losses = train_linear(x, y_clean, lr=0.2, epochs=3000)
    assert abs(w - 3) < 0.05, f"w 没收敛: {w}"
    assert abs(b - 2) < 0.05, f"b 没收敛: {b}"
    assert len(losses) == 3000
    assert losses[0] > losses[-1]
    assert all(losses[i + 1] <= losses[i] + 1e-12 for i in range(len(losses) - 1)), \
        "损失应该单调下降（学习率过大？）"

    # 6. 收敛判断
    assert has_converged([1.0, 1.0, 1.0, 1.0, 1.0]) is True
    assert has_converged([1.0, 2.0, 3.0]) is False
    assert has_converged([1.0, 2.0]) is False, "样本不足 window 应返回 False"
    assert has_converged(losses[-10:]) is True

    # 7. 标准化（含全相等的边界）
    z, mu, sigma = standardize(x)
    assert abs(z.mean()) < 1e-12 and abs(z.std() - 1) < 1e-12
    assert abs(mu - x.mean()) < 1e-12 and abs(sigma - x.std()) < 1e-12
    z0, mu0, s0 = standardize([5, 5, 5])
    assert np.allclose(z0, [0, 0, 0]) and mu0 == 5.0 and s0 == 1.0

    # 8. 小批量：覆盖全部、不重复、可复现
    batches = list(batch_iterator(x, y_clean, 16))
    assert len(batches) == 4
    assert sum(len(xb) for xb, _ in batches) == len(x)
    assert np.array_equal(np.concatenate([xb for xb, _ in batches]), x)
    assert len(list(batch_iterator(x, y_clean, 100))) == 1
    a = [(xb.tolist(), yb.tolist()) for xb, yb in batch_iterator(x, y_clean, 10, shuffle=True)]
    c = [(xb.tolist(), yb.tolist()) for xb, yb in batch_iterator(x, y_clean, 10, shuffle=True)]
    assert a == c, "同样的 seed 必须产出同样的批次"

    # 9. 学习率过大发散，正常学习率收敛
    assert diverges(x, y_clean, lr=10.0) is True
    assert diverges(x, y_clean, lr=0.05) is False

    print("ch04 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def linear_predict(x, w, b):
    return w * np.asarray(x, dtype=float) + b

def mse_loss(y, y_pred):
    y = np.asarray(y, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean((y - y_pred) ** 2))

def mse_gradients(x, y, w, b):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    err = y - (w * x + b)
    return (-2 * float(np.mean(x * err)), -2 * float(np.mean(err)))

def gradient_step(x, y, w, b, lr):
    dw, db = mse_gradients(x, y, w, b)
    return (w - lr * dw, b - lr * db)

def numerical_gradient(x, y, w, b, eps=1e-6):
    dw = (mse_loss(y, linear_predict(x, w + eps, b))
          - mse_loss(y, linear_predict(x, w - eps, b))) / (2 * eps)
    db = (mse_loss(y, linear_predict(x, w, b + eps))
          - mse_loss(y, linear_predict(x, w, b - eps))) / (2 * eps)
    return (dw, db)

def train_linear(x, y, lr=0.1, epochs=500, w0=0.0, b0=0.0):
    w, b = w0, b0
    losses = []
    for _ in range(epochs):
        losses.append(mse_loss(y, linear_predict(x, w, b)))
        dw, db = mse_gradients(x, y, w, b)
        w, b = w - lr * dw, b - lr * db
    return (w, b, losses)

def has_converged(losses, tol=1e-6, window=5):
    if len(losses) < window:
        return False
    recent = losses[-window:]
    return all(abs(recent[i] - recent[i - 1]) < tol for i in range(1, len(recent)))

def standardize(x):
    x = np.asarray(x, dtype=float)
    mu, sigma = float(x.mean()), float(x.std())
    if sigma == 0:
        return (np.zeros_like(x), mu, 1.0)
    return ((x - mu) / sigma, mu, sigma)

def batch_iterator(x, y, batch_size, shuffle=False, seed=42):
    x = np.asarray(x)
    y = np.asarray(y)
    idx = np.arange(len(x))
    if shuffle:
        np.random.default_rng(seed).shuffle(idx)
    for start in range(0, len(idx), batch_size):
        sel = idx[start:start + batch_size]
        yield x[sel], y[sel]

def diverges(x, y, lr, epochs=100):
    w, b = 0.0, 0.0
    initial = mse_loss(y, linear_predict(x, w, b))
    for _ in range(epochs):
        w, b = gradient_step(x, y, w, b, lr)
        if not (np.isfinite(w) and np.isfinite(b)):
            return True
        cur = mse_loss(y, linear_predict(x, w, b))
        if not np.isfinite(cur) or cur > initial * 10:
            return True
    return False
"""
# endregion
