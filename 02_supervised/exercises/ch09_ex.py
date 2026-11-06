"""
ch09 练习：集成方法（Ensemble Methods）
──────────────────────────────────────────────────
对应章节：docs/ch09_ensemble.md
重点：Bootstrap / OOB / 多数决与分歧度 / 手写 Bagging 森林 /
      回归树桩与梯度提升（拟合残差）/ 学习率收缩
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy，不需要 scikit-learn。
下方「已提供的基学习器」是一份精简 CART（思路见 ch08 第 7 题），
为了让本文件能独立运行直接放在这里，**不用你写**；阈值只取分位数候选以控制耗时。
本文件是【ML 第 9 章】的练习，与
00_foundations/python_basics/exercises/ch09_ex.py（文件与异常）不是同一份。
"""

import numpy as np


# ============ 已提供：精简 CART 基学习器（无需修改） ============
def _gini(y):
    y = np.asarray(y, dtype=int)
    p = np.bincount(y) / len(y)
    return float(1 - np.sum(p ** 2))


def _best_split(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    base = _gini(y)
    best_j, best_t, best_gain = 0, float(X[:, 0].min()), -np.inf
    for j in range(X.shape[1]):
        # 只试 8 个分位数阈值：比遍历 np.unique 快一个量级，结论不变
        for t in np.quantile(X[:, j], np.linspace(0.1, 0.9, 8)):
            m = X[:, j] <= t
            if m.all() or not m.any():
                continue
            gain = base - (m.sum() * _gini(y[m]) + (~m).sum() * _gini(y[~m])) / len(y)
            if gain > best_gain:
                best_j, best_t, best_gain = int(j), float(t), float(gain)
    return best_j, best_t, best_gain


def _build_tree(X, y, max_depth=5, depth=0):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    leaf = {"leaf": True, "value": int(np.bincount(y).argmax())}
    if len(np.unique(y)) == 1 or depth >= max_depth or len(y) < 2:
        return leaf
    j, t, gain = _best_split(X, y)
    m = X[:, j] <= t
    if gain == -np.inf or m.all() or not m.any():
        return leaf
    return {"leaf": False, "j": j, "t": t,
            "left": _build_tree(X[m], y[m], max_depth, depth + 1),
            "right": _build_tree(X[~m], y[~m], max_depth, depth + 1)}


def _tree_predict_one(node, row):
    while not node["leaf"]:
        node = node["left"] if row[node["j"]] <= node["t"] else node["right"]
    return node["value"]


def _tree_predict(tree, X):
    return np.array([_tree_predict_one(tree, row)
                     for row in np.asarray(X, dtype=float)], dtype=int)


# ---------- 1. 自助采样（锚点 c09-01） ----------
def bootstrap_indices(n, seed):
    """有放回抽 n 个下标，返回 (n,) 的 int 数组；同一 seed 结果可复现"""
    # TODO
    return None


# ---------- 2. 袋外掩码（锚点 c09-01） ----------
def oob_mask(n, idx):
    """返回 (n,) 布尔数组：True 表示该下标没出现在 idx 里"""
    # TODO
    return None


# ---------- 3. 多数决（锚点 c09-01） ----------
def majority_vote(preds):
    """preds 为 (B, m) 的 0/1 预测，返回 (m,)；平票取 0"""
    # TODO
    return None


# ---------- 4. 分歧度（锚点 c09-03） ----------
def disagreement_rate(preds):
    """(B, m) 二分类预测的分歧度 = 1 - 各列众数占比的平均；完全一致为 0"""
    # TODO
    return None


# ---------- 5. 训练 Bagging 森林（锚点 c09-01） ----------
def fit_bagging(X, y, B=12, max_depth=5, seed=42):
    """返回 [(tree, bootstrap_idx), ...]；第 b 棵树用 seed+b 抽样，调 _build_tree"""
    # TODO
    return None


# ---------- 6. Bagging 预测（锚点 c09-01） ----------
def bagging_predict(forest, X):
    """收集各树对 X 的预测组成 (B, m)，再 majority_vote"""
    # TODO
    return None


# ---------- 7. 袋外评分（锚点 c09-01） ----------
def oob_score(forest, X, y):
    """每个样本只用「没抽到它」的树投票，返回 float 准确率；无可用树的样本跳过"""
    # TODO
    return None


# ---------- 8. 回归树桩（锚点 c09-02） ----------
def regression_stump(x, r):
    """一维 x、一维残差 r；找 SSE 最小的阈值，返回 (t, 左侧 r 均值, 右侧 r 均值)"""
    # TODO
    return None


# ---------- 9. 树桩预测（锚点 c09-02） ----------
def stump_predict(stump, x):
    """按 x <= t 返回左/右均值，形状与 x 相同"""
    # TODO
    return None


# ---------- 10. 梯度提升拟合（锚点 c09-02） ----------
def gradient_boost_fit(x, y, n_estimators=30, lr=0.1):
    """
    一维回归：F 初始化为 y.mean()，每轮用 regression_stump 拟合当前残差，
    再 F += lr * stump_predict(...)。返回 (F0, stumps, lr)。
    """
    # TODO
    return None


# ---------- 11. 梯度提升预测（锚点 c09-02） ----------
def gradient_boost_predict(model, x):
    """从 F0 出发累加各树桩的 lr 倍修正，返回 (n,) 预测值"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    # 和教学文档同一份数据：10 维、只有前 2 维有信号、只用 80 个训练点
    X = rng.normal(0, 1, (400, 10))
    y = (X[:, 0] + 0.7 * X[:, 1] > 0).astype(int)
    X_tr, y_tr, X_va, y_va = X[:80], y[:80], X[80:], y[80:]

    # 1. bootstrap：有放回、可复现、长度不变
    idx = bootstrap_indices(80, seed=0)
    assert idx.shape == (80,) and idx.min() >= 0 and idx.max() < 80
    assert len(np.unique(idx)) < 80, "有放回抽样必然有重复"
    assert np.array_equal(idx, bootstrap_indices(80, seed=0)), "同 seed 必须可复现"
    assert not np.array_equal(idx, bootstrap_indices(80, seed=1))

    # 2. OOB：约 36.8% 样本没被抽到，且与 idx 不交
    m = oob_mask(80, idx)
    assert m.shape == (80,) and m.dtype == bool
    assert 0.2 < m.mean() < 0.55, f"袋外比例应接近 e^-1: {m.mean()}"
    assert not set(np.flatnonzero(m)) & set(idx.tolist())
    assert oob_mask(5, np.array([0, 0, 2, 2])).tolist() == [False, True, False, True, True]

    # 3. 多数决：平票取 0
    assert majority_vote(np.array([[1, 0, 1], [1, 1, 1], [1, 0, 0]])).tolist() == [1, 0, 1]
    assert majority_vote(np.array([[0, 1], [1, 0]])).tolist() == [0, 0], "平票取编号小的类"

    # 4. 分歧度：方差的代理指标
    assert np.isclose(disagreement_rate(np.ones((10, 5), dtype=int)), 0.0)
    assert np.isclose(disagreement_rate(np.array([[0] * 5, [1] * 5])), 0.5)
    assert 0 < disagreement_rate(np.array([[0, 1, 1], [1, 1, 0], [0, 1, 1]])) < 0.5

    # 5~7. 手写 Bagging：成员分歧、集成不比平均差、OOB 能算
    forest = fit_bagging(X_tr, y_tr, B=12, max_depth=5, seed=42)
    assert len(forest) == 12 and isinstance(forest[0], tuple)
    member_preds = np.array([_tree_predict(tree, X_va) for tree, _ in forest])
    member_accs = (member_preds == y_va).mean(axis=1)
    ens_pred = bagging_predict(forest, X_va)
    ens_acc = float(np.mean(ens_pred == y_va))
    assert ens_pred.shape == (len(X_va),) and set(np.unique(ens_pred)) <= {0, 1}
    assert disagreement_rate(member_preds) > 0.01, "成员树之间应该有分歧"
    assert member_accs.max() - member_accs.min() > 0, "换一批数据，单棵树表现应该会抖"
    assert ens_acc >= member_accs.mean() - 0.02, "集成不该明显差于成员平均"
    assert ens_acc > 0.70, f"集成至少得学到信号: {ens_acc}"
    oob = oob_score(forest, X_tr, y_tr)
    assert isinstance(oob, float) and 0.0 <= oob <= 1.0

    # 8~9. 回归树桩
    xs = np.array([0., 1., 2., 3.])
    rs = np.array([1., 1., -1., -1.])
    t, lv, rv = regression_stump(xs, rs)
    assert 1.0 <= t < 2.0 and np.isclose(lv, 1.0) and np.isclose(rv, -1.0), (t, lv, rv)
    assert np.allclose(stump_predict((t, lv, rv), xs), rs)

    # 10~11. 梯度提升：轮数越多残差越小；lr 过大会打回基线
    reg_rng = np.random.default_rng(42)
    x_reg = reg_rng.uniform(-3, 3, 100)
    y_reg = np.sin(x_reg) + reg_rng.normal(0, 0.15, 100)
    baseline = float(np.mean((y_reg - y_reg.mean()) ** 2))
    m1 = gradient_boost_fit(x_reg, y_reg, n_estimators=1, lr=0.1)
    m30 = gradient_boost_fit(x_reg, y_reg, n_estimators=30, lr=0.1)
    m_big = gradient_boost_fit(x_reg, y_reg, n_estimators=30, lr=2.0)
    mse1 = float(np.mean((y_reg - gradient_boost_predict(m1, x_reg)) ** 2))
    mse30 = float(np.mean((y_reg - gradient_boost_predict(m30, x_reg)) ** 2))
    mse_big = float(np.mean((y_reg - gradient_boost_predict(m_big, x_reg)) ** 2))
    assert gradient_boost_predict(m30, x_reg).shape == (100,)
    assert mse1 < baseline and mse30 < mse1, "每轮拟合残差应让 MSE 下降"
    assert mse_big > mse30, "lr 太大会震荡，反而比正常学习率差"
    assert m30[0] == float(y_reg.mean()) and len(m30[1]) == 30 and m30[2] == 0.1

    print("ch09 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def bootstrap_indices(n, seed):
    return np.random.default_rng(seed).integers(0, n, n)

def oob_mask(n, idx):
    mask = np.ones(n, dtype=bool)
    mask[np.asarray(idx, dtype=int)] = False
    return mask

def majority_vote(preds):
    return (np.asarray(preds, dtype=float).mean(axis=0) > 0.5).astype(int)

def disagreement_rate(preds):
    P = np.asarray(preds, dtype=int)
    B = P.shape[0]
    mode_count = np.maximum((P == 0).sum(axis=0), (P == 1).sum(axis=0))
    return float(1 - mode_count.mean() / B)

def fit_bagging(X, y, B=12, max_depth=5, seed=42):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    forest = []
    for b in range(B):
        idx = bootstrap_indices(len(X), seed + b)
        forest.append((_build_tree(X[idx], y[idx], max_depth), idx))
    return forest

def bagging_predict(forest, X):
    preds = np.array([_tree_predict(tree, X) for tree, _ in forest])
    return majority_vote(preds)

def oob_score(forest, X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=int)
    preds = np.array([_tree_predict(tree, X) for tree, _ in forest])
    hits = []
    for i in range(len(X)):
        votes = [preds[b, i] for b, (_, idx) in enumerate(forest) if i not in idx]
        if votes:
            hits.append(float(np.mean(votes) > 0.5) == y[i])
    return float(np.mean(hits)) if hits else 0.0

def regression_stump(x, r):
    x = np.asarray(x, dtype=float)
    r = np.asarray(r, dtype=float)
    best, best_sse = None, np.inf
    for t in np.unique(x):
        m = x <= t
        if m.all() or not m.any():
            continue
        lv, rv = float(r[m].mean()), float(r[~m].mean())
        sse = float(np.sum((r - np.where(m, lv, rv)) ** 2))
        if sse < best_sse:
            best, best_sse = (float(t), lv, rv), sse
    return best

def stump_predict(stump, x):
    t, lv, rv = stump
    return np.where(np.asarray(x, dtype=float) <= t, lv, rv)

def gradient_boost_fit(x, y, n_estimators=30, lr=0.1):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    F0 = float(y.mean())
    F = np.full(len(y), F0)
    stumps = []
    for _ in range(n_estimators):
        stump = regression_stump(x, y - F)
        F = F + lr * stump_predict(stump, x)
        stumps.append(stump)
    return (F0, stumps, lr)

def gradient_boost_predict(model, x):
    F0, stumps, lr = model
    x = np.asarray(x, dtype=float)
    pred = np.full(len(x), F0)
    for stump in stumps:
        pred = pred + lr * stump_predict(stump, x)
    return pred
"""
# endregion
