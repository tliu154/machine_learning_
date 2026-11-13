"""
ch17 练习：常见网络结构（Common Architectures）
──────────────────────────────────────────────────
重点：卷积输出尺寸 / 参数量 / 感受野、手写 conv2d、深度可分离卷积、
      IoU 与 NMS、RNN / LSTM 单步、RNN 系参数量、
      缩放点积注意力、因果掩码、√d_k 的作用、多头拆分、位置编码、注意力成本。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch17_architectures.md

说明：本文件是 ML 全局第 17 章。基础教程只到 ch12，这里没有同名文件。

本练习只用 numpy，不用 PyTorch / sklearn，不依赖仓库外文件。
教学文档里的所有数字来自同一套固定 seed，注释里标了出处。
"""

import numpy as np


# ---------- 公共工具（已给实现，不是题目） ----------
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


# ---------- 第 1 题：卷积输出尺寸 / 锚点 c17-01 ----------
def conv_output_size(H, k, s=1, p=0):
    """按 floor((H - k + 2p)/s) + 1 返回输出边长。"""
    # TODO
    return None


# ---------- 第 2 题：卷积参数量 / 锚点 c17-01 ----------
def conv_params(c_in, c_out, k, bias=True):
    """C_out * C_in * k * k (+ C_out)。"""
    # TODO
    return None


# ---------- 第 3 题：感受野 / 锚点 c17-01 ----------
def receptive_field(L, k=3, s=1):
    """L 层堆叠后的感受野边长：rf = rf + (k - 1) * 累积步长。"""
    # TODO
    return None


# ---------- 第 4 题：手写 conv2d / 锚点 c17-01 ----------
def conv2d(x, w, b, stride=1, pad=0):
    """x: (C_in,H,W)  w: (C_out,C_in,k,k)  b: (C_out,)  ->  (C_out,Ho,Wo)"""
    # TODO
    return None


# ---------- 第 5 题：深度可分离卷积参数量 / 锚点 c17-01 ----------
def depthwise_separable_params(c_in, c_out, k):
    """返回 (depthwise 部分, 1x1 投影部分, 合计)。都要算偏置。"""
    # TODO
    return None


# ---------- 第 6 题：IoU / 锚点 c17-01 ----------
def iou(a, b):
    """a,b = [x1,y1,x2,y2]，返回交并比。"""
    # TODO
    return None


# ---------- 第 7 题：NMS / 锚点 c17-01 ----------
def nms(boxes, scores, thr=0.5):
    """按分数从高到低保留框，抑制与已保留框 IoU > thr 的。返回保留的下标列表（升序输出不做要求）。"""
    # TODO
    return None


# ---------- 第 8 题：RNN 单步 / 锚点 c17-02 ----------
def rnn_step(x, h, Wx, Wh, b):
    """h_new = tanh(x @ Wx + h @ Wh + b)。"""
    # TODO
    return None


# ---------- 第 9 题：LSTM 单步 / 锚点 c17-02 ----------
def lstm_step(x, h, c, W, b):
    """W: (d_in+d_h, 4*d_h)，b: (4*d_h,)。门顺序 [f, i, o, g]。
    返回 (h_new, c_new)。"""
    # TODO
    return None


# ---------- 第 10 题：RNN 系参数量 / 锚点 c17-02 ----------
def recurrent_params(d_in, d_h, cell="lstm"):
    """cell in {"rnn","gru","lstm"}；PyTorch 每个门都有两个偏置（ih / hh），
    即单个单元为 h*(in+h) + 2h。"""
    # TODO
    return None


# ---------- 第 11 题：缩放点积注意力 / 锚点 c17-03 ----------
def attention(Q, K, V):
    """返回 (注意力矩阵 A, 输出 A@V)。按行 softmax，数值要稳定。"""
    # TODO
    return None


# ---------- 第 12 题：因果掩码 / 锚点 c17-03 ----------
def causal_mask(n):
    """返回 n x n 的布尔矩阵，True 表示允许注意（下三角含对角）。"""
    # TODO
    return None


# ---------- 第 13 题：√d_k 的作用 / 锚点 c17-03 ----------
def scaled_dot_std(d_k, n=2000, seed=7, scale=True):
    """随机 q,k（各分量 N(0,1)），返回 n 个点积的标准差。
    scale=True 时除以 sqrt(d_k)。"""
    # TODO
    return None


# ---------- 第 14 题：多头拆分 / 锚点 c17-03 ----------
def multihead_split(X, heads):
    """X: (batch, n, d_model) -> (batch, heads, n, d_model/heads)。"""
    # TODO
    return None


# ---------- 第 15 题：位置编码 / 锚点 c17-03 ----------
def positional_encoding(L, d):
    """正弦位置编码：偶数维 sin(pos / 10000^(i/d))，奇数维 cos(同分母)。"""
    # TODO
    return None


if __name__ == "__main__":
    # ---- 第 1 题 ----
    assert conv_output_size(32, 3, 1, 1) == 32
    assert conv_output_size(32, 3, 2, 1) == 16
    assert conv_output_size(224, 7, 2, 3) == 112
    assert conv_output_size(64, 5, 1, 0) == 60

    # ---- 第 2 题 ----
    assert conv_params(3, 5, 3) == 140
    assert conv_params(256, 256, 3) == 590080
    assert conv_params(256, 256, 1) == 65792
    assert conv_params(256, 256, 3, bias=False) == 589824

    # ---- 第 3 题 ----
    assert receptive_field(1) == 3
    assert receptive_field(10) == 21
    # stride=2 时：rf = 1 + (3-1)*(1+2+4) = 15
    assert receptive_field(3, k=3, s=2) == 15

    # ---- 第 4 题 ----
    x = np.array([[[1.0, 2.0], [3.0, 4.0]]])
    w = np.array([[[[1.0, 0.0], [0.0, 1.0]]]])
    b0 = np.zeros(1)
    out = conv2d(x, w, b0)
    assert out.shape == (1, 1, 1)
    assert np.isclose(out[0, 0, 0], 5.0)          # 1*1 + 4*1
    out_pad = conv2d(x, w, b0, pad=1)
    assert out_pad.shape == (1, 3, 3)
    assert np.isclose(out_pad[0, 1, 1], 5.0)
    assert np.isclose(out_pad[0, 0, 0], 1.0)      # 左上角只盖住 1
    # 教学文档：3->5, k=3, p=1, 输入 9x9 输出 5x9x9
    xx = np.random.default_rng(0).standard_normal((3, 9, 9))
    ww = np.random.default_rng(1).standard_normal((5, 3, 3, 3))
    assert conv2d(xx, ww, np.zeros(5), pad=1).shape == (5, 9, 9)

    # ---- 第 5 题 ----
    dw, pw, total = depthwise_separable_params(256, 256, 3)
    assert (dw, pw, total) == (2560, 65792, 68352)
    # 比普通 3x3 卷积省 8.6 倍
    assert total * 8 < conv_params(256, 256, 3) < total * 9

    # ---- 第 6 题 ----
    assert np.isclose(iou([10, 10, 50, 50], [12, 12, 52, 52]), 0.8223, atol=1e-3)
    assert np.isclose(iou([10, 10, 50, 50], [10, 10, 50, 80]), 0.5714, atol=1e-3)
    assert iou([0, 0, 10, 10], [20, 20, 30, 30]) == 0.0
    assert np.isclose(iou([0, 0, 10, 10], [0, 0, 10, 10]), 1.0)

    # ---- 第 7 题 ----
    boxes = np.array([[10, 10, 50, 50], [12, 12, 52, 52], [10, 10, 50, 80],
                      [10, 10, 50, 66], [100, 100, 140, 140]], dtype=float)
    scores = np.array([0.95, 0.88, 0.80, 0.72, 0.90])
    assert sorted(nms(boxes, scores, 0.5)) == [0, 4]
    assert sorted(nms(boxes, scores, 0.7)) == [0, 2, 4]
    assert sorted(nms(boxes, scores, 0.9)) == [0, 1, 2, 3, 4]

    # ---- 第 8 题 ----
    Wh = np.eye(2)
    h = rnn_step(np.zeros(2), np.zeros(2), np.eye(2), Wh, np.zeros(2))
    assert np.allclose(h, 0.0)
    # 输入 1、隐状态 0 -> tanh(1)
    h = rnn_step(np.ones(2), np.zeros(2), np.eye(2), Wh, np.zeros(2))
    assert np.allclose(h, np.tanh(1.0))

    # ---- 第 9 题 ----
    d_in, d_h = 2, 2
    W0 = np.zeros((d_in + d_h, 4 * d_h))
    hn, cn = lstm_step(np.ones(d_in), np.zeros(d_h), np.ones(d_h), W0, np.zeros(4 * d_h))
    # 全零权重 + 零偏置：f=i=o=0.5，g=0 -> c=0.5，h=0.5*tanh(0.5)
    assert np.allclose(cn, 0.5)
    assert np.allclose(hn, 0.5 * np.tanh(0.5))

    # ---- 第 10 题 ----
    assert recurrent_params(16, 32, "rnn") == 1600
    assert recurrent_params(16, 32, "gru") == 4800
    assert recurrent_params(16, 32, "lstm") == 6400

    # ---- 第 11 题 ----
    rng = np.random.default_rng(1)
    Q, K, V = (rng.normal(0, 1, (3, 4)) for _ in range(3))
    A, out = attention(Q, K, V)
    assert A.shape == (3, 3) and out.shape == (3, 4)
    assert np.allclose(A.sum(axis=1), 1.0)                 # 每行和为 1
    assert np.allclose(A[0], [0.2552, 0.4599, 0.2849], atol=1e-3)

    # ---- 第 12 题 ----
    m = causal_mask(3)
    assert m.dtype == bool and m.shape == (3, 3)
    assert np.array_equal(m, np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]], dtype=bool))
    assert np.triu(causal_mask(5), k=1).sum() == 0

    # ---- 第 13 题 ----
    assert np.isclose(scaled_dot_std(64, scale=True), 1.0, atol=0.06)
    assert np.isclose(scaled_dot_std(64, scale=False), 8.0, atol=0.5)
    assert np.isclose(scaled_dot_std(1024, scale=False), 32.0, atol=2.0)
    # 不缩放时 std ≈ sqrt(d_k)
    for dk in (8, 64, 256):
        assert np.isclose(scaled_dot_std(dk, scale=False), np.sqrt(dk), atol=0.1 * np.sqrt(dk))

    # ---- 第 14 题 ----
    X = np.arange(2 * 4 * 8, dtype=float).reshape(2, 4, 8)
    Y = multihead_split(X, 2)
    assert Y.shape == (2, 2, 4, 4)
    # 拼回去要和原张量一致
    assert np.allclose(Y.transpose(0, 2, 1, 3).reshape(2, 4, 8), X)

    # ---- 第 15 题 ----
    pe = positional_encoding(50, 32)
    assert pe.shape == (50, 32)
    assert np.isclose(pe[0, 0], 0.0) and np.isclose(pe[0, 1], 1.0)   # pos=0: sin=0, cos=1

    def cos_sim(a, b):
        return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

    # 教学文档：位置 0 与 1/5/10 的余弦相似度
    assert np.isclose(cos_sim(pe[0], pe[1]), 0.957, atol=5e-3)
    assert np.isclose(cos_sim(pe[0], pe[5]), 0.736, atol=5e-3)
    assert cos_sim(pe[0], pe[49]) < cos_sim(pe[0], pe[5])          # 越远越不像

    print("ch17 全部通过 ✓")


# region 参考答案
"""
def conv_output_size(H, k, s=1, p=0):
    return (H - k + 2 * p) // s + 1


def conv_params(c_in, c_out, k, bias=True):
    return c_out * c_in * k * k + (c_out if bias else 0)


def receptive_field(L, k=3, s=1):
    rf, jump = 1, 1
    for _ in range(L):
        rf += (k - 1) * jump
        jump *= s
    return rf


def conv2d(x, w, b, stride=1, pad=0):
    if pad:
        x = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    C_in, H, W = x.shape
    C_out, _, k, _ = w.shape
    Ho = (H - k) // stride + 1
    Wo = (W - k) // stride + 1
    out = np.zeros((C_out, Ho, Wo))
    for co in range(C_out):
        for i in range(Ho):
            for j in range(Wo):
                patch = x[:, i * stride:i * stride + k, j * stride:j * stride + k]
                out[co, i, j] = np.sum(patch * w[co]) + b[co]
    return out


def depthwise_separable_params(c_in, c_out, k):
    dw = c_in * k * k + c_in
    pw = c_in * c_out + c_out
    return dw, pw, dw + pw


def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter + 1e-12)


def nms(boxes, scores, thr=0.5):
    order = np.argsort(scores)[::-1]
    keep = []
    while len(order):
        i = order[0]
        keep.append(int(i))
        rest = order[1:]
        if len(rest) == 0:
            break
        ious = np.array([iou(boxes[i], boxes[j]) for j in rest])
        order = rest[ious <= thr]
    return keep


def rnn_step(x, h, Wx, Wh, b):
    return np.tanh(x @ Wx + h @ Wh + b)


def lstm_step(x, h, c, W, b):
    z = np.concatenate([x, h]) @ W + b
    f, i, o, g = np.split(z, 4)
    f, i, o = sigmoid(f), sigmoid(i), sigmoid(o)
    c_new = f * c + i * np.tanh(g)
    h_new = o * np.tanh(c_new)
    return h_new, c_new


def recurrent_params(d_in, d_h, cell="lstm"):
    unit = d_h * (d_in + d_h) + 2 * d_h
    gates = {"rnn": 1, "gru": 3, "lstm": 4}[cell]
    return gates * unit


def attention(Q, K, V):
    d_k = Q.shape[-1]
    s = Q @ K.T / np.sqrt(d_k)
    s = s - s.max(axis=-1, keepdims=True)
    a = np.exp(s) / np.exp(s).sum(axis=-1, keepdims=True)
    return a, a @ V


def causal_mask(n):
    return np.tril(np.ones((n, n), dtype=bool))


def scaled_dot_std(d_k, n=2000, seed=7, scale=True):
    rng = np.random.default_rng(seed)
    q = rng.normal(0, 1, (n, d_k))
    k = rng.normal(0, 1, (n, d_k))
    dots = np.sum(q * k, axis=1)
    if scale:
        dots = dots / np.sqrt(d_k)
    return float(dots.std())


def multihead_split(X, heads):
    batch, n, d = X.shape
    return X.reshape(batch, n, heads, d // heads).transpose(0, 2, 1, 3)


def positional_encoding(L, d):
    pe = np.zeros((L, d))
    for pos in range(L):
        for i in range(0, d, 2):
            pe[pos, i] = np.sin(pos / 10000 ** (i / d))
            if i + 1 < d:
                pe[pos, i + 1] = np.cos(pos / 10000 ** (i / d))
    return pe
"""
# endregion
