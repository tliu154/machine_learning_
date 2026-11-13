"""
ch12 练习：降维与表示（Dimensionality Reduction）
──────────────────────────────────────────────────
重点：协方差与特征值分解、解释方差比、投影/重构恒等式、白化、
      保邻域率、t-SNE 的 Q 与 KL 梯度、线性自编码器、降维检索的 recall 权衡。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch12_dimensionality.md

⚠️ 章号撞名：00_foundations/python_basics/exercises/ch12_ex.py 是
Python 基础教程自己的第 12 章「递归」，与本文件（ML 全局第 12 章降维）
毫无关系。两套 ch12_ex.py 内容完全不同，按完整路径打开，别只搜文件名。

本练习只用 numpy，不依赖 sklearn、不依赖仓库外文件。
教学文档里的对比数字全部来自同一套数据生成器，跑通即可亲手复现。
"""

import numpy as np


# ---------- 与教学文档一致的数据 ----------
def make_redundant(n=300, d=10, seed=42):
    """真实秩只有 3：d 维全是 3 个隐变量的线性混合 + 小噪声。"""
    r = np.random.default_rng(seed)
    Z = r.normal(size=(n, 3)) * np.array([3.0, 1.5, 0.7])
    M = r.normal(size=(3, d))
    return Z @ M + r.normal(0, 0.05, (n, d))


def make_scale(n=200, seed=7):
    """x 是 sigma=500 的纯噪声，y 才是两簇信号。"""
    r = np.random.default_rng(seed)
    y = np.r_[np.zeros(n // 2, int), np.ones(n // 2, int)]
    X = np.column_stack([r.normal(0, 500, n),
                         np.where(y == 0, -2., 2.) + r.normal(0, 0.3, n)])
    return X, y


def make_roll(n=300, seed=0):
    """瑞士卷（自己造，不依赖 sklearn）：返回 3D 点和沿卷的参数 t。"""
    r = np.random.default_rng(seed)
    t = 1.5 * np.pi * (1 + 2 * r.random(n))
    return np.column_stack([t * np.cos(t), 21 * r.random(n), t * np.sin(t)]), t


def make_embeddings(n_groups=20, per=25, d=64, seed=42):
    """模拟以图搜图：500 张图的 64 维 embedding，20 组，每组一条 query。"""
    r = np.random.default_rng(seed)
    C = r.normal(size=(n_groups, d))
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    X = np.repeat(C, per, axis=0) + r.normal(0, 0.35, (n_groups * per, d))
    Q = C + r.normal(0, 0.15, (n_groups, d))
    y = np.repeat(np.arange(n_groups), per)
    return X, Q, y


# ---------- 第 1 题：协方差矩阵 / 锚点 c12-01 ----------
def covariance_matrix(X):
    """返回 (Xc, C)：Xc = 中心化后的 X；C = Xc.T @ Xc / n（ddof=0）。
    不得修改传入的 X。"""
    # TODO
    return None


# ---------- 第 2 题：特征值分解 / 锚点 c12-01 ----------
def pca_components(X):
    """返回 (evals, V, mean)：特征值降序、V 的列是对应单位特征向量、mean 是列均值。
    对称矩阵用 np.linalg.eigh；【固定符号】每列绝对值最大的元素取正，保证结果可复现。"""
    # TODO
    return None


# ---------- 第 3 题：解释方差比 / 锚点 c12-01 ----------
def explained_variance_ratio(evals, k):
    """返回前 k 个主成分的累计解释方差比（float）。
    k<=0 返回 0.0；k 超过维数返回 1.0；全零特征值返回 0.0。"""
    # TODO
    return None


# ---------- 第 4 题：投影 / 锚点 c12-01 ----------
def pca_project(X, mean, V, k):
    """把 X 投影到前 k 个主成分上，返回 (n,k) 的编码 Z。"""
    # TODO
    return None


# ---------- 第 5 题：重构 / 锚点 c12-01 ----------
def pca_reconstruct(X, mean, V, k):
    """投影再还原回原空间，返回 (n,d) 的 Xhat（加回 mean）。"""
    # TODO
    return None


# ---------- 第 6 题：白化 / 锚点 c12-01 ----------
def whiten(Z, evals):
    """Z 除以每列对应特征值的平方根；evals<=0 时用 1e-12 兜底防除零。
    不得修改传入的 Z。"""
    # TODO
    return None


# ---------- 第 7 题：保邻域率 / 锚点 c12-02 ----------
def knn_preservation(Xh, Yl, k=10):
    """高维 k 近邻里有多少在低维仍是 k 近邻，返回平均比例 [0,1]。
    自身不算邻居；k 会被截断到 n-1。n<=1 返回 1.0。"""
    # TODO
    return None


# ---------- 第 8 题：Student-t Q 矩阵 / 锚点 c12-02 ----------
def student_t_q(Y):
    """返回 t-SNE 低维配对概率 Q：q_ij ∝ (1+||y_i-y_j||²)^(-1)，
    对角置 0，全矩阵归一化到和为 1。"""
    # TODO
    return None


# ---------- 第 9 题：t-SNE 的 KL 梯度 / 锚点 c12-02 ----------
def tsne_gradient(P, Y):
    """返回 dC/dY（与 Y 同形状），
    C = KL(P||Q)，梯度 = 4 (diag(D.sum(axis=1)) - D) @ Y，D=(P-Q)*inv。"""
    # TODO
    return None


# ---------- 第 10 题：线性自编码器梯度 / 锚点 c12-03 ----------
def ae_gradient(Xc, W, V):
    """线性 AE：M = W @ V，L = ||Xc - Xc @ M||² / n。
    返回 (dL/dW, dL/dV)，不要修改输入。"""
    # TODO
    return None


# ---------- 第 11 题：训练线性 AE / 锚点 c12-03 ----------
def train_linear_ae(Xc, k, lr=0.05, steps=5000, seed=0):
    """梯度下降训练线性 AE，返回 (W, V)。
    初始化 default_rng(seed).normal(0, 0.1, ...) 两个矩阵。"""
    # TODO
    return None


# ---------- 第 12 题：降维后的检索召回率 / 章末实践 ----------
def pca_recall_at_k(Xdb, Q, ydb, yq, k, topk=5):
    """在 Xdb 上 fit PCA 并降到 k 维（Xdb/Q 都减训练集均值），
    用余弦相似度取 topk，返回每条 query 命中同组样本的平均比例。"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    def ae_loss(Xc, W, V):
        R = Xc - Xc @ W @ V
        return float(np.sum(R ** 2) / len(Xc))

    X = make_redundant()
    Xs, ys = make_scale()
    Xroll, troll = make_roll()
    Xe, Qe, ye = make_embeddings()
    yq = np.arange(20)
    eps = 1e-6

    # 第 1 题：数值、对称、中心化、无副作用
    Xt = np.array([[0., 0.], [2., 0.], [0., 2.], [2., 2.]])
    Xc, C = covariance_matrix(Xt)
    assert np.allclose(Xc.mean(axis=0), 0.0)
    assert np.allclose(C, [[1., 0.], [0., 1.]])
    assert np.allclose(C, C.T)
    Xt_copy = Xt.copy()
    covariance_matrix(Xt)
    assert np.array_equal(Xt, Xt_copy), "不应该修改输入 X"

    # 第 2 题：降序、正交、符号固定、特征值方程、与实跑数值一致、缩放前后 PC1
    evals, V, mean = pca_components(X)
    assert np.all(np.diff(evals) <= 1e-10), "特征值要降序"
    assert np.allclose(V.T @ V, np.eye(X.shape[1]), atol=1e-8), "特征向量要正交"
    for j in range(V.shape[1]):
        assert V[np.argmax(np.abs(V[:, j])), j] > 0, "每列最大绝对值元素应为正"
    Xc_big, C_big = covariance_matrix(X)
    assert np.allclose(C_big @ V[:, 0], evals[0] * V[:, 0], atol=1e-8), "Cv = lambda v"
    assert np.allclose(evals[:3], [99.9805, 23.2048, 1.9115], atol=1e-3)
    assert abs(evals[3]) < 0.01
    _, V_raw, _ = pca_components(Xs)
    assert abs(V_raw[1, 0]) < 0.001, "缩放前 PC1 几乎不碰真实信号列"
    Xz = (Xs - Xs.mean(axis=0)) / Xs.std(axis=0)
    _, V_z, _ = pca_components(Xz)
    assert abs(V_z[1, 0]) > 0.7, "标准化后 PC1 必须包含真实信号列"

    # 第 3 题：累计解释方差比、边界
    assert np.isclose(explained_variance_ratio([4, 3, 2, 1], 2), 0.7)
    assert explained_variance_ratio([4, 3, 2, 1], 0) == 0.0
    assert explained_variance_ratio([4, 3, 2, 1], 99) == 1.0
    assert explained_variance_ratio([0, 0, 0], 2) == 0.0
    assert np.isclose(explained_variance_ratio(evals, 3), 0.99986, atol=1e-4)

    # 第 4 / 5 题：形状、k=d 完全还原、重构误差恒等式
    Z = pca_project(X, mean, V, 3)
    assert Z.shape == (300, 3)
    assert np.allclose(Z, (X - mean) @ V[:, :3])
    Xhat = pca_reconstruct(X, mean, V, X.shape[1])
    assert np.allclose(Xhat, X, atol=1e-8), "k=d 应无损还原"
    for k, expect in [(1, 2.513379), (2, 0.192896), (3, 0.001748)]:
        err = float(np.mean((X - pca_reconstruct(X, mean, V, k)) ** 2))
        assert np.isclose(err, expect, atol=1e-5)
        assert np.isclose(err, evals[k:].sum() / X.shape[1], atol=1e-8), \
            "重构误差必须等于丢弃特征值之和 / d"

    # 第 6 题：白化后协方差是单位阵（ddof=0），常数方向不炸，无副作用
    Z3 = pca_project(X, mean, V, 3)
    Zw = whiten(Z3, evals[:3])
    assert np.allclose(Zw.T @ Zw / len(Zw), np.eye(3), atol=1e-8)
    assert np.all(np.isfinite(whiten(np.ones((2, 2)), np.array([0., 0.]))))
    Z3_copy = Z3.copy()
    whiten(Z3, evals[:3])
    assert np.array_equal(Z3, Z3_copy), "不应该修改输入 Z"

    # 第 7 题：相同坐标=1、PCA 2D 明显优于随机、k 截断不报错
    _, Vr, mr = pca_components(Xroll)
    Y_pca = pca_project(Xroll, mr, Vr, 2)
    Y_rand = np.random.default_rng(123).normal(size=(len(Xroll), 2))
    assert knn_preservation(Xroll, Xroll, 10) == 1.0
    p_pca = knn_preservation(Xroll, Y_pca, 10)
    p_rand = knn_preservation(Xroll, Y_rand, 10)
    assert 0.35 < p_pca < 0.50 and p_rand < 0.10
    assert p_pca > p_rand + 0.2
    assert 0.0 <= knn_preservation(Xroll[:4], Y_pca[:4], 99) <= 1.0
    assert knn_preservation(np.array([[1., 2.]]), np.array([[0., 0.]])) == 1.0

    # 第 8 题：对称、对角 0、和为 1、两点解析值
    Q2 = student_t_q(np.array([[0., 0.], [1., 0.]]))
    assert np.allclose(Q2, [[0., 0.5], [0.5, 0.]])
    Q = student_t_q(np.random.default_rng(0).normal(size=(12, 2)))
    assert Q.shape == (12, 12) and np.allclose(Q, Q.T)
    assert np.allclose(np.diag(Q), 0.0) and np.isclose(Q.sum(), 1.0)

    # 第 9 题：解析梯度 vs 中心差分（KL 数值求导）
    P = student_t_q(np.random.default_rng(1).normal(size=(12, 2)))
    P = (P + P.T) / 2
    P /= P.sum()
    Y = np.random.default_rng(0).normal(size=(12, 2))
    G = tsne_gradient(P, Y)

    def kl(P, Y):
        Qq = student_t_q(Y)
        m = P > 0
        return float(np.sum(P[m] * np.log(P[m] / Qq[m])))

    num = np.zeros_like(Y)
    for i in range(len(Y)):
        for j in range(Y.shape[1]):
            Yp, Ym = Y.copy(), Y.copy()
            Yp[i, j] += eps
            Ym[i, j] -= eps
            num[i, j] = (kl(P, Yp) - kl(P, Ym)) / (2 * eps)
    assert G.shape == Y.shape
    assert np.allclose(G, num, atol=1e-6), "KL 梯度应与数值梯度一致"

    # 第 10 题：AE 解析梯度 vs 中心差分（W 和 V 各抽一项）
    Xae = (X - X.mean(axis=0)) / 10.0
    W0 = np.random.default_rng(0).normal(0, 0.1, (10, 3))
    V0 = np.random.default_rng(0).normal(0, 0.1, (3, 10))
    gW, gV = ae_gradient(Xae, W0, V0)
    Wp, Wm = W0.copy(), W0.copy()
    Wp[0, 0] += eps
    Wm[0, 0] -= eps
    assert np.isclose(gW[0, 0], (ae_loss(Xae, Wp, V0) - ae_loss(Xae, Wm, V0)) / (2 * eps), atol=1e-6)
    Vp, Vm = V0.copy(), V0.copy()
    Vp[0, 0] += eps
    Vm[0, 0] -= eps
    assert np.isclose(gV[0, 0], (ae_loss(Xae, W0, Vp) - ae_loss(Xae, W0, Vm)) / (2 * eps), atol=1e-6)
    assert gW.shape == W0.shape and gV.shape == V0.shape

    # 第 11 题：训练后收敛到 PCA 的理论最优重构损失
    e_ae, _, _ = pca_components(Xae)
    target = float(e_ae[3:].sum())
    Wf, Vf = train_linear_ae(Xae, 3, lr=0.05, steps=5000, seed=0)
    final = ae_loss(Xae, Wf, Vf)
    assert np.isfinite(final) and final > 0
    assert abs(final - target) / target < 0.05, "线性 AE 应收敛到 PCA 最优（差 2.24%）"

    # 第 12 题：亲手复现「维度 → 召回率」权衡表
    r64 = pca_recall_at_k(Xe, Qe, ye, yq, 64)
    r16 = pca_recall_at_k(Xe, Qe, ye, yq, 16)
    r8 = pca_recall_at_k(Xe, Qe, ye, yq, 8)
    assert np.isclose(r64, 0.74, atol=1e-6)
    assert np.isclose(r16, 0.70, atol=1e-6)
    assert np.isclose(r8, 0.52, atol=1e-6)
    assert r64 >= r16 > r8, "降到 16 维几乎不掉点，8 维断崖"

    print("ch12 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def covariance_matrix(X):
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0)
    return Xc, Xc.T @ Xc / len(Xc)


def pca_components(X):
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=0)
    Xc = X - mean
    C = Xc.T @ Xc / len(Xc)
    evals, V = np.linalg.eigh(C)
    order = np.argsort(evals)[::-1]
    evals, V = evals[order], V[:, order].copy()
    for j in range(V.shape[1]):
        if V[np.argmax(np.abs(V[:, j])), j] < 0:
            V[:, j] *= -1
    return evals, V, mean


def explained_variance_ratio(evals, k):
    evals = np.asarray(evals, dtype=float)
    total = evals.sum()
    if total <= 0:
        return 0.0
    return float(evals[:k].sum() / total)


def pca_project(X, mean, V, k):
    X = np.asarray(X, dtype=float)
    return (X - np.asarray(mean, dtype=float)) @ np.asarray(V, dtype=float)[:, :k]


def pca_reconstruct(X, mean, V, k):
    X = np.asarray(X, dtype=float)
    V = np.asarray(V, dtype=float)
    Z = pca_project(X, mean, V, k)
    return Z @ V[:, :k].T + np.asarray(mean, dtype=float)


def whiten(Z, evals):
    Z = np.asarray(Z, dtype=float)
    evals = np.asarray(evals, dtype=float)
    return Z / np.sqrt(np.maximum(evals, 1e-12))


def knn_preservation(Xh, Yl, k=10):
    Xh = np.asarray(Xh, dtype=float)
    Yl = np.asarray(Yl, dtype=float)
    kk = min(k, len(Xh) - 1)
    if kk <= 0:
        return 1.0

    def neigh(A):
        d2 = ((A[:, None, :] - A[None, :, :]) ** 2).sum(axis=2)
        np.fill_diagonal(d2, np.inf)
        return np.argsort(d2, axis=1)[:, :kk]

    a, b = neigh(Xh), neigh(Yl)
    return float(np.mean([len(set(a[i]) & set(b[i])) / kk
                         for i in range(len(a))]))


def student_t_q(Y):
    Y = np.asarray(Y, dtype=float)
    d2 = ((Y[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2)
    num = 1.0 / (1.0 + d2)
    np.fill_diagonal(num, 0.0)
    total = num.sum()
    if total <= 0:
        return np.zeros_like(num)
    return num / total


def tsne_gradient(P, Y):
    P = np.asarray(P, dtype=float)
    Y = np.asarray(Y, dtype=float)
    d2 = ((Y[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2)
    inv = 1.0 / (1.0 + d2)
    np.fill_diagonal(inv, 0.0)
    Q = inv / inv.sum()
    D = (P - Q) * inv
    return 4.0 * (np.diag(D.sum(axis=1)) - D) @ Y


def ae_gradient(Xc, W, V):
    Xc = np.asarray(Xc, dtype=float)
    W = np.asarray(W, dtype=float)
    V = np.asarray(V, dtype=float)
    n = len(Xc)
    R = Xc - Xc @ W @ V
    G = -2.0 * Xc.T @ R / n
    return G @ V.T, W.T @ G


def train_linear_ae(Xc, k, lr=0.05, steps=5000, seed=0):
    Xc = np.asarray(Xc, dtype=float)
    r = np.random.default_rng(seed)
    W = r.normal(0, 0.1, (Xc.shape[1], k))
    V = r.normal(0, 0.1, (k, Xc.shape[1]))
    for _ in range(steps):
        gW, gV = ae_gradient(Xc, W, V)
        W -= lr * gW
        V -= lr * gV
    return W, V


def pca_recall_at_k(Xdb, Q, ydb, yq, k, topk=5):
    Xdb = np.asarray(Xdb, dtype=float)
    Q = np.asarray(Q, dtype=float)
    _, V, mean = pca_components(Xdb)
    C = V[:, :k]
    Xp = (Xdb - mean) @ C
    Qp = (Q - mean) @ C
    Xn = Xp / np.linalg.norm(Xp, axis=1, keepdims=True)
    Qn = Qp / np.linalg.norm(Qp, axis=1, keepdims=True)
    idx = np.argsort(-(Qn @ Xn.T), axis=1)[:, :topk]
    ydb = np.asarray(ydb)
    yq = np.asarray(yq)
    return float(np.mean([np.mean(ydb[idx[i]] == yq[i])
                         for i in range(len(Q))]))
"""
# endregion
