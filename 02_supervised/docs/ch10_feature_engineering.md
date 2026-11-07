# 第 10 章 特征工程（Feature Engineering）

> 前置：第 7 章（线性模型 / 多项式特征）、第 8 章（KNN、SVM 对缩放敏感）、第 4 章（数据泄漏伏笔）
> 对应练习：[`ch10_ex.py`](../exercises/ch10_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`02_supervised/`

**一句话**：模型改不动的时候，改数据往往更有效 —— 但「从数据里学出来的量」全都是陷阱，
只要算它的时候偷看了验证集，分数就会虚高。这章把 ch04 埋的伏笔兑现，并**量化**它。

> 第 3 篇到此收口：ch07 线性模型 → ch08 经典算法 → ch09 集成 → ch10 怎么把数据喂给它们。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [特征缩放（Feature Scaling）](#c10-01) · [标准化（Standardization）](#c10-01) · [归一化 / Min-Max](#c10-01) · [fit / transform 分离](#c10-01) | 10.1 |
| [缺失值（Missing Values）](#c10-02) · [填充（Imputation）](#c10-02) · [缺失指示列（Missing Indicator）](#c10-02) · [异常值（Outlier）](#c10-02) · [IQR 裁剪](#c10-02) | 10.2 |
| [类别编码（Categorical Encoding）](#c10-03) · [独热编码（One-Hot）](#c10-03) · [序数编码（Ordinal Encoding）](#c10-03) · [目标编码（Target Encoding）](#c10-03) | 10.3 |
| [特征选择（Feature Selection）](#c10-04) · [特征构造（Feature Construction）](#c10-04) · [交互项（Interaction）](#c10-04) · [数据增强（Data Augmentation）](#c10-04) | 10.4 |

### 先看结论：四种「学出来的量」，泄漏程度差两个数量级

全部实跑（numpy 手写 + 固定种子）。每行都是同一个对比：
**错误做法 = 在全量数据上 fit，正确做法 = 只在训练集上 fit**，模型与数据完全相同。

| 从数据里学出来的量 | 错误 val | 正确 val | 虚高 |
|---|---|---|---|
| 标准化的均值 / 标准差（线性数据） | 0.820 | 0.820 | **+0.000** |
| 缺失值填充的均值 | 0.850 | 0.840 | +0.010 |
| 目标编码（300 个类别的高基数特征） | 0.787 | 0.527 | **+0.260** |
| 特征选择（200 个纯噪声特征里挑 top-20） | 0.733 | 0.433 | **+0.300** |

**规律**：越**靠近标签**的统计量，泄漏越致命。缩放和填充只学了特征的边际分布，
跟标签无关，所以泄漏弱；目标编码和特征选择直接把验证集标签用进了统计量，分数直接虚高 0.3。

注意第一行那个 `+0.000` —— **不代表先缩放再划分是对的**，只代表 i.i.d. 数据上运气好。
线上分布一漂移（比如新设备传感器量程变了），全量 fit 混入的测试集统计量就会实打实地坑你。

---

<a id="c10-01"></a>

### 10.1 缩放与归一化（Feature Scaling and Normalization）

**概念定义**：把不同量纲的特征拉到同一尺度。
**标准化**（Standardization）减均值除标准差，结果均值 0、方差 1，不限制取值区间；
**Min-Max 归一化**压到 $[0,1]$，对异常值敏感；
**Robust Scaling** 用中位数和 IQR，抗离群点。

**数学形式**：

$$z_j = \frac{x_j - \mu_j}{\sigma_j},\qquad
x'_j = \frac{x_j - \min_j}{\max_j - \min_j}$$

第一式是「离均值几个标准差」，第二式是「在这个特征的取值范围里排第几」。
numpy：`mu, sigma = X_tr.mean(0), X_tr.std(0)`，然后 `(X - mu) / sigma`；
标准差为 0 的列要按 1 处理，否则除零。

**最小代码**（关键是把 `fit` 和 `apply` 拆成两个函数）：

```python
def fit_standardizer(X_tr):
    X_tr = np.asarray(X_tr, float)
    sigma = X_tr.std(axis=0)
    return X_tr.mean(axis=0), np.where(sigma == 0, 1.0, sigma)

def apply_standardizer(X, stats):
    mu, sigma = stats
    return (np.asarray(X, float) - mu) / sigma

stats = fit_standardizer(X_tr)          # 只看训练集
X_tr_s, X_va_s = apply_standardizer(X_tr, stats), apply_standardizer(X_va, stats)
```

**为什么必须拆开**：`fit` 产出的是「从数据里学出来的量」，`apply` 只是套用。
合并成一个 `standardize(X)` 就会忍不住对全量调用一次 —— 这正是 ch04 说的数据泄漏。
sklearn 的 `StandardScaler().fit_transform(X_tr)` / `.transform(X_va)` 就是这套约定。

**不是所有模型都要缩放**：

| 需要 | 不需要 |
|---|---|
| KNN、RBF SVM（距离主导）、梯度下降、带正则的线性模型、PCA、神经网络 | 决策树 / 随机森林 / GBDT（只比单个特征内的大小） |

ch08 实测过：量纲差 $10^4$ 倍时 KNN val 只有 **0.533**，标准化后 **0.933**。

**常见误区**：**别对全量数据 `fit`，也别对验证集单独 `fit`**。
后者更隐蔽 —— 验证集自己算自己的均值，等于每个样本都按「这批验证数据的分布」重新标度，
线上来一条样本时根本算不出这个均值。

**对应练习**：[第 1、2 题](../exercises/ch10_ex.py)

> 和 C++ / 已有认知的差异：C++ 里你会写一个 `normalize(double* a, int n)` 就地改数组，
> 没有「先学统计量、再复用」的概念。Python 数据栈把**有状态**的预处理器当成一等对象，
> `fit` 学参数、`transform` 用参数 —— 这个区分是本章所有正确做法的地基。

---

<a id="c10-02"></a>

### 10.2 缺失值与异常值（Missing Values and Outliers）

**概念定义**：`np.nan` 不是 0，也不是「没信息」。
常见做法是**均值 / 中位数填充 + 加一列缺失指示**：
填充让模型还能算，指示列把「这里本来是缺的」这个信息保留下来
（缺失本身常常有信号，比如「没填收入」和「收入 0」是两回事）。
异常值用 IQR 边界**裁剪（winsorize）**而不是删除，避免白白丢样本。

**数学形式**：

$$\mathrm{IQR} = Q_3 - Q_1,\qquad
\text{下界} = Q_1 - 1.5\,\mathrm{IQR},\quad \text{上界} = Q_3 + 1.5\,\mathrm{IQR}$$

「把超出 1.5 倍四分位距的值夹到边界上」。
numpy：`lo, hi = np.quantile(X_tr, [0.25, 0.75], axis=0)` → `np.clip(X, lo_k, hi_k)`。
填充均值用 `np.nanmean(X_tr, axis=0)`，整列都是 nan 时兜底填 0。

**最小代码**：

```python
def fit_imputer(X_tr):
    X_tr = np.asarray(X_tr, float)
    mu = np.nanmean(X_tr, axis=0)
    return np.nan_to_num(mu, nan=0.0)      # 整列缺失 -> 0

def apply_imputer(X, means):
    X = np.asarray(X, float).copy()
    nan = np.isnan(X)
    X[nan] = np.take(means, np.where(nan)[1])
    return X

def missing_indicator(X):
    return np.isnan(np.asarray(X, float)).astype(float)
```

`np.take(means, 列下标)` 把每个 nan 换成它所在列的均值，一步完成、不用循环。

**常见误区**：**填充值、IQR 边界同样是「学出来的量」，只能在训练集上 fit**。
本章实测全量均值填充 → 0.850，训练集均值 → 0.840，虚高 +0.010。
数字小，但它是系统性的、方向永远对你有利 —— 这正是它难被发现的原因。
另外 `np.nan` 直接喂给 sklearn 大多数 estimator 会直接抛错，别指望它自动跳过。

**对应练习**：[第 3~6 题](../exercises/ch10_ex.py)

---

<a id="c10-03"></a>

### 10.3 类别编码（Categorical Encoding）

**概念定义**：模型只吃数字，类别特征得先变成数。
**序数编码**给每个类别一个整数（只适用于**真有顺序**的：低/中/高）；
**独热编码（One-Hot）** 把 $K$ 个类别展开成 $K$ 个 0/1 列（无顺序，线性模型的默认选择）；
**目标编码**用「该类别样本的平均标签」当数值，专门对付 $K$ 很大时 one-hot 炸出上千列的问题。

**数学形式**：

$$\text{one-hot}(c) = e_c \in \lbrace 0,1 \rbrace^K,\qquad
\hat{x}_c = \mathrm{mean}(y \mid \text{cat}=c)$$

第一式是「只有第 c 位是 1」，第二式是「这个类别历史上正例的比例」。
numpy：`np.eye(K)[codes]`；目标编码按类别分组求 `y.mean()`，未见类别填全局先验。

**最小代码**：

```python
def one_hot(cats):
    cats = np.asarray(cats)
    classes, codes = np.unique(cats, return_inverse=True)
    return np.eye(len(classes))[codes]

def target_encode(cat_fit, y_fit, cat_apply, default=None):
    cat_fit, y_fit = np.asarray(cat_fit), np.asarray(y_fit, float)
    if default is None:
        default = float(y_fit.mean())
    means = {g: y_fit[cat_fit == g].mean() for g in np.unique(cat_fit)}
    return np.array([means.get(g, default) for g in np.asarray(cat_apply)], dtype=float)
```

注意 `target_encode` 的签名里 **`cat_fit`/`y_fit` 与 `cat_apply` 是分开的** ——
这个接口本身就在逼你把「算统计量用的数据」和「应用的数据」分开。

**常见误区**：**目标编码是泄漏重灾区**。它直接把标签统计写进特征，
只要算均值时用了验证集标签，验证分数就会虚高。本章实测 300 个类别、
每类平均只有 1 个样本时：全量算编码 **0.787**，只用训练集算 **0.527**（≈瞎猜），差 **+0.260**。
原因很直白：类别基数越高，均值越接近「这条样本自己的标签」，等于把答案抄进特征。
正确做法：只用训练集算 + 对未见类别填全局先验 + 平滑 / out-of-fold 编码。
另一个坑：给无顺序的类别（红/绿/蓝）做序数编码，等于凭空强加 `红 < 绿 < 蓝`，
线性模型和树都会被带偏。

**对应练习**：[第 7、8 题](../exercises/ch10_ex.py)

---

<a id="c10-04"></a>

### 10.4 特征选择与构造（Feature Selection and Construction）

**概念定义**：**选择**是从 $d$ 列里挑出有用的（去掉噪声、降维、省算力），
**构造**是造新列（多项式、交互项、分箱、时间特征）。
ch07 讲过：把 $x^2$ 当新特征喂进去，线性模型照样能拟合曲线 —— 这就是构造的价值，
**「线性」指的是对参数线性，不是对原始特征线性**。

**数学形式**：

$$|r_j| = \frac{\left|\sum_i (x_{ij}-\bar{x}_j)(y_i-\bar y)\right|}
{\sqrt{\sum_i (x_{ij}-\bar{x}_j)^2}\,\sqrt{\sum_i (y_i-\bar y)^2}},\qquad
\text{交互项} = x_p \cdot x_q$$

第一式是「第 j 列与标签的绝对相关系数」，挑最大的 $k$ 列；
第二式补上「两个特征共同起作用」的情形（比如「温度高 **且** 湿度大」才报警）。
numpy：`np.abs(((X-X.mean(0)) * (y-y.mean())[:,None]).sum(0) / (...))`。

**最小代码**（选择 + 交互项）：

```python
def corr_scores(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    Xc, yc = X - X.mean(0), y - y.mean()
    denom = np.sqrt((Xc ** 2).sum(0)) * np.sqrt((yc ** 2).sum()) + 1e-12
    return np.abs((Xc * yc[:, None]).sum(0) / denom)

def add_interactions(X):
    X = np.asarray(X, float)
    d = X.shape[1]
    return np.column_stack([X[:, i] * X[:, j]
                            for i in range(d) for j in range(i + 1, d)])
```

**常见误区**：**特征选择是泄漏之王，而且数据可以全是噪声**。
本章实测：120 个样本、200 列**纯随机噪声**、标签也随机，
在**全量**（含验证集标签）上挑 top-20 列 → val **0.733**；
只在训练集上挑 → val **0.433**。虚高 **+0.300**，而真实信号是 0。
机制：在全量上挑，等于让验证集自己挑出「碰巧和自己标签相关」的那几列噪声。
**选择必须放进 Pipeline，只在训练集 fit；要评估就用交叉验证的 out-of-fold 选择。**

**数据增强**同理但方向相反：翻转/裁剪/加噪声是**只在训练集上造样本**，
它不产生新信息，只是把「模型该对什么不变」这个先验注入进去。
对验证集做增强等于自己改考卷，而且会重复计分。

**最小代码**（sklearn 三行对照，需要 `pip install scikit-learn`；**本章练习不依赖它**）：

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = make_pipeline(SimpleImputer(), StandardScaler(), LogisticRegression())
pipe.fit(X_tr, y_tr)              # 每一步只在 X_tr 上 fit
print(pipe.score(X_va, y_va))     # transform 时自动复用训练集的统计量
```

`Pipeline` 存在的意义不是少写几行，是**让你没法手滑把 `fit` 放到全量数据上**。

**什么时候会翻车**（篇 README 要求的固定项）：

- 树模型不需要缩放，但高基数 one-hot 会炸出极稀疏矩阵，反而更难切分
- 线性模型怕未缩放（收敛慢）、怕共线（ch07 的 `lstsq` 会不稳）、怕目标编码泄漏
- **测试集分布漂移时，全量 fit 的「+0.000」会变成实打实的负分** ——
  这是缩放泄漏最阴的地方：离线看不出来，上线才炸
- 特征构造出的列也要参与同样的 fit 边界；分箱的边界点同样是学出来的量

**常见误区**：**别把「特征工程」理解成「越多特征越好」**。
加 200 列噪声 + 在全量上挑 20 列，能拿到 0.733 的漂亮分数，然后线上原形毕露。
判断标准只有一条：**这个统计量，能不能在只见到训练样本时算出来？**

**对应练习**：[第 9~11 题](../exercises/ch10_ex.py)（第 11 题亲手量化泄漏）

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| `normalize()` 就地改数组 | `fit` 学统计量 / `apply` 复用，预处理器是**有状态对象** |
| 缺失值当 0 处理 | `nanmean` 填充 + 缺失指示列保留「缺过」这个信息 |
| `enum` 直接当整数 | one-hot（无序）/ 序数（有序）/ 目标编码（高基数，但要防泄漏） |
| 手写循环算每列相关 | 广播一次算完 `(n,d)` 的相关向量 |
| 全局常量写死 | 凡是「从数据里学出来的量」都只在训练集 fit |

> **最容易踩的 3 个坑**：
> 1. 先 `fit_transform(全量)` 再划分 —— 分数看不出差别不代表没错
> 2. 目标编码 / 特征选择用了验证集标签 —— 实测虚高 **0.26 / 0.30**，最致命
> 3. 给验证集单独 fit 一套统计量 —— 线上单条样本时根本复现不出来

**一条判据带走**：把预处理写成 `fit(train) → apply(any)` 两段。
只要某个数字是「看数据算出来的」，就问一句 —— **它见过验证集吗？**

## 练习

本章练习统一在 [`ch10_ex.py`](../exercises/ch10_ex.py)：从 `fit/apply` 标准化、
缺失填充与指示列、IQR 裁剪、one-hot 与目标编码，到相关系数、交互项，
最后是**亲手量化特征选择泄漏**的第 11 题。文件顶部内置一个极简 `lstsq` 评估器，
保证本文件独立运行；**全部只用 numpy**，跑通所有 `assert` 即过关。

上一篇：[第 9 章 集成方法](ch09_ensemble.md)
下一篇：第 11 章 聚类（待写，见 [SYLLABUS](../../SYLLABUS.md)）
