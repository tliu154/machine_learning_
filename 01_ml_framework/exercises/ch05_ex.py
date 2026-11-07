"""
ch05 练习：误差来源与模型选择（Error Sources and Model Selection）
──────────────────────────────────────────────────
对应章节：docs/ch05_error_sources.md
重点：多项式特征与 Ridge / 偏差—方差分解 / 阶数扫描看 train-val 分叉 /
      正则化压权重 / K 折 CV / 外推灾难 / 误差诊断流程
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。

注意：本章练习只依赖 numpy。
本文件是【ML 第 5 章】的练习，与
00_foundations/python_basics/exercises/ch05_ex.py（字典与集合）不是同一份。
"""

import numpy as np


# ---------- 1. 多项式特征（锚点 c05-01） ----------
def poly_features(x, degree):
    """返回 (n, degree+1) 的 Vandermonde：列为 [1, x, x^2, ...]；x 可为标量或一维"""
    # TODO
    return None


# ---------- 2. 拟合（锚点 c05-01 / c05-04） ----------
def fit_poly(x, y, degree, alpha=0.0):
    """
    最小二乘拟合；alpha>0 时加 L2 惩罚（截距不罚）。
    用增广 lstsq 实现，不要手写 np.linalg.inv(A.T @ A)。
    """
    # TODO
    return None


# ---------- 3. 预测（锚点 c05-01） ----------
def predict_poly(theta, x):
    """用 theta 预测 x；theta 长度即最高阶数 + 1"""
    # TODO
    return None


# ---------- 4. 偏差—方差分解（锚点 c05-01） ----------
def bias_variance(preds, f0, sigma):
    """由同一测试点上的 B 个预测，返回 (bias^2, var, sigma^2, 三者之和)"""
    # TODO
    return None


# ---------- 5. 阶数扫描（锚点 c05-03） ----------
def degree_scan(x_tr, y_tr, x_va, y_va, max_degree):
    """对 d=0..max_degree 拟合，返回 (train_mses, val_mses) 两个长度 max_degree+1 的数组"""
    # TODO
    return None


# ---------- 6. 正则化效果（锚点 c05-04） ----------
def ridge_effect(x_tr, y_tr, x_va, y_va, degree, alphas):
    """对每个 alpha 拟合同一阶数，返回 (val_mses, 权重范数) 两个数组；范数不含截距"""
    # TODO
    return None


# ---------- 7. K 折划分（锚点 c05-05） ----------
def kfold_indices(n, k, seed=42):
    """返回 k 个 (train_idx, val_idx)；每个样本恰好当一次验证，n 不整除 k 时允许折大小差 1"""
    # TODO
    return None


# ---------- 8. CV 打分（锚点 c05-05） ----------
def cv_score(x, y, degree, k=5, seed=42):
    """返回 K 折验证 MSE 的均值，float"""
    # TODO
    return None


# ---------- 9. 外推灾难（锚点 c05-06） ----------
def extrapolation_gap(x_tr, y_tr, x_te, y_te, degree):
    """返回 (训练分布内 MSE, 外推测试 MSE)"""
    # TODO
    return None


# ---------- 10. 误差诊断（锚点 c05-07） ----------
def diagnose(train_mse, val_mse, noise_var):
    """
    按 5.7 的流程返回 'high_bias' / 'high_variance' / 'ok'：
    train 远高于噪声 → 高偏差；否则 train-val 间隙超过噪声 → 高方差；其余 ok。
    「远高于」取 train_mse > 2 * noise_var。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    SIG = 0.3

    def f(x):
        return np.sin(2 * np.pi * np.asarray(x))

    # 1~3. 特征、拟合、预测
    x = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    A = poly_features(x, 2)
    assert A.shape == (5, 3)
    assert np.allclose(A[:, 0], 1) and np.allclose(A[:, 1], x) and np.allclose(A[:, 2], x ** 2)
    assert poly_features(x, 0).shape == (5, 1)
    assert poly_features(0.5, 2).shape == (1, 3), "标量输入也要能用"
    y = f(x)
    th = fit_poly(x, y, 4)
    assert np.allclose(predict_poly(th, x), y, atol=1e-8), "5 个点 4 阶应能插值"
    th0 = fit_poly(x, np.ones(5), 0)
    assert np.isclose(predict_poly(th0, np.array([0.3]))[0], 1.0), "常数模型 / degree=0"
    snap = x.copy()
    fit_poly(x, y, 2)
    assert np.array_equal(x, snap), "不该修改输入"

    # 2 的 alpha：权重范数必须被压下来
    xr = rng.uniform(0, 1, 30)
    yr = f(xr) + rng.normal(0, SIG, 30)
    w0 = np.linalg.norm(fit_poly(xr, yr, 12)[1:])
    w1 = np.linalg.norm(fit_poly(xr, yr, 12, alpha=1e-3)[1:])
    assert w1 < w0 / 10, (w0, w1)

    # 4. 偏差—方差分解（等式要能算出来）
    b2, var, noise, expected = bias_variance(np.array([1.0, 1.1, 0.9, 1.0]), 1.0, 0.2)
    assert np.isclose(b2, 0.0) and np.isclose(var, 0.005)
    assert np.isclose(noise, 0.04) and np.isclose(expected, 0.045)
    b2c, varc, _, _ = bias_variance(np.full(5, 2.0), 1.0, 0.3)
    assert np.isclose(b2c, 1.0) and np.isclose(varc, 0.0), "常数预测：纯偏差、零方差"

    # 5. 阶数扫描：train 单调降、val U 型，按 train 挑必然选错
    g = np.random.default_rng(7)
    xtr = g.uniform(0, 1, 30)
    ytr = f(xtr) + g.normal(0, SIG, 30)
    xva = g.uniform(0, 1, 300)
    yva = f(xva) + g.normal(0, SIG, 300)
    tr_mses, va_mses = degree_scan(xtr, ytr, xva, yva, max_degree=10)
    assert len(tr_mses) == len(va_mses) == 11
    assert tr_mses[-1] < tr_mses[0], "train 误差应随容量下降"
    best_va, best_tr = int(np.argmin(va_mses)), int(np.argmin(tr_mses))
    assert best_va < best_tr, "按 train 挑会选到过拟合的阶数"

    # 6. 正则化：压权重 + 适度 alpha 改善 val
    alphas = [0.0, 1e-6, 1e-2, 1.0]
    va_r, wnorms = ridge_effect(xtr, ytr, xva, yva, 12, alphas)
    assert len(va_r) == len(wnorms) == 4
    assert wnorms[0] > wnorms[-1] * 100, (wnorms[0], wnorms[-1])
    assert min(va_r) < va_r[0], "适度正则应改善 val"

    # 7~8. K 折：每个样本恰好验证一次，训练/验证不重叠
    folds = kfold_indices(10, 5, seed=0)
    assert len(folds) == 5
    assert np.array_equal(np.sort(np.concatenate([va for _, va in folds])), np.arange(10))
    for tr, va in folds:
        assert len(tr) == 8 and len(va) == 2
        assert len(np.intersect1d(tr, va)) == 0
    assert sum(len(va) for _, va in kfold_indices(11, 3, seed=1)) == 11, "不整除时也不丢样本"
    cvs = cv_score(xtr, ytr, 3, k=5, seed=0)
    assert isinstance(cvs, float) and np.isfinite(cvs) and cvs > 0

    # 9. 分布不匹配：CV/训练内看不到外推灾难
    g5 = np.random.default_rng(23)
    xd = g5.uniform(0, 0.6, 120)
    yd = f(xd) + g5.normal(0, SIG, 120)
    xt = g5.uniform(0.6, 1.0, 500)
    yt = f(xt) + g5.normal(0, SIG, 500)
    in_m, out_m = extrapolation_gap(xd, yd, xt, yt, 5)
    assert out_m > in_m * 10, (in_m, out_m)

    # 10. 诊断流程
    assert diagnose(0.35, 0.36, 0.09) == "high_bias"
    assert diagnose(0.05, 0.40, 0.09) == "high_variance"
    assert diagnose(0.09, 0.10, 0.09) == "ok"

    print("ch05 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def poly_features(x, degree):
    x = np.atleast_1d(np.asarray(x, dtype=float))
    return np.vander(x, degree + 1, increasing=True)

def fit_poly(x, y, degree, alpha=0.0):
    A = poly_features(x, degree)
    y = np.asarray(y, dtype=float)
    if alpha > 0:
        p = A.shape[1]
        L = np.sqrt(alpha) * np.eye(p)
        L[0, 0] = 0.0
        A = np.vstack([A, L])
        y = np.r_[y, np.zeros(p)]
    return np.linalg.lstsq(A, y, rcond=None)[0]

def predict_poly(theta, x):
    theta = np.asarray(theta, dtype=float)
    x = np.atleast_1d(np.asarray(x, dtype=float))
    return np.vander(x, len(theta), increasing=True) @ theta

def bias_variance(preds, f0, sigma):
    p = np.asarray(preds, dtype=float)
    b2 = float((p.mean() - f0) ** 2)
    var = float(p.var())
    noise = float(sigma ** 2)
    return b2, var, noise, b2 + var + noise

def degree_scan(x_tr, y_tr, x_va, y_va, max_degree):
    trs, vas = [], []
    y_tr = np.asarray(y_tr, dtype=float)
    y_va = np.asarray(y_va, dtype=float)
    for d in range(max_degree + 1):
        th = fit_poly(x_tr, y_tr, d)
        trs.append(float(np.mean((y_tr - predict_poly(th, x_tr)) ** 2)))
        vas.append(float(np.mean((y_va - predict_poly(th, x_va)) ** 2)))
    return np.array(trs), np.array(vas)

def ridge_effect(x_tr, y_tr, x_va, y_va, degree, alphas):
    vals, norms = [], []
    y_va = np.asarray(y_va, dtype=float)
    for a in alphas:
        th = fit_poly(x_tr, y_tr, degree, alpha=a)
        vals.append(float(np.mean((y_va - predict_poly(th, x_va)) ** 2)))
        norms.append(float(np.linalg.norm(th[1:])))
    return np.array(vals), np.array(norms)

def kfold_indices(n, k, seed=42):
    idx = np.random.default_rng(seed).permutation(n)
    folds = np.array_split(idx, k)
    return [(np.setdiff1d(np.arange(n), va), va) for va in folds]

def cv_score(x, y, degree, k=5, seed=42):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    losses = []
    for tr, va in kfold_indices(len(x), k, seed):
        th = fit_poly(x[tr], y[tr], degree)
        losses.append(np.mean((y[va] - predict_poly(th, x[va])) ** 2))
    return float(np.mean(losses))

def extrapolation_gap(x_tr, y_tr, x_te, y_te, degree):
    th = fit_poly(x_tr, y_tr, degree)
    in_m = float(np.mean((np.asarray(y_tr) - predict_poly(th, x_tr)) ** 2))
    out_m = float(np.mean((np.asarray(y_te) - predict_poly(th, x_te)) ** 2))
    return in_m, out_m

def diagnose(train_mse, val_mse, noise_var):
    if train_mse > 2 * noise_var:
        return "high_bias"
    if val_mse - train_mse > noise_var:
        return "high_variance"
    return "ok"
"""
# endregion
