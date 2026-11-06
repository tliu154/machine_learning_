"""
ch08 练习：经典分类算法（Classical Classification Algorithms）
──────────────────────────────────────────────────
对应章节：docs/ch08_classical_classifiers.md
重点：KNN 距离与投票 / 缩放对距离的影响 / 基尼与熵 / 最佳切分 /
      手写递归决策树与 train-val 深度曲线 / RBF 核矩阵 / 高斯朴素贝叶斯
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy，不需要 scikit-learn。
"""

import numpy as np


# ---------- 1. 欧氏距离（锚点 c08-01） ----------
def euclidean_distances(X, x):
    """X 为 (n, d)、x 为 (d,)，返回 (n,) 个距离；用广播，不写 for"""
    # TODO
    return None


# ---------- 2. KNN 单样本投票（锚点 c08-01） ----------
def knn_predict(X_tr, y_tr, x, k=5):
    """返回最近 k 个邻居里票数最多的类（int）；平票时取编号最小的类"""
    # TODO
    return None


# ---------- 3. KNN 批量预测（锚点 c08-01） ----------
def knn_predict_batch(X_tr, y_tr, X_va, k=5):
    """对 X_va 每行调用 knn_predict，返回 (m,) 的 int 数组"""
    # TODO
    return None


# ---------- 4. 基尼不纯度（锚点 c08-02） ----------
def gini(y):
    """G = 1 - sum(p_c^2)，纯节点为 0；y 是非负整数标签"""
    # TODO
    return None


# ---------- 5. 熵（锚点 c08-02） ----------
def entropy(y):
    """H = -sum(p_c * log2(p_c))；p=0 的项要跳过，别让 log(0) 污染结果"""
    # TODO
    return None


# ---------- 6. 最佳切分（锚点 c08-02） ----------
def best_split(X, y):
    """遍历每个特征的每个取值作阈值，返回 (j, threshold, gini_gain) 最大的那组"""
    # TODO
    return None


# ---------- 7. 递归建树（锚点 c08-02） ----------
def build_tree(X, y, max_depth=3, depth=0):
    """
    返回嵌套 dict：
      叶节点   {"leaf": True,  "value": 多数类}
      内部节点 {"leaf": False, "j": j, "t": t, "left": 子树, "right": 子树}
    全纯 / 到达 max_depth / 样本不足 / 切不动 时返回叶节点。
    """
    # TODO
    return None


# ---------- 8. 树预测（锚点 c08-02） ----------
def tree_predict(tree, X):
    """对 (m, d) 每行沿树走到底，返回 (m,) 的预测标签"""
    # TODO
    return None


# ---------- 9. RBF 核矩阵（锚点 c08-03） ----------
def rbf_kernel(A, B, gamma=1.0):
    """A 为 (n, d)、B 为 (m, d)，返回 (n, m) 的 exp(-gamma * 平方距离)"""
    # TODO
    return None


# ---------- 10. 训练高斯朴素贝叶斯（锚点 c08-04） ----------
def fit_gaussian_nb(X, y, eps=1e-9):
    """返回 [(类标签, log 无关的先验 prior, 均值向量, 方差向量+eps), ...]"""
    # TODO
    return None


# ---------- 11. 高斯朴素贝叶斯预测（锚点 c08-04） ----------
def gaussian_nb_predict(model, X):
    """对每类累加 log(prior) + 各维 log 高斯密度，返回 (m,) 的类标签"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # 主数据：XOR，逻辑回归在这里只能到 0.675（见教学 8.5 实测表）
    X = rng.uniform(-1, 1, (160, 2))
    y = (X[:, 0] * X[:, 1] > 0).astype(int)
    X_tr, y_tr, X_va, y_va = X[:120], y[:120], X[120:], y[120:]

    # 1. 距离：广播 + 两个已知值
    assert np.allclose(euclidean_distances(np.array([[0., 0.], [3., 4.]]),
                                          np.array([0., 0.])), [0., 5.])
    assert euclidean_distances(X_tr, X_tr[0]).shape == (120,)
    assert np.isclose(euclidean_distances(X_tr, X_tr[7])[7], 0.0)

    # 2~3. KNN 在 XOR 上应该明显赢过线性模型
    assert knn_predict(X_tr, y_tr, X_va[0], 5) in (0, 1)
    pred_knn = knn_predict_batch(X_tr, y_tr, X_va, 5)
    assert pred_knn.shape == (40,)
    acc_knn = np.mean(pred_knn == y_va)
    assert acc_knn > 0.85, f"KNN 应该轻松解决 XOR: {acc_knn}"

    # 缩放：真正有判别力的特征量纲极小，噪声特征量纲极大
    Xr = rng.normal(0, 1, (120, 2))
    Xs = Xr * np.array([0.01, 100.0])
    ys = (Xr[:, 0] > 0).astype(int)
    acc_raw = np.mean(knn_predict_batch(Xs[:90], ys[:90], Xs[90:], 5) == ys[90:])
    mu, sd = Xs[:90].mean(axis=0), Xs[:90].std(axis=0)
    Xs_s = (Xs - mu) / sd
    acc_scaled = np.mean(knn_predict_batch(Xs_s[:90], ys[:90], Xs_s[90:], 5) == ys[90:])
    assert acc_raw < 0.8 and acc_scaled > 0.9, \
        f"KNN 必须标准化: raw={acc_raw}, scaled={acc_scaled}"

    # 4. 基尼不纯度
    assert np.isclose(gini(np.array([1, 1, 1])), 0.0)
    assert np.isclose(gini(np.array([0, 0, 1, 1])), 0.5)
    assert np.isclose(gini(np.array([0, 1, 2])), 2 / 3)

    # 5. 熵（含 p=0 的边界）
    assert np.isclose(entropy(np.array([1, 1])), 0.0)
    assert np.isclose(entropy(np.array([0, 0, 1, 1])), 1.0)
    assert np.isclose(entropy(np.array([0, 1, 2])), np.log2(3))

    # 6. 最佳切分：一维可分数据，最佳阈值应落在 1~2 之间、增益 0.5
    Xsp = np.array([[0.], [1.], [2.], [3.]])
    ysp = np.array([0, 0, 1, 1])
    j, t, gain = best_split(Xsp, ysp)
    assert j == 0 and 1.0 <= t <= 2.0 and np.isclose(gain, 0.5), (j, t, gain)

    # 7~8. 递归决策树：不同 max_depth 的 train/val 曲线（篇 README 点名要的对比）
    Xt = rng.uniform(-1, 1, (200, 2))
    yt = ((Xt[:, 0] > 0.2) & (Xt[:, 1] > -0.3)).astype(int)
    flip = rng.choice(200, 10, replace=False)
    yt[flip] = 1 - yt[flip]                 # 5% 标签噪声
    Xt_tr, yt_tr, Xt_va, yt_va = Xt[:150], yt[:150], Xt[150:], yt[150:]
    train_accs, val_accs = [], []
    for depth in (1, 2, 4, 8):
        tree = build_tree(Xt_tr, yt_tr, max_depth=depth)
        train_accs.append(np.mean(tree_predict(tree, Xt_tr) == yt_tr))
        val_accs.append(np.mean(tree_predict(tree, Xt_va) == yt_va))
    assert train_accs[-1] > train_accs[0] + 0.1, "深树应该更能拟合训练集"
    assert train_accs[-1] > 0.95, f"深树应接近背下训练集: {train_accs}"
    assert val_accs[-1] < train_accs[-1] + 1e-9, "val 不该超过 train（过拟合的表现）"
    pure = build_tree(np.array([[0.], [1.]]), np.array([1, 1]), max_depth=3)
    assert pure["leaf"] is True and pure["value"] == 1, "全纯应直接成叶"
    assert tree_predict(pure, np.array([[0.5]])).tolist() == [1]

    # 9. RBF 核矩阵：对称、对角为 1、值域 (0, 1]
    K = rbf_kernel(X_tr[:10], X_tr[:10], gamma=2.0)
    assert K.shape == (10, 10)
    assert np.allclose(K, K.T) and np.allclose(np.diag(K), 1.0)
    assert np.all((K > 0) & (K <= 1))
    assert np.all(K[~np.eye(10, dtype=bool)] < 1)
    assert rbf_kernel(X_tr[:5], X_va[:3], 1.0).shape == (5, 3)

    # 10~11. 高斯朴素贝叶斯：假设成立时满分，XOR 上崩掉
    Xn = np.vstack([rng.normal((-1, -1), 0.4, (60, 2)),
                    rng.normal((1, 1), 0.4, (60, 2))])
    yn = np.r_[np.zeros(60, int), np.ones(60, int)]
    model_nb = fit_gaussian_nb(Xn[:90], yn[:90])
    assert len(model_nb) == 2 and len(model_nb[0]) == 4
    assert np.isclose(sum(m[1] for m in model_nb), 1.0), "先验之和应为 1"
    acc_nb = np.mean(gaussian_nb_predict(model_nb, Xn[90:]) == yn[90:])
    acc_xor = np.mean(gaussian_nb_predict(fit_gaussian_nb(X_tr, y_tr), X_va) == y_va)
    assert acc_nb > 0.9, f"高斯簇上应该几乎全对: {acc_nb}"
    assert acc_xor < 0.75, f"XOR 上独立性假设崩掉，应接近瞎猜: {acc_xor}"

    print("ch08 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def euclidean_distances(X, x):
    X = np.asarray(X, dtype=float)
    x = np.asarray(x, dtype=float)
    return np.sqrt(((X - x) ** 2).sum(axis=1))

def knn_predict(X_tr, y_tr, x, k=5):
    X_tr = np.asarray(X_tr, dtype=float)
    y_tr = np.asarray(y_tr, dtype=int)
    x = np.asarray(x, dtype=float)
    dist = np.sqrt(((X_tr - x) ** 2).sum(axis=1))
    idx = np.argsort(dist)[:k]
    return int(np.bincount(y_tr[idx]).argmax())

def knn_predict_batch(X_tr, y_tr, X_va, k=5):
    X_va = np.asarray(X_va, dtype=float)
    return np.array([knn_predict(X_tr, y_tr, x, k) for x in X_va], dtype=int)

def gini(y):
    y = np.asarray(y, dtype=int)
    p = np.bincount(y) / len(y)
    return float(1 - np.sum(p ** 2))

def entropy(y):
    y = np.asarray(y, dtype=int)
    p = np.bincount(y) / len(y)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))

def best_split(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    base = gini(y)
    best_j, best_t, best_gain = 0, float(X[:, 0].min()), -np.inf
    for j in range(X.shape[1]):
        for t in np.unique(X[:, j]):
            m = X[:, j] <= t
            if m.all() or not m.any():
                continue
            gain = base - (m.sum() * gini(y[m]) + (~m).sum() * gini(y[~m])) / len(y)
            if gain > best_gain:
                best_j, best_t, best_gain = int(j), float(t), float(gain)
    return best_j, best_t, best_gain

def build_tree(X, y, max_depth=3, depth=0):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    leaf = {"leaf": True, "value": int(np.bincount(y).argmax())}
    if len(np.unique(y)) == 1 or depth >= max_depth or len(y) < 2:
        return leaf
    j, t, gain = best_split(X, y)
    m = X[:, j] <= t
    if gain == -np.inf or m.all() or not m.any():
        return leaf
    return {"leaf": False, "j": j, "t": t,
            "left": build_tree(X[m], y[m], max_depth, depth + 1),
            "right": build_tree(X[~m], y[~m], max_depth, depth + 1)}

def _predict_one(node, row):
    while not node["leaf"]:
        node = node["left"] if row[node["j"]] <= node["t"] else node["right"]
    return node["value"]

def tree_predict(tree, X):
    X = np.asarray(X, dtype=float)
    return np.array([_predict_one(tree, row) for row in X], dtype=int)

def rbf_kernel(A, B, gamma=1.0):
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    d2 = ((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=2)
    return np.exp(-gamma * d2)

def fit_gaussian_nb(X, y, eps=1e-9):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    return [(int(c), float(np.mean(y == c)), X[y == c].mean(axis=0),
             X[y == c].var(axis=0) + eps) for c in np.unique(y)]

def gaussian_nb_predict(model, X):
    X = np.asarray(X, dtype=float)
    scores = np.column_stack([
        np.log(prior) + (-0.5 * np.log(2 * np.pi * var)
                         - (X - mu) ** 2 / (2 * var)).sum(axis=1)
        for _, prior, mu, var in model
    ])
    return np.array([model[k][0] for k in scores.argmax(axis=1)], dtype=int)
"""
# endregion
