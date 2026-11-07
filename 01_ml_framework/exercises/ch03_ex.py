"""
ch03 练习：机器学习是什么（What is Machine Learning）
──────────────────────────────────────────────────
对应章节：docs/ch03_what_is_ml.md
重点：规则从数据里学出来（而非手写）/ 漂移后重学 / 自监督伪标签 /
      无监督分组 / 任务类型判定 / 半监督自训练为什么不涨
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy。
本文件是【ML 第 3 章】的练习，与
00_foundations/python_basics/exercises/ch03_ex.py（字符串）不是同一份。
"""

import numpy as np


# ---------- 1. 从数据学阈值（锚点 c03-01） ----------
def learn_threshold(x, y):
    """
    候选阈值 = 相邻不同 x 的中点；返回训练集 0-1 损失最小的那个。
    平局取【较小】阈值；所有 x 相同时（无候选）返回该唯一取值。
    """
    # TODO
    return None


# ---------- 2. 应用规则（锚点 c03-01） ----------
def predict_threshold(x, t):
    """返回 (x > t).astype(int)；x 等于 t 时预测 0"""
    # TODO
    return None


# ---------- 3. 漂移后重学（锚点 c03-04） ----------
def relearn_after_drift(x_new, y_new, x_te, y_te, old_t):
    """用新数据重学阈值，返回 (沿用旧规则的 test acc, 重学后的 test acc)"""
    # TODO
    return None


# ---------- 4. 自监督：造伪标签再拟合（锚点 c03-02） ----------
def self_supervised_fit(series, lag=1):
    """把序列错开 lag 位，用 lstsq 拟合 s[t+lag] = a*s[t] + b，返回 [a, b]"""
    # TODO
    return None


# ---------- 5. 无监督 2-means（锚点 c03-02） ----------
def two_means(X, iters=20, seed=0):
    """只用 X 不用标签，返回 (centers(2,d), labels(n,))；空簇时保持旧中心"""
    # TODO
    return None


# ---------- 6. 事后评估聚类（锚点 c03-02） ----------
def cluster_accuracy(y, labels):
    """两种簇→标签映射里取较高准确率；标签只在评估时用"""
    # TODO
    return None


# ---------- 7. 任务类型判定（锚点 c03-03） ----------
def task_type(y):
    """唯一值很少或全是整数 → 'classification'，否则 'regression'；空输入按分类"""
    # TODO
    return None


# ---------- 8. 半监督自训练（锚点 c03-02） ----------
def self_training_threshold(x, y, labeled_idx):
    """只用 labeled_idx 的真标签学阈值，再给全量打伪标签重学；返回 (t_before, t_after)"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # 1~2. 「学习」= 从样本里解出规则参数
    x = rng.uniform(0, 1, 200)
    y = (x > 0.62).astype(int)
    t = learn_threshold(x, y)
    assert abs(t - 0.62) < 0.03, t
    assert np.array_equal(predict_threshold(x, t), y), "无噪声数据应能完美分开"
    assert predict_threshold(np.array([t]), t)[0] == 0, "x == t 时预测 0（严格大于）"
    assert learn_threshold(np.ones(5), np.array([0, 1, 0, 1, 0])) == 1.0, "无候选的边界"
    x_snap = x.copy()
    learn_threshold(x, y)
    assert np.array_equal(x, x_snap), "不该修改输入"

    # 3. 真实边界漂移后，重学能救回来
    x_new = rng.uniform(0, 1, 200)
    y_new = (x_new > 0.80).astype(int)
    x_te = rng.uniform(0, 1, 1000)
    y_te = (x_te > 0.80).astype(int)
    old_acc, new_acc = relearn_after_drift(x_new, y_new, x_te, y_te, t)
    assert new_acc > old_acc + 0.1, (old_acc, new_acc)
    assert 0.0 <= old_acc <= 1.0 and 0.0 <= new_acc <= 1.0

    # 4. 自监督：没有人工标签，也能学回生成系数
    T = 500
    s = np.zeros(T)
    for i in range(1, T):
        s[i] = 0.6 * s[i - 1] + rng.normal(0, 0.2)
    theta = self_supervised_fit(s)
    assert abs(theta[0] - 0.6) < 0.05, theta
    assert abs(theta[1]) < 0.1
    assert np.allclose(self_supervised_fit(np.arange(5.0)), [1.0, 1.0]), "完美线性序列"

    # 5~6. 无监督：训练没看标签，评估才用
    X2 = np.vstack([rng.normal(np.array([-1., -1.]), 0.4, (100, 2)),
                    rng.normal(np.array([1., 1.]), 0.4, (100, 2))])
    y2 = np.r_[np.zeros(100, int), np.ones(100, int)]
    centers, lab = two_means(X2)
    assert centers.shape == (2, 2) and lab.shape == (200,)
    assert set(np.unique(lab)).issubset({0, 1})
    assert cluster_accuracy(y2, lab) > 0.95
    assert np.isclose(cluster_accuracy(y2, 1 - lab),
                      cluster_accuracy(y2, lab)), "映射方向应自动选优"

    # 7. 任务类型看 y，不看模型名字
    assert task_type(np.array([0, 1, 0, 1, 1])) == "classification"
    assert task_type(rng.normal(0, 1, 100)) == "regression"
    assert task_type(np.array([0.0, 0.0, 0.0])) == "classification"
    assert task_type(np.array([])) == "classification"

    # 8. 伪标签自训练：没有新信息，阈值几乎不动
    idx = rng.choice(200, 10, replace=False)
    t0, t1 = self_training_threshold(x, y, idx)
    assert abs(t1 - t0) < 0.05, (t0, t1)
    assert isinstance(t0, float) and isinstance(t1, float)

    print("ch03 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def learn_threshold(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y).astype(int)
    xs = np.sort(np.unique(x))
    if len(xs) < 2:
        return float(xs[0])
    cand = (xs[:-1] + xs[1:]) / 2
    pred = x[:, None] > cand[None, :]
    err = (pred != y[:, None]).mean(axis=0)
    return float(cand[int(np.argmin(err))])

def predict_threshold(x, t):
    return (np.asarray(x) > t).astype(int)

def relearn_after_drift(x_new, y_new, x_te, y_te, old_t):
    new_t = learn_threshold(x_new, y_new)
    old_acc = float(np.mean(predict_threshold(x_te, old_t) == np.asarray(y_te)))
    new_acc = float(np.mean(predict_threshold(x_te, new_t) == np.asarray(y_te)))
    return old_acc, new_acc

def self_supervised_fit(series, lag=1):
    s = np.asarray(series, dtype=float)
    lag = int(lag)
    X = s[:-lag]
    y_tilde = s[lag:]
    A = np.column_stack([X, np.ones(len(X))])
    return np.linalg.lstsq(A, y_tilde, rcond=None)[0]

def two_means(X, iters=20, seed=0):
    X = np.asarray(X, dtype=float)
    g = np.random.default_rng(seed)
    c = X[g.choice(len(X), 2, replace=False)].copy()
    lab = np.zeros(len(X), dtype=int)
    for _ in range(iters):
        lab = np.argmin(((X[:, None, :] - c[None, :, :]) ** 2).sum(axis=2), axis=1)
        for k in range(2):
            if np.any(lab == k):
                c[k] = X[lab == k].mean(axis=0)
    return c, lab

def cluster_accuracy(y, labels):
    y = np.asarray(y)
    lab = np.asarray(labels)
    return max(float(np.mean(m == y)) for m in (lab, 1 - lab))

def task_type(y):
    y = np.asarray(y)
    if len(y) == 0:
        return "classification"
    if len(np.unique(y)) <= max(10, 0.05 * len(y)):
        return "classification"
    if np.all(y == y.astype(int)):
        return "classification"
    return "regression"

def self_training_threshold(x, y, labeled_idx):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y).astype(int)
    idx = np.asarray(labeled_idx, dtype=int)
    t0 = learn_threshold(x[idx], y[idx])
    pseudo = predict_threshold(x, t0)
    t1 = learn_threshold(x, pseudo)
    return float(t0), float(t1)
"""
# endregion
