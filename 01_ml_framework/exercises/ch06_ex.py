"""
ch06 练习：评估指标（Evaluation Metrics）
──────────────────────────────────────────────────
对应章节：docs/ch06_evaluation_metrics.md
重点：混淆矩阵与 P/R/F1 / 阈值扫描与 ROC-AUC / 回归四指标 /
      业务代价与最优阈值 / 测试集调参泄漏（胜者诅咒）/ 重复样本泄漏
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy，不需要 scikit-learn（教学文档里才做库对照）。
本文件是【ML 第 6 章】的练习，与
00_foundations/python_basics/exercises/ch06_ex.py（控制流）不是同一份。
"""

import numpy as np


# ---------- 1. 混淆矩阵（锚点 c06-01） ----------
def confusion_matrix(y_true, y_pred):
    """返回 [[TN, FP], [FN, TP]] 的 int 数组；输入可为 list；不改输入"""
    # TODO
    return None


# ---------- 2. 四个分类指标（锚点 c06-01） ----------
def prf_from_cm(cm):
    """由 2x2 混淆矩阵返回 (accuracy, precision, recall, f1)；分母为 0 一律按 0.0"""
    # TODO
    return None


# ---------- 3. 扫出 F1 最高的阈值（锚点 c06-01 / c06-03） ----------
def best_f1_threshold(y, scores):
    """
    阈值候选取 np.unique(scores) 从大到小，pred = scores >= t。
    返回 (best_t, best_f1)；F1 平局时取【较大】阈值（更保守，少报正例）。
    scores 为空时返回 (0.0, 0.0)。
    """
    # TODO
    return None


# ---------- 4. ROC 曲线点（锚点 c06-01） ----------
def roc_points(y, scores):
    """返回 (fpr, tpr) 两个 float 数组，阈值从高到低；不含 (0,0) 起点，末点应为 (1,1)"""
    # TODO
    return None


# ---------- 5. AUC（锚点 c06-01） ----------
def auc_roc(y, scores):
    """补 (0,0) 起点后对 ROC 点做梯形积分；完美分离返回 1.0"""
    # TODO
    return None


# ---------- 6. 回归四指标（锚点 c06-02） ----------
def regression_metrics(y, y_pred):
    """返回 (mae, mse, rmse, r2)；y 全相等（SST=0）时 r2 约定 0.0"""
    # TODO
    return None


# ---------- 7. 期望代价（锚点 c06-03） ----------
def expected_cost(y, scores, t, c_fp, c_fn):
    """返回 c_fp * FP(t) + c_fn * FN(t)，float"""
    # TODO
    return None


# ---------- 8. 最小代价阈值（锚点 c06-03） ----------
def best_cost_threshold(y, scores, c_fp, c_fn, grid=None):
    """
    grid 默认为 np.round(np.arange(0.05, 1.0, 0.01), 2)。
    返回 (best_t, best_cost)；代价平局时取【较大】阈值。
    """
    # TODO
    return None


# ---------- 9. 胜者诅咒（锚点 c06-04） ----------
def selection_bias(val_scores, test_scores):
    """
    val_scores[i] / test_scores[i] 是第 i 个候选模型在验证集 / 测试集上的分数。
    返回 (picked_on_test, picked_on_val)：
      picked_on_test = 按测试分数挑最好的候选，再报【它自己的测试分数】
      picked_on_val  = 按验证分数挑最好的候选，报它的测试分数
    """
    # TODO
    return None


# ---------- 10. 重复样本泄漏率（锚点 c06-04） ----------
def duplicate_leak_rate(X_train, X_test):
    """X_test 中有多少比例的行能在 X_train 里找到逐元素完全相同的行；空输入返回 0.0"""
    # TODO
    return None


# ---------- 11. 平衡准确率（锚点 c06-01 / c06-03） ----------
def balanced_accuracy(y, y_pred):
    """返回 (TPR + TNR) / 2；某一类不存在时只算存在的类，两类都不存在返回 0.0"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    # 全章共用：1000 个样本、10 个正例（1% 正例率）
    rng = np.random.default_rng(42)
    n = 1000
    y = np.zeros(n, dtype=int)
    y[rng.choice(n, 10, replace=False)] = 1
    all_neg = np.zeros(n, dtype=int)
    pos_idx, neg_idx = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    catch = np.zeros(n, dtype=int)
    catch[pos_idx[:5]] = 1
    catch[neg_idx[:20]] = 1

    # 1~2. 混淆矩阵与 P/R/F1
    cm = confusion_matrix(y, catch)
    assert cm.tolist() == [[970, 20], [5, 5]], cm
    acc, prec, rec, f1 = prf_from_cm(cm)
    assert np.isclose(acc, 0.975) and np.isclose(prec, 0.2)
    assert np.isclose(rec, 0.5) and np.isclose(f1, 0.2857142857), f1
    y_snap, catch_snap = y.copy(), catch.copy()
    confusion_matrix(y, catch)
    assert np.array_equal(y, y_snap) and np.array_equal(catch, catch_snap), "不该改输入"
    # 全预测负例：accuracy 0.99 却一个正例没抓到
    a0, p0, r0, f0 = prf_from_cm(confusion_matrix(y, all_neg))
    assert np.isclose(a0, 0.99) and (p0, r0, f0) == (0.0, 0.0, 0.0)
    # 除零边界
    assert prf_from_cm(np.zeros((2, 2), dtype=int)) == (0.0, 0.0, 0.0, 0.0)

    # 3. 扫 F1 阈值
    y3 = np.array([0, 0, 0, 1, 1])
    s3 = np.array([0.1, 0.2, 0.4, 0.6, 0.9])
    bt, bf = best_f1_threshold(y3, s3)
    assert np.isclose(bt, 0.6) and np.isclose(bf, 1.0), (bt, bf)
    assert best_f1_threshold(y3, np.full(5, 0.5))[0] == 0.5, "全相等分数只有一个阈值"
    assert best_f1_threshold(np.array([]), np.array([])) == (0.0, 0.0), "空输入"
    # 所有阈值 F1 都是 0 时，平局取较大阈值
    bt3, bf3 = best_f1_threshold(np.array([0, 0]), np.array([0.3, 0.7]))
    assert bt3 == 0.7 and bf3 == 0.0, (bt3, bf3)

    # 4~5. ROC 点与 AUC
    y4 = np.array([0, 0, 1, 1])
    s4 = np.array([0.1, 0.2, 0.8, 0.9])
    fpr, tpr = roc_points(y4, s4)
    assert fpr.shape == tpr.shape and fpr[-1] == 1.0 and tpr[-1] == 1.0
    assert np.all(np.diff(fpr) >= 0) and np.all(np.diff(tpr) >= 0), "两轴应单调不减"
    assert np.isclose(auc_roc(y4, s4), 1.0)
    assert np.isclose(auc_roc(y4, np.array([0.9, 0.8, 0.2, 0.1])), 0.0)
    assert np.isclose(auc_roc(y4, s4 + 5.0), 1.0), "AUC 只看排序，平移不变"

    # 6. 回归四指标与除零 / 负数边界
    assert np.allclose(regression_metrics(np.array([1., 2., 3.]),
                                         np.array([1., 2., 3.])), (0, 0, 0, 1))
    y6, p6 = np.zeros(100), np.zeros(100)
    p6[0] = 8.0
    ma, ms, rm, r2 = regression_metrics(y6, p6)
    assert np.isclose(ma, 0.08) and np.isclose(ms, 0.64), (ma, ms)
    assert np.isclose(rm, 0.8) and r2 == 0.0, "SST=0 时 r2 约定 0"
    assert regression_metrics(np.array([0., 1., 2.]),
                              np.array([5., 5., 5.]))[3] < 0, "R² 可以为负"

    # 7. 期望代价
    y7, s7 = np.array([0, 0, 1, 1]), np.array([0.1, 0.4, 0.6, 0.9])
    assert expected_cost(y7, s7, 0.5, 1.0, 10.0) == 0.0
    assert expected_cost(y7, s7, 0.95, 1.0, 10.0) == 20.0, "全漏报 → 2 个 FN"
    assert expected_cost(y7, s7, 0.0, 1.0, 10.0) == 2.0, "全报正 → 2 个 FP"

    # 8. 代价翻转 → 最优阈值反向移动；平局取较大阈值
    y8, s8 = np.array([0, 0, 1, 1]), np.array([0.1, 0.55, 0.45, 0.9])
    grid8 = np.array([0.4, 0.5, 0.6])
    t_lo, _ = best_cost_threshold(y8, s8, 1.0, 10.0, grid=grid8)
    t_hi, _ = best_cost_threshold(y8, s8, 10.0, 1.0, grid=grid8)
    assert t_lo == 0.4 and t_hi == 0.6, "漏诊贵就放宽，误报贵就收紧"
    assert best_cost_threshold(y8, s8, 0.0, 0.0, grid=grid8)[0] == 0.6
    assert 0.0 <= best_cost_threshold(y7, s7, 1.0, 10.0)[0] < 1.0, "默认 grid 可用"

    # 9. 胜者诅咒：候选之间没有真实差别，用测试集挑仍会系统性虚高
    g = np.random.default_rng(2026)
    gaps = []
    for _ in range(200):
        va = g.uniform(0, 1, 40)
        te = g.uniform(0, 1, 40)          # 与 va 独立 = 40 个候选其实一样好
        w, r = selection_bias(va, te)
        gaps.append(w - r)
    assert np.mean(gaps) > 0.15, "用测试集挑必然虚高"
    assert np.isclose(selection_bias(np.array([0.1, 0.9]),
                                     np.array([0.3, 0.7]))[0], 0.7)

    # 10. 重复样本泄漏
    Xtr = np.array([[1., 2.], [3., 4.]])
    Xte = np.array([[5., 6.], [1., 2.], [1., 2.]])
    assert np.isclose(duplicate_leak_rate(Xtr, Xte), 2 / 3)
    assert duplicate_leak_rate(Xtr, np.empty((0, 2))) == 0.0
    assert duplicate_leak_rate(np.empty((0, 2)), Xte) == 0.0
    base = np.arange(400, dtype=float).reshape(80, 5)
    X_dup = np.vstack([base, base[:40]])
    gg = np.random.default_rng(7)
    idx = gg.permutation(len(X_dup))
    k = int(0.7 * len(X_dup))
    leak = duplicate_leak_rate(X_dup[idx[:k]], X_dup[idx[k:]])
    assert 0.4 < leak < 0.6, f"随机划分后大量测试样本在训练集有副本: {leak}"

    # 11. 平衡准确率戳破 0.99 的假象
    assert np.isclose(balanced_accuracy(y, all_neg), 0.5)
    assert np.isclose(prf_from_cm(confusion_matrix(y, all_neg))[0], 0.99)
    assert np.isclose(balanced_accuracy(y, catch), (0.5 + 970 / 990) / 2)
    assert np.isclose(balanced_accuracy(np.ones(5), np.ones(5)), 1.0), "只有一个类时只算它"

    print("ch06 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def confusion_matrix(y_true, y_pred):
    yt = np.asarray(y_true).astype(int)
    yp = np.asarray(y_pred).astype(int)
    return np.array([
        [np.sum((yt == 0) & (yp == 0)), np.sum((yt == 0) & (yp == 1))],
        [np.sum((yt == 1) & (yp == 0)), np.sum((yt == 1) & (yp == 1))],
    ], dtype=int)

def prf_from_cm(cm):
    tn, fp, fn, tp = np.asarray(cm).ravel()
    total = tn + fp + fn + tp
    acc = (tp + tn) / total if total else 0.0
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return float(acc), float(prec), float(rec), float(f1)

def best_f1_threshold(y, scores):
    y = np.asarray(y).astype(int)
    s = np.asarray(scores, dtype=float)
    if len(s) == 0:
        return 0.0, 0.0
    best_t, best_f1 = float(s.min()), -1.0
    for t in np.unique(s)[::-1]:
        pred = (s >= t).astype(int)
        f1 = prf_from_cm(confusion_matrix(y, pred))[3]
        if f1 > best_f1:
            best_f1, best_t = f1, float(t)
    return best_t, float(best_f1)

def roc_points(y, scores):
    y = np.asarray(y).astype(int)
    s = np.asarray(scores, dtype=float)
    P, N = int(np.sum(y == 1)), int(np.sum(y == 0))
    fpr, tpr = [], []
    for t in np.unique(s)[::-1]:
        pred = s >= t
        fpr.append(np.sum(pred & (y == 0)) / N if N else 0.0)
        tpr.append(np.sum(pred & (y == 1)) / P if P else 0.0)
    return np.array(fpr, dtype=float), np.array(tpr, dtype=float)

def auc_roc(y, scores):
    fpr, tpr = roc_points(y, scores)
    fpr, tpr = np.r_[0.0, fpr], np.r_[0.0, tpr]
    return float(np.sum(np.diff(fpr) * (tpr[:-1] + tpr[1:]) / 2))

def regression_metrics(y, y_pred):
    y = np.asarray(y, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    e = y - p
    mae = float(np.mean(np.abs(e)))
    mse = float(np.mean(e ** 2))
    sst = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - float(np.sum(e ** 2)) / sst if sst > 0 else 0.0
    return mae, mse, float(np.sqrt(mse)), float(r2)

def expected_cost(y, scores, t, c_fp, c_fn):
    y = np.asarray(y).astype(int)
    pred = np.asarray(scores) >= t
    return float(np.sum(pred & (y == 0)) * c_fp
                 + np.sum(~pred & (y == 1)) * c_fn)

def best_cost_threshold(y, scores, c_fp, c_fn, grid=None):
    if grid is None:
        grid = np.round(np.arange(0.05, 1.0, 0.01), 2)
    grid = np.asarray(grid, dtype=float)
    costs = np.array([expected_cost(y, scores, t, c_fp, c_fn) for t in grid])
    pos = len(costs) - 1 - int(np.argmin(costs[::-1]))
    return float(grid[pos]), float(costs[pos])

def selection_bias(val_scores, test_scores):
    va = np.asarray(val_scores, dtype=float)
    te = np.asarray(test_scores, dtype=float)
    return float(te[int(np.argmax(te))]), float(te[int(np.argmax(va))])

def duplicate_leak_rate(X_train, X_test):
    tr = np.asarray(X_train, dtype=float)
    te = np.asarray(X_test, dtype=float)
    if len(te) == 0 or len(tr) == 0:
        return 0.0
    hit = (te[:, None, :] == tr[None, :, :]).all(axis=2).any(axis=1)
    return float(np.mean(hit))

def balanced_accuracy(y, y_pred):
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    parts = []
    if tp + fn > 0:
        parts.append(tp / (tp + fn))
    if tn + fp > 0:
        parts.append(tn / (tn + fp))
    return float(np.mean(parts)) if parts else 0.0
"""
# endregion
