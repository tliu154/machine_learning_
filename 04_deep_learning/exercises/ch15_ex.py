"""
ch15 练习：激活函数与初始化（Activation and Initialization）
──────────────────────────────────────────────────
重点：数值稳定的激活函数与导数上界、GELU / Leaky ReLU、Sigmoid 饱和、
      8 层网络的前向激活 std 与逐层梯度范数、梯度消失 / 爆炸的量化、
      死 ReLU 统计、Xavier / He 初始化，最后亲手复现 ch14 那个卡住的 seed=0。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch15_activation_init.md

说明：本文件是 ML 全局第 15 章。00_foundations/python_basics/exercises/
只到 ch12（基础教程自己的章号），这里没有同名文件，按完整路径打开即可。

本练习只用 numpy，不用 PyTorch / sklearn，不依赖仓库外文件。
教学文档里的所有数字来自同一套数据生成器与固定 seed=0/42。
"""

import numpy as np


# ---------- 公共工具（已给实现，不是题目） ----------
def sigmoid(z):
    """数值稳定的 sigmoid，clip 防 exp 溢出。"""
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def relu(z):
    return np.maximum(0.0, z)


def relu_grad(z):
    """ReLU 对输入的导数：正半轴 1，其余 0（z=0 处按框架惯例取 0）。"""
    return (z > 0).astype(float)


def make_deep(std, d=32, L=8, n=64, seed=0):
    """造一套 8 层网络：X(n,d) + L 个 W(d,d)，权重 std 由参数指定。
    与教学文档的实验装置完全一致，先抽 X 再抽 W，顺序别改。"""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d))
    W = [rng.normal(0.0, std, (d, d)) for _ in range(L)]
    return X, W


def make_xor(seed=42):
    """和 ch08 / ch14 一模一样的 XOR：160 样本，120 训练 / 40 验证。"""
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (160, 2))
    y = (X[:, 0] * X[:, 1] > 0).astype(int)
    return X[:120], y[:120], X[120:], y[120:]


# ---------- 第 1 题：Sigmoid 导数 / 锚点 c15-01 ----------
def sigmoid_grad(z):
    """返回 sigma(z)*(1-sigma(z))，逐元素；大正负输入不得溢出。"""
    # TODO
    return None


# ---------- 第 2 题：Leaky ReLU / 锚点 c15-01 ----------
def leaky_relu(z, a=0.01):
    """z>0 返回 z，否则返回 a*z；a 是负半轴斜率。"""
    # TODO
    return None


# ---------- 第 3 题：GELU / 锚点 c15-01 ----------
def gelu(z):
    """精确式的 tanh 近似：0.5*z*(1+tanh(sqrt(2/pi)*(z+0.044715*z^3)))。"""
    # TODO
    return None


# ---------- 第 4 题：导数上界 / 锚点 c15-01 ----------
def derivative_bound(name):
    """返回该激活导数的上界：sigmoid=0.25，tanh/relu/leaky=1.0；
    GELU 没有简洁解析上界，这里不收（遇到未知名字抛 ValueError）。"""
    # TODO
    return None


# ---------- 第 5 题：饱和 / 锚点 c15-01 ----------
def saturation_loss(z):
    """返回 sigmoid 导数相对最大值 0.25 的比例（1.0 = 完全没饱和）。"""
    # TODO
    return None


# ---------- 第 6 题：8 层前向激活 std / 锚点 c15-02 ----------
def deep_forward_std(X, W, act):
    """逐层算 A = act(A @ w)，返回每层激活值的标准差列表（长度 L）。"""
    # TODO
    return None


# ---------- 第 7 题：逐层梯度范数 / 锚点 c15-02 ----------
def deep_grad_norms(X, W, act, local_grad):
    """上游梯度归一到 1，按反向传播逐层乘 (local_grad(Z) 和 W.T)，
    返回按【第 1 层 → 第 L 层】排好的梯度范数列表。"""
    # TODO
    return None


# ---------- 第 8 题：首末层梯度比 / 锚点 c15-02 ----------
def gradient_ratio(norms):
    """返回 norms[-1] / norms[0]。
    >>1 表示越往回传越小（梯度消失），<<1 表示越往回传越大（梯度爆炸）。"""
    # TODO
    return None


# ---------- 第 9 题：死 ReLU 比例 / 锚点 c15-02 ----------
def dead_relu_fraction(Z):
    """Z 形状 (n, d)，返回「在全部 n 个样本上都 <= 0」的神经元占比。"""
    # TODO
    return None


# ---------- 第 10 题：Xavier / He 的 scale / 锚点 c15-03 ----------
def init_scale(method, fan_in, fan_out):
    """xavier: sqrt(2/(fan_in+fan_out))；he: sqrt(2/fan_in)；其余抛 ValueError。"""
    # TODO
    return None


# ---------- 第 11 题：按方法初始化权重 / 锚点 c15-03 ----------
def init_weights(d, L, method, seed=0):
    """返回 L 个 (d,d) 权重矩阵，用 default_rng(seed).normal(0, scale, ...)。"""
    # TODO
    return None


# ---------- 第 12 题：ch14 的 h=3 悬念 / 锚点 c15-04 ----------
def train_xor(seed, scale, h=3, lr=0.5, steps=10000):
    """ch14 同一套 tanh 两层网络 + BCE + 全批量梯度下降。
    返回 (val_acc, first_loss, final_loss)。
    W1/W2 用 default_rng(seed).normal(0, scale, ...)，偏置全 0。"""
    # TODO
    return None


if __name__ == "__main__":
    # ---- 第 1~5 题：激活函数 ----
    z = np.linspace(-20, 20, 400001)
    assert np.isclose(sigmoid_grad(z).max(), 0.25, atol=1e-6)
    assert np.allclose(sigmoid_grad(np.array([-100., 0., 100.])),
                       [0., 0.25, 0.], atol=1e-12)
    assert np.allclose(leaky_relu(np.array([-1., 0., 2.])), [-0.01, 0., 2.])
    assert np.allclose(leaky_relu(np.array([-1., 2.]), a=0.2), [-0.2, 2.])
    assert np.isclose(gelu(0.0), 0.0)
    for v, ref in [(-3., -0.003637392), (-1., -0.158808009),
                   (1., 0.841191991), (3., 2.996362608)]:
        assert np.isclose(gelu(v), ref, atol=1e-8), (v, gelu(v))
    assert np.isclose(derivative_bound("sigmoid"), 0.25)
    for name in ("tanh", "relu", "leaky"):
        assert np.isclose(derivative_bound(name), 1.0)
    try:
        derivative_bound("nope")
        raise AssertionError("未知激活名应抛 ValueError")
    except ValueError:
        pass
    assert np.isclose(saturation_loss(0.0), 1.0)
    assert saturation_loss(10.0) < 2e-4
    assert saturation_loss(5.0) < saturation_loss(2.0)

    # ---- 第 6~9 题：8 层网络的信号尺度 ----
    X, W_he = make_deep(np.sqrt(2 / 32))
    stds_he = deep_forward_std(X, W_he, relu)
    assert len(stds_he) == 8
    assert 0.5 < stds_he[0] < 1.5 and 0.5 < stds_he[-1] < 1.5

    _, W_small = make_deep(0.1)
    stds_small = deep_forward_std(X, W_small, relu)
    assert stds_small[-1] < stds_small[0] * 0.01          # 太小 → 激活被压没

    _, W_big = make_deep(1.0)
    stds_big = deep_forward_std(X, W_big, relu)
    assert stds_big[-1] > stds_big[0] * 100               # 太大 → 激活爆炸

    g_he = deep_grad_norms(X, W_he, relu, relu_grad)
    assert len(g_he) == 8
    assert 0.1 < gradient_ratio(g_he) < 10                # He 基本保持
    g_small = deep_grad_norms(X, W_small, relu, relu_grad)
    assert gradient_ratio(g_small) > 100                  # 太小 → 梯度消失
    g_big = deep_grad_norms(X, W_big, relu, relu_grad)
    assert gradient_ratio(g_big) < 0.01                   # 太大 → 梯度爆炸

    Xsig, Wsig = make_deep(1.0)
    g_sig = deep_grad_norms(Xsig, Wsig, sigmoid, sigmoid_grad)
    assert gradient_ratio(g_sig) > 10                     # Sigmoid 8 层也消失

    Z = np.array([[-1., -2., 1.], [-3., -1., 2.]])
    assert np.isclose(dead_relu_fraction(Z), 2 / 3)
    assert np.isclose(dead_relu_fraction(np.full((4, 8), -1.0)), 1.0)
    assert np.isclose(dead_relu_fraction(np.full((4, 8), 1.0)), 0.0)

    # ---- 第 10~11 题：初始化 ----
    assert np.isclose(init_scale("xavier", 32, 32), np.sqrt(1 / 32))
    assert np.isclose(init_scale("he", 32, 32), 0.25)
    assert np.isclose(init_scale("xavier", 2, 3), np.sqrt(2 / 5))
    Ws = init_weights(32, 8, "he", seed=0)
    assert len(Ws) == 8 and Ws[0].shape == (32, 32)
    assert abs(Ws[0].std() - 0.25) < 0.02

    # ---- 第 12 题：seed=0 那个卡住的 h=3 ----
    acc05, first05, last05 = train_xor(0, 0.5)
    acc01, first01, last01 = train_xor(0, 0.1)
    assert 0.0 <= acc05 <= 1.0 and 0.0 <= acc01 <= 1.0
    assert last05 < first05 and last01 < first01          # 两边都在降
    assert last01 < last05                                # 0.1 收得更好
    assert acc01 >= acc05                                 # seed=0 被「救」回来了

    print("ch15 全部通过 ✓")

# region 参考答案
"""
def sigmoid_grad(z):
    s = sigmoid(z)
    return s * (1 - s)


def leaky_relu(z, a=0.01):
    z = np.asarray(z, dtype=float)
    return np.where(z > 0, z, a * z)


def gelu(z):
    z = np.asarray(z, dtype=float)
    return 0.5 * z * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (z + 0.044715 * z ** 3)))


def derivative_bound(name):
    bounds = {"sigmoid": 0.25, "tanh": 1.0, "relu": 1.0, "leaky": 1.0}
    if name not in bounds:
        raise ValueError(name)
    return bounds[name]


def saturation_loss(z):
    return sigmoid_grad(np.asarray(z, dtype=float)) / 0.25


def deep_forward_std(X, W, act):
    A = np.asarray(X, dtype=float)
    out = []
    for w in W:
        A = act(A @ w)
        out.append(float(A.std()))
    return out


def deep_grad_norms(X, W, act, local_grad):
    A = np.asarray(X, dtype=float)
    Zs = []
    for w in W:
        Z = A @ w
        Zs.append(Z)
        A = act(Z)
    n, d = A.shape
    dA = np.ones_like(A) / np.sqrt(n * d)
    out = []
    for l in reversed(range(len(W))):
        dA = (dA * local_grad(Zs[l])) @ W[l].T
        out.append(float(np.linalg.norm(dA)))
    return out[::-1]


def gradient_ratio(norms):
    return float(norms[-1]) / float(norms[0])


def dead_relu_fraction(Z):
    Z = np.asarray(Z, dtype=float)
    return float((Z <= 0).all(axis=0).mean())


def init_scale(method, fan_in, fan_out):
    if method == "xavier":
        return float(np.sqrt(2.0 / (fan_in + fan_out)))
    if method == "he":
        return float(np.sqrt(2.0 / fan_in))
    raise ValueError(method)


def init_weights(d, L, method, seed=0):
    rng = np.random.default_rng(seed)
    s = init_scale(method, d, d)
    return [rng.normal(0.0, s, (d, d)) for _ in range(L)]


def train_xor(seed, scale, h=3, lr=0.5, steps=10000):
    Xtr, ytr, Xv, yv = make_xor()
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0.0, scale, (2, h))
    b1 = np.zeros(h)
    W2 = rng.normal(0.0, scale, (h, 1))
    b2 = np.zeros(1)
    yt = ytr.reshape(-1, 1)
    n = len(Xtr)

    def loss_of(P):
        P = np.clip(P, 1e-12, 1 - 1e-12)
        return float(-np.mean(yt * np.log(P) + (1 - yt) * np.log(1 - P)))

    A1 = np.tanh(Xtr @ W1 + b1)
    first_loss = loss_of(sigmoid(A1 @ W2 + b2))
    for _ in range(steps):
        Z1 = Xtr @ W1 + b1
        A1 = np.tanh(Z1)
        P = sigmoid(A1 @ W2 + b2)
        dZ2 = (P - yt) / n
        gW2 = A1.T @ dZ2
        gb2 = dZ2.sum(axis=0)
        dZ1 = (dZ2 @ W2.T) * (1 - A1 ** 2)
        gW1 = Xtr.T @ dZ1
        gb1 = dZ1.sum(axis=0)
        W1 -= lr * gW1
        b1 -= lr * gb1
        W2 -= lr * gW2
        b2 -= lr * gb2
    A1v = np.tanh(Xv @ W1 + b1)
    Pv = sigmoid(A1v @ W2 + b2)
    acc = float(((Pv.ravel() >= 0.5).astype(int) == yv).mean())
    return acc, first_loss, loss_of(sigmoid(np.tanh(Xtr @ W1 + b1) @ W2 + b2))
"""
# endregion
