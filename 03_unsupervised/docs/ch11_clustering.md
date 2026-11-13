# 第 11 章 聚类（Clustering）

> 前置：[第 2 章 2.1](../../00_foundations/docs/ch02_math_foundations.md#c02-01)（向量与距离）、
> [ch06 评估指标](../../01_ml_framework/docs/ch06_evaluation_metrics.md)、
> [ch10 特征缩放](../../02_supervised/docs/ch10_feature_engineering.md)
> 对应练习：[`ch11_ex.py`](../exercises/ch11_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`03_unsupervised/`

**一句话**：分类是「照着标签学边界」，聚类是**没有标签，只能靠「长得像不像」自己分组**。
所以本章真正的难点不是算法，而是**「什么叫分得好」这件事没有标准答案** ——
指标全是启发式，本章会用一组实测让你亲眼看到指标把错结果夸成更好的。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [K-means](#c11-01) · [质心（Centroid）](#c11-01) · [惯性 / 簇内平方和（Inertia）](#c11-01) · [局部最优（Local Optimum）](#c11-01) | 11.1 |
| [层次聚类（Hierarchical Clustering）](#c11-02) · [树状图（Dendrogram）](#c11-02) · [连接方式（Linkage）](#c11-02) · [链式效应（Chaining）](#c11-02) | 11.2 |
| [DBSCAN](#c11-03) · [核心点 / 边界点 / 噪声（Core / Border / Noise）](#c11-03) · [ε-邻域](#c11-03) · [密度可达](#c11-03) | 11.3 |
| [轮廓系数（Silhouette Coefficient）](#c11-04) · [肘部法（Elbow Method）](#c11-04) · [调整兰德指数（ARI）](#c11-04) · [簇数选择](#c11-04) | 11.4 |

### 全章共用的三份数据

```python
import numpy as np

rng = np.random.default_rng(42)
# ① 三团高斯簇：K-means 的主场
centers = np.array([[-3., -3.], [0., 3.], [3., -3.]])
y_blobs = np.repeat(np.arange(3), 50)
X_blobs = centers[y_blobs] + rng.normal(0, 0.6, (150, 2))

# ② 两个同心环：凸簇假设的死穴
def make_rings(n_per=150, seed=42):
    r = np.random.default_rng(seed)
    t1 = np.linspace(0, 2*np.pi, n_per, endpoint=False) + r.normal(0, 0.01, n_per)
    t2 = np.linspace(0, 2*np.pi, n_per, endpoint=False) + r.normal(0, 0.01, n_per)
    inner = np.column_stack([np.cos(t1), np.sin(t1)]) + r.normal(0, 0.06, (n_per, 2))
    outer = 2.5 * np.column_stack([np.cos(t2), np.sin(t2)]) + r.normal(0, 0.06, (n_per, 2))
    return np.vstack([inner, outer]), np.r_[np.zeros(n_per, int), np.ones(n_per, int)]

X_rings, y_rings = make_rings()

# ③ 量纲差 10^3 倍：真实簇由 y 决定，x 只是 ±500 的噪声
r2 = np.random.default_rng(7)
y_scale = np.r_[np.zeros(60, int), np.ones(60, int)]
X_scale = np.column_stack([r2.normal(0, 500, 120),
                           np.where(y_scale == 0, -2., 2.) + r2.normal(0, 0.3, 120)])
```

> ② 用**均匀角度 + 小扰动**而不是 `uniform(0, 2π)` 撒点：随机角度会留下大空隙，
> 密度算法会把一个环切成十几段。造数据的方式本身就会改变结论，这是无监督的第一课。

### 先看结论：同一批数据上的实测

手写实现与 sklearn 结果逐一对照过（标注 `pip install scikit-learn`，**本章练习不依赖它**）。
「对齐准确率」是为了演示，用真值做标签排列对齐后算的；**真实项目里你没有这个真值**。

| 数据 | 算法 | 对齐准确率 | ARI | 轮廓系数 |
|---|---|---|---|---|
| 三团高斯簇 | K-means `K=3` | **1.0000** | — | 0.8405 |
| 三团高斯簇 | 层次聚类 `single` | 1.0000 | — | — |
| 两同心环 | K-means `K=2` | 0.5100 | **−0.0030** | **0.3280** |
| 两同心环 | DBSCAN `eps=0.5` | **1.0000** | **1.0000** | 0.1574 |

**这张表里藏着本章最重要的一句话**：环形数据上 K-means 分得跟瞎猜一样（ARI ≈ 0），
可轮廓系数却给它 **0.3280**，比 DBSCAN 那个完全正确的 **0.1574** 高出一倍。
**无监督指标只能排除明显坏的结果，不能证明一个结果是对的。**

---

<a id="c11-01"></a>
### 11.1 K-means（K-Means Clustering）

**概念定义**：先猜 $K$ 个**质心**（簇中心），然后反复做两步直到不动：
① 每个点归到最近的质心；② 把质心挪到它那一堆点的平均值。
它优化的目标是**簇内平方和**（inertia）—— 本质上是「让每一堆尽量紧」。

**数学形式**：

$$J = \sum_{i=1}^{n}\left\| x_i - \mu_{c_i}\right\|^2,\qquad
c_i = \arg\min_j \|x_i - \mu_j\|^2,\qquad
\mu_j = \frac{1}{|C_j|}\sum_{i \in C_j} x_i$$

第一式是「所有点到自己质心的距离平方和」，后两式就是那两步。
**两步各自都不会让 $J$ 变大**，所以 $J$ 单调下降、必然收敛 —— 但只保证收敛到**局部**最优。

**最小代码**（一轮迭代，数据现场造）：

```python
def assign(X, C):
    d2 = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)   # (n, K)
    return d2.argmin(axis=1), float(d2.min(axis=1).sum())      # labels, inertia

def kmeans_once(X, C):
    labels, J = assign(X, C)
    newC = C.copy()
    for j in range(len(C)):
        if np.any(labels == j):                # 空簇：保持旧质心，别求 mean(空)
            newC[j] = X[labels == j].mean(axis=0)
    return newC, labels, J
```

在三团高斯簇上，从每类各取一点初始化：$J$ 从 `190.0230` 两步降到 `93.0361`，
质心停在 $(-3.023,-3.037)$、$(0.005,2.982)$、$(2.984,-3.059)$，对齐准确率 `1.0000`；
sklearn `KMeans(3, n_init=10, random_state=42).inertia_` 同样是 `93.0361`。

**常见误区**：**初始化不是小事**。只跑一次（`n_init=1`）、随机取 3 个起点重复 20 次，
$J$ 落在 `93.0361 ~ 1217.6673`（均值 `451.3840`），其中 **7/20 次**陷进明显更差的解，
最差那次对齐准确率只有 `0.5200`。**永远多跑几次取 $J$ 最小的**，这就是 `n_init` 的意义。
另外 **K-means 假设簇是凸的、大小相近的**：两同心环上它只会沿 $x$ 轴把两个环一起切成左右两半
（质心 $(-1.158,-0.017)$、$(1.078,0.010)$），ARI `-0.0030`。

**对应练习**：[第 1~5 题](../exercises/ch11_ex.py)（第 4 题即「手工迭代一轮验证质心更新」）

> 和 C++ 的差异：C++ 里这是双重循环累加距离；numpy 用 `(n,1,d) - (1,K,d)` 一次广播出
> $(n,K)$ 距离矩阵。代价是 $O(nK)$ 内存，簇多、点多了会先炸内存而不是先变慢。
> 空簇在 C++ 里是 `sum/count` 除零崩溃，这里必须显式 `if` 兜住。

**缩放是硬前提**（呼应 [ch10](../../02_supervised/docs/ch10_feature_engineering.md)）：
数据 ③ 里 $x$ 的量纲比 $y$ 大 $10^3$ 倍，缩放前 K-means 的簇心在 $x=\pm 400$ 附近、
$y$ 几乎没分开，准确率 `0.5000`；`StandardScaler` 之后簇心落在 $y=\pm 0.991$，准确率 `1.0000`。
**距离被大尺度特征垄断** —— 和 [ch08 KNN](../../02_supervised/docs/ch08_classical_classifiers.md#c08-01) 的坑是同一个。

---

<a id="c11-02"></a>
### 11.2 层次聚类（Hierarchical Clustering）

**概念定义**：不预设 $K$，而是**自底向上**：一开始每个点自己一簇，
每轮把「最近」的两簇合并，直到剩 $K$ 簇（或全部并成一棵树）。
合并过程画出来就是**树状图**，想切几簇就在树上横着切一刀。

**数学形式**：关键是「两簇之间有多远」，三种**连接方式（Linkage）**给出完全不同的结果：

$$d_{\text{single}}(A,B)=\min_{a\in A,b\in B}\|a-b\|,\quad
d_{\text{complete}}=\max_{a\in A,b\in B}\|a-b\|,\quad
d_{\text{average}}=\frac{1}{|A||B|}\sum_{a\in A,b\in B}\|a-b\|$$

「single 看两簇最近的一对点，complete 看最远的一对，average 看全部点对的平均值」。
**这不是同一个算法的三个参数，是三种对「簇」的定义。**

**最小代码**（手写合并，`n` 小才跑得动）：

```python
def agglomerative(X, k, method="single"):
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    clusters = [[i] for i in range(len(X))]
    while len(clusters) > k:
        best = (np.inf, -1, -1)
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                sub = D[np.ix_(clusters[a], clusters[b])]
                d = {"single": sub.min, "complete": sub.max, "average": sub.mean}[method]()
                if d < best[0]:
                    best = (d, a, b)
        _, a, b = best
        clusters[a] += clusters[b]
        clusters.pop(b)
    labels = np.empty(len(X), int)
    for j, cl in enumerate(clusters):
        labels[cl] = j
    return labels
```

在环形数据取 80 点子集上，手写与 sklearn `AgglomerativeClustering` 三种 linkage **完全一致**：

| linkage | 对齐准确率 | 最后一次合并距离 | 为什么 |
|---|---|---|---|
| `single` | **1.0000** | 0.2920 | 只要环上相邻点够近，就能顺着环串起来 |
| `complete` | 0.6750 | 2.7421 | 要求整簇都近，倾向紧凑球簇，环被切断 |
| `average` | 0.6625 | 1.7486 | 介于两者之间 |

**常见误区**：**single 的链式效应是双刃剑** —— 它能找出环，也会把两团本来分开的簇
用中间几个噪声点「搭桥」连成一串。另外这套写法要存 $O(n^2)$ 距离矩阵、跑 $O(n^3)$，
几千个点就别用了；层次聚类的主场是**小数据 + 想看层级结构**（比如分类体系、基因谱系）。

**对应练习**：[第 6、7 题](../exercises/ch11_ex.py)

> 和 C++ 的差异：C++ 里你会用并查集 + 优先队列把合并做到 $O(n^2\log n)$；
> 上面这份教学实现故意用最直白的「每轮扫全部簇对」，因为重点在 linkage 的定义，不在性能。

---

<a id="c11-03"></a>
### 11.3 DBSCAN（Density-Based Spatial Clustering of Applications with Noise）

**概念定义**：**簇 = 密度连通的一片区域**，形状随意。它把点分三类：

- **核心点**：半径 $\varepsilon$ 内至少有 `min_samples` 个邻居
- **边界点**：自己不够核心，但落在某个核心点的 $\varepsilon$ 邻域里
- **噪声点**：都不是，标签记 `-1`

**数学形式**：

$$N_\varepsilon(x) = \lbrace x' \in X \mid \|x - x'\| \le \varepsilon \rbrace,\qquad
\text{核心点} \iff |N_\varepsilon(x)| \ge \text{min\_samples}$$

「$N_\varepsilon$ 是以 $x$ 为圆心、$\varepsilon$ 为半径画个圈圈到的所有点」。
从一个核心点出发，沿密度可达关系不断扩张，连通的一整片就是一个簇。

**最小代码**（BFS 扩张，不用递归）：

```python
def dbscan(X, eps, min_samples=5):
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    nb = [np.flatnonzero(D[i] <= eps) for i in range(len(X))]
    labels = np.full(len(X), -2, int)         # -2 未访问，-1 噪声
    cid = 0
    for i in range(len(X)):
        if labels[i] != -2:
            continue
        if len(nb[i]) < min_samples:
            labels[i] = -1                    # 暂时标噪声，可能被后面收编
            continue
        labels[i] = cid
        queue, q = list(nb[i]), 0
        while q < len(queue):
            j = queue[q]; q += 1
            if labels[j] == -1:
                labels[j] = cid               # 噪声 → 边界点
            if labels[j] != -2:
                continue
            labels[j] = cid
            if len(nb[j]) >= min_samples:
                queue.extend(nb[j])           # 只有核心点才继续扩张
        cid += 1
    return labels
```

环形数据上 `eps=0.5, min_samples=5` 得到 **2 簇、0 个噪声点、ARI 1.0000**，
手写标签与 sklearn `DBSCAN` **逐个完全一致**。K-means 在这里彻底失效的同一份数据，DBSCAN 满分。

**常见误区**：**$\varepsilon$ 是全局的，密度不均就无解**。环形数据上扫一遍 `eps`：

| `eps` | 簇数 | 噪声点 | ARI（非噪声） |
|---|---|---|---|
| 0.05 | 2 | **290 / 300** | 0.0000 |
| 0.10 | 15 | 202 | 0.0000 |
| 0.20 | 6 | 122 | 0.9505 |
| 0.30 | 3 | 0 | 0.9434 |
| **0.50** | **2** | **0** | **1.0000** |
| 1.00 | 2 | 0 | 1.0000 |
| 1.60 | 1 | 0 | — |

太小几乎全是噪声、太大把两个环并成一团，中间只有一个窄窗口是对的。
**DBSCAN 不是「不用调 K」就省事了，它把 K 换成了更难调的 $\varepsilon$**，
而且高维下距离本身失效（[ch08](../../02_supervised/docs/ch08_classical_classifiers.md#c08-01) 讲过），
所以以图搜图里通常先降维（第 12 章）再聚类。

**对应练习**：[第 8、9 题](../exercises/ch11_ex.py)（含环形数据上 K-means 失败 / DBSCAN 成功的亲手复现）

> 和 C++ 的差异：Python 递归深度上限 1000（基础教程 ch12 讲过），
> 密度扩张写成 DFS 递归，簇一大就 `RecursionError`。用显式 `queue` + 游标，
> 等价于 C++ 里手写 `std::queue` 的 BFS，也更好调试。

---

<a id="c11-04"></a>
### 11.4 聚类评估与簇数选择（Evaluation and Choosing K）

**概念定义**：没有标签，就没有「准确率」。能算的只有两类量：
① **内部指标** —— 只看数据和簇本身（inertia、轮廓系数）；
② **外部指标** —— 需要真值（ARI），**真实项目里用不了，本章只拿来量化演示**。

**数学形式**：

$$\mathrm{Inertia}=\sum_i \|x_i-\mu_{c_i}\|^2,\qquad
s(i)=\frac{b(i)-a(i)}{\max\lbrace a(i),b(i)\rbrace}$$

「$a(i)$ 是 $i$ 到同簇其他点的平均距离，$b(i)$ 是到最近的其他簇的平均距离」。
轮廓系数 $s\in[-1,1]$，越大表示「自己簇紧、离别的簇远」。
注意 **inertia 随 $K$ 单调下降**（$K=n$ 时为 0），所以它**永远不能单独用来选 K**。

**最小代码**：

```python
def silhouette(X, labels):
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    out = []
    for i in range(len(X)):
        same = (labels == labels[i]); same[i] = False
        if not same.any():
            out.append(0.0); continue          # 单样本簇定义为 0
        a = D[i, same].mean()
        b = min(D[i, labels == c].mean() for c in np.unique(labels) if c != labels[i])
        out.append((b - a) / max(a, b))
    return float(np.mean(out))
```

手写轮廓在三团高斯簇上得 `0.840501`，sklearn `silhouette_score` 也是 `0.840501`，差 `0.00e+00`。

**三团高斯簇上扫 $K=2\sim8$**（sklearn `KMeans(n_init=10, random_state=42)`）：

| $K$ | 2 | **3** | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| inertia | 995.054 | 93.036 | 80.514 | 69.056 | 59.393 | 49.545 | **40.736** |
| 轮廓系数 | 0.6009 | **0.8405** | 0.6721 | 0.5435 | 0.5185 | 0.3999 | 0.3786 |
| 对齐准确率 | 0.6667 | **1.0000** | 0.8400 | 0.7933 | 0.7200 | 0.6000 | 0.4667 |

inertia 一路降到 40.736、毫无「肘部」可挑；**轮廓系数在 $K=3$ 处有明确峰值**，这次和真值对上了。

**什么时候会翻车**（篇 README 要求的固定项）：

- **轮廓系数偏好凸簇**：环形数据上，分错的 K-means 拿 **0.3280**，分对的 DBSCAN 只有 **0.1574**。
  原因很直白 —— 一个环上两点的最远距离能到直径，同簇平均距离 $a(i)$ 很大，
  而它被算成「簇很松」，完全不管这个形状本身是对的
- **inertia 没有肘部**：数据没有明显簇结构时曲线平滑下降，肘部法是人眼找拐点的主观游戏
- **密度不均 / 簇大小悬殊**：K-means 倾向把大簇切小、把小簇并掉；DBSCAN 的单一 $\varepsilon$ 照顾不了疏密不同的区域
- **高维**：所有基于欧氏距离的算法一起退化，先降维再谈聚类
- **噪声标签 `-1` 参与计算**：算轮廓系数前必须把噪声点剔掉，否则 `-1` 会被当成一个「簇」

> **诚实的结论**：无监督没有真值。**内部指标只能帮你排掉明显坏的结果，不能替你宣布哪个对**。
> 真正靠得住的是把簇拿出来看 —— 看几个代表样本、看业务上能不能解释，
> 这和 [第 20 章 项目流程](../../SYLLABUS.md)（待写）里「误差分析」是同一种工作。
> 本章所有「准确率 / ARI」都只在有真值的教学数据上用来量化演示。

**常见误区**：**别拿聚类结果当分类器用**。簇编号是任意的（这次内环叫 0，换次初始化可能叫 1），
新样本来了也没有直接的归属规则（K-means 可以算最近质心，DBSCAN 不行）。
这点在 [ch03](../../01_ml_framework/docs/ch03_what_is_ml.md) 讲「监督 vs 无监督」时已经埋过伏笔。

**对应练习**：[第 10~12 题](../exercises/ch11_ex.py)

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| 双重循环累加距离 | `(n,1,d) - (1,K,d)` 广播出距离矩阵 |
| 并查集 + 优先队列做合并 | 教学版直接扫簇对，重点在 linkage 定义 |
| DFS 递归遍历连通块 | 显式 `queue` + 游标 BFS，避开递归深度上限 |
| `sum/count` 遇空集崩溃 | 空簇显式 `if` 保持旧质心 |
| 「有标准答案就能打分」 | 无监督指标只是启发式，会夸奖错的结果 |

| | K-means | 层次聚类 | DBSCAN |
|---|---|---|---|
| 要预设 | $K$ | $K$（或切树高度） | $\varepsilon$、`min_samples` |
| 簇形状 | 凸 / 球 | 看 linkage | 任意 |
| 噪声 | 全部分配 | 全部分配 | **能标 `-1`** |
| 复杂度 | $O(nKd\cdot\text{iters})$ | $O(n^2)$ 内存、$O(n^3)$ 时间 | $O(n^2)$ 内存（可索引优化） |
| 必须缩放 | **是** | **是** | **是** |
| 主要失效 | 非凸簇、初始化差 | 大数据、链式效应 | 密度不均、高维 |

> **最容易踩的 3 个坑**：
> 1. **不标准化就聚类** —— 实测准确率 `0.5000 → 1.0000`，距离被大尺度特征垄断
> 2. **`n_init=1` 直接用** —— 20 次里 7 次陷进局部最优，最差 $J=1217.67$（最优 93.04）
> 3. **拿轮廓系数当验收标准** —— 环形数据上它给错结果 0.3280、给对结果 0.1574

**和实践终点的联系**：以图搜图的链路里，预训练模型抽出 embedding 后，
先降维（第 12 章）再聚类做粗分组 / 建索引，正是本章的直接用途，
见 [`06_engineering/README.md`](../../06_engineering/README.md)。
高维 embedding 上尤其记住两件事：**先降维**、**别信单一指标**。

## 练习

本章练习统一在 [`ch11_ex.py`](../exercises/ch11_ex.py)：从距离矩阵、K-means 分配/更新/完整迭代、
缩放前后对比、三种 linkage、DBSCAN 与 `eps` 扫描，到轮廓系数与 $K$ 扫描，共 12 题。
**全部只用 numpy**，跑通所有 `assert` 即过关。

上一篇：[第 10 章 特征工程](../../02_supervised/docs/ch10_feature_engineering.md)
下一篇：第 12 章 降维与表示（见 [SYLLABUS](../../SYLLABUS.md) 的预定路径）
