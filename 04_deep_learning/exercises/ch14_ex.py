"""
ch14 练习：神经网络基础（Neural Network Basics）
──────────────────────────────────────────────────
重点：数值稳定的激活函数与导数、参数初始化、前向传播与缓存、
      带 clip 的二元交叉熵、手写反向传播、全参数数值梯度检验、
      XOR 两层网络训练与预测、两层线性退化。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch14_nn_basics.md

说明：本文件是 ML 全局第 14 章。00_foundations/python_basics/exercises/
只到 ch12（基础教程自己的章号），这里没有同名文件，按完整路径打开即可。

本练习只用 numpy，不用 PyTorch / sklearn，不依赖仓库外文件。
教学文档里的对比数字全部来自同一套数据生成器，跑通即可亲手复现。
"""

import numpy as np


# ---------- 与 ch08 / 教学文档完全一致的 XOR ----------
def make_xor(seed=42):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (160, 2))
    y = (X[:, 0] * X[:, 1] > 0).astype(int)
    return X[:120], y[:120], X[120:], y[120:]


# ---------- 第 1 题：sigmoid / 锚点 c14-01 ----------
def sigmoid(z):
    """逐元素 sigmoid，必须数值稳定（大正负输入不溢出、不产生 nan）。"""
    # TODO
    return None


# ---------- 第 2 题：sigmoid 导数 / 锚点 c14-01 ----------
def sigmoid_grad(z):
    """返回 sigma(z) * (1 - sigma(z))，逐元素。"""
    # TODO
    return None


# ---------- 第 3 题：tanh 导数 / 锚点 c14-01 ----------
def tanh_grad(a):
    """参数 a 是【tanh 的输出】而不是输入 z，返回 1 - a**2。"""
    # TODO
    return None


# ---------- 第 4 题：参数初始化 / 锚点 c14-02 ----------
def init_params(d, h, o=1, seed=0, scale=0.5):
    """返回 dict：W1(d,h) / b1(h,) / W2(h,o) / b2(o,)。
    W 用 default_rng(seed).normal(0, scale, ...)，偏置全 0。
    （为什么这么选 scale 是 ch15 的事，这里够用就行。）"""
    # TODO
    return None


# ---------- 第 5 题：前向传播 / 锚点 c14-03 ----------
def forward(X, params):
    """隐藏层 tanh、输出层 sigmoid。
    返回 (P, cache)，cache = (Z1, A1, Z2, P)，P 形状 (n, o)。"""
    # TODO
    return None


# ---------- 第 6 题：二元交叉熵 / 锚点 c14-03 ----------
def bce_loss(y, P):
    """返回标量。y 是 (n,)，P 是 (n,1)；计算前把 P clip 到 [1e-12, 1-1e-12]。"""
    # TODO
    return None


# ---------- 第 7 题：反向传播 / 锚点 c14-04 ----------
def backward(X, y, params, cache):
    """返回与 params 同 key、同形状的梯度 dict。
    dZ2 = (P - y) / n；dZ1 = dA1 * (1 - A1**2)；注意 loss 是 mean，梯度要除以 n。"""
    # TODO
    return None


# ---------- 第 8 题：单项数值梯度 / 锚点 c14-04 ----------
def numerical_gradient(X, y, params, key, idx, eps=1e-6):
    """只对 params[key][idx] 做中心差分，返回标量 dL/d(param)。
    不得修改传入的 params。"""
    # TODO
    return None


# ---------- 第 9 题：全参数梯度检验 / 锚点 c14-04 ----------
def gradient_check(X, y, params, eps=1e-6):
    """对每个参数逐元素比较解析梯度与数值梯度，
    返回 dict {key: 最大绝对差}。ch04 定的警戒线是 1e-5。"""
    # TODO
    return None


# ---------- 第 10 题：训练两层网络 / 锚点 c14-05 ----------
def train_network(X, y, h=4, lr=0.5, steps=10000, seed=0, scale=0.5):
    """全批量梯度下降，返回 (params, history)。
    history 是 [(step, loss), ...]，在 step∈(1,100,500,2000,5000,steps) 时记录。"""
    # TODO
    return None


# ---------- 第 11 题：预测 / 锚点 c14-05 ----------
def predict(X, params, threshold=0.5):
    """返回 (n,) 的 0/1 整数数组。"""
    # TODO
    return None


# ---------- 第 12 题：两层线性退化 / 锚点 c14-02 ----------
def linear_collapse(W1, b1, W2, b2):
    """把 (X@W1+b1)@W2+b2 折叠成 X@W_eq+b_eq，返回 (W_eq, b_eq)。"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    X_tr, y_tr, X_va, y_va = make_xor()
    eps = 1e-6

    # 第 1 题：与 ch02 2.8 同一个数、极值稳定、形状保持
    assert np.isclose(sigmoid(np.array([0.5]))[0], 0.6224593312)
    s = sigmoid(np.array([-100., 0., 100.]))
    assert np.all(np.isfinite(s)) and s[0] > 0 and s[2] <= 1.0
    assert np.isclose(s[1], 0.5)
    assert sigmoid(np.zeros((2, 3))).shape == (2, 3)
    assert np.all(np.isfinite(sigmoid(np.array([-1e6, 1e6]))))

    # 第 2 / 3 题：解析导数 vs 中心差分
    g2 = float(sigmoid_grad(np.array([0.5]))[0])
    num2 = (float(sigmoid(np.array([0.5 + eps]))[0])
            - float(sigmoid(np.array([0.5 - eps]))[0])) / (2 * eps)
    assert np.isclose(g2, 0.2350037122) and np.isclose(g2, num2, atol=1e-8)
    a = np.tanh(np.array([0.5]))[0]
    num3 = (np.tanh(0.5 + eps) - np.tanh(0.5 - eps)) / (2 * eps)
    assert np.isclose(float(tanh_grad(np.array([a]))[0]), 1 - a ** 2)
    assert np.isclose(float(tanh_grad(np.array([a]))[0]), num3, atol=1e-8)

    # 第 4 题：形状、偏置为 0、固定种子可复现
    p = init_params(2, 4, 1, seed=0, scale=0.5)
    assert set(p) == {"W1", "b1", "W2", "b2"}
    assert p["W1"].shape == (2, 4) and p["b1"].shape == (4,)
    assert p["W2"].shape == (4, 1) and p["b2"].shape == (1,)
    assert np.all(p["b1"] == 0) and np.all(p["b2"] == 0)
    assert np.array_equal(p["W1"], init_params(2, 4, 1, seed=0)["W1"])
    assert not np.array_equal(p["W1"], init_params(2, 4, 1, seed=1)["W1"])
    assert sum(v.size for v in p.values()) == 17, "2*4+4+4*1+1 = 17"

    # 第 5 题：前向、缓存内容、广播形状
    P, cache = forward(X_tr, p)
    Z1, A1, Z2, P2 = cache
    assert P.shape == (120, 1) and np.all((P > 0) & (P < 1))
    assert np.array_equal(P, P2)
    assert np.allclose(Z1, X_tr @ p["W1"] + p["b1"])
    assert np.allclose(A1, np.tanh(Z1))
    assert np.allclose(Z2, A1 @ p["W2"] + p["b2"])
    assert np.allclose(P, sigmoid(Z2))

    # 第 6 题：P=0.5 时正好 ln2、P=y 时近 0、clip 后不炸
    assert np.isclose(bce_loss(y_tr, np.full((120, 1), 0.5)), np.log(2))
    assert bce_loss(y_tr, np.asarray(y_tr, float).reshape(-1, 1)) < 1e-9
    assert np.isfinite(bce_loss(np.array([0, 1]), np.array([[0.], [1.]])))
    assert bce_loss(np.array([1]), np.array([[0.]])) > 10
    assert 0.69 < bce_loss(y_tr, P) < 0.70, "初始 loss 应接近 ln2"

    # 第 7 题：梯度形状 + 全参数数值梯度检验
    Xg, yg = X_tr[:8], y_tr[:8]
    _, cg = forward(Xg, p)
    Z1g, A1g, Z2g, Pg = cg
    g = backward(Xg, yg, p, cg)
    assert set(g) == set(p)
    for k in p:
        assert g[k].shape == p[k].shape, f"{k} 梯度形状要和参数一致"
    assert np.allclose(g["W2"], A1g.T @ ((Pg - yg.reshape(-1, 1)) / 8), atol=1e-8)

    # 第 8 题：单项中心差分与解析梯度一致
    assert np.isclose(numerical_gradient(Xg, yg, p, "W1", (0, 0)),
                      g["W1"][0, 0], atol=1e-7)
    p_before = {k: v.copy() for k, v in p.items()}
    numerical_gradient(Xg, yg, p, "W2", (2, 0))
    assert all(np.array_equal(p[k], p_before[k]) for k in p), "不应该修改传入的 params"

    # 第 9 题：全参数最大差远小于 ch04 的 1e-5 警戒线
    diffs = gradient_check(Xg, yg, p)
    assert set(diffs) == set(p)
    assert max(diffs.values()) < 1e-6, f"梯度写错了：{diffs}"

    # 第 10 题：XOR 训练到收敛（亲手跑出 ch08 那条 0.675 的反例）
    pf, hist = train_network(X_tr, y_tr, h=4, lr=0.5, steps=10000, seed=0)
    assert len(hist) == 6 and hist[0][0] == 1 and hist[-1][0] == 10000
    assert hist[0][1] > hist[-1][1], "损失必须下降"
    assert np.isclose(hist[-1][1], 0.023061, atol=1e-3)
    assert np.mean(predict(X_tr, pf) == y_tr) == 1.0
    assert np.mean(predict(X_va, pf) == y_va) == 1.0

    # 第 11 题：四个象限的预测（对角结构，不是背答案）
    quad = np.array([[-0.7, -0.7], [0.7, 0.7], [-0.7, 0.7], [0.7, -0.7]])
    assert np.array_equal(predict(quad, pf), np.array([1, 1, 0, 0]))
    assert predict(quad, pf, threshold=1.1).sum() == 0
    assert predict(quad, pf, threshold=-0.1).sum() == 4

    # 第 12 题：两层线性 = 一层线性
    r = np.random.default_rng(0)
    Xs = r.normal(size=(5, 2))
    W1, W2 = r.normal(size=(2, 3)), r.normal(size=(3, 1))
    b1, b2 = r.normal(size=3), r.normal(size=1)
    We, be = linear_collapse(W1, b1, W2, b2)
    assert We.shape == (2, 1) and be.shape == (1,)
    Y_two = (Xs @ W1 + b1) @ W2 + b2
    Y_one = Xs @ We + be
    assert np.allclose(Y_two, Y_one, atol=1e-12), "不加激活函数时两层就是一层"

    print("ch14 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def sigmoid(z):
    z = np.asarray(z, dtype=float)
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def sigmoid_grad(z):
    s = sigmoid(z)
    return s * (1.0 - s)


def tanh_grad(a):
    a = np.asarray(a, dtype=float)
    return 1.0 - a ** 2


def init_params(d, h, o=1, seed=0, scale=0.5):
    r = np.random.default_rng(seed)
    return {"W1": r.normal(0, scale, (d, h)), "b1": np.zeros(h),
            "W2": r.normal(0, scale, (h, o)), "b2": np.zeros(o)}


def forward(X, params):
    X = np.asarray(X, dtype=float)
    Z1 = X @ params["W1"] + params["b1"]
    A1 = np.tanh(Z1)
    Z2 = A1 @ params["W2"] + params["b2"]
    P = sigmoid(Z2)
    return P, (Z1, A1, Z2, P)


def bce_loss(y, P):
    P = np.clip(np.asarray(P, dtype=float), 1e-12, 1 - 1e-12)
    yy = np.asarray(y, dtype=float).reshape(-1, 1)
    return float(-np.mean(yy * np.log(P) + (1 - yy) * np.log(1 - P)))


def backward(X, y, params, cache):
    X = np.asarray(X, dtype=float)
    Z1, A1, Z2, P = cache
    n = len(X)
    yy = np.asarray(y, dtype=float).reshape(-1, 1)
    dZ2 = (P - yy) / n
    dW2 = A1.T @ dZ2
    db2 = dZ2.sum(axis=0)
    dA1 = dZ2 @ params["W2"].T
    dZ1 = dA1 * (1 - A1 ** 2)
    dW1 = X.T @ dZ1
    db1 = dZ1.sum(axis=0)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


def numerical_gradient(X, y, params, key, idx, eps=1e-6):
    pp, pm = dict(params), dict(params)
    pp[key] = params[key].copy()
    pm[key] = params[key].copy()
    pp[key][idx] += eps
    pm[key][idx] -= eps
    lp = bce_loss(y, forward(X, pp)[0])
    lm = bce_loss(y, forward(X, pm)[0])
    return (lp - lm) / (2 * eps)


def gradient_check(X, y, params, eps=1e-6):
    _, cache = forward(X, params)
    analytic = backward(X, y, params, cache)
    out = {}
    for k in params:
        diff = np.zeros_like(params[k], dtype=float)
        for idx in np.ndindex(params[k].shape):
            diff[idx] = numerical_gradient(X, y, params, k, idx, eps) - analytic[k][idx]
        out[k] = float(np.abs(diff).max())
    return out


def train_network(X, y, h=4, lr=0.5, steps=10000, seed=0, scale=0.5):
    X = np.asarray(X, dtype=float)
    params = init_params(X.shape[1], h, 1, seed, scale)
    marks = (1, 100, 500, 2000, 5000, steps)
    hist = []
    for t in range(1, steps + 1):
        _, cache = forward(X, params)
        grads = backward(X, y, params, cache)
        for k in params:
            params[k] -= lr * grads[k]
        if t in marks:
            hist.append((t, bce_loss(y, forward(X, params)[0])))
    return params, hist


def predict(X, params, threshold=0.5):
    P, _ = forward(X, params)
    return (P.ravel() >= threshold).astype(int)


def linear_collapse(W1, b1, W2, b2):
    return W1 @ W2, b1 @ W2 + b2
"""
# endregion
