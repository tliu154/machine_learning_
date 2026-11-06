# 第 8 章 经典分类算法（Classical Classification Algorithms）

> 前置：第 7 章（逻辑回归的失效场景）、第 1 章 1.3（广播、布尔掩码、`argsort`）
> 对应练习：[`ch08_ex.py`](../exercises/ch08_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`02_supervised/`

**一句话**：ch07 的逻辑回归只能画一条超平面。本章四个算法从**四个完全不同的角度**
解决「线性分不开」：KNN 索性不建模、决策树沿坐标轴切、SVM 把数据搬去高维、朴素贝叶斯算概率。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [K 近邻（KNN）](#c08-01) · [懒惰学习（Lazy Learning）](#c08-01) · [距离度量（Distance Metric）](#c08-01) | 8.1 |
| [决策树（Decision Tree）](#c08-02) · [基尼不纯度（Gini Impurity）](#c08-02) · [信息增益（Information Gain）](#c08-02) · [最大深度（Max Depth）](#c08-02) | 8.2 |
| [支持向量机（SVM）](#c08-03) · [最大间隔（Maximum Margin）](#c08-03) · [核方法（Kernel Method）](#c08-03) · [RBF 核](#c08-03) | 8.3 |
| [朴素贝叶斯（Naive Bayes）](#c08-04) · [贝叶斯定理（Bayes' Theorem）](#c08-04) · [条件独立（Conditional Independence）](#c08-04) | 8.4 |
| [偏差—方差（Bias–Variance）](#c08-05) · [特征缩放（Feature Scaling）](#c08-05) | 8.5 |

### 全章共用的数据

```python
import numpy as np

rng = np.random.default_rng(42)
X = rng.uniform(-1, 1, (160, 2))
y = (X[:, 0] * X[:, 1] > 0).astype(int)   # XOR：一三象限为 1，二四象限为 0
X_tr, y_tr, X_va, y_va = X[:120], y[:120], X[120:], y[120:]
```

这是**线性模型的死穴**：任何直线都没法把对角的两块分到同一类。
后面还会用到三份小数据：带两个阈值的「树结构数据」、量纲差 $10^4$ 倍的「缩放数据」、
以及两类高斯簇（练习里现场造，和这里共用同一套生成器）。

### 先看结论：同一份 XOR 上，七个模型的实测准确率

sklearn 实跑，`random_state=42`，120 训练 / 40 验证。**这张表就是本章存在的理由**：

| 模型 | train | val | 为什么 |
|---|---|---|---|
| 逻辑回归（ch07） | 0.692 | **0.675** | 只能画一条直线 |
| 线性 SVM | 0.708 | **0.675** | 同上，只是换了个损失 |
| 朴素贝叶斯 | 0.667 | **0.625** | 两个特征强相关，独立性假设直接崩 |
| 决策树 `max_depth=3` | 0.783 | 0.800 | 矩形切得太粗 |
| 决策树 `max_depth=8` | **1.000** | 0.975 | 树够深就能拼出对角结构，但 train 已满分 |
| KNN `k=5` | 0.967 | **0.975** | 局部投票，天然不管全局边界形状 |
| RBF SVM `gamma=2` | 0.967 | **0.925** | 核把数据搬去高维，那里线性可分 |

**没有哪个算法「更好」，只有哪个假设和你的数据更配。** 下面逐个拆开看它们各自的假设。

---

<a id="c08-01"></a>

### 8.1 K 近邻（K-Nearest Neighbors）

**概念定义**：**它不训练**。所谓「模型」就是整个训练集本身（懒惰学习 / 基于实例的方法）。
预测时算新点到所有训练点的距离，取最近的 $K$ 个投票，多数决。
这是对「边界长什么样」最不加假设的算法 —— 边界由数据自己长出来。

**数学形式**：

$$d(x, x_i) = \sqrt{\sum_j (x_j - x_{ij})^2},\qquad
\hat{y} = \arg\max_c \sum_{i \in N_K(x)} \mathbb{1}[y_i = c]$$

第一式是欧氏距离「各维差的平方和再开方」，第二式是「最近的 K 个邻居里哪类票多」。
numpy：`np.sqrt(((X_tr - x) ** 2).sum(axis=1))`，`(n, 2) - (2,)` 会自动广播（见 np02）。

**最小代码**：

```python
def knn_predict(X_tr, y_tr, x, k=5):
    dist = np.sqrt(((np.asarray(X_tr) - x) ** 2).sum(axis=1))
    idx = np.argsort(dist)[:k]                 # 最近的 k 个下标
    return np.bincount(y_tr[idx].astype(int)).argmax()   # 票数最多的类
```

`np.bincount` 只能吃非负整数，所以标签要先 `.astype(int)`；平票时 `argmax` 取编号最小的类，
结果是确定的（docstring 里要写清这个约定）。

**常见误区**：**特征必须先标准化，且 $K$ 是最敏感的那个旋钮**。
量纲差 $10^4$ 倍时，距离几乎完全由大尺度那一维决定 —— 本章实测：
同一份数据、同一个 `k=5`，标准化前 val 只有 **0.600**，标准化后 **1.000**。
另外 $K=1$ 会把每个噪声点都记成边界（过拟合），$K$ 太大又把所有点投成多数类（欠拟合）。
高维下所有点距离都差不多，KNN 会失效（维度灾难）。

**对应练习**：[第 1~3 题](../exercises/ch08_ex.py)

> 和 C++ / 已有认知的差异：C++ 里要 `std::sort` 一个 `pair<double,int>` 数组再手写投票循环；
> numpy 里 `argsort` + `bincount` 两行。**整个「训练阶段」在这里根本不存在** ——
> 代价是每次预测都要扫全量训练数据 $O(nd)$，训练集一大就得上 KD 树或近似最近邻。

---

<a id="c08-02"></a>

### 8.2 决策树（Decision Tree）

**概念定义**：递归地在「某个特征的某个阈值」上切一刀，让切完的左右子集**更纯**，
直到子集全同类或到达 `max_depth`。最终决策边界是一堆**平行于坐标轴的矩形**。
它也是 ch09 集成方法的原料 —— 单棵树往往不准，但一堆树投票就很强。

**数学形式**：

$$G = 1 - \sum_c p_c^2,\qquad
H = -\sum_c p_c \log_2 p_c,\qquad
IG = G_{\text{parent}} - \frac{n_L}{n}G_L - \frac{n_R}{n}G_R$$

$G$ 是基尼不纯度（「随机抽两个样本类别不同的概率」，纯节点为 0、二分类各半为 0.5），
$H$ 是熵，$IG$ 是这次切分带来的**信息增益**：挑 $IG$ 最大的 $(j, t)$。
numpy：`p = np.bincount(y) / len(y); gini = 1 - np.sum(p**2)`。

**最小代码**（找最佳切分，递归建树在练习里）：

```python
def gini(y):
    y = np.asarray(y, dtype=int)
    p = np.bincount(y) / len(y)
    return 1 - np.sum(p ** 2)

def best_split(X, y):
    X, y = np.asarray(X, float), np.asarray(y, int)
    best = (0, float(X[:, 0].min()), -1.0)
    for j in range(X.shape[1]):
        for t in np.unique(X[:, j]):
            m = X[:, j] <= t
            if m.all() or not m.any():
                continue
            gain = gini(y) - (m.sum() * gini(y[m]) + (~m).sum() * gini(y[~m])) / len(y)
            if gain > best[2]:
                best = (j, float(t), float(gain))
    return best                      # (特征下标, 阈值, 增益)
```

阈值候选直接取该特征出现过的值，`np.unique` 兼做去重和排序。
建好的树用嵌套 dict 表示：`{"leaf": True, "value": c}` 或
`{"leaf": False, "j": j, "t": t, "left": ..., "right": ...}`。

**常见误区**：**不限制 `max_depth` 会一直切到每个叶子只剩一个样本，把噪声也背下来**。
本章实测（带 5% 标签噪声的树结构数据）：

| `max_depth` | train | val |
|---|---|---|
| 1 | 0.853 | 0.760 |
| 2 | 0.953 | 0.900 |
| 4 | 0.973 | 0.900 |
| 12 | **1.000** | 0.900 |

train 一路涨到满分，val 从深度 2 起纹丝不动 —— **这就是过拟合最直观的一条曲线**，
篇 README 点名要的 train/val 对比就在练习第 7 题里亲手画一遍。

**对应练习**：[第 4~8 题](../exercises/ch08_ex.py)

> 和 C++ / 已有认知的差异：C++ 里节点是 `struct Node { Node* left, *right; }`，
> 要管内存和空指针；Python 里嵌套 dict 就够了，读起来就是数据本身。
> 但递归深度默认上限 1000（基础教程 ch12 讲过），树太深会 `RecursionError` —— 
> 这也是 sklearn 用非递归实现的原因之一。

---

<a id="c08-03"></a>

### 8.3 支持向量机与核方法（SVM and Kernel Methods）

**概念定义**：线性可分时不满足于「分开」，而要找**间隔最大**的那条超平面；
最终边界只由离它最近的少数几个点（支持向量）决定。
线性分不开时用**核技巧**把样本映射到高维空间，在那里找超平面 —— 关键在于
**不用真的算出 $\phi(x)$，只要能算内积 $K(x, x') = \phi(x)^\top\phi(x')$ 就够了**。

**数学形式**：

$$\max \frac{2}{\lVert w \rVert},\qquad
K_{\text{RBF}}(x, x') = \exp\left(-\gamma \lVert x - x' \rVert^2\right),\qquad
f(x) = \sum_i \alpha_i y_i K(x_i, x) + b$$

第一式是「让两类之间的空隙尽量宽」，第二式是 RBF（高斯）核「距离越远相似度越按指数衰减」，
第三式是最终决策「所有支持向量按相似度加权投票」。$\gamma$ 控制单个点的影响半径。

**最小代码**（核矩阵，纯 numpy 广播）：

```python
def rbf_kernel(A, B, gamma=1.0):
    # (n,1,d) - (1,m,d) -> (n,m,d) -> 沿 d 求和 -> (n,m)
    d2 = ((np.asarray(A)[:, None, :] - np.asarray(B)[None, :, :]) ** 2).sum(axis=2)
    return np.exp(-gamma * d2)

K = rbf_kernel(X_tr, X_tr, gamma=2.0)
print(K.shape, np.diag(K)[:3])   # (120, 120)，对角线恒为 1（自己和自己距离 0）
```

这一行 `A[:, None, :] - B[None, :, :]` 是 np02 广播规则最漂亮的一次应用：
**成对距离矩阵不需要任何 for 循环**。sklearn 里对应 `SVC(kernel="rbf", gamma=2.0)`，
它在 XOR 上实测 val 0.925，而 `SVC(kernel="linear")` 只有 0.675。

**常见误区**：**SVM 对特征缩放和 $\gamma$ 极度敏感**。
$\gamma$ 太大时每个训练点自成一岛（train 高、val 崩），太小又退回线性边界；
距离尺度不统一时 RBF 核同样会被大尺度特征主导。用之前先标准化、再调 $\gamma$ 和 $C$。

**对应练习**：[第 9 题](../exercises/ch08_ex.py)

> 和 C++ / 已有认知的差异：手写核矩阵是三重循环 $O(n^2 d)$，且要小心下标；
> numpy 靠一个 `None` 插维度就把外层两重循环消掉了。
> 但 `(n, n)` 的核矩阵内存是平方增长 —— $n=10^5$ 时直接爆内存，
> 这是 SVM 在大数据上被树模型取代的根本原因。

---

<a id="c08-04"></a>

### 8.4 朴素贝叶斯（Naive Bayes）

**概念定义**：用贝叶斯定理算「给定特征，属于每一类的概率」，取最大的那类。
**「朴素」不是「简单」，而是一个很强的假设：给定类别后，各特征条件独立**。
明知不真，但它把联合概率拆成一堆一维概率的乘积，参数量从指数级降到线性级 ——
所以它是高维稀疏文本分类几十年不倒的基线。

**数学形式**：

$$P(c \mid x) \propto P(c)\prod_j P(x_j \mid c),\qquad
\log P(c \mid x) = \log P(c) + \sum_j \log \mathcal{N}(x_j; \mu_{jc}, \sigma_{jc}^2)$$

第一式是「类先验乘各特征的类条件概率」，第二式是高斯朴素贝叶斯取对数后的形式
（连乘改连加，**防概率下溢**）。高斯版的每个类只要存每维的均值、方差和一个先验。
numpy：`-0.5*np.log(2*np.pi*var) - (x - mu)**2/(2*var)`。

**最小代码**：

```python
def fit_gaussian_nb(X, y, eps=1e-9):
    X, y = np.asarray(X, float), np.asarray(y, int)
    classes = np.unique(y)
    return [(c, float(np.mean(y == c)), X[y == c].mean(axis=0),
             X[y == c].var(axis=0) + eps) for c in classes]

# 预测：对每类累加 log 先验 + 各维 log 高斯密度，取 argmax
def gaussian_nb_predict(model, X):
    X = np.asarray(X, float)
    scores = np.column_stack([
        np.log(prior) + (-0.5 * np.log(2 * np.pi * var)
                         - (X - mu) ** 2 / (2 * var)).sum(axis=1)
        for _, prior, mu, var in model
    ])
    return np.array([model[k][0] for k in scores.argmax(axis=1)])
```

方差加 `eps` 是防某一维在某个类里完全相同导致除零。

**常见误区**：**独立性假设不成立时，它不是「稍微差一点」，是彻底失效**。
本章实测：两类高斯簇上 val **1.000**，同一套代码搬到 XOR 上只有 **0.625**（接近瞎猜）——
因为 XOR 的标签由 $x_0 \times x_1$ 决定，两维**完全不独立**。
把「朴素」理解成「简单好用」是最常见的误读。

**对应练习**：[第 10、11 题](../exercises/ch08_ex.py)

> 和 C++ / 已有认知的差异：`double` 连乘几十个小于 1 的概率很快下溢成 0；
> 这里统一在对数域做加法。这种「把乘法搬到 log 域」的手法，
> 在 ch18 的 LLM 里算 token 联合概率时会原样再出现一次。

---

<a id="c08-05"></a>

### 8.5 算法对比与适用场景（Comparison and When to Use）

**概念定义**：上面四个算法的差别，本质是**各自对数据做了什么假设**。
选模型不是挑「准确率最高的」，是挑「假设最不可能被你的数据违背的」。

| | KNN | 决策树 | RBF SVM | 朴素贝叶斯 | 逻辑回归（ch07） |
|---|---|---|---|---|---|
| 假设 | 近邻同类 | 边界轴平行 | 高维线性可分 | 特征条件独立 | 对数几率线性 |
| 训练 | **无** | 递归切分 | 凸优化 | 统计数而已 | 梯度下降 |
| 预测成本 | $O(nd)$ 最慢 | $O(\text{depth})$ 快 | $O(\#SV \cdot d)$ | $O(d)$ 最快 | $O(d)$ |
| 必须缩放 | **是** | 否 | **是** | 否 | 建议 |
| 非线性 | 天然支持 | 靠深度 | 靠核 | 不支持 | 不支持 |
| 可解释性 | 低（举邻居） | **高（能画成规则）** | 低 | 中（看均值） | 高（看权重） |
| 主要失效 | 高维、大数据 | 过拟合、边界斜着 | 大数据、$\gamma$ 敏感 | 特征相关 | 线性不可分 |

**最小代码**（sklearn 三行对照，需要 `pip install scikit-learn`；**本章练习不依赖它**）：

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

for model in (KNeighborsClassifier(n_neighbors=5),
              DecisionTreeClassifier(max_depth=4, random_state=42),
              SVC(kernel="rbf", gamma=2.0),
              GaussianNB()):
    model.fit(X_tr, y_tr)
    print(type(model).__name__, model.score(X_va, y_va))
```

**什么时候会翻车**（篇 README 要求的固定项）：

- **KNN**：维度上去后「最近」和「最远」差别很小，距离失去意义；训练集 $n$ 大时预测极慢
- **决策树**：斜着的真实边界要切成大量锯齿才能近似；单棵树对训练集的微小扰动很敏感
  （这正是 ch09 用 Bagging 解决的问题）
- **RBF SVM**：核矩阵 $O(n^2)$ 内存；$\gamma$ / $C$ 没调好时表现可以从 0.95 掉到 0.5
- **朴素贝叶斯**：特征相关（如图像相邻像素、XOR）时假设直接崩；但它训练极快、
  高维稀疏文本上依然是最靠谱的基线

> **工程上的顺序**：先用逻辑回归跑一条基线（ch07），再用树集成拿性能（ch09），
> 别一上来就上深度学习。**基线不是为了赢，是为了知道后面每一分提升值不值。**

**常见误区**：**别拿训练集准确率选模型**。本章决策树深度 12 时 train 1.000、val 0.900，
按 train 挑就会选到最过拟合的那个。划分验证集、只看 val，是 ch05 / ch06 的主题。

**对应练习**：[第 7、8 题](../exercises/ch08_ex.py)（自测里用不同 `max_depth` 跑 train/val 曲线对比）

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| `struct Node` + 指针递归 | 嵌套 dict 表示树，叶/内部节点靠 `leaf` 字段区分 |
| `std::sort` + 手写投票循环 | `argsort` + `bincount` |
| 三重循环算成对距离 | `A[:, None, :] - B[None, :, :]` 一次广播 |
| 概率连乘（易下溢） | 取 log 改成连加 |
| 「模型 = 训练出来的参数」 | KNN 根本没有训练阶段，训练集本身就是模型 |
| 编译期决定数据结构 | 树的形状完全由数据运行时决定 |

> **最容易踩的 3 个坑**：
> 1. KNN / RBF SVM **不标准化就直接用** —— 距离被大尺度特征垄断（实测 0.600 → 1.000）
> 2. 决策树不设 `max_depth`，train 满分、val 不动，还以为模型很强
> 3. 把朴素贝叶斯的「朴素」当成卖点，在特征强相关的数据上用它

## 练习

本章练习统一在 [`ch08_ex.py`](../exercises/ch08_ex.py)：从距离与 KNN 投票、
基尼/熵/最佳切分、手写递归决策树与 train/val 深度曲线，到 RBF 核矩阵和高斯朴素贝叶斯，
共 11 题。**全部只用 numpy**，跑通所有 `assert` 即过关。

上一篇：[第 7 章 线性模型](ch07_linear_models.md)
下一篇：第 9 章 集成方法（待写，见 [SYLLABUS](../../SYLLABUS.md)）
