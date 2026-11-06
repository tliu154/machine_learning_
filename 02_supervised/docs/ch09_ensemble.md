# 第 9 章 集成方法（Ensemble Methods）

> 前置：第 8 章（决策树、`max_depth` 与 train/val 曲线）、第 4 章（梯度下降）
> 对应练习：[`ch09_ex.py`](../exercises/ch09_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`02_supervised/`

**一句话**：ch08 结尾说单棵深树对训练数据的微小扰动很敏感（高方差）。集成方法**不改造这棵树**，
而是训练很多棵再合起来：Bagging 用「并行 + 平均」压方差，Boosting 用「串行 + 纠错」压偏差。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [Bagging](#c09-01) · [自助采样（Bootstrap）](#c09-01) · [袋外估计（OOB）](#c09-01) · [随机森林（Random Forest）](#c09-01) | 9.1 |
| [Boosting](#c09-02) · [AdaBoost](#c09-02) · [梯度提升（Gradient Boosting）](#c09-02) · [残差（Residual）](#c09-02) · [收缩率（Shrinkage / Learning Rate）](#c09-02) · [XGBoost / LightGBM](#c09-02) | 9.2 |
| [偏差—方差分解（Bias–Variance Decomposition）](#c09-03) · [堆叠（Stacking）](#c09-03) | 9.3 |

### 全章共用的数据

```python
import numpy as np

rng = np.random.default_rng(42)
X = rng.normal(0, 1, (400, 10))          # 10 维特征，只有前 2 维真的有信号
y = (X[:, 0] + 0.7 * X[:, 1] > 0).astype(int)
X_tr, y_tr, X_va, y_va = X[:80], y[:80], X[80:], y[80:]   # 故意只用 80 个训练点
```

小训练集 + 一堆无关特征，正是深树最容易「记住噪声」的场合，把方差问题放大到看得见。

### 先看结论：同一份数据上，一棵树 vs 一群树

sklearn 实跑，`random_state=42`。**这张表就是本章的动机**：

| 模型 | train | val |
|---|---|---|
| 单棵不剪枝决策树 | **1.000** | 0.831 |
| Bagging 里 25 棵成员树（各自） | — | 平均 0.825，**std 0.033**，范围 0.762~0.934 |
| 这 25 棵多数决 | — | **0.866** |
| Bagging `B=50` | — | 0.872 |
| 随机森林 `B=50` | 1.000 | 0.878 |
| AdaBoost `M=50` | 1.000 | 0.891 |
| 梯度提升 `M=50` | 1.000 | **0.909** |

两个关键观察：① 成员树之间 val 能差 0.17，说明**单棵树的结果有多不稳定**；
② 把它们平均一下就拿到 0.866，**比几乎每一棵成员树都好**，而且没改过树本身。

---

<a id="c09-01"></a>

### 9.1 Bagging 与随机森林（Bagging and Random Forest）

**概念定义**：Bootstrap Aggregating —— 有放回地从训练集抽 $B$ 份等大的新训练集，
各训一棵**不剪枝的深树**，回归取平均、分类取多数决。
重点不在「模型变多」，而在**让各模型的错误尽量不相关**，这样平均时噪声才能互相抵消。

**数学形式**（全章最该记住的一条）：

$$\mathrm{Var}\left(\frac{1}{B}\sum_{b=1}^{B} f_b(x)\right)
= \rho\,\sigma^2 + \frac{1-\rho}{B}\sigma^2$$

$\sigma^2$ 是单棵树的方差，$\rho$ 是两棵树预测之间的相关系数。
「第一项是所有模型共享、平均不掉的部分；第二项随 $B$ 增大趋近 0」。
$B\to\infty$ 时方差**不会降到 0，而是卡在 $\rho\sigma^2$** ——
这就解释了为什么随机森林还要**在每个节点随机选一部分特征**：
人为让树之间长得不一样，把 $\rho$ 压下去，比一味加 $B$ 更有效。

**最小代码**：

```python
def bootstrap_indices(n, seed):
    return np.random.default_rng(seed).integers(0, n, n)   # 有放回，长度仍为 n

def majority_vote(preds):
    # preds: (B, m)，每行是一棵树的预测；平票取编号小的类
    return (np.asarray(preds).mean(axis=0) > 0.5).astype(int)

# fit_bagging / bagging_predict 的完整实现见练习第 5、6 题
idx = bootstrap_indices(len(X_tr), seed=0)
print(len(np.unique(idx)), len(X_tr))    # 约 0.632*n：有 36.8% 样本没被抽到
```

**袋外估计（OOB）**：一次有放回抽样，某个样本没被抽中的概率是
$(1-1/n)^n \approx e^{-1} \approx 0.368$。
这些没参与训练的样本可以**只对没见过它的那些树投票**，白捡一个验证集，
不用额外切数据。随机森林里 `oob_score=True` 就是干这个的。

**常见误区**：**Bagging 降方差，不降偏差**。
所以基学习器必须是「低偏差、高方差」的深树；拿浅树或线性模型做 Bagging，
等于把同一个欠拟合结论抄 50 遍，几乎不会变好。另外 $B$ 不是越大越好 ——
本章实测 `B=1/2/5/10/25/50` 对应 val `0.819/0.797/0.859/0.825/0.866/0.872`，
总体上升但有波动，且过了 25 棵收益已经很小。

**对应练习**：[第 1~7 题](../exercises/ch09_ex.py)

> 和 C++ / 已有认知的差异：C++ 里并行训练 $B$ 棵树要自己管线程/任务队列；
> 这里每棵树彼此独立，sklearn 一个 `n_jobs=-1` 就并行了。
> 而 numpy 手写版更直白 —— 一个列表推导出 $B$ 棵树，投票就是沿 `axis=0` 求平均。
> **Boosting 恰好相反：串行，天然难并行**，这是两类方法工程性质上的分水岭。

---

<a id="c09-02"></a>

### 9.2 Boosting 与梯度提升（Boosting and Gradient Boosting）

**概念定义**：**串行**训练，每一棵新树只负责纠正「前面所有树加起来还剩下的错误」。
AdaBoost 的做法是提高上一轮分错样本的权重；
梯度提升（Gradient Boosting）把这个想法写成更一般的形式：
**把「错误」定义为损失函数对当前预测的负梯度，让新树去拟合它**。

**数学形式**：

$$F_m(x) = F_{m-1}(x) + \eta\, h_m(x),\qquad
r_i = -\left.\frac{\partial L(y_i, F)}{\partial F}\right|_{F=F_{m-1}(x_i)}$$

第一式是「每轮往总预测上叠加一个小的修正项」，$\eta$ 是收缩率（学习率）；
第二式是这个修正项要拟合的目标。
**平方损失下 $r_i$ 正好就是残差 $y_i - F_{m-1}(x_i)$**（差个常数因子，可吸收进 $\eta$）——
所以「拟合残差」不是拍脑袋的启发式，而是**在函数空间里做梯度下降**：
ch04 对参数 $w$ 走一步，这里对「整个函数 $F$」走一步。

**最小代码**（一维回归，树桩做基学习器）：

```python
reg_rng = np.random.default_rng(42)
x_reg = reg_rng.uniform(-3, 3, 100)
y_reg = np.sin(x_reg) + reg_rng.normal(0, 0.15, 100)

def regression_stump(x, r):
    """找最佳阈值，返回 (t, 左侧残差均值, 右侧残差均值)"""
    best, best_sse = None, np.inf
    for t in np.unique(x):
        m = x <= t
        if m.all() or not m.any():
            continue
        lv, rv = r[m].mean(), r[~m].mean()
        sse = np.sum((r - np.where(m, lv, rv)) ** 2)
        if sse < best_sse:
            best, best_sse = (float(t), float(lv), float(rv)), sse
    return best

F = np.full(len(y_reg), y_reg.mean())
for _ in range(30):
    t, lv, rv = regression_stump(x_reg, y_reg - F)   # 拟合当前残差
    F += 0.1 * np.where(x_reg <= t, lv, rv)          # 小步叠加（shrinkage）
```

本章实测（$y=\sin x +$ 噪声，100 点）：常数基线 MSE **0.6097**，
手写树桩版 `M=1/5/20/50` 依次降到 `0.5161 / 0.2831 / 0.0831 / 0.0469`，
sklearn 的 `GradientBoostingRegressor(M=50, lr=0.1)` 为 0.0366 —— 一个量级。

**常见误区**：**学习率 $\eta$ 和轮数 $M$ 是一对此消彼长的旋钮，且 $\eta$ 太大会直接发散**。
同样 `M=30`，sklearn 实测 `lr=0.01/0.1/1.0/2.0` 的 train MSE 是
`0.3791 / 0.0553 / 0.0184 / 0.6097` —— 最后那个已经打回基线（震荡）。
另外 Boosting 会死磕分错的样本，**对噪声标签比 Bagging 敏感得多**。

> 工程补充：`XGBoost / LightGBM` 不是新算法，是梯度提升的工程实现 ——
> 加正则项、用二阶梯度、直方图分箱、特征并行、缺失值默认方向。
> 表格数据的比赛里它们长期是默认基线，但**先看懂上面的 10 行树桩再用库**。

**对应练习**：[第 8~11 题](../exercises/ch09_ex.py)

---

<a id="c09-03"></a>

### 9.3 偏差—方差视角与模型选择（Bias–Variance and Model Choice）

**概念定义**：泛化误差可以拆成三块，前两块是模型能改的、第三块是数据自带的：

$$\mathrm{Err}(x) = \mathrm{Bias}^2[\hat f(x)] + \mathrm{Var}[\hat f(x)] + \sigma^2$$

**偏差**是「平均而言偏离真相多远」，**方差**是「换一批训练数据结果抖多厉害」。
Bagging 打方差，Boosting 打偏差 —— **它们不是二选一的竞品，是治不同病的两种药**：
一堆浅树（高偏差）该用 Boosting，一堆深树（高方差）该用 Bagging。

**诊断表**（先画 train/val 曲线，再决定动哪个）：

| 现象 | 判断 | 该做什么 |
|---|---|---|
| train 差、val 也差 | 高偏差 / 欠拟合 | 加深树、Boosting、加特征、减正则 |
| train 好、val 明显差 | 高方差 / 过拟合 | Bagging、限制深度、加数据、加正则 |
| train 好、val 也好 | 正常 | 可以收工了 |

**堆叠（Stacking）**：不投票，改用另一个模型（元学习器）**学怎么组合**各基模型的输出。
关键约束：元学习器必须拿**out-of-fold 预测**来训练，否则它看到的是基模型在训练集上的
「背答案」结果，会严重高估 → 这又是 ch04 数据泄漏的一个变体。

**最小代码**（sklearn 三行对照，需要 `pip install scikit-learn`；**本章练习不依赖它**）：

```python
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

for model in (BaggingClassifier(DecisionTreeClassifier(), n_estimators=50, random_state=42),
              RandomForestClassifier(n_estimators=50, random_state=42),
              GradientBoostingClassifier(n_estimators=50, random_state=42)):
    model.fit(X_tr, y_tr)
    print(type(model).__name__, round(model.score(X_va, y_va), 3))
# BaggingClassifier 0.872 / RandomForestClassifier 0.878 / GradientBoostingClassifier 0.909
```

**什么时候会翻车**（篇 README 要求的固定项）：

- **Bagging**：基学习器本身欠拟合时，平均只会保留同样的偏差；各成员错误高度相关（$\rho\to1$）
  时 $B$ 再大也只剩第一项。信噪比极低、连单棵树都抓不到信号时，投票救不回来
- **Boosting**：噪声标签会被反复加权，比 Bagging 更容易过拟合；$\eta$ 过大会震荡（见上）
- **Stacking**：元学习器在 in-sample 预测上训练 → 泄漏，线上分数崩塌
- **共性**：集成把可解释性几乎赔光了。单棵树能画出规则，200 棵树的森林只能给个特征重要度

**常见误区**：**别不看 train/val 曲线就调集成**。本章开头单棵树 train 1.000 / val 0.831
是典型高方差，所以 Bagging 有效；若换成 train 0.60 / val 0.58 的高偏差场景，
该做的是加深模型或上 Boosting，堆 200 棵树纯属浪费算力。

**对应练习**：[第 4 题（分歧度 = 方差的代理）](../exercises/ch09_ex.py)、
[第 10 题（自测里对比不同 `lr`）](../exercises/ch09_ex.py)

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| 训练一个模型，调它的参数 | 训练一堆模型，调它们**怎么组合** |
| 并行化要自己管线程 | Bagging 天然并行（`n_jobs=-1`），Boosting 天生串行 |
| 梯度下降作用在参数向量 $w$ 上 | 梯度提升作用在**函数** $F$ 上，每轮加一个 $h_m$ |
| 一个 `predict` 一个结果 | `(B, m)` 预测矩阵沿 `axis=0` 投票 |
| 验证集必须单独切 | OOB 袋外样本白捡一个验证集 |

| | Bagging / 随机森林 | Boosting / 梯度提升 |
|---|---|---|
| 训练方式 | 并行，各树独立 | 串行，后一棵依赖前面 |
| 基学习器 | 深树（低偏差高方差） | 浅树/树桩（高偏差低方差） |
| 主要降低 | 方差 | 偏差 |
| 关键旋钮 | $B$、`max_features`（降 $\rho$） | $M$、$\eta$、`max_depth` |
| 对噪声 | 较鲁棒 | 较敏感 |
| 本章 val | 0.872 / 0.878 | 0.891 / **0.909** |

> **最容易踩的 3 个坑**：
> 1. 拿欠拟合的浅树做 Bagging —— 平均消不掉偏差
> 2. 以为 $B$ 越大越好 —— 方差下限是 $\rho\sigma^2$，该降的是相关性
> 3. Boosting 的 $\eta$ 开太大 —— 实测 `lr=2.0` 时 MSE 直接退回基线

## 练习

本章练习统一在 [`ch09_ex.py`](../exercises/ch09_ex.py)：从 bootstrap 抽样、OOB 掩码、
多数决与分歧度，到手写 Bagging 森林、袋外评分，再到回归树桩与梯度提升，共 11 题。
文件顶部**内置一份精简决策树**作为基学习器（思路见 ch08），保证本文件能独立运行；
**全部只用 numpy**，跑通所有 `assert` 即过关。

上一篇：[第 8 章 经典分类算法](ch08_classical_classifiers.md)
下一篇：第 10 章 特征工程（待写，见 [SYLLABUS](../../SYLLABUS.md)）
