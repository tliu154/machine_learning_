"""
ch10 练习：特征工程（Feature Engineering）
──────────────────────────────────────────────────
对应章节：docs/ch10_feature_engineering.md
重点：fit / apply 分离（防数据泄漏）/ 标准化与缺失填充 / IQR 裁剪 /
      one-hot 与目标编码 / 相关系数与交互项 / 亲手量化特征选择泄漏
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy，不需要 scikit-learn。
下方「已提供的评估器」是一个极简 lstsq 分类器，供第 11 题量化泄漏用，**不用你写**。
本文件是【ML 第 10 章】的练习，与
00_foundations/python_basics/exercises/ch10_ex.py（类）不是同一份。
"""

import numpy as np


# ============ 已提供：极简评估器（无需修改） ============
def _fit_lstsq(A, t):
    M = np.column_stack([np.asarray(A, float), np.ones(len(A))])
    return np.linalg.lstsq(M, np.asarray(t, float), rcond=None)[0]


def _predict(M, theta):
    return np.column_stack([np.asarray(M, float), np.ones(len(M))]) @ theta


def _val_acc(A_tr, t_tr, A_va, t_va, cols):
    theta = _fit_lstsq(A_tr[:, cols], t_tr)
    pred = (_predict(A_va[:, cols], theta) > 0.5).astype(int)
    return float(np.mean(pred == t_va))


# ---------- 1. fit 标准化器（锚点 c10-01） ----------
def fit_standardizer(X):
    """返回 (mu, sigma)，按列；标准差为 0 的列按 1.0 处理"""
    # TODO
    return None


# ---------- 2. apply 标准化器（锚点 c10-01） ----------
def apply_standardizer(X, stats):
    """用已有的 (mu, sigma) 变换 X；不重新 fit，不改原数组"""
    # TODO
    return None


# ---------- 3. fit 填充值（锚点 c10-02） ----------
def fit_imputer(X):
    """按列算非 nan 均值，返回 (d,) 数组；整列都是 nan 时填 0.0"""
    # TODO
    return None


# ---------- 4. apply 填充（锚点 c10-02） ----------
def apply_imputer(X, means):
    """把 X 里的 nan 换成对应列的均值；不改原数组"""
    # TODO
    return None


# ---------- 5. 缺失指示列（锚点 c10-02） ----------
def missing_indicator(X):
    """返回与 X 同形的 0/1 float 数组：原来是 nan 的位置为 1"""
    # TODO
    return None


# ---------- 6. IQR 裁剪（锚点 c10-02） ----------
def clip_iqr(fit_X, apply_X, k=1.5):
    """只用 fit_X 算 Q1/Q3 与上下界，再把 apply_X 夹到边界内并返回"""
    # TODO
    return None


# ---------- 7. 独热编码（锚点 c10-03） ----------
def one_hot(cats):
    """cats 为一维类别数组（数值或字符串）；返回 (n, K) 的 0/1 矩阵"""
    # TODO
    return None


# ---------- 8. 目标编码（锚点 c10-03） ----------
def target_encode(cat_fit, y_fit, cat_apply, default=None):
    """
    只用 (cat_fit, y_fit) 算每个类别的平均标签，编码 cat_apply。
    未见类别填 default；default=None 时用 y_fit 的全局均值。
    """
    # TODO
    return None


# ---------- 9. 相关系数打分（锚点 c10-04） ----------
def corr_scores(X, y):
    """返回 (d,) 的 |corr(x_j, y)|；常数列或 y 为常数时返回 0"""
    # TODO
    return None


# ---------- 10. 交互项（锚点 c10-04） ----------
def add_interactions(X):
    """返回所有 i<j 的 x_i * x_j，形状 (n, d*(d-1)//2)；d<2 时返回 (n, 0)"""
    # TODO
    return None


# ---------- 11. 量化特征选择泄漏（锚点 c10-04） ----------
def leakage_gap(X_all, y_all, n_train, k=20):
    """
    返回 (wrong_acc, right_acc)：
      wrong = 在【全量】上按相关度挑 top-k 列（偷看了验证集标签）
      right = 只在【训练集】上挑 top-k 列
    两者都用训练集拟合 _fit_lstsq，在同一份验证集上算准确率。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    # 和教学文档同一份数据：120 样本 / 200 列纯噪声 / 标签随机
    X_all = rng.normal(0, 1, (120, 200))
    y_all = rng.integers(0, 2, 120)
    X_tr, y_tr, X_va, y_va = X_all[:60], y_all[:60], X_all[60:], y_all[60:]

    # 1~2. fit / apply 分离
    Xs = np.array([[1., 2., 5.], [3., 4., 5.], [5., 6., 5.]])
    mu, sigma = fit_standardizer(Xs)
    assert np.allclose(mu, [3., 4., 5.])
    assert np.isclose(sigma[2], 1.0), "标准差为 0 的列要兜底成 1"
    Z_tr = apply_standardizer(Xs, (mu, sigma))
    assert np.allclose(Z_tr.mean(axis=0), 0, atol=1e-12)
    assert np.allclose(Z_tr[:, 0].std(), 1, atol=1e-12)
    snapshot = Xs.copy()
    apply_standardizer(Xs, (mu, sigma))
    assert np.array_equal(Xs, snapshot), "不应该修改输入"
    # 验证集必须用训练集统计量，不能自己 fit 一套
    stats_tr = fit_standardizer(X_tr)
    assert np.allclose(apply_standardizer(X_tr, stats_tr).mean(0), 0, atol=1e-12)
    assert not np.allclose(apply_standardizer(X_va, stats_tr),
                           apply_standardizer(X_va, fit_standardizer(X_va))), \
        "给验证集单独 fit 一套统计量，结果会不一样"

    # 3~5. 缺失值：均值、填充、指示列、整列缺失
    Xm = np.array([[1., 2., np.nan], [3., np.nan, np.nan], [5., 6., np.nan]])
    means = fit_imputer(Xm)
    assert np.allclose(means, [3., 4., 0.]), means
    filled = apply_imputer(Xm, means)
    assert np.allclose(filled, [[1., 2., 0.], [3., 4., 0.], [5., 6., 0.]])
    assert np.isnan(Xm).any(), "不应该修改输入"
    assert np.array_equal(missing_indicator(Xm),
                          [[0, 0, 1], [0, 1, 1], [0, 0, 1]])

    # 6. IQR 裁剪：边界只来自 fit_X
    Xf = np.array([[1.], [2.], [3.], [4.], [100.]])
    clipped = clip_iqr(Xf[:4], Xf)
    q1, q3 = np.quantile(Xf[:4], [0.25, 0.75], axis=0)
    upper = q3 + 1.5 * (q3 - q1)
    assert np.isclose(clipped[4, 0], upper[0]), "离群点应被夹到 fit_X 算出的上界"
    assert clipped[0, 0] == 1. and clipped[3, 0] == 4.

    # 7. one-hot
    oh = one_hot(np.array(["b", "a", "b", "c"]))
    assert oh.shape == (4, 3) and np.allclose(oh.sum(axis=1), 1)
    assert oh[0].tolist() == oh[2].tolist() and not np.array_equal(oh[0], oh[1])

    # 8. 目标编码：只用训练集、未见类别填先验、绝不偷看 y_va
    cat_fit = np.array([0, 0, 1, 1])
    yf = np.array([0., 1., 1., 1.])
    enc = target_encode(cat_fit, yf, np.array([0, 1, 2]))
    assert np.allclose(enc[:2], [0.5, 1.0])
    assert np.isclose(enc[2], yf.mean()), "未见类别应填全局先验"
    enc2 = target_encode(cat_fit, yf, np.array([0, 2]), default=-1.0)
    assert enc2[1] == -1.0

    # 9. 相关系数：常数列为 0，完全相关为 1
    Xc = np.column_stack([np.arange(10.), np.ones(10), -np.arange(10.)])
    sc = corr_scores(Xc, np.arange(10.))
    assert np.isclose(sc[0], 1.0) and np.isclose(sc[1], 0.0) and np.isclose(sc[2], 1.0), sc

    # 10. 交互项
    Xi = np.array([[1., 2., 3.], [2., 4., 6.]])
    inter = add_interactions(Xi)
    assert inter.shape == (2, 3)
    assert np.allclose(inter[0], [2., 3., 6.])
    assert add_interactions(np.array([[1.], [2.]])).shape == (2, 0)

    # 11. 泄漏量化：数据全是噪声，错误做法却能「考」出高分
    wrong, right = leakage_gap(X_all, y_all, n_train=60, k=20)
    assert isinstance(wrong, float) and isinstance(right, float)
    assert wrong - right > 0.15, \
        f"在全量上挑特征应明显虚高: wrong={wrong}, right={right}"
    assert right < 0.60, "正确做法在纯噪声上应该接近瞎猜"

    print("ch10 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def fit_standardizer(X):
    X = np.asarray(X, dtype=float)
    sigma = X.std(axis=0)
    return (X.mean(axis=0), np.where(sigma == 0, 1.0, sigma))

def apply_standardizer(X, stats):
    mu, sigma = stats
    return (np.asarray(X, dtype=float) - mu) / sigma

def fit_imputer(X):
    X = np.asarray(X, dtype=float)
    cnt = np.sum(~np.isnan(X), axis=0)
    total = np.nansum(X, axis=0)
    return np.where(cnt > 0, total / np.maximum(cnt, 1), 0.0)

def apply_imputer(X, means):
    X = np.asarray(X, dtype=float).copy()
    nan = np.isnan(X)
    X[nan] = np.take(means, np.where(nan)[1])
    return X

def missing_indicator(X):
    return np.isnan(np.asarray(X, dtype=float)).astype(float)

def clip_iqr(fit_X, apply_X, k=1.5):
    q1, q3 = np.quantile(np.asarray(fit_X, dtype=float), [0.25, 0.75], axis=0)
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    return np.clip(np.asarray(apply_X, dtype=float), lo, hi)

def one_hot(cats):
    cats = np.asarray(cats)
    classes, codes = np.unique(cats, return_inverse=True)
    return np.eye(len(classes))[codes]

def target_encode(cat_fit, y_fit, cat_apply, default=None):
    cat_fit = np.asarray(cat_fit)
    y_fit = np.asarray(y_fit, dtype=float)
    cat_apply = np.asarray(cat_apply)
    if default is None:
        default = float(y_fit.mean())
    out = np.full(len(cat_apply), default, dtype=float)
    for g in np.unique(cat_fit):
        m = cat_fit == g
        out[cat_apply == g] = y_fit[m].mean()
    return out

def corr_scores(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    Xc, yc = X - X.mean(axis=0), y - y.mean()
    denom = np.sqrt((Xc ** 2).sum(axis=0)) * np.sqrt((yc ** 2).sum()) + 1e-12
    return np.abs((Xc * yc[:, None]).sum(axis=0) / denom)

def add_interactions(X):
    X = np.asarray(X, dtype=float)
    d = X.shape[1]
    cols = [X[:, i] * X[:, j] for i in range(d) for j in range(i + 1, d)]
    return np.column_stack(cols) if cols else np.empty((len(X), 0))

def leakage_gap(X_all, y_all, n_train, k=20):
    X_tr, y_tr = X_all[:n_train], y_all[:n_train]
    X_va, y_va = X_all[n_train:], y_all[n_train:]
    wrong_cols = np.argsort(corr_scores(X_all, y_all))[-k:]
    right_cols = np.argsort(corr_scores(X_tr, y_tr))[-k:]
    return (_val_acc(X_tr, y_tr, X_va, y_va, wrong_cols),
            _val_acc(X_tr, y_tr, X_va, y_va, right_cols))
"""
# endregion
