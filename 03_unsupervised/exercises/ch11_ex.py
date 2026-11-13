"""
ch11 练习：聚类（Clustering）
──────────────────────────────────────────────────
重点：距离矩阵、K-means 分配/更新/收敛、缩放、层次聚类 linkage、
      DBSCAN 密度扩张、轮廓系数与簇数选择。
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：../docs/ch11_clustering.md

⚠️ 章号撞名：00_foundations/python_basics/exercises/ch11_ex.py 是
Python 基础教程自己的第 11 章「模块与包」，与本文件（ML 全局第 11 章聚类）
毫无关系。两套 ch11_ex.py 内容完全不同，按完整路径打开，别只搜文件名。

本练习只用 numpy + 标准库 itertools，不依赖 sklearn、不依赖仓库外文件。
教学文档里的对比数字全部来自同一套数据生成器，跑通即可亲手复现。
"""

import numpy as np
from itertools import permutations


# ---------- 与教学文档一致的三份数据 ----------
def make_blobs(n_per=50, seed=42):
    centers = np.array([[-3., -3.], [0., 3.], [3., -3.]])
    y = np.repeat(np.arange(3), n_per)
    X = centers[y] + np.random.default_rng(seed).normal(0, 0.6, (3 * n_per, 2))
    return X, y


def make_rings(n_per=150, seed=42):
    r = np.random.default_rng(seed)
    t1 = np.linspace(0, 2 * np.pi, n_per, endpoint=False) + r.normal(0, 0.01, n_per)
    t2 = np.linspace(0, 2 * np.pi, n_per, endpoint=False) + r.normal(0, 0.01, n_per)
    inner = np.column_stack([np.cos(t1), np.sin(t1)]) + r.normal(0, 0.06, (n_per, 2))
    outer = 2.5 * np.column_stack([np.cos(t2), np.sin(t2)]) + r.normal(0, 0.06, (n_per, 2))
    X = np.vstack([inner, outer])
    y = np.r_[np.zeros(n_per, int), np.ones(n_per, int)]
    return X, y


def make_scale(n_per=60, seed=7):
    r = np.random.default_rng(seed)
    y = np.r_[np.zeros(n_per, int), np.ones(n_per, int)]
    X = np.column_stack([r.normal(0, 500, 2 * n_per),
                         np.where(y == 0, -2., 2.) + r.normal(0, 0.3, 2 * n_per)])
    return X, y


# ---------- 第 1 题：成对距离 / 锚点 c11-01 ----------
def pairwise_distances(X):
    """返回 (n,n) 欧氏距离矩阵，对角线为 0。X 至少 1 个点。"""
    # TODO
    return None


# ---------- 第 2 题：K-means 分配步 / 锚点 c11-01 ----------
def assign_clusters(X, C):
    """返回 (labels, inertia)：每个点归到最近的质心（平局取较小下标）；
    inertia = 各点到自己质心的距离平方和。"""
    # TODO
    return None


# ---------- 第 3 题：K-means 更新步 / 锚点 c11-01 ----------
def update_centers(X, labels, C):
    """按 labels 求各簇均值作为新质心；【空簇保持旧质心 C[j] 不变】。
    不得修改传入的 C，返回新数组。"""
    # TODO
    return None


# ---------- 第 4 题：完整 K-means / 锚点 c11-01 ----------
def kmeans_fit(X, C0, iters=100, tol=1e-10):
    """反复「分配 → 更新」直到质心几乎不动或到 iters。
    返回 (C, labels, n_iter)，其中 labels 必须用【最终】质心重新分配。
    iters=1 就是篇 README 要求的「手工迭代一轮验证质心更新」。"""
    # TODO
    return None


# ---------- 第 5 题：标准化 / 锚点 c11-01 ----------
def standardize(X):
    """逐列减均值除标准差（ddof=0）；标准差为 0 的列整列返回 0（防除零）。
    不得修改传入的 X。"""
    # TODO
    return None


# ---------- 第 6 题：簇间距离 / 锚点 c11-02 ----------
def linkage_distance(D, idx_a, idx_b, method="single"):
    """给定距离矩阵 D 和两簇的样本下标（一维数组），返回簇间距离：
    single=min / complete=max / average=mean。未知 method 抛 ValueError。"""
    # TODO
    return None


# ---------- 第 7 题：层次聚类 / 锚点 c11-02 ----------
def agglomerative(X, k, method="single"):
    """自底向上每轮合并距离最近的两簇，直到剩 k 簇；返回标签数组 0..k-1。
    k>=1；k=1 时全为 0。"""
    # TODO
    return None


# ---------- 第 8 题：DBSCAN / 锚点 c11-03 ----------
def dbscan(X, eps, min_samples=5):
    """密度聚类：返回标签，噪声记 -1，簇编号从 0 起。
    核心点 = eps 邻域内至少 min_samples 个点（含自身）；只有核心点能继续扩张。"""
    # TODO
    return None


# ---------- 第 9 题：eps 敏感性 / 锚点 c11-03 ----------
def eps_scan(X, eps_values, min_samples=5):
    """对每个 eps 调 dbscan，返回 [(eps, 簇数, 噪声点数), ...]；簇数不含噪声类。"""
    # TODO
    return None


# ---------- 第 10 题：轮廓系数 / 锚点 c11-04 ----------
def silhouette(X, labels):
    """返回平均轮廓系数 s=(b-a)/max(a,b)；单样本簇的 s 定义为 0。
    调用前请自行剔除噪声点（标签 -1），本函数不自动过滤。"""
    # TODO
    return None


# ---------- 第 11 题：标签对齐准确率 / 锚点 c11-04 ----------
def cluster_acc(y, labels):
    """枚举标签排列，返回最佳对齐准确率（教学演示用，真实项目没有真值）。
    簇数 k = max(labels)+1；k>5 时返回 0.0 防止排列爆炸；不允许负标签。"""
    # TODO
    return None


# ---------- 第 12 题：簇数扫描 / 锚点 c11-04 ----------
def k_scan(X, k_values, seed=42, n_init=5):
    """对每个 k 跑 n_init 次随机初始化的 K-means，取 inertia 最小的结果。
    返回 (rows, best_k)：rows = [(k, inertia, silhouette), ...]，
    best_k = 轮廓系数最大的那个 k。"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    def purity(labels, y):
        """簇纯度：不依赖标签编号，用于无监督结果的粗略对照。"""
        labels, y = np.asarray(labels), np.asarray(y)
        return sum(max(int(np.sum(y[labels == j] == c)) for c in np.unique(y))
                   for j in range(labels.max() + 1)) / len(y)

    X_blobs, y_blobs = make_blobs()
    X_rings, y_rings = make_rings()
    X_scale, y_scale = make_scale()

    # 第 1 题：数值、对称、对角线、单点、与 for 循环一致
    D = pairwise_distances(np.array([[0., 0.], [3., 4.]]))
    assert D.shape == (2, 2) and np.allclose(D, [[0., 5.], [5., 0.]])
    assert np.allclose(np.diag(pairwise_distances(X_blobs)), 0.0)
    assert np.allclose(pairwise_distances(np.array([[1., 2.]])), [[0.]])
    assert np.allclose(D, D.T)

    # 第 2 题：标签、inertia、平局取小下标、单质心
    Xs = np.array([[0.], [1.], [10.], [11.]])
    lab, J = assign_clusters(Xs, np.array([[0.], [10.]]))
    assert np.array_equal(lab, [0, 0, 1, 1]) and np.isclose(J, 2.0)
    lab2, J2 = assign_clusters(np.array([[1.]]), np.array([[0.], [2.]]))
    assert lab2[0] == 0 and np.isclose(J2, 1.0)      # 距离相等，取下标 0
    assert np.array_equal(assign_clusters(Xs, np.array([[5.]]))[0], np.zeros(4, int))

    # 第 3 题：正常、空簇保持旧质心、无副作用
    C0 = np.array([[0., 0.], [10., 10.]])
    Cn = update_centers(np.array([[0., 0.], [2., 2.], [9., 9.]]),
                        np.array([0, 0, 1]), C0)
    assert np.allclose(Cn, [[1., 1.], [9., 9.]])
    Ce = update_centers(np.array([[0., 0.], [2., 2.]]), np.array([0, 0]), C0)
    assert np.allclose(Ce[1], C0[1]), "空簇应保持旧质心"
    assert np.allclose(Ce[0], [1., 1.]), "非空簇仍要更新"
    assert np.allclose(C0, [[0., 0.], [10., 10.]]), "不应该修改输入 C"

    # 第 4 题：iters=1 手工一轮、完整收敛轮数与 inertia、最终 labels 一致
    init = X_blobs[[0, 50, 100]]
    C1, l1, n1 = kmeans_fit(X_blobs, init, iters=1)
    l_init, _ = assign_clusters(X_blobs, init)
    assert n1 == 1
    assert np.allclose(C1, update_centers(X_blobs, l_init, init)), "一轮后质心应等于各簇均值"
    C, labels, n_iter = kmeans_fit(X_blobs, init)
    assert n_iter == 2
    assert np.isclose(assign_clusters(X_blobs, C)[1], 93.0361, atol=1e-3)
    assert np.array_equal(labels, assign_clusters(X_blobs, C)[0]), "labels 要用最终质心重算"
    assert cluster_acc(y_blobs, labels) == 1.0

    # 第 5 题：均值/标准差、全相等列、无副作用；并亲手复现缩放前后差距
    Z = standardize(X_scale)
    assert np.allclose(Z.mean(axis=0), 0.0, atol=1e-10)
    assert np.allclose(Z.std(axis=0), 1.0, atol=1e-10)
    Xc = X_scale.copy()
    Zc = standardize(np.array([[5., 1.], [5., 3.], [5., 9.]]))
    assert np.allclose(Zc[:, 0], 0.0), "标准差为 0 的列应整列为 0"
    assert np.array_equal(X_scale, Xc), "不应该修改输入 X"
    _, l_raw, _ = kmeans_fit(X_scale, X_scale[[0, 60]])
    _, l_std, _ = kmeans_fit(Z, Z[[0, 60]])
    assert purity(l_raw, y_scale) < 0.7, "缩放前被大量纲特征垄断"
    assert purity(l_std, y_scale) > 0.95, "缩放后应按 y 分开"

    # 第 6 题：三种 linkage、单元素簇、非法 method
    Dm = pairwise_distances(np.array([[0.], [1.], [5.], [9.]]))
    a, b = np.array([0, 1]), np.array([2, 3])
    assert np.isclose(linkage_distance(Dm, a, b, "single"), 4.0)
    assert np.isclose(linkage_distance(Dm, a, b, "complete"), 9.0)
    assert np.isclose(linkage_distance(Dm, a, b, "average"), 6.5)
    assert np.isclose(linkage_distance(Dm, np.array([0]), np.array([3]), "single"), 9.0)
    try:
        linkage_distance(Dm, a, b, "oops")
        assert False, "未知 method 应该抛 ValueError"
    except ValueError:
        pass

    # 第 7 题：环形数据上 single 明显优于 complete；k 的两端边界
    sub = np.r_[np.arange(0, 40), np.arange(150, 190)]
    Xs2, ys2 = X_rings[sub], y_rings[sub]
    lsingle = agglomerative(Xs2, 2, "single")
    lcomplete = agglomerative(Xs2, 2, "complete")
    assert purity(lsingle, ys2) > 0.95
    assert purity(lsingle, ys2) > purity(lcomplete, ys2) + 0.2
    assert np.all(agglomerative(Xs2, 1) == 0)
    assert len(np.unique(agglomerative(Xs2[:5], 5))) == 5

    # 第 8 题：环形数据 2 簇 0 噪声、eps 太小几乎全噪声、简单三点例子
    ld = dbscan(X_rings, eps=0.5, min_samples=5)
    assert len(set(ld)) == 2 and np.all(ld >= 0), "eps=0.5 应得 2 簇且无噪声"
    assert cluster_acc(y_rings, ld) == 1.0
    assert (dbscan(X_rings, eps=0.05, min_samples=5) == -1).sum() > 250
    l3 = dbscan(np.array([[0.], [0.1], [10.]]), eps=0.5, min_samples=2)
    assert l3[0] == l3[1] >= 0 and l3[2] == -1

    # 第 9 题：eps 扫描的结构与两端行为
    epss = [0.05, 0.5, 1.6]
    rows = eps_scan(X_rings, epss)
    assert len(rows) == 3 and [r[0] for r in rows] == epss
    assert rows[0][2] > 250, "eps 太小应几乎全是噪声"
    assert rows[1][1] == 2 and rows[1][2] == 0
    assert rows[2][1] == 1, "eps 太大应全部并成一簇"

    # 第 10 题：与 sklearn 一致的 0.840501、单样本簇为 0、值域、完美两簇
    sil = silhouette(X_blobs, labels)
    assert np.isclose(sil, 0.840501, atol=1e-4)
    assert -1.0 <= sil <= 1.0
    assert silhouette(X_blobs[:3], np.arange(3)) == 0.0, "全是单样本簇应为 0"
    assert 0.0 < silhouette(X_blobs[y_blobs < 2], y_blobs[y_blobs < 2]) < 1.0

    # 第 12 题：轮廓峰值在真实簇数 K=3，且 inertia 随 k 单调降
    scan_rows, best_k = k_scan(X_blobs, [2, 3, 4], seed=42, n_init=5)
    assert len(scan_rows) == 3
    assert best_k == 3, "三团高斯簇上轮廓系数应在 K=3 达峰"
    js = [r[1] for r in scan_rows]
    assert all(js[i] > js[i + 1] for i in range(len(js) - 1)), "inertia 随 K 单调降"

    # 第 11 题：完全一致、标签重编号、瞎猜、边界
    assert cluster_acc(np.array([0, 0, 1, 1]), np.array([1, 1, 0, 0])) == 1.0
    assert cluster_acc(np.array([0, 0, 1, 1]), np.array([0, 0, 1, 1])) == 1.0
    assert cluster_acc(np.array([0, 0, 1, 1]), np.array([0, 1, 0, 1])) == 0.5
    assert cluster_acc(np.array([0]), np.array([0])) == 1.0
    assert cluster_acc(np.arange(6), np.arange(6)) == 0.0, "k>5 应返回 0.0 防止排列爆炸"

    print("ch11 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def pairwise_distances(X):
    X = np.asarray(X, dtype=float)
    diff = X[:, None, :] - X[None, :, :]
    D = np.sqrt((diff ** 2).sum(axis=2))
    np.fill_diagonal(D, 0.0)
    return D


def assign_clusters(X, C):
    X = np.asarray(X, dtype=float)
    C = np.asarray(C, dtype=float)
    d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    return d2.argmin(axis=1), float(d2.min(axis=1).sum())


def update_centers(X, labels, C):
    X = np.asarray(X, dtype=float)
    C = np.asarray(C, dtype=float)
    labels = np.asarray(labels)
    newC = C.copy()
    for j in range(len(C)):
        if np.any(labels == j):
            newC[j] = X[labels == j].mean(axis=0)
    return newC


def kmeans_fit(X, C0, iters=100, tol=1e-10):
    X = np.asarray(X, dtype=float)
    C = np.asarray(C0, dtype=float).copy()
    used = 0
    for t in range(1, iters + 1):
        labels, _ = assign_clusters(X, C)
        newC = update_centers(X, labels, C)
        used = t
        if np.linalg.norm(newC - C) < tol:
            C = newC
            break
        C = newC
    labels, _ = assign_clusters(X, C)
    return C, labels, used


def standardize(X):
    X = np.asarray(X, dtype=float)
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd = np.where(sd == 0, 1.0, sd)
    return (X - mu) / sd


def linkage_distance(D, idx_a, idx_b, method="single"):
    D = np.asarray(D, dtype=float)
    sub = D[np.ix_(np.asarray(idx_a), np.asarray(idx_b))]
    if method == "single":
        return float(sub.min())
    if method == "complete":
        return float(sub.max())
    if method == "average":
        return float(sub.mean())
    raise ValueError("unknown linkage: " + str(method))


def agglomerative(X, k, method="single"):
    X = np.asarray(X, dtype=float)
    D = pairwise_distances(X)
    clusters = [[i] for i in range(len(X))]
    while len(clusters) > k:
        best = (np.inf, -1, -1)
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                d = linkage_distance(D, clusters[a], clusters[b], method)
                if d < best[0]:
                    best = (d, a, b)
        _, a, b = best
        clusters[a] = clusters[a] + clusters[b]
        clusters.pop(b)
    out = np.empty(len(X), dtype=int)
    for j, cl in enumerate(clusters):
        out[cl] = j
    return out


def dbscan(X, eps, min_samples=5):
    X = np.asarray(X, dtype=float)
    D = pairwise_distances(X)
    n = len(X)
    nb = [np.flatnonzero(D[i] <= eps) for i in range(n)]
    labels = np.full(n, -2, dtype=int)
    cid = 0
    for i in range(n):
        if labels[i] != -2:
            continue
        if len(nb[i]) < min_samples:
            labels[i] = -1
            continue
        labels[i] = cid
        queue, q = list(nb[i]), 0
        while q < len(queue):
            j = queue[q]
            q += 1
            if labels[j] == -1:
                labels[j] = cid
            if labels[j] != -2:
                continue
            labels[j] = cid
            if len(nb[j]) >= min_samples:
                queue.extend(nb[j])
        cid += 1
    return labels


def eps_scan(X, eps_values, min_samples=5):
    out = []
    for eps in eps_values:
        lab = dbscan(X, eps, min_samples)
        out.append((eps, len(set(lab[lab >= 0])), int((lab == -1).sum())))
    return out


def silhouette(X, labels):
    X = np.asarray(X, dtype=float)
    labels = np.asarray(labels)
    D = pairwise_distances(X)
    vals = []
    for i in range(len(X)):
        same = (labels == labels[i])
        same[i] = False
        if not same.any():
            vals.append(0.0)
            continue
        a = D[i, same].mean()
        b = min(D[i, labels == c].mean()
                for c in np.unique(labels) if c != labels[i])
        vals.append((b - a) / max(a, b))
    return float(np.mean(vals))


def cluster_acc(y, labels):
    y = np.asarray(y)
    labels = np.asarray(labels)
    if len(labels) == 0:
        return 0.0
    k = int(labels.max()) + 1
    if k > 5:
        return 0.0
    return max(float(np.mean(np.array([p[l] for l in labels]) == y))
               for p in permutations(range(k)))


def k_scan(X, k_values, seed=42, n_init=5):
    X = np.asarray(X, dtype=float)
    rng = np.random.default_rng(seed)
    rows = []
    for k in k_values:
        best = None
        for _ in range(n_init):
            idx = rng.choice(len(X), k, replace=False)
            C, lab, _ = kmeans_fit(X, X[idx])
            J = assign_clusters(X, C)[1]
            if best is None or J < best[0]:
                best = (J, C, lab)
        rows.append((k, float(best[0]), silhouette(X, best[2])))
    return rows, max(rows, key=lambda r: r[2])[0]
"""
# endregion
