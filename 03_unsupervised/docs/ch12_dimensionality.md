# 第 12 章 降维与表示（Dimensionality Reduction）

> 前置：[第 2 章 2.1 / 2.2 / 2.7](../../00_foundations/docs/ch02_math_foundations.md#c02-01)（向量、矩阵乘法、梯度）、
> [ch04 梯度下降](../../01_ml_framework/docs/ch04_training_steps.md)、
> [ch07 线性模型](../../02_supervised/docs/ch07_linear_models.md)、
> [ch10 特征缩放](../../02_supervised/docs/ch10_feature_engineering.md)、
> [ch11 聚类](ch11_clustering.md)
> 对应练习：[`ch12_ex.py`](../exercises/ch12_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`03_unsupervised/`

**一句话**：降维不是「把列删掉」，是**换一组坐标轴，让信息尽量挤在前几根轴上**。
本章兑现 [ch02 2.1](../../00_foundations/docs/ch02_math_foundations.md#c02-01) 留的伏笔
（「行列式、逆矩阵、特征值留给第 12 章 PCA」），也直接服务你选的实践终点：
以图搜图里 embedding 先降维、再建索引，到底省了什么、又赔了什么，本章用实测算清楚。

> 数学基础薄弱也不用怕：特征值分解这一节只要求你**知道它在干什么**，
> 不要求会手算，也不写推导证明。符号第一次出现都配了读法和人话。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [主成分分析（PCA）](#c12-01) · [协方差矩阵（Covariance Matrix）](#c12-01) · [特征值分解（Eigendecomposition）](#c12-01) · [解释方差比（Explained Variance Ratio）](#c12-01) · [重构误差（Reconstruction Error）](#c12-01) · [白化（Whitening）](#c12-01) | 12.1 |
| [流形（Manifold）](#c12-02) · [t-SNE](#c12-02) · [KL 散度（KL Divergence）](#c12-02) · [UMAP](#c12-02) · [保邻域率（kNN Preservation）](#c12-02) | 12.2 |
| [自编码器（Autoencoder）](#c12-03) · [瓶颈（Bottleneck）](#c12-03) · [重构损失（Reconstruction Loss）](#c12-03) · [线性 AE ≡ PCA](#c12-03) | 12.3 |
| [降维的工程收益](#c12-04) · [召回率（Recall@k）](#c12-04) · [计算量权衡](#c12-04) · [向量索引（Vector Index）](#c12-04) | 12.4 |

### 全章共用的数据

```python
import numpy as np

def make_redundant(n=300, d=10, seed=42):
    """真实秩只有 3：10 维全是 3 个隐变量的线性混合 + 小噪声。"""
    r = np.random.default_rng(seed)
    Z = r.normal(size=(n, 3)) * np.array([3.0, 1.5, 0.7])
    M = r.normal(size=(3, d))
    return Z @ M + r.normal(0, 0.05, (n, d))

def my_pca(X):
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / len(Xc)                    # 协方差（ddof=0）
    evals, evecs = np.linalg.eigh(C)           # 对称矩阵：用 eigh 不用 eig
    order = np.argsort(evals)[::-1]
    return evals[order], evecs[:, order], Xc   # 降序
```

`make_redundant` 是本章的主力：**10 列里只有 3 个真正自由的方向**，
所以「降到 3 维几乎不丢东西」应该在数字上表现得非常干净。

### 先看结论：同一套数据上的实测

手写实现与 sklearn 对照过（教学里的库代码需要 `pip install scikit-learn`，
**本章练习一律只用 numpy**）。

| 现象 | 实测 | 落在哪一节 |
|---|---|---|
| 前 3 个主成分吃掉多少方差 | `0.99986` | [12.1](#c12-01) |
| 重构误差恒等式 `mean((X−X̂)²) = Σ_{j>k} λ_j / d` | 误差 `≤ 8.9e-16` | [12.1](#c12-01) |
| 不标准化，PC1 在真实信号列上的权重 | `0.000227` → 标准化后 `0.7071` | [12.1](#c12-01) |
| 瑞士卷上保邻域率：PCA 2D vs t-SNE 2D | `0.493` vs `0.848` | [12.2](#c12-02) |
| 线性 AE 训练后重构误差 vs PCA 最优 | `0.0001782` vs `0.0001748`（差 `1.91%`） | [12.3](#c12-03) |
| 以图搜图：64 维 → 16 维 | recall@5 `0.740 → 0.700`，计算量降到 `1/4` | [12.4](#c12-04) |

**这张表想说的是**：降维的收益能精确算（方差、重构误差、计算量），
但代价必须用**业务指标**（召回率）来验收 —— 「保留 99% 方差」不等于「检索不掉点」。

---

<a id="c12-01"></a>
### 12.1 主成分分析（Principal Component Analysis, PCA）

**概念定义**：把原来的 $d$ 个特征，线性组合成一组彼此**不相关**的新坐标轴，
按「数据在这个方向上散得有多开」从大到小排序，只留前 $k$ 根。
留下的叫主成分，删掉的是方差最小（通常也就是噪声）的方向。

先用四句话说清特征值分解在干嘛，**不要求会手算**：

| 符号 | 读法 | 人话 |
|---|---|---|
| $C = X_c^{\top} X_c / n$ | 「C 等于 X c 转置乘 X c 除以 n」 | 协方差矩阵：第 $(i,j)$ 格记「第 $i$ 列和第 $j$ 列是不是一起变大变小」 |
| $\lambda_j$ | 「lambda j」 | 第 $j$ 根新轴上方差有多大，可以理解为**这根轴有多重要** |
| $v_j$ | 「v j」 | 第 $j$ 根新轴在原坐标里的方向（单位向量） |
| $C v_j = \lambda_j v_j$ | — | 「$C$ 作用在 $v_j$ 上，只把长度拉长 $\lambda_j$ 倍、方向不变」，满足这句的 $v_j$ 就是主成分 |

ch02 讲矩阵乘法时说过「矩阵乘向量 = 对空间做变换」；
特征值就是**这个变换在哪些方向上只拉伸、不旋转**。numpy 里一行 `np.linalg.eigh(C)` 全给你算好。

**数学形式**：

$$C = \frac{1}{n} X_c^{\top} X_c,\qquad C v_j = \lambda_j v_j,\qquad
Z = X_c V_k,\qquad \hat{X} = Z V_k^{\top}$$

$$r_k = \frac{\sum_{j\le k}\lambda_j}{\sum_{j=1}^{d}\lambda_j},\qquad
\frac{1}{nd}\lVert X_c - \hat{X}\rVert_F^2 = \frac{1}{d}\sum_{j>k}\lambda_j$$

第二个式子是本章最漂亮的一条：**丢掉的信息恰好等于丢掉的特征值之和**。
所以「留几个主成分」不是拍脑袋，看累计解释方差比 $r_k$ 就有数。

**最小代码**：

```python
def pca_fit(X):
    Xc = X - X.mean(axis=0)
    evals, V = np.linalg.eigh(Xc.T @ Xc / len(Xc))
    order = np.argsort(evals)[::-1]
    return evals[order], V[:, order], X.mean(axis=0)

def pca_apply(X, mean, V, k):
    Z = (X - mean) @ V[:, :k]          # 编码：d -> k
    return Z, Z @ V[:, :k].T + mean    # 解码：k -> d
```

**实跑数字**（`make_redundant()`，n=300、d=10）：

| 主成分 | 1 | 2 | 3 | 4 起 |
|---|---|---|---|---|
| 特征值 $\lambda_j$ | 99.9805 | 23.2048 | 1.9115 | ≤ 0.0031 |
| 单个解释方差比 | 0.7991 | 0.1855 | 0.0153 | ≈ 0 |

前 3 个累计 `0.99986`。手写 `eigh` 与 sklearn `PCA(n_components=10)` 的
`explained_variance_ratio_` 最大差 `1.11e-16`，第一主成分方向的内积绝对值 `1.0000`。
（sklearn 用 `ddof=1` 报 `explained_variance_ = [100.3149, 23.2824, 1.9179, …]`，
数值比手写的略大 `300/299` 倍，但**比值完全一致** —— 这正是 [ch02 2.5](../../00_foundations/docs/ch02_math_foundations.md#c02-05) 讲过的 `ddof` 问题。）

重构误差恒等式逐项验证：

| $k$ | 实测 `mean((X−X̂)²)` | 理论 `Σ_{j>k} λ_j / d` | 差 |
|---|---|---|---|
| 1 | 2.513379 | 2.513379 | 8.9e-16 |
| 2 | 0.192896 | 0.192896 | 2.5e-16 |
| 3 | 0.001748 | 0.001748 | 6.8e-16 |
| 10 | 0.000000 | 0.000000 | 2.6e-30 |

**常见误区**（这一节坑最密）：

1. **主成分符号是任意的**。`eigh` 这次给 PC1 的符号是 −1，sklearn 可能给 +1，
   $v$ 和 $-v$ 是同一根轴。对照方向要比较 `abs(v1 @ v2)`，别直接 `np.allclose`。
2. **不标准化就 PCA = 白做**。数据 ② 里 $x$ 是 $\sigma=500$ 的纯噪声、$y$ 才是两簇信号：
   缩放前 PC1 `[-1, -0.0002]`（解释方差比 `0.99998`），几乎全押在噪声列上；
   `StandardScaler` 之后 PC1 `[0.7071, 0.7071]`。
   两类样本在 PC1 上的标准化间距从 `0.0939` 涨到 `1.4318`。
   和 [ch10](../../02_supervised/docs/ch10_feature_engineering.md) 的 KNN 缩放、[ch11](ch11_clustering.md#c11-01) 的聚类缩放是同一个坑。
3. **`np.cov` 默认 `ddof=1`**。白化 $Z_w = Z / \sqrt{\lambda}$ 之后，
   用 `Z.T @ Z / n` 算协方差与单位阵最大偏差 `5.2e-13`；
   用 `np.cov(...)` 则得到 `1.0033 I`，多出来的正好是 $n/(n-1)=300/299$。不是 bug。
4. **解释方差比高 ≠ 下游任务不掉点**。它只保证「重构得回来」，不保证「区分得开」；
   章末的检索实测会把这件事讲透。

> 和 C++ 的差异：`np.linalg.eigh` 底层就是 LAPACK 的 `dsyevd`，和你调 Eigen 的
> `SelfAdjointEigenSolver` 是同一套算法。区别在于 C++ 里要自己申请对称矩阵、管 leading dimension，
> numpy 里 `Xc.T @ Xc` 一行完事。另外**对称矩阵一定用 `eigh` 不要用 `eig`** —— 后者返回复数、
> 排序也没保证，会平白多出一堆 `np.real` 和 `argsort`。

**对应练习**：[第 1~6 题](../exercises/ch12_ex.py)（协方差 → 特征值分解 → 解释方差比 → 投影 / 重构 → 恒等式 → 白化）

---

<a id="c12-02"></a>
### 12.2 保局部结构：t-SNE 与 UMAP（Manifold Visualization）

**概念定义**：PCA 只会**线性投影**。如果数据是一张卷起来的纸（流形，Manifold），
纸面上离得远的两点在 3D 空间里可能贴在一起，线性投影会把不同层压到同一块。
t-SNE / UMAP 换了个目标：**不保全局距离，只保「谁是谁的邻居」**，专门用来画 2D 可视化图。

**数学形式**（t-SNE 的核心三步，符号都配了人话）：

| 式子 | 在算什么 |
|---|---|
| $p_{j|i} \propto \exp(-\lVert x_i-x_j\rVert^2 / 2\sigma_i^2)$ | 高维里，$j$ 算不算 $i$ 的邻居（近的给高概率）；$\sigma_i$ 由 perplexity 反解 |
| $q_{ij} = \dfrac{(1+\lVert y_i-y_j\rVert^2)^{-1}}{\sum_{a\ne b}(1+\lVert y_a-y_b\rVert^2)^{-1}}$ | 低维里，用**重尾**的 Student-t 核算配对概率；重尾是为了给远点留点推力，缓解拥挤 |
| $C = \sum_{i\ne j} p_{ij}\log\dfrac{p_{ij}}{q_{ij}}$ | KL 散度：两张「谁挨着谁」的概率表差多少，越小越像 |

$$\frac{\partial C}{\partial y_i} = 4\sum_{j}(p_{ij}-q_{ij})(1+\lVert y_i-y_j\rVert^2)^{-1}(y_i-y_j)$$

最后这条梯度是可以直接手写的（每个点被「该近的拉、该远的推」），
用 [ch04 的中心差分](../../01_ml_framework/docs/ch04_training_steps.md) 就能验。

**最小代码**（Q 矩阵与梯度，纯 numpy）：

```python
def student_t_q(Y):
    d2 = ((Y[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2)
    num = 1.0 / (1.0 + d2)
    np.fill_diagonal(num, 0.0)
    return num / num.sum()

def tsne_gradient(P, Y):
    d2 = ((Y[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2)
    inv = 1.0 / (1.0 + d2)
    np.fill_diagonal(inv, 0.0)
    Q = inv / inv.sum()
    D = (P - Q) * inv
    return 4.0 * (np.diag(D.sum(axis=1)) - D) @ Y
```

在 12 个随机点上，解析梯度与中心差分的最大绝对差 `8.6e-11`，梯度范数 `0.1408`。

**实跑数字**（`make_swiss_roll(n_samples=300, noise=0.05)`，用「高维 kNN 里有多少在低维仍是邻居」当保邻域率，$k=10$）：

| 降到 2D 的方法 | 保邻域率 |
|---|---|
| PCA（线性投影） | `0.493` |
| `TSNE(perplexity=30, init="pca", learning_rate="auto")` | **`0.848`** |

差距很大：**t-SNE 把卷起来的流形摊平了**。但别急着把它当万能药，看下一节的失效清单。

**常见误区**：

- **t-SNE 的轴没有物理意义，簇间距离不可解释**。图上两团离得远，不代表原空间里差得远；
  换 `perplexity` 或随机种子，图会长得完全不一样。**别拿 t-SNE 图当「确实分成了几类」的证据** ——
  那是 [ch11 聚类](ch11_clustering.md#c11-04) 该干的活。
- **没有 out-of-sample**：t-SNE 只给训练集里已有的点算坐标，来一张新图得整批重跑。
  所以**它不能用在以图搜图的在线检索链路里**，只能离线看数据长什么样。
- **保邻域率只查「邻居丢了没」，不查「陌生人被硬拉过来没」**。完整的可视化质量还有
  trustworthiness / continuity 一对指标，本章只实现一个下限。
  练习里自造瑞士卷（不依赖 sklearn）实测：相同 3D 坐标 `1.0`、PCA 2D `0.4123`、随机 2D `0.0327`。
- **UMAP 不是 t-SNE 的换皮**：它基于模糊单纯复形，通常更快、保更多全局结构，
  而且 `transform()` 能映射新样本。需要 `pip install umap-learn`（sklearn 里没有），
  **本章没有实测 UMAP，因此不给任何数字** —— 真要用时自己跑一遍对照。
- **完整 t-SNE 还有 perplexity 二分搜索、动量、early exaggeration**，
  手写这几十行只是梯度核心，工程上直接用库，别重复造轮子。

**对应练习**：[第 7~9 题](../exercises/ch12_ex.py)（保邻域率、Student-t Q、KL 梯度的数值梯度检验）

---

<a id="c12-03"></a>
### 12.3 自编码器与「线性 AE ≡ PCA」（Autoencoder）

**概念定义**：训练一个**沙漏形**网络：编码器把 $d$ 维压成 $k$ 维（**瓶颈**，Bottleneck），
解码器再还原回 $d$ 维，目标是让还原结果尽量像原输入。
它不需要任何标签 —— **输入自己就是标签**，所以属于无监督。

**数学形式**：先看**线性**自编码器（两层都不加激活函数），
编码器 $W\in\mathbb{R}^{d\times k}$、解码器 $V\in\mathbb{R}^{k\times d}$，合起来就是 $M = WV$：

$$L = \frac{1}{n}\lVert X_c - X_c W V\rVert_F^2,\qquad
\frac{\partial L}{\partial M} = -\frac{2}{n}X_c^{\top}(X_c - X_c M)$$

$$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial M}V^{\top},\qquad
\frac{\partial L}{\partial V} = W^{\top}\frac{\partial L}{\partial M}$$

后两行只是 [ch02 2.8 链式法则](../../00_foundations/docs/ch02_math_foundations.md#c02-08) 的矩阵版。
**这里不需要反向传播**：把 $M=WV$ 当成两层线性层的复合，手推一次梯度即可；
真正的多层 / 非线性网络要等 [第 14 章](../../04_deep_learning/docs/ch14_nn_basics.md#c14-04) 讲计算图和反向传播。

**最小代码**：

```python
def ae_gradient(Xc, W, V):
    n = len(Xc)
    R = Xc - Xc @ W @ V
    G = -2.0 * Xc.T @ R / n       # dL/dM
    return G @ V.T, W.T @ G      # dL/dW, dL/dV

def train_linear_ae(Xc, k, lr=0.05, steps=5000, seed=0):
    r = np.random.default_rng(seed)
    W = r.normal(0, 0.1, (Xc.shape[1], k))
    V = r.normal(0, 0.1, (k, Xc.shape[1]))
    for _ in range(steps):
        gW, gV = ae_gradient(Xc, W, V)
        W -= lr * gW; V -= lr * gV
    return W, V
```

**实跑数字**（`make_redundant()` 中心化后 $X_c/10$，只缩放数值尺度、不改 PCA 子空间）：

- 解析梯度 `−2.0980196667` vs 中心差分 `−2.0980196638`，差 `3e-9`
- PCA 的理论最优重构损失 `0.0001748435`
- `lr=0.05` 训练轨迹：`1.241286`（第 1 步）→ `0.188122`（100）→ `0.019134`（500）
  → `0.003030`（2000）→ `0.000178`（5000 步），与最优差 **`1.91%`**
- 学到的编码器列空间与 PCA 主子空间的主角度余弦 `[0.9943, 0.9910, 0.9529]` —— 基本重合

**结论是一个定理，不是巧合**：线性 AE + 平方损失的最优解张成的子空间，
**就是 PCA 的主子空间**（差一个可逆线性变换）。所以别指望「换个模型就能比 PCA 压得更好」。

**常见误区**：

- **线性 AE 学不到 PCA 之外的东西**。想要更强的表示，必须加非线性激活（ReLU / tanh）
  或堆深层 —— 那才需要[反向传播](../../04_deep_learning/docs/ch14_nn_basics.md#c14-04)（第 14 章）。
- **学习率过大会发散，和 [ch04](../../01_ml_framework/docs/ch04_training_steps.md) 一模一样**。
  在未经缩放的原始数据上（最大特征值约 `100`）用 `lr=0.05`，**第 8 步就 `inf`**；
  把数据统一除以 10 之后同样的 `lr` 才稳定。`lr=0.001` 跑 20000 步还剩 `0.0192`，
  慢得以为模型坏了 —— 其实只是步长太小。
- **瓶颈维数 $k$ 是唯一真正的超参**，等价于 PCA 里选几个主成分；
  别在编码器层数上折腾，线性情形下加层不改变表达能力。
- **重构误差小 ≠ 表示好用**。恒等映射（$k=d$）误差为 0 但什么也没学到，
  和 [ch05 过拟合](../../01_ml_framework/docs/ch05_error_sources.md) 是同一种病。

**对应练习**：[第 10、11 题](../exercises/ch12_ex.py)（手写 AE 梯度 + 训练到收敛，亲手验证它撞回 PCA）

---

<a id="c12-04"></a>
### 12.4 降维的工程收益与实践终点（Engineering Trade-off）

以图搜图的链路是「图像集 → 预训练模型抽 embedding → 降维 / 聚类（[ch11](ch11_clustering.md)、本章）
→ 建向量索引 → 查询服务」，见 [`06_engineering/README.md`](../../06_engineering/README.md)。
用 500 张图的模拟 embedding（64 维、20 组）、20 条 query 做余弦 top-5 检索：

| 降到 $k$ 维 | recall@5 | 相对原始 | 单次查询内积乘法 | 计算量 |
|---|---|---|---|---|
| 64（原始） | **0.7400** | — | 32000 | 1.000× |
| 32 | 0.7200 | −0.0200 | 16000 | 0.500× |
| **16** | **0.7000** | **−0.0400** | **8000** | **0.250×** |
| 8 | 0.5200 | −0.2200 | 4000 | 0.125× |
| 4 | 0.3000 | −0.4400 | 2000 | 0.062× |
| 2 | 0.0800 | −0.6600 | 1000 | 0.031× |

**读法**：降到 16 维，召回率只掉 `0.04`，内积计算量直接砍到 `1/4` —— 这就是降维的工程价值；
但再降到 8 维，召回率断崖到 `0.52`，省下的算力完全不值。
拐点在哪儿**只能靠业务指标试出来**：前 16 个主成分已经累计 `0.99986` 的方差，
可「方差保留 99.99%」并不能保证「检索不掉点」，第 8 维丢掉的方差极小，
偏偏把区分不同组的方向削掉了。这呼应 [ch06](../../01_ml_framework/docs/ch06_evaluation_metrics.md)：
**损失给优化器看，指标给人看，验收只认业务指标**。

**对应练习**：[第 12 题](../exercises/ch12_ex.py)（亲手跑出这张「维度 → 召回率 / 计算量」权衡表）

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| Eigen `SelfAdjointEigenSolver` | `np.linalg.eigh(Xc.T @ Xc / n)`，对称矩阵别用 `eig` |
| 手写双重循环算协方差 | `Xc.T @ Xc` 一次矩阵乘，$(d,d)$ 小矩阵 |
| 手写投影循环 | `Xc @ V[:, :k]` 一次广播 |
| 连通块 DFS | t-SNE / 聚类一样是 $O(n^2)$ 距离矩阵，大样本先建索引 |
| 「维度越低越快越好」 | 要拿 recall 验收，16 维是拐点、8 维就崩 |

| | PCA | t-SNE / UMAP | 自编码器 |
|---|---|---|---|
| 保什么 | 全局方差 | 局部邻域 | 重构误差 |
| 线性 / 非线性 | 线性 | 非线性 | 线性时 ≡ PCA，非线性才有增量 |
| 能映射新样本 | **能**（`transform`） | t-SNE 不能 / UMAP 能 | **能**（前向一次） |
| 输出坐标可解释 | 轴 = 原特征线性组合 | **轴无意义、簇间距不可信** | 瓶颈维无直接语义 |
| 主要用途 | 降维 / 去噪 / 加速检索 | **只做可视化** | 表示学习（第 14 章续） |
| 必须缩放 | **是** | 是 | 是（否则梯度发散） |

> **最容易踩的 3 个坑**：
> 1. **不标准化就 PCA** —— PC1 会全押在量纲最大的噪声列上（权重 `0.000227` vs `0.7071`）
> 2. **拿 t-SNE 图当聚类证据 / 当检索用** —— 它没有 out-of-sample，轴和簇间距都不可解释
> 3. **只看解释方差比就拍板维度** —— 实测 16→8 维方差几乎没变，recall@5 却从 `0.70` 掉到 `0.52`

## 练习

本章练习统一在 [`ch12_ex.py`](../exercises/ch12_ex.py)：从协方差与特征值分解、
解释方差比、投影 / 重构 / 恒等式、白化，到保邻域率、Student-t Q 与 KL 梯度、
线性 AE 梯度与训练，最后是降维检索的 recall 权衡，共 12 题。
**全部只用 numpy**，跑通所有 `assert` 即过关。

上一篇：[第 11 章 聚类](ch11_clustering.md)
下一篇：[第 14 章 神经网络基础](../../04_deep_learning/docs/ch14_nn_basics.md)（第 13 章 `[选读]`，已跳过）
