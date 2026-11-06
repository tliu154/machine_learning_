# 第 7 章 线性模型（Linear Models）

> 前置：第 4 章（模型 → 损失 → 优化三步骤）、第 1 章 1.3（矩阵乘 `@`、广播）
> 对应练习：[`ch07_ex.py`](../exercises/ch07_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`02_supervised/`

**一句话**：ch04 把「训练」拆成三步骤，本章第一次把这三步骤**装进一整个能上手的算法族** ——
只换模型和损失，同样的流程就从「预测一个连续值」变成「判断是不是装甲板」。

> ch04 埋的伏笔在这里兑现：MSE 有**闭式解**，一步就能算出最优参数，不必迭代。
> 本章所有代码只用 numpy；7.4 再给出 scikit-learn 的等价写法作为对照。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [线性回归（Linear Regression）](#c07-01) · [最小二乘（Least Squares）](#c07-01) · [正规方程（Normal Equation）](#c07-01) · [梯度下降（Gradient Descent）](#c07-01) | 7.1 |
| [逻辑回归（Logistic Regression）](#c07-02) · [Sigmoid 函数](#c07-02) · [交叉熵损失（Cross-Entropy Loss）](#c07-02) | 7.2 |
| [正则化（Regularization）](#c07-03) · [Ridge / Lasso](#c07-03) | 7.3 |
| [特征缩放（Feature Scaling）](#c07-04) · [决定系数（R²）](#c07-04) | 7.4 |

### 全章共用的数据

```python
import numpy as np

rng = np.random.default_rng(42)
X = rng.uniform(-2, 2, (80, 2))                       # 设计矩阵 (n, d) = (80, 2)
y = 1.5 * X[:, 0] - 2.0 * X[:, 1] + 0.5 \
    + rng.normal(0, 0.05, 80)                         # 回归：真参数 (1.5, -2.0, 0.5)
yc = (X[:, 0] + X[:, 1] > 0).astype(float)            # 分类：两个特征线性可分
```

`X` 形状恒为 `(n_samples, n_features)`；**一维特征必须 `reshape(-1, 1)`**（见
[NOTATION.md](../../NOTATION.md) 的形状约定）。这句话后面每一章都会重复，因为踩的人最多。

---

<a id="c07-01"></a>

### 7.1 线性回归与最小二乘（Linear Regression and Least Squares）

**概念定义**：把 ch04 的一元直线 $\hat{y}=wx+b$ 推广成「多个特征的加权和」。
做法是在 $X$ 右边补一列 1，把偏置 $b$ 塞进参数向量，于是模型和损失都只剩一次矩阵乘：
$\hat{y} = \tilde{X}\theta$。**「线性」说的是对参数 $\theta$ 线性，不是对 $x$ 线性**。

**数学形式**：

$$\hat{y} = \tilde{X}\theta,\qquad
L(\theta) = \frac{1}{n}\lVert y - \tilde{X}\theta \rVert^2,\qquad
\theta^* = (\tilde{X}^{\top}\tilde{X})^{-1}\tilde{X}^{\top}y$$

第一式是模型，第二式是 MSE 的矩阵写法「残差平方和的平均」，第三式是**正规方程**：
令梯度等于 0 直接解出来的最优参数，不需要学习率、不需要迭代。
numpy：`np.linalg.lstsq(A, y, rcond=None)[0]`，其中 `A = add_bias(X)`。

**最小代码**：

```python
def add_bias(X):
    """右边补一列 1，把 b 吸进 theta；(n, d) -> (n, d+1)"""
    return np.column_stack([X, np.ones(len(X))])

A = add_bias(X)
theta = np.linalg.lstsq(A, y, rcond=None)[0]
print(np.round(theta, 2))          # [ 1.5 -2.   0.5]，一步到位
y_pred = A @ theta
```

闭式解和 ch04 的梯度下降是**同一道题的两种解法**，取舍很清楚：

| | 正规方程（闭式解） | 梯度下降（ch04） |
|---|---|---|
| 调参 | 无学习率、无 epoch | 要选 `lr`、轮数、初始化 |
| 特征数 | $d$ 大时 $O(d^3)$ 很慢 | 每轮 $O(nd)$，可扩展到大数据 |
| 数据 | 小中型表格数据 | 大批量 / 小批量 / 神经网络 |
| 特征相关 | 矩阵可能奇异，靠 `lstsq` 兜底 | 不受影响，只是收敛慢 |

**工程手段：多项式特征**。想拟合曲线，不必换模型，把 $x^2, x^3$ 当新特征喂进去就行：

```python
def polynomial_features(x, degree=3):
    """[x, x^2, ..., x^degree]，不含常数项（常数项交给 add_bias）"""
    return np.column_stack([np.asarray(x) ** k for k in range(1, degree + 1)])

xs = np.linspace(-2, 2, 60)
A_poly = add_bias(polynomial_features(xs, 2))
theta_poly = np.linalg.lstsq(A_poly, 1 + 2 * xs + 0.5 * xs ** 2, rcond=None)[0]
```

$\hat{y}=w_1x+w_2x^2+b$ 对 $x$ 是二次曲线，**对 $\theta$ 仍然是线性的**，所以还是线性模型、还能用同一个 `lstsq`。
这是「线性模型」这个词最容易被误解的地方。

**常见误区**：**别手写 `np.linalg.inv(A.T @ A) @ A.T @ y`**。
特征共线或 $d>n$ 时 $A^{\top}A$ 奇异，求逆要么直接报错、要么给出天文数字般的参数。
`lstsq` 走 SVD，奇异时返回最小范数解，数值上稳得多。真要写逆，也该用 `np.linalg.solve`。

**对应练习**：[第 1~4 题](../exercises/ch07_ex.py)

> 和 C++ / 已有认知的差异：C++ 里要实现最小二乘得手写高斯消元或自己引 Eigen，
> 还得操心主元选取；numpy 一个 `lstsq` 搞定。**代价是形状错了不编译报错** ——
> `A @ theta` 少一列只会给你一个诡异结果，所以 ML 代码里 `print(A.shape)` 出现频率极高。

---

<a id="c07-02"></a>

### 7.2 逻辑回归与交叉熵（Logistic Regression and Cross-Entropy）

**概念定义**：**名字叫「回归」，做的是二分类**。
线性部分 $z=\tilde{X}\theta$ 输出任意实数，用 Sigmoid 把它压进 $(0,1)$ 当「属于正类的概率」，
再以 0.5 为阈值判类别。它和线性回归共用同一个骨架，只换了**输出变换**和**损失函数** ——
这正是 ch04 那张「三步骤在后面各章长什么样」表的第一次兑现。

**数学形式**：

$$p = \sigma(z) = \frac{1}{1+e^{-z}},\qquad
L(\theta) = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i\log p_i + (1-y_i)\log(1-p_i)\right]$$
$$\nabla_\theta L = \frac{1}{n}\tilde{X}^{\top}(p - y)$$

第一式把实数映射到概率；第二式是**二元交叉熵**：$y=1$ 时只看 $-\log p$，$y=0$ 时只看 $-\log(1-p)$，
预测越离谱惩罚越重；第三式是它的梯度，形状 $(\text{预测}-\text{真实})$ 乘回特征矩阵再取平均。
numpy：`grad = A.T @ (p - y) / len(A)` —— 和线性回归的梯度长得几乎一样，只是把残差换成了 $p-y$。

**最小代码**：

```python
def sigmoid(z):
    z = np.clip(np.asarray(z, dtype=float), -500, 500)   # 防 exp 溢出
    return 1.0 / (1.0 + np.exp(-z))

def bce(y, p, eps=1e-12):
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)  # 防 log(0)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

A = add_bias(X)
theta = np.zeros(A.shape[1])
for _ in range(2000):
    p = sigmoid(A @ theta)
    theta -= 0.5 * (A.T @ (p - yc)) / len(A)   # 梯度下降，和 ch04 完全同构

print(bce(yc, p), np.mean((p > 0.5) == yc))    # 损失很小、准确率接近 1
```

**常见误区**：**别拿 MSE 训分类**。
Sigmoid + MSE 对 $\theta$ 非凸，且预测错到饱和区时梯度趋近 0，模型「卡住不动」；
交叉熵刚好相反，$p$ 离真实标签越远梯度越大。另外 `log(0)` 会得到 `-inf`，
**概率进 log 前一律 clip**，这是写完能跑和跑出 `nan` 的分界线。

**对应练习**：[第 5~8 题](../exercises/ch07_ex.py)

> 和 C++ / 已有认知的差异：`exp(1000)` 在 C++ 里同样溢出成 `inf`，但你要么手写分支、
> 要么逐元素判断；numpy 的 `np.clip` 一次把所有元素夹住，也不用手写逐元素分支。
> 另一个直觉差异：C++ 里 `bool` 和 `double` 是两种类型，这里 `yc` 用 `float` 存 0/1，
> 是为了能直接进矩阵乘 —— **标签的「类型」由运算决定，不由语义决定**。

---

<a id="c07-03"></a>

### 7.3 正则化线性模型（Regularized Linear Models）

**概念定义**：权重绝对值很大，意味着输入一点扰动就会让预测剧烈跳变 —— 这通常就是过拟合。
正则化在损失里加一项「权重大小的罚款」，逼模型用更小的权重解释数据。
罚款用平方叫 **Ridge（L2）**，用绝对值叫 **Lasso（L1）**（后者还会把某些权重压成 0，顺带做特征选择）。

**数学形式**：

$$L_{\text{ridge}}(\theta) = \frac{1}{n}\lVert y - A\theta \rVert^2 + \alpha\lVert w \rVert^2,\qquad
\theta^* = (A^{\top}A + \alpha I')^{-1}A^{\top}y$$

$\alpha$（sklearn 里叫 `alpha`）越大，权重被压得越小。$I'$ 是单位矩阵但**最后一个对角元为 0** ——
偏置 $b$ 不该被惩罚，否则模型连「数据整体偏高 2」都没法表达。
numpy：`np.linalg.solve(A.T @ A + reg, A.T @ y)`。

**最小代码**：

```python
def ridge_closed_form(X, y, alpha):
    A = add_bias(X)
    reg = alpha * np.eye(A.shape[1])
    reg[-1, -1] = 0.0                      # 偏置不参与正则化
    return np.linalg.solve(A.T @ A + reg, A.T @ y)

for a in (0.0, 0.1, 10.0):
    print(a, np.round(ridge_closed_form(X, y, a), 2))
```

$\alpha=0$ 时应当和 7.1 的 `lstsq` 结果一致；$\alpha$ 增大时两个权重向 0 收缩，截距基本不动。

**常见误区**：**正则化之前必须先标准化特征，而且偏置不参与正则化**。
各特征量纲不同时，「权重大小」本身没有可比性，罚一项等于乱罚；
标准化又只能**在训练集上 fit**（ch04 讲过的数据泄漏），否则验证分数虚高。
Lasso 没有这么干净的闭式解，需要坐标下降，这里先不展开。

**对应练习**：[第 9 题](../exercises/ch07_ex.py)

---

<a id="c07-04"></a>

### 7.4 从 NumPy 实现到 scikit-learn（From NumPy to scikit-learn）

**概念定义**：库没有魔法，`fit` 就是上面那几行求解，`predict` 就是一次矩阵乘，
`score` 是决定系数 $R^2$。手写一遍之后，你看 `coef_` 就知道它对应 $\theta$ 的哪几项。

$$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$$

「比『无脑预测均值』好多少」：1 是完美，0 等于没学到东西，负数说明还不如预测均值。
numpy：`1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)`。

**最小代码**（需要 `pip install scikit-learn`；本章练习**不依赖它**）：

```python
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_tr)                 # 只在训练集 fit！
X_tr_s, X_va_s = scaler.transform(X_tr), scaler.transform(X_va)

model = LinearRegression().fit(X_tr_s, y_tr)
print(model.coef_, model.intercept_)                # 对应手写 theta[:-1] / theta[-1]
print(model.score(X_va_s, y_va))                   # R²，等价 1 - SSE/SST

clf = LogisticRegression().fit(X_tr_s, (y_tr > y_tr.mean()).astype(int))
print(clf.predict_proba(X_va_s)[:3])               # 等价于 sigmoid(A @ theta)
print(Ridge(alpha=10.0).fit(X_tr_s, y_tr).coef_)   # 对应 7.3 的 ridge_closed_form
```

三段代码和前三节的 numpy 版本一一对应：**换的是接口，不是数学**。
本章实例上实测过：`LinearRegression().coef_` 与
`np.linalg.lstsq(add_bias(X_tr_s), y_tr, rcond=None)[0][:-1]` 的差为 0，
`intercept_` 与 `theta[-1]` 也完全一致。

**常见误区**：**一维特征要 `reshape(-1, 1)`，且预处理器只能 `fit` 训练集**。
前者是 sklearn 最经典的报错（`Expected 2D array, got 1D array instead`）；
后者是 ch04 的数据泄漏，先在全量数据上 `fit_transform` 再划分，验证分数会偷偷虚高。

**对应练习**：[第 10、11 题](../exercises/ch07_ex.py)

> 和 C++ / 已有认知的差异：C++ 各库各写各的接口，没有统一约定；
> Python 数据栈的 estimator 是**鸭子类型约定**（有 `fit` / `predict` 就行，不要求继承某个基类），
> 所以 `LinearRegression` 和 `LogisticRegression` 能塞进同一条 `Pipeline`。
> 从 C++ 的「编译期接口检查」到这里的「运行时约定」，是这个生态最需要适应的地方。

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| 手写高斯消元解线性方程组 | `np.linalg.lstsq` / `solve` 一步到位 |
| `struct Params { double w[2], b; }` | 一列 1 把 $b$ 吸进 `theta` 向量 |
| 分支判断输出类别 | `sigmoid` 出概率，阈值 0.5 分类 |
| 自己写 `exp` 的溢出保护 | `np.clip` 向量化夹取 |
| `bool` 与 `double` 泾渭分明 | 标签存成 0.0/1.0 的 float 直接进矩阵乘 |
| 每个库一套接口 | `fit` / `predict` / `score` 鸭子类型约定 |

| 三步骤 | 线性回归 | 逻辑回归 |
|---|---|---|
| 模型 $f_\theta$ | $\tilde{X}\theta$ | $\sigma(\tilde{X}\theta)$ |
| 损失 $L$ | MSE | 二元交叉熵 |
| 优化 | 正规方程（闭式解） | 梯度下降（无闭式解） |

**什么时候会翻车**：线性模型假设「输出约等于特征的加权和」。
XOR 型数据、强非线性交互、类别边界是曲线时，它连训练集都拟合不好；
逻辑回归还额外假设**对数几率是线性的**，一条斜线分不开就得换 ch08 的核方法或树模型。
另外最小二乘用平方放大误差，个别离群点就能把直线拽歪 —— 这时要换鲁棒损失或先清洗数据。

> **最容易踩的 3 个坑**：
> 1. 手写 `inv(A.T @ A)` 在共线/高维时炸 → 用 `lstsq` 或 `solve`
> 2. 概率进 `log` 不 clip → `-inf` 污染整轮训练；分类别用 MSE
> 3. 先 `fit_transform` 全量再划分 → 数据泄漏，验证分数虚高

## 练习

本章练习统一在 [`ch07_ex.py`](../exercises/ch07_ex.py)：从最小二乘闭式解、
多项式特征、Sigmoid 与交叉熵、手写逻辑回归，到 Ridge 和防泄漏的划分标准化，共 11 题。
**全部只用 numpy**，跑通所有 `assert` 即过关；7.4 的 sklearn 代码仅作对照，不进练习。

上一篇：第 6 章 评估指标（待写，见 [SYLLABUS](../../SYLLABUS.md)）
下一篇：第 8 章 经典分类算法（待写，见 [SYLLABUS](../../SYLLABUS.md)）
