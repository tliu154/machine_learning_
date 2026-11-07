# 第 6 章 评估指标（Evaluation Metrics）

> 前置：第 4 章（损失函数）、第 7 章（模型会输出得分；跳读者看 6.1 的「得分」一句即可）
> 对应练习：[`ch06_ex.py`](../exercises/ch06_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`01_ml_framework/`

**一句话**：**损失是给优化器看的，指标是给人看的**。前者要可导，后者要能回答业务问题 ——
一个 0.99 准确率的模型可能一个正例都没抓到。这章把「分数是怎么骗人的」拆开算一遍。

> 和 [ch10](../../02_supervised/docs/ch10_feature_engineering.md) 的分工：ch10 管**预处理器的 fit 边界**
> （统计量别偷看验证集），本章管**评估协议**（测试集别被反复使用）。两处都叫数据泄漏，发生在不同环节。

### 先看结论：同一个「高分」，四种骗法

全部实跑，固定种子 42，numpy 手写 + sklearn 对照。

| 现象 | 表面分数 | 真相 |
|---|---|---|
| 1% 正例，全预测负例 | accuracy **0.990** | 召回率 0、F1 0，一个正例没抓到 |
| 抓到 5 个正例、误报 20 个 | accuracy **0.975**（反而更低） | F1 0.286，比上面那个有用得多 |
| 纯噪声上用测试集挑 40 个候选 | test acc **0.616** | 换验证集挑只有 0.514，真实水平本来就是 0.5 |
| 数据有重复行还按行随机划分 | 测试集里 **47.2%** 的样本在训练集有自己的副本 | 考卷漏进了练习册 |

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [混淆矩阵（Confusion Matrix）](#c06-01) · [准确率（Accuracy）](#c06-01) · [精确率（Precision）](#c06-01) · [召回率（Recall）](#c06-01) · [F1 分数（F1 Score）](#c06-01) | 6.1 |
| [阈值（Threshold）](#c06-01) · [ROC / AUC](#c06-01) · [平衡准确率（Balanced Accuracy）](#c06-01) | 6.1 |
| [MAE](#c06-02) · [MSE](#c06-02) · [RMSE](#c06-02) · [决定系数（R²）](#c06-02) | 6.2 |
| [业务代价（Business Cost）](#c06-03) · [代价敏感阈值](#c06-03) · [PR 曲线](#c06-03) · [指标选择](#c06-03) | 6.3 |
| [数据泄漏（Data Leakage）](#c06-04) · [测试集调参 / 胜者诅咒](#c06-04) · [重复样本](#c06-04) · [时间序列划分](#c06-04) | 6.4 |

---

<a id="c06-01"></a>

### 6.1 分类指标（Classification Metrics）

**概念定义**：把预测按「真实是正/负 × 预测是正/负」分成四格，就是**混淆矩阵**。
所有分类指标都是这四格的比值组合。全仓库统一：正例记为 1，布局 `[[TN, FP], [FN, TP]]`
（与 sklearn 的 `confusion_matrix` 一致）。模型给的是**得分**（概率或 margin），阈值把它变成硬标签。

**数学形式**：

$$\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN},\qquad
\text{Precision} = \frac{TP}{TP+FP},\qquad
\text{Recall} = \frac{TP}{TP+FN}$$
$$F_1 = \frac{2PR}{P+R} = \frac{2TP}{2TP+FP+FN}$$

「Accuracy 是整体猜对多少，Precision 是报出来的里面有多少是真的，Recall 是真的里面报出来多少」。
F1 是 P 和 R 的**调和平均**：任一个塌到 0，整体就被拉到 0（算术平均会被 0 和 1 平均成 0.5 骗过去）。
numpy：四次布尔计数 `np.sum((y == 0) & (p == 1))` 等；分母为 0 时用 `if tp + fp else 0.0` 兜底。

**最小代码**：

```python
import numpy as np

def confusion(y_true, y_pred):
    yt, yp = np.asarray(y_true).astype(int), np.asarray(y_pred).astype(int)
    return np.array([
        [np.sum((yt == 0) & (yp == 0)), np.sum((yt == 0) & (yp == 1))],
        [np.sum((yt == 1) & (yp == 0)), np.sum((yt == 1) & (yp == 1))],
    ])

def prf(y_true, y_pred):
    tn, fp, fn, tp = confusion(y_true, y_pred).ravel()
    acc = (tp + tn) / (tp + tn + fp + fn)
    prec = tp / (tp + fp) if tp + fp else 0.0     # 一次正例都没报过，约定为 0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return acc, prec, rec, f1
```

sklearn 对照（需要 `pip install scikit-learn`；**本章练习不依赖它**）。实测逐格、四位小数全部一致：

```python
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                             recall_score, f1_score)
print(confusion_matrix(y, pred))                          # 与手写逐格相同
print(precision_score(y, pred, zero_division=0),         # 0.2000
      recall_score(y, pred), f1_score(y, pred))          # 0.5000 / 0.2857
```

**为什么 0.990 是废的**（1000 个样本、10 个正例）：

| 模型 | 混淆矩阵 | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|---|
| 全预测负例 | `[[990, 0], [10, 0]]` | **0.990** | 0.000 | 0.000 | 0.000 |
| 抓 5 个正例、误报 20 个 | `[[970, 20], [5, 5]]` | 0.975 | 0.200 | 0.500 | **0.286** |

有用的那个模型 accuracy 反而更低。**类别越不平衡，accuracy 越是被多数类绑架。**
不平衡时改看 **平衡准确率** $\tfrac{1}{2}(\text{TPR}+\text{TNR})$：全预测负例只有 0.5。

**ROC / AUC**：把阈值从高扫到低，每扫一次得到一个 $(\text{FPR},\text{TPR})$ 点，连起来就是 ROC 曲线：

$$\mathrm{FPR} = \frac{FP}{FP+TN},\qquad \mathrm{TPR} = \mathrm{Recall} = \frac{TP}{TP+FN}$$

AUC 是曲线下面积，等价于「**随机取一个正例和一个负例，正例得分更高的概率**」。
它只衡量**排序质量**，跟阈值无关，也不直接受类别比例影响。梯形积分手写：

```python
def roc_points(y, s):
    y, s = np.asarray(y), np.asarray(s)
    P, N = (y == 1).sum(), (y == 0).sum()
    fpr, tpr = [], []
    for t in np.unique(s)[::-1]:              # 阈值从高到低
        pred = s >= t
        fpr.append(np.sum(pred & (y == 0)) / N)
        tpr.append(np.sum(pred & (y == 1)) / P)
    return np.array(fpr), np.array(tpr)

def auc_roc(y, s):
    fpr, tpr = roc_points(y, s)
    fpr, tpr = np.r_[0.0, fpr], np.r_[0.0, tpr]       # 补 (0, 0) 起点
    return float(np.sum(np.diff(fpr) * (tpr[:-1] + tpr[1:]) / 2))
```

实测：200 正 / 800 负、两份有重叠的正态得分 → 手写 **0.7891**、`roc_auc_score` **0.7891**
（差 1e-6，来自离散阈值的梯形近似，不是实现错）。

**常见误区**：**别把精确率叫成准确率**（[NOTATION 易混词](../../NOTATION.md)），两者分母完全不同；
**AUC 高不等于能用** —— 极不平衡时负例基数大，FPR 的分母把误报稀释了，ROC 会显得乐观，
这时要看 PR 曲线（6.3）；**别在训练集上报指标**，那是拟合程度不是泛化（ch05）。

**对应练习**：[第 1、2、3、4、5 题](../exercises/ch06_ex.py)

> 和 C++ 的差异：C++ 里判断对错是 `if (pred == label) ok++`，一个布尔累加就完事。
> ML 里「错」要按四格分开记，因为**四种错的代价完全不同** —— 从「程序正确性」转向「决策质量」。

---

<a id="c06-02"></a>

### 6.2 回归指标（Regression Metrics）

**概念定义**：回归预测连续值，误差 $e_i = y_i - \hat{y}_i$。四个指标只是把这一串误差用不同方式压成一个数。

**数学形式**：

$$\mathrm{MAE} = \frac{1}{n}\sum_i |e_i|,\qquad
\mathrm{MSE} = \frac{1}{n}\sum_i e_i^2,\qquad
\mathrm{RMSE} = \sqrt{\mathrm{MSE}}$$
$$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$$

「MAE 是平均差多少，RMSE 与 MAE 和 $y$ **同单位**（MSE 是平方单位，不方便读）」；
R² 是「比无脑预测均值好多少」：1 完美、0 等于没学到、**负数说明还不如预测均值**。
numpy：`np.mean(np.abs(e))`、`np.mean(e**2)`、`1 - (e**2).sum() / ((y - y.mean())**2).sum()`。

**损失 vs 指标（本章最该带走的区分）**：MSE 在 ch04 里当损失函数，因为它处处可导、梯度好算；
Accuracy / F1 是**离散计数**，不可导，没法拿去做梯度下降。训练时用可导的代理损失（如交叉熵），
评估时用业务认的指标。**两者不一致是常态，不是 bug。**

**最小代码**：

```python
def regression_metrics(y, y_pred):
    y, y_pred = np.asarray(y, float), np.asarray(y_pred, float)
    e = y - y_pred
    sst = np.sum((y - y.mean()) ** 2)
    mse = float(np.mean(e ** 2))
    return (float(np.mean(np.abs(e))), mse, float(np.sqrt(mse)),
            1 - np.sum(e ** 2) / sst if sst > 0 else 0.0)
```

实测（200 个样本，$y\sim\mathcal{N}(0,1)$，预测加 0.3 噪声）。
sklearn 的 `mean_absolute_error` / `mean_squared_error` / `r2_score` 与手写四位小数一致：

| | MAE | MSE | RMSE | R² |
|---|---|---|---|---|
| 正常 | 0.2520 | 0.0990 | 0.3147 | 0.8979 |
| 只把 1 个残差拉大 8 | 0.2920 | 0.4403 | 0.6635 | 0.5460 |
| 倍数 | ×1.16 | **×4.45** | ×2.11 | — |

**常见误区**：**别只看 MSE 就下结论** —— 一个离群点就能让它翻 4 倍多，先看残差分布，
必要时换 MAE 或 Huber；**别对不同量纲的数据横向比 MSE**，报 RMSE / MAE 或无量纲的 R²；
**R² 为负不是 bug**（实测恒预测 $\bar y + 3$ 得到 −9.2792），是模型比均值基线还差；
[ch07](../../02_supervised/docs/ch07_linear_models.md) 的 `model.score()` 返回的就是它。

**对应练习**：[第 6 题](../exercises/ch06_ex.py)

---

<a id="c06-03"></a>

### 6.3 指标选择与业务代价（Metric Selection and Business Cost）

**概念定义**：模型输出得分，**阈值才把得分变成决策**。0.5 只是习惯，不是最优。
选哪个指标、定哪个阈值，由「四种错误各罚多少」决定。

**数学形式**：

$$C(t) = c_{FP}\cdot FP(t) + c_{FN}\cdot FN(t),\qquad t^* = \arg\min_t C(t)$$

「把每个阈值下的误报数、漏报数按单价加权求和，取代价最小的那个阈值」。
numpy：对 `grid` 里每个 $t$ 算一次 `np.sum(pred & (y == 0))` 和 `np.sum(~pred & (y == 1))`，再 `np.argmin`。

**最小代码**：

```python
def expected_cost(y, s, t, c_fp, c_fn):
    pred = np.asarray(s) >= t
    return float(np.sum(pred & (y == 0)) * c_fp
                 + np.sum(~pred & (y == 1)) * c_fn)

def best_cost_threshold(y, s, c_fp, c_fn):
    grid = np.round(np.arange(0.05, 1.0, 0.01), 2)
    costs = np.array([expected_cost(y, s, t, c_fp, c_fn) for t in grid])
    return float(grid[np.argmin(costs)]), float(costs.min())
```

实测（还是 6.1 那份 200 正 / 800 负的得分，**模型一个字没改，只翻代价矩阵**）：

| 代价设定 | 最优阈值 | 最小代价 | 死守 0.5 的代价 |
|---|---|---|---|
| 漏诊 : 误报 = 10 : 1 | **0.35** | 599 | 764 |
| 误报 : 漏诊 = 10 : 1 | **0.96** | 211 | 2195 |

同一份得分，最优阈值从 0.35 跳到 0.96。**阈值是业务参数，不是模型参数**（对照 NOTATION 的「参数 vs 超参数」）。

阈值扫描还暴露另一件事：

| 阈值 | 0.8 | 0.6 | 0.5 | 0.4 | 0.2 |
|---|---|---|---|---|---|
| Accuracy | **0.814** | 0.783 | 0.731 | 0.601 | 0.375 |
| Precision | 0.635 | 0.462 | 0.404 | 0.318 | 0.241 |
| Recall | 0.165 | 0.510 | 0.725 | 0.870 | 0.990 |
| F1 | 0.262 | 0.485 | **0.519** | 0.466 | 0.388 |

accuracy 最高的阈值（0.8）和 F1 最高的（0.5）**不是同一个** ——「按哪个指标调」本身就是决策。

**PR 曲线 / 不平衡**：ROC 的横轴 FPR 以 $FP+TN$ 为分母，负例一多就把误报稀释了。
1% 正例时 AUC 可能仍有 0.9，精确率却已经惨不忍睹。这时改看 **PR 曲线**（横轴 Recall、纵轴 Precision），
它只关心「被报为正例」的那部分，对少数类更诚实。ch08 的 KNN、ch09 的集成遇到不平衡数据都该配 PR-AUC。

**常见误区**：**别先挑指标再想业务** —— 垃圾邮件过滤里 FP（正常邮件进垃圾箱）代价远高于 FN，
该盯 Precision；疾病筛查反过来，该盯 Recall。**别把 `predict_proba` 的输出直接当决策**，
它还缺一个按业务定的阈值。**别在测试集上扫阈值** —— 阈值也是超参数，那样做就是 6.4 的泄漏。

**对应练习**：[第 3、7、8、11 题](../exercises/ch06_ex.py)（第 3 题扫 F1，第 7/8 题按代价挑阈值，第 11 题平衡准确率）

---

<a id="c06-04"></a>

### 6.4 数据泄漏与评估陷阱（Data Leakage and Evaluation Pitfalls）

**概念定义**：数据泄漏 = **模型在预测时本该拿不到的信息，提前进了训练或选择过程**。
ch10 管「预处理器在全量上 fit」；本节管**评估协议被破坏** —— 你没在测试集上训练，
却用测试集做了决定，效果一样。三段式铁律：

```
训练集 fit 模型 → 验证集挑超参 / 阈值 → 测试集只报一次，报完封存
```

**① 用测试集调参（胜者诅咒 / Winner's Curse）** —— 最隐蔽也最常见。
实测设计：240 个样本、60 列**纯高斯噪声**、标签也是随机硬币；40 个候选「超参」= 随机 5 列特征子集；
每个候选只用 100 个训练样本拟合一个最小二乘分类器。

- 错误做法：40 个候选全在测试集上打分，挑最高的那个**报它自己的测试分数**
- 正确做法：在 70 个验证样本上挑，测试集只用来报一次分
- 独立重复 30 轮（种子 1000~1029）：

| | 平均 test acc | 范围 |
|---|---|---|
| 用测试集挑 | **0.6157** | 0.529 ~ 0.686 |
| 用验证集挑 | **0.5143** | 0.371 ~ 0.614 |
| 虚高 | **+0.1014** | — |

真实水平本来就是 0.5（全是噪声）。**正确做法不是「分数更高」，是「分数可以信」**。
验证集那组波动更大（70 个样本太小，挑谁都带噪声）—— 这本身也说明：评估结论要给方差，别报孤零零一个数。

**② 重复样本跨集合**：80 条原始样本，复制其中 40 条凑成 120 行，按行随机 70/30 划分后，
测试集里 **47.2%** 的样本能在训练集找到逐元素完全相同的副本。
去重必须在划分**之前**做；有关联的数据要按实体 ID（用户、设备、时间窗）分组划分，别按行随机。

**③ 时间序列随机划分**：按时间排序的数据（日志、传感器、检索日志）随机打乱，
等于让模型用「未来」预测「过去」。要按时间切：前 80% 训练、后 20% 测试，
调参再用训练段末尾做验证。以图搜图项目（第 7 篇）里新图入库的漂移监控同理。

**④ 交叉验证时在全量上 fit**：K 折只是把「划分」重复 K 次，**每一折内部照样要先划分再 fit**。
`StandardScaler().fit_transform(X_all)` 然后 `cross_val_score` 是经典错法，
链回 [ch10 10.4](../../02_supervised/docs/ch10_feature_engineering.md#c10-04)。

**什么时候会翻车**（篇 README 要求的固定项）：

- 候选多、验证集小 → 挑出来的「最优」几乎必然掺着运气（本节的 40 候选 / 70 验证样本）
- 数据有重复、按用户或时间相关 → 随机划分必然泄漏，离线分数和线上差一大截
- 测试集被反复看过几次之后，它就已经变成验证集了；再要可信估计就得换一批新数据
- 类别极不平衡又只看 accuracy 或 ROC-AUC → 6.1 和 6.3 的坑叠加

**常见误区**：**「我又没在测试集上训练」不等于没泄漏**。
调超参、挑特征、定阈值、早停、看了一眼结果决定再改一版 —— 全都是把测试集的信息写进了模型选择。
测试集是**消耗品**，报完一次就该封存；要继续迭代，就再开一份新的。

**对应练习**：[第 9、10 题](../exercises/ch06_ex.py)（第 9 题亲手量化胜者诅咒，第 10 题算重复样本泄漏率）

> 和 C++ 的差异：C++ 里测试是「同一批输入反复跑，结果不变就对」，测试集无成本、可复用。
> ML 里**测试集会被用旧**：每看一次、按它改一次，它就少一分独立性。这是最反直觉的一条。

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| `assert(pred == label)`，对/错二值 | 四格混淆矩阵，四种错的代价不同 |
| 平均值代表整体表现 | 平均值会被多数类绑架，要分 P / R / F1 |
| 阈值写死 `> 0.5` | 阈值是按业务代价选出来的决策变量 |
| 损失越小越好 | 损失给优化器，指标给人，两者不必一致 |
| 测试集反复跑、结果稳定就行 | 测试集是消耗品，看过就污染 |

> **最容易踩的 3 个坑**：
> 1. 1% 正例上看 accuracy —— 0.990 的模型一个正例没抓到
> 2. 用测试集挑超参 / 阈值 —— 纯噪声上也能「考」出 0.616，虚高 +0.10
> 3. 精确率 ↔ 准确率、验证集 ↔ 测试集混用（[NOTATION 易混词](../../NOTATION.md)）

**一条判据带走**：报任何分数前先问三句 —— **它算的是哪一种错误？代价对称吗？这批数据模型之前见过吗？**

## 练习

本章练习统一在 [`ch06_ex.py`](../exercises/ch06_ex.py)：手写混淆矩阵与 P/R/F1、扫 F1 阈值、
ROC 点与 AUC、回归四指标、期望代价与最优阈值、平衡准确率，最后亲手量化胜者诅咒与重复样本泄漏，
共 11 题。文件**只用 numpy**，跑通所有 `assert` 即过关。

上一篇：第 5 章 误差来源与模型选择（待写，见 [SYLLABUS](../../SYLLABUS.md)）
下一篇：[第 7 章 线性模型](../../02_supervised/docs/ch07_linear_models.md)
