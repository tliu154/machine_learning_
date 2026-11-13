"""
ch02 练习：数学基础（Mathematical Foundations）
──────────────────────────────────────────────────
重点：向量/矩阵、概率与贝叶斯、期望方差、导数、梯度、链式法则。
每题都同时练「会算」和「知道在 ML 哪一行用到」，按教学 2.1~2.8 顺序排，
可以只做自己按需补学的那几节对应的题，不必全刷。

把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch02_math_foundations.md

⚠️ 章号撞名：00_foundations/python_basics/exercises/ch02_ex.py 是
Python 基础教程自己的第 2 章「数字与运算」，与本文件（ML 全局第 2 章数学基础）
毫无关系。两套 ch02_ex.py 内容完全不同，按完整路径打开，别只搜文件名。

本练习只用 numpy，不依赖 sklearn、不依赖仓库外文件。
"""

import numpy as np


# ---------- 第 1 题：向量长度 / 锚点 c02-01 ----------
def vector_norm(x):
    """返回向量 x 的 L2 长度 sqrt(sum(x_j^2))。零向量返回 0.0，整数输入也要能用。"""
    # TODO
    return None


# ---------- 第 2 题：行 vs 列 / 锚点 c02-01 ----------
def row_and_column(X):
    """返回 (第 0 行, 第 0 列)，各为一维数组，且必须是【副本】（改返回值不影响 X）。
    X 至少 1 行 1 列。"""
    # TODO
    return None


# ---------- 第 3 题：矩阵乘做批量预测 / 锚点 c02-02 ----------
def batch_predict(X, w, b):
    """返回 X @ w + b，形状 (n,)；不许写 for 循环。"""
    # TODO
    return None


# ---------- 第 4 题：* 与 @ 的区别 / 锚点 c02-02 ----------
def elementwise_vs_matmul(X, w):
    """返回 (X * w, X @ w)：前者逐元素乘（会广播），后者矩阵乘。"""
    # TODO
    return None


# ---------- 第 5 题：频率收敛到概率 / 锚点 c02-03 ----------
def frequency_converges(p, n, seed=42):
    """做 n 次伯努利(p) 试验，返回正例频率；n=0 时返回 0.0。
    同一种子必须得到同一结果（可复现）。"""
    # TODO
    return None


# ---------- 第 6 题：贝叶斯后验 / 锚点 c02-04 ----------
def bayes_posterior(prior, sensitivity, fpr):
    """返回 P(病|阳) = sens*prior / (sens*prior + fpr*(1-prior))。
    分母为 0 时返回 0.0。"""
    # TODO
    return None


# ---------- 第 7 题：均值 / 方差 / 标准差 / 锚点 c02-05 ----------
def mean_var_std(x, ddof=0):
    """返回 (均值, 方差, 标准差)；ddof 要透传给方差与标准差。
    x 非空；单元素或全相等时方差、标准差均为 0。"""
    # TODO
    return None


# ---------- 第 8 题：中心差分求导数 / 锚点 c02-06 ----------
def numerical_derivative(f, x, eps=1e-6):
    """用 (f(x+eps) - f(x-eps)) / (2*eps) 近似 f'(x)。"""
    # TODO
    return None


# ---------- 第 9 题：偏导只动一个变量 / 锚点 c02-06 ----------
def partial_derivative(f, point, i, eps=1e-6):
    """多元函数 f(*point) 对第 i 个变量的偏导；其余变量保持不动。
    不得修改传进来的 point。point 可以是 list 或 tuple。"""
    # TODO
    return None


# ---------- 第 10 题：MSE 对参数的梯度 / 锚点 c02-07 ----------
def mse_gradient(X, y, theta):
    """L = mean((y - X@theta)^2) 对 theta 的梯度 = -2/n * X.T @ (y - X@theta)。
    返回形状与 theta 一致的一维数组。"""
    # TODO
    return None


# ---------- 第 11 题：负梯度是最陡下坡 / 锚点 c02-07 ----------
def descent_direction(loss_fn, theta, grad, step=0.1):
    """沿 grad 的【单位方向】各走 step，返回 (沿 -grad 的 loss, 沿 +grad 的 loss)。
    grad 为零向量时原地不动，两个值都等于 loss_fn(theta)。
    不得修改 theta。"""
    # TODO
    return None


# ---------- 第 12 题：链式法则 / 锚点 c02-08 ----------
def chain_rule_check(x, y, w, b, eps=1e-6):
    """单样本 L = (y - (w*x + b))^2，令 yhat = w*x + b。
    返回 (dL_dw_by_chain, abs_gap)：
      dL_dw_by_chain = (-2*(y - yhat)) * x   （dL/dyhat 乘 dyhat/dw）
      abs_gap = 它与直接对 w 做中心差分所得数值导数的绝对差。"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    X = np.array([[1., 2.], [3., 4.], [5., 6.]])
    w = np.array([2., -1.])

    # 第 1 题：正常、负数、零向量、整数输入
    assert np.isclose(vector_norm(np.array([3., 4.])), 5.0)
    assert np.isclose(vector_norm(np.array([2., -1.])), np.sqrt(5))
    assert vector_norm(np.array([0., 0., 0.])) == 0.0
    assert np.isclose(vector_norm([3, 4]), 5.0)

    # 第 2 题：行/列别看反；单行边界；返回副本
    r, c = row_and_column(X)
    assert np.allclose(r, [1., 2.]) and np.allclose(c, [1., 3., 5.])
    assert r.ndim == 1 and c.ndim == 1
    r1, c1 = row_and_column(np.array([[7., 8.]]))
    assert np.allclose(r1, [7., 8.]) and np.allclose(c1, [7.])
    X0 = X.copy()
    r[0] = 99.0
    assert X0[0, 0] == 1.0, "返回的行不该是视图"

    # 第 3 题：一次算完 + 与逐行手算一致 + 单样本
    pred = batch_predict(X, w, 1.0)
    assert pred.shape == (3,)
    assert np.allclose(pred, [1., 3., 5.])
    assert np.allclose(pred, [float(X[i] @ w) + 1.0 for i in range(3)])
    assert np.allclose(batch_predict(np.array([[1., 2.]]), w, 0.0), [0.])

    # 第 4 题：* 广播成 (3,2)，@ 压成 (3,)
    e, m = elementwise_vs_matmul(X, w)
    assert e.shape == (3, 2) and m.shape == (3,)
    assert np.allclose(e[0], [2., -2.]) and np.allclose(m, [0., 2., 4.])

    # 第 5 题：n=0 边界、可复现、大样本逼近 p、小样本允许偏
    assert frequency_converges(0.17, 0) == 0.0
    assert frequency_converges(0.5, 100, 7) == frequency_converges(0.5, 100, 7)
    assert abs(frequency_converges(0.17, 10000, 42) - 0.17) < 0.02
    assert abs(frequency_converges(0.17, 10, 42) - 0.17) < 0.35

    # 第 6 题：反直觉的 16.67%、分母为 0、无误报时必为 1
    assert np.isclose(bayes_posterior(0.01, 0.99, 0.05), 1 / 6)
    assert bayes_posterior(0.01, 0.0, 0.0) == 0.0
    assert np.isclose(bayes_posterior(0.01, 0.99, 0.0), 1.0)
    assert bayes_posterior(0.0, 0.9, 0.1) == 0.0

    # 第 7 题：ddof=0 与 ddof=1 的差别、单元素、全相等
    mu, var, sd = mean_var_std([2., 4., 4., 4., 5., 5., 7., 9.])
    assert np.isclose(mu, 5.0) and np.isclose(var, 4.0) and np.isclose(sd, 2.0)
    assert np.isclose(mean_var_std([2., 4., 4., 4., 5., 5., 7., 9.], ddof=1)[1], 4.571428571428571)
    assert mean_var_std([7.0]) == (7.0, 0.0, 0.0)
    assert mean_var_std([3., 3., 3.]) == (3.0, 0.0, 0.0)

    # 第 8 题：二次、三角、常数、线性函数
    assert np.isclose(numerical_derivative(lambda t: t ** 2, 3.0), 6.0, atol=1e-6)
    assert np.isclose(numerical_derivative(np.sin, 0.0), 1.0, atol=1e-6)
    assert np.isclose(numerical_derivative(lambda t: 5.0, 2.0), 0.0, atol=1e-9)
    assert np.isclose(numerical_derivative(lambda t: 3 * t + 1, 10.0), 3.0, atol=1e-6)

    # 第 9 题：两个偏导、无副作用、与某维无关时偏导为 0
    g = lambda a, b: (2 * a + b - 5) ** 2
    assert np.isclose(partial_derivative(g, (1., 1.), 0), -8.0, atol=1e-6)
    assert np.isclose(partial_derivative(g, (1., 1.), 1), -4.0, atol=1e-6)
    pt = [1., 1.]
    partial_derivative(g, pt, 0)
    assert pt == [1., 1.], "不应该修改输入 point"
    h = lambda a, b: b ** 2
    assert np.isclose(partial_derivative(h, (2., 3.), 0), 0.0, atol=1e-9)

    # 第 10 题：解析梯度、形状、与数值梯度一致、完美拟合时梯度为 0
    Xs = np.array([[1., 0.], [0., 1.], [1., 1.]])
    ys = np.array([1., 2., 3.])
    grad = mse_gradient(Xs, ys, np.array([0., 0.]))
    assert grad.shape == (2,)
    assert np.allclose(grad, [-8 / 3, -10 / 3])
    # partial_derivative 用 f(*point)，所以 loss 要写成两个标量参数
    loss_of = lambda a, b: float(np.mean((ys - (a * Xs[:, 0] + b * Xs[:, 1])) ** 2))
    assert np.allclose(grad, [partial_derivative(loss_of, [0., 0.], i) for i in range(2)], atol=1e-6)
    assert np.allclose(mse_gradient(np.array([[1.], [2.]]), np.array([2., 4.]), np.array([2.])), [0.])

    # 第 11 题：负梯度方向降、正梯度方向升、零梯度原地、无副作用
    xx = np.linspace(0, 1, 50)
    yy = 3 * xx + 2 + np.random.default_rng(42).normal(0, 0.05, 50)
    loss_fn = lambda th: float(np.mean((yy - (th[0] * xx + th[1])) ** 2))
    g0 = mse_gradient(np.column_stack([xx, np.ones_like(xx)]), yy, np.array([0., 0.]))
    theta0 = np.array([0., 0.])
    lm, lp = descent_direction(loss_fn, theta0, g0, step=0.1)
    assert lm < loss_fn(theta0) < lp, "负梯度应下降、正梯度应上升"
    assert np.allclose(theta0, [0., 0.]), "不应该修改 theta"
    z0, z1 = descent_direction(loss_fn, theta0, np.array([0., 0.]), step=0.1)
    assert z0 == z1 == loss_fn(theta0)

    # 第 12 题：链式和数值导数一致、换组数据仍一致、x=0 时导数为 0
    val, gap = chain_rule_check(2., 5., 1., 1.)
    assert np.isclose(val, -8.0) and gap < 1e-6
    val2, gap2 = chain_rule_check(3., -1., 0.5, 2.)
    assert np.isclose(val2, 27.0) and gap2 < 1e-6
    val3, gap3 = chain_rule_check(0., 5., 1., 1.)
    assert val3 == 0.0 and gap3 < 1e-9

    print("ch02 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def vector_norm(x):
    return float(np.sqrt(np.sum(np.asarray(x, dtype=float) ** 2)))


def row_and_column(X):
    X = np.asarray(X, dtype=float)
    return X[0].copy(), X[:, 0].copy()


def batch_predict(X, w, b):
    return np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b


def elementwise_vs_matmul(X, w):
    X = np.asarray(X, dtype=float)
    w = np.asarray(w, dtype=float)
    return X * w, X @ w


def frequency_converges(p, n, seed=42):
    if n == 0:
        return 0.0
    return float(np.random.default_rng(seed).binomial(1, p, n).mean())


def bayes_posterior(prior, sensitivity, fpr):
    denom = sensitivity * prior + fpr * (1 - prior)
    if denom == 0:
        return 0.0
    return sensitivity * prior / denom


def mean_var_std(x, ddof=0):
    a = np.asarray(x, dtype=float)
    return float(a.mean()), float(a.var(ddof=ddof)), float(a.std(ddof=ddof))


def numerical_derivative(f, x, eps=1e-6):
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def partial_derivative(f, point, i, eps=1e-6):
    p1, p2 = list(point), list(point)
    p1[i] += eps
    p2[i] -= eps
    return (f(*p1) - f(*p2)) / (2 * eps)


def mse_gradient(X, y, theta):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    theta = np.asarray(theta, dtype=float)
    return -2.0 / len(y) * (X.T @ (y - X @ theta))


def descent_direction(loss_fn, theta, grad, step=0.1):
    theta = np.asarray(theta, dtype=float)
    grad = np.asarray(grad, dtype=float)
    norm = np.linalg.norm(grad)
    if norm == 0:
        v = float(loss_fn(theta))
        return v, v
    u = grad / norm
    return float(loss_fn(theta - step * u)), float(loss_fn(theta + step * u))


def chain_rule_check(x, y, w, b, eps=1e-6):
    yhat = w * x + b
    chain = (-2.0 * (y - yhat)) * x
    L = lambda ww: (y - (ww * x + b)) ** 2
    numeric = (L(w + eps) - L(w - eps)) / (2 * eps)
    return float(chain), float(abs(chain - numeric))
"""
# endregion
