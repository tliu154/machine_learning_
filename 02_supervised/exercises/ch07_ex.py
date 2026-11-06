"""
ch07 练习：线性模型（Linear Models）
──────────────────────────────────────────────────
对应章节：docs/ch07_linear_models.md
重点：最小二乘闭式解 / 多项式特征 / Sigmoid 与交叉熵 / 手写逻辑回归 /
      Ridge 正则化 / 先划分再标准化（防数据泄漏）
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy，不需要 scikit-learn（7.4 的库代码仅作对照）。
"""

import numpy as np


# ---------- 1. 偏置列（锚点 c07-01） ----------
def add_bias(X):
    """在 X 右边补一列 1，返回 (n, d+1)；一维输入先按列向量处理；不改原数组"""
    # TODO
    return None


# ---------- 2. 最小二乘闭式解（锚点 c07-01） ----------
def fit_least_squares(X, y):
    """用 np.linalg.lstsq 求 theta（含偏置，长度 d+1），不要用 inv"""
    # TODO
    return None


# ---------- 3. 线性预测（锚点 c07-01） ----------
def predict_linear(X, theta):
    """返回 add_bias(X) @ theta"""
    # TODO
    return None


# ---------- 4. 多项式特征（锚点 c07-01） ----------
def polynomial_features(x, degree=3):
    """x 为一维数组，返回 [x, x^2, ..., x^degree]，形状 (n, degree)，不含常数项"""
    # TODO
    return None


# ---------- 5. Sigmoid（锚点 c07-02） ----------
def sigmoid(z):
    """数值稳定版：极端正负值不产生 inf / nan，支持标量或数组"""
    # TODO
    return None


# ---------- 6. 二元交叉熵（锚点 c07-02） ----------
def binary_cross_entropy(y, p, eps=1e-12):
    """返回 float；概率进 log 前必须 clip 到 [eps, 1-eps]，防 log(0)"""
    # TODO
    return None


# ---------- 7. 逻辑回归梯度（锚点 c07-02） ----------
def logistic_gradient(A, y, p):
    """A 已含偏置列，返回 A.T @ (p - y) / len(A)，形状 (d+1,)"""
    # TODO
    return None


# ---------- 8. 手写逻辑回归（锚点 c07-02） ----------
def fit_logistic(X, y, lr=0.5, epochs=2000):
    """从全零 theta 开始梯度下降，返回 (theta, losses)；losses 长度 = epochs"""
    # TODO
    return None


# ---------- 9. Ridge 闭式解（锚点 c07-03） ----------
def ridge_closed_form(X, y, alpha):
    """解 (A.T@A + alpha*I') theta = A.T@y，I' 最后一个对角元为 0（偏置不正则化）"""
    # TODO
    return None


# ---------- 10. 决定系数（锚点 c07-04） ----------
def r2_score(y, y_pred):
    """R^2 = 1 - SSE/SST；SST 为 0 时，完美预测返回 1.0，否则返回 0.0"""
    # TODO
    return None


# ---------- 11. 划分 + 标准化（锚点 c07-04） ----------
def split_standardize(X, y, train_ratio=0.8):
    """
    按顺序切分（不打乱），只用【训练集】的均值和标准差标准化两个集合。
    返回 (X_tr_s, X_va_s, y_tr, y_va)；某列标准差为 0 时按 1.0 处理；不改原数组。
    真实项目里切分前通常先打乱，见 ch20。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    X = rng.uniform(-2, 2, (80, 2))
    true_theta = np.array([1.5, -2.0, 0.5])       # w1, w2, b
    y = X @ true_theta[:2] + true_theta[2] + rng.normal(0, 0.05, 80)
    yc = (X[:, 0] + X[:, 1] > 0).astype(float)    # 线性可分的二分类标签

    # 1. 偏置列：形状、内容、无副作用、一维输入
    A = add_bias(X)
    assert A.shape == (80, 3)
    assert np.array_equal(A[:, :2], X) and np.all(A[:, 2] == 1)
    assert add_bias(np.array([1.0, 2.0])).shape == (2, 2)
    snapshot = X.copy()
    add_bias(X)
    assert np.array_equal(X, snapshot), "不应该修改输入"

    # 2. 最小二乘闭式解：一步恢复真参数
    theta = fit_least_squares(X, y)
    assert theta.shape == (3,)
    assert np.allclose(theta, true_theta, atol=0.05), f"没拟合出真参数: {theta}"

    # 3. 预测
    assert np.allclose(predict_linear(X, theta), A @ theta)
    assert np.allclose(predict_linear(X, true_theta), y, atol=0.2)

    # 4. 多项式特征：线性模型照样拟合二次曲线
    P = polynomial_features(np.array([1.0, 2.0, 3.0]), 3)
    assert np.array_equal(P, [[1, 1, 1], [2, 4, 8], [3, 9, 27]])
    xs = np.linspace(-2, 2, 60)
    th_poly = fit_least_squares(polynomial_features(xs, 2), 1 + 2 * xs + 0.5 * xs ** 2)
    assert np.allclose(th_poly, [2.0, 0.5, 1.0], atol=1e-8), \
        "线性指的是对参数线性，二次曲线也能用 lstsq"

    # 5. Sigmoid：数值稳定
    assert np.isclose(sigmoid(0.0), 0.5)
    assert np.all(np.isfinite(sigmoid(np.array([-1e6, 1e6]))))
    assert np.isclose(sigmoid(-1000.0), 0.0) and np.isclose(sigmoid(1000.0), 1.0)
    assert np.allclose(sigmoid(np.array([-1.0, 0.0, 1.0])),
                       [0.26894142, 0.5, 0.73105858], atol=1e-6)

    # 6. 交叉熵：完美预测、全猜 0.5、以及 log(0) 边界
    assert np.isclose(binary_cross_entropy(np.array([0.0, 1.0]), np.array([0.0, 1.0])), 0.0)
    assert np.isclose(binary_cross_entropy(np.array([1.0, 0.0]), np.array([0.5, 0.5])), np.log(2))
    assert np.isfinite(binary_cross_entropy(np.array([1.0]), np.array([0.0]))), \
        "概率必须是 clip 过的，否则 log(0) 变 -inf"

    # 7. 梯度：解析解 vs 数值梯度（呼应 ch04 的梯度检验）
    theta0 = np.array([0.3, -0.4, 0.1])
    p0 = sigmoid(A @ theta0)
    g = logistic_gradient(A, yc, p0)
    assert g.shape == (3,)

    def loss_at(t):
        return binary_cross_entropy(yc, sigmoid(A @ t))

    eps = 1e-6
    numeric = np.array([
        (loss_at(theta0 + eps * np.eye(3)[i]) - loss_at(theta0 - eps * np.eye(3)[i])) / (2 * eps)
        for i in range(3)
    ])
    assert np.allclose(g, numeric, atol=1e-6), f"梯度写错了: 解析={g}, 数值={numeric}"

    # 8. 手写逻辑回归能分对、损失下降
    theta_c, losses = fit_logistic(X, yc, lr=0.5, epochs=2000)
    assert len(losses) == 2000 and losses[0] > losses[-1]
    assert np.all(np.isfinite(losses))
    acc = np.mean((sigmoid(A @ theta_c) > 0.5) == yc)
    assert acc > 0.9, f"分类没学出来: acc={acc}"

    # 9. Ridge：alpha=0 退化成 lstsq、权重收缩、偏置不被惩罚
    th0 = ridge_closed_form(X, y, 0.0)
    assert np.allclose(th0, theta, atol=1e-8)
    th10 = ridge_closed_form(X, y, 10.0)
    assert np.linalg.norm(th10[:2]) < np.linalg.norm(th0[:2]), "正则化应该压小权重"
    const_y = np.full(80, 7.0)
    th_cst = ridge_closed_form(X, const_y, 50.0)
    assert np.isclose(th_cst[-1], 7.0, atol=1e-6) and np.allclose(th_cst[:2], 0, atol=1e-6), \
        "偏置不该被正则化，否则常数标签都拟合不了"

    # 10. R^2 与分母为 0 的边界
    assert np.isclose(r2_score(y, y), 1.0)
    assert np.isclose(r2_score(y, np.full_like(y, y.mean())), 0.0)
    assert r2_score(np.array([1.0, 1.0, 1.0]), np.array([1.0, 1.0, 1.0])) == 1.0
    assert np.isclose(r2_score(np.array([1.0, 1.0, 1.0]), np.array([2.0, 2.0, 2.0])), 0.0)

    # 11. 先划分、再只用训练集的统计量标准化
    Xtr_s, Xva_s, ytr, yva = split_standardize(X, y, 0.8)
    assert Xtr_s.shape[0] == 64 and Xva_s.shape[0] == 16
    assert ytr.size + yva.size == 80
    assert np.allclose(Xtr_s.mean(axis=0), 0, atol=1e-12)
    assert np.allclose(Xtr_s.std(axis=0), 1, atol=1e-12)
    mu, sigma = X[:64].mean(axis=0), X[:64].std(axis=0)
    assert np.allclose(Xva_s, (X[64:] - mu) / sigma), \
        "验证集必须用训练集的均值/标准差，不能自己 fit"
    assert np.array_equal(X, snapshot), "不应该修改输入"

    print("ch07 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def add_bias(X):
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    return np.column_stack([X, np.ones(len(X))])

def fit_least_squares(X, y):
    A = add_bias(X)
    return np.linalg.lstsq(A, np.asarray(y, dtype=float), rcond=None)[0]

def predict_linear(X, theta):
    return add_bias(X) @ np.asarray(theta, dtype=float)

def polynomial_features(x, degree=3):
    x = np.asarray(x, dtype=float)
    return np.column_stack([x ** k for k in range(1, degree + 1)])

def sigmoid(z):
    z = np.clip(np.asarray(z, dtype=float), -500, 500)
    return 1.0 / (1.0 + np.exp(-z))

def binary_cross_entropy(y, p, eps=1e-12):
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

def logistic_gradient(A, y, p):
    A = np.asarray(A, dtype=float)
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    return A.T @ (p - y) / len(A)

def fit_logistic(X, y, lr=0.5, epochs=2000):
    A = add_bias(X)
    y = np.asarray(y, dtype=float)
    theta = np.zeros(A.shape[1])
    losses = []
    for _ in range(epochs):
        p = sigmoid(A @ theta)
        losses.append(binary_cross_entropy(y, p))
        theta = theta - lr * (A.T @ (p - y) / len(A))
    return theta, losses

def ridge_closed_form(X, y, alpha):
    A = add_bias(X)
    reg = alpha * np.eye(A.shape[1])
    reg[-1, -1] = 0.0
    return np.linalg.solve(A.T @ A + reg, A.T @ np.asarray(y, dtype=float))

def r2_score(y, y_pred):
    y = np.asarray(y, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    sse = float(np.sum((y - y_pred) ** 2))
    sst = float(np.sum((y - y.mean()) ** 2))
    if sst == 0:
        return 1.0 if sse == 0 else 0.0
    return 1.0 - sse / sst

def split_standardize(X, y, train_ratio=0.8):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    k = int(len(X) * train_ratio)
    X_tr, X_va = X[:k], X[k:]
    y_tr, y_va = y[:k], y[k:]
    mu, sigma = X_tr.mean(axis=0), X_tr.std(axis=0)
    sigma = np.where(sigma == 0, 1.0, sigma)
    return (X_tr - mu) / sigma, (X_va - mu) / sigma, y_tr, y_va
"""
# endregion
