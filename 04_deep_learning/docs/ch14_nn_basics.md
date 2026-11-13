# 第 14 章 神经网络基础（Neural Network Basics）

> 前置：[第 2 章 2.6~2.8](../../00_foundations/docs/ch02_math_foundations.md#c02-06)（导数 / 梯度 / 链式法则）、
> [ch04 训练三步骤](../../01_ml_framework/docs/ch04_training_steps.md)、
> [ch07 逻辑回归](../../02_supervised/docs/ch07_linear_models.md)、
> [ch08 XOR](../../02_supervised/docs/ch08_classical_classifiers.md)、
> [ch12 线性 AE](../../03_unsupervised/docs/ch12_dimensionality.md#c12-03)
> 对应练习：[`ch14_ex.py`](../exercises/ch14_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`04_deep_learning/`

**一句话**：神经网络就是把「线性层 → 非线性激活」堆几次，
再用**反向传播**把误差从输出一路乘回每个参数。
本章**全部用 numpy 手写，不引入任何框架**（[第 5 篇的底线](../README.md)）——
先看清里面在算什么，[ch15](ch15_activation_init.md) 再往深里堆，
[ch16](ch16_training_dnn.md) 起换 PyTorch 才不是拿框架当黑箱。

> 数学基础薄弱也不用怕：本章严格守 [ch02 2.8 的「够用边界」](../../00_foundations/docs/ch02_math_foundations.md#c02-08)：
> **会「拆中间量 → 逐段求导 → 相乘」就够，不写 Jacobian、不写矩阵微分推导**。
> 每一条梯度都会告诉你「它在算什么」，并用中心差分当场验证。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [神经元（Neuron）](#c14-01) · [权重 / 偏置（Weight / Bias）](#c14-01) · [激活函数（Activation Function）](#c14-01) · [层（Layer）](#c14-01) | 14.1 |
| [多层叠加（Stacking Layers）](#c14-02) · [线性退化](#c14-02) · [隐藏层（Hidden Layer）](#c14-02) · [模型容量（Capacity）](#c14-02) | 14.2 |
| [前向传播（Forward Propagation）](#c14-03) · [计算图（Computational Graph）](#c14-03) · [缓存（Cache）](#c14-03) · [Logit / 概率](#c14-03) | 14.3 |
| [反向传播（Backpropagation）](#c14-04) · [局部梯度（Local Gradient）](#c14-04) · [数值梯度检验（Gradient Checking）](#c14-04) | 14.4 |
| [两层网络（Two-Layer Network）](#c14-05) · [XOR](#c14-05) · [学习率（Learning Rate）](#c14-05) · [局部最优（Local Optimum）](#c14-05) | 14.5 |

### 全章共用的数据：和 ch08 一模一样的 XOR

```python
import numpy as np

def make_xor(seed=42):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (160, 2))
    y = (X[:, 0] * X[:, 1] > 0).astype(int)   # 一三象限为 1，二四象限为 0
    return X[:120], y[:120], X[120:], y[120:]
```

[ch07 结尾](../../02_supervised/docs/ch07_linear_models.md)说过「一条斜线分不开就得换模型」，
[ch08](../../02_supervised/docs/ch08_classical_classifiers.md) 用核方法和树解决了它，
本章用**一个自己手写的两层网络**再把这件事做一遍。

### 先看结论：同一份 XOR 上的实测

| 现象 | 实测 | 小节 |
|---|---|---|
| `sigmoid(0.5)` 的导数 | `0.235004`（与 ch02 2.8 同一个数） | [14.1](#c14-01) |
| 两层**线性**叠起来 vs 一层线性 | 输出最大差 `1.11e-16` | [14.2](#c14-02) |
| 单样本逐段连乘 vs 中心差分 | `-0.0403845059` vs `-0.0403845060` | [14.4](#c14-04) |
| 手写反向传播，全参数数值梯度检验 | 最大差 `8.3e-11`（[ch04 的警戒线是 1e-5](../../01_ml_framework/docs/ch04_training_steps.md)） | [14.4](#c14-04) |
| XOR 验证准确率：逻辑回归 → 两层网络 | `0.675` → **`1.0000`** | [14.5](#c14-05) |
| 隐藏层宽度 `h=1` → `h=4` | val `0.6500` → `1.0000` | [14.5](#c14-05) |
| `lr=20` 跑 200 步 | loss `0.692 → 1.166`（发散） | [14.5](#c14-05) |

---

<a id="c14-01"></a>
### 14.1 神经元与层（Neuron and Layer）

**概念定义**：一个神经元做三件事 —— 把输入**加权求和**、加一个**偏置**、过一道**激活函数**。
把 $h$ 个神经元并排放在同一层，就只是把一次标量运算换成一次矩阵乘法。

| 符号 | 读法 | 人话 |
|---|---|---|
| $x\in\mathbb{R}^{d}$ | 「x 属于 R 的 d 次方」 | 一个样本的 $d$ 个特征 |
| $W,\ b$ | 「W」「b」 | 这一层**要从数据里学出来**的参数：权重矩阵、偏置向量 |
| $z = xW + b$ | 「z 等于 x W 加 b」 | 激活前的加权和，叫 **logit** |
| $a = \sigma(z)$ | 「a 等于 sigma z」 | 激活后的输出；$\sigma$ 读「sigma」，就是一个把数压弯的函数 |

**数学形式**：

$$z = xW + b,\qquad a = \sigma(z),\qquad
A = \sigma(XW + b)\ \ (\text{一整批样本一次算完})$$

$\sigma$ 可以换成任何非线性函数。本章用两个：

$$\mathrm{sigmoid}(z)=\frac{1}{1+e^{-z}},\quad \sigma'(z)=\sigma(z)(1-\sigma(z));\qquad
\tanh'(z)=1-\tanh(z)^2$$

**最小代码**：

```python
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))   # clip 防 exp 溢出

def linear_layer(X, W, b):
    return X @ W + b          # (n,d) @ (d,h) + (h,) -> (n,h)，靠广播
```

**实跑数字**（正好对上 [ch02 2.8](../../00_foundations/docs/ch02_math_foundations.md#c02-08) 那一段）：
`sigmoid(0.5) = 0.6224593312`，$\sigma'(0.5)=0.2350037122$，
中心差分 `0.2350037122`，差 `1e-11`；`sigmoid(-100) = 8.76e-27`、`sigmoid(100) = 1.0`，都没溢出。

**常见误区**：

- **clip 不是可选项**。`exp(1000)` 会先给 `RuntimeWarning` 再变 `inf`；
  而 [ch07](../../02_supervised/docs/ch07_linear_models.md) 讲过的 `log(0)` 会直接把整轮训练污染成 `nan`。
  激活里 clip `z`、损失里 clip 概率，两处都要做。
- **别把 logit 和概率搞混**：$z$ 可以是任意实数，$a$ 才在 $(0,1)$。
  交叉熵吃的是概率，后面 `dL/dZ2 = P - y` 那个漂亮结论吃的是 logit。
- **`@` 不是 `*`**：`X @ W` 是矩阵乘，`X * W` 是逐元素乘（[ch02 2.2](../../00_foundations/docs/ch02_math_foundations.md#c02-02)）。
  形状对不上时先打印 `X.shape, W.shape`，比读报错快。

> 和 C++ 的差异：C++ 里这是 `for i / for j` 双重循环累加，
> numpy 里 `X @ W` 一次 BLAS 调用，偏置 `+ b` 靠广播自动贴到每一行。
> 代价是 `(n,h)` 中间矩阵要实打实占内存 —— 大批量时先算内存再调 `batch_size`。

**对应练习**：[第 1~3 题](../exercises/ch14_ex.py)（数值稳定的 sigmoid、两个激活函数的导数）

---

<a id="c14-02"></a>
### 14.2 多层叠加与「为什么必须加非线性」（Stacking Layers）

**概念定义**：把 14.1 的层串起来，前一层的输出当后一层的输入，
夹在中间、看不见的层叫**隐藏层**。听起来层数越多越强 —— 但有个前提。

**数学形式**：先看**不加激活函数**的两层：

$$(XW_1+b_1)W_2+b_2 = X\underbrace{(W_1W_2)}_{W'} + \underbrace{(b_1W_2+b_2)}_{b'}$$

右边又是一个 $XW'+b'$。**两层线性 = 一层线性**，堆 100 层也一样。

**最小代码 + 实测**：

```python
W_eq = W1 @ W2
b_eq = b1 @ W2 + b2
Y_two = (X @ W1 + b1) @ W2 + b2
Y_one = X @ W_eq + b_eq
print(np.abs(Y_two - Y_one).max())    # 1.11e-16（浮点误差量级）
```

随机 $X\in\mathbb{R}^{5\times2}$、$W_1\in\mathbb{R}^{2\times3}$、$W_2\in\mathbb{R}^{3\times1}$ 上，
两种写法最大差 `1.11e-16`，等价权重 $W'$ 形状 `(2, 1)`。

**所以激活函数不是装饰品，它才是「深度」的来源**。
这和 [ch12 12.3](../../03_unsupervised/docs/ch12_dimensionality.md#c12-03) 的「线性 AE ≡ PCA」是同一件事的两种说法：
只要全是线性变换，不管堆几层，表达能力的上限都被锁死在线性映射里。

**常见误区**：

- **层数 ≠ 表达能力**。真正决定容量的是「非线性 + 宽度」，
  隐藏层宽度 $h$ 才是这一章要调的旋钮（呼应 [ch05 模型容量](../../01_ml_framework/docs/ch05_error_sources.md)）。
- **别拿万能逼近定理当承诺**：它只说「存在一个足够宽的网络能拟合任意连续函数」，
  不保证梯度下降**找得到**它。14.5 里 `h=3` 反而比 `h=2` 差就是活例子。
- **参数量要会数**：$d\to h\to o$ 的两层网络共 $d\cdot h + h + h\cdot o + o$ 个参数。
  本章 XOR 用 $2\to4\to1$，正好 `2*4+4+4+1 = 17` 个 —— 数值梯度检验只扰动 17 个数，很便宜。

**对应练习**：[第 4、12 题](../exercises/ch14_ex.py)（参数初始化与形状、亲手验证线性退化）

---

<a id="c14-03"></a>
### 14.3 前向传播与计算图（Forward Propagation and Computational Graph）

**概念定义**：从 $X$ 一路算到预测 $P$ 和损失 $L$ 叫**前向传播**。
把每一步写成一个节点、箭头表示「谁由谁算出来」，就是**计算图**。
关键动作只有一个：**把中间量存下来（缓存）**，因为 14.4 要倒着用。

**数学形式**（本章的两层网络，隐藏层用 `tanh`、输出层用 `sigmoid`）：

$$Z_1 = XW_1+b_1,\quad A_1=\tanh(Z_1),\quad Z_2=A_1W_2+b_2,\quad P=\sigma(Z_2)$$

$$L = -\frac{1}{n}\sum_i\big[y_i\log P_i + (1-y_i)\log(1-P_i)\big]$$

计算图就是一条链，反向时沿它从右往左走：

```
X ──[Z1=XW1+b1]──[A1=tanh(Z1)]──[Z2=A1W2+b2]──[P=σ(Z2)]──[L=BCE(y,P)]
                        ↑ 缓存 Z1,A1,Z2,P 给反向用
```

**最小代码**：

```python
def forward(X, p):
    Z1 = X @ p["W1"] + p["b1"]
    A1 = np.tanh(Z1)
    Z2 = A1 @ p["W2"] + p["b2"]
    P = sigmoid(Z2)
    return P, (Z1, A1, Z2, P)      # 第二个返回值就是缓存

def bce_loss(y, P):
    P = np.clip(P, 1e-12, 1 - 1e-12)
    yy = np.asarray(y).reshape(-1, 1)
    return float(-np.mean(yy * np.log(P) + (1 - yy) * np.log(1 - P)))
```

**实跑数字**：随机初始化（`default_rng(0)`、`scale=0.5`、偏置全 0）时
$P\approx0.5$、初始 loss `0.6915599`；理论上 $P=0.5$ 的交叉熵正好是 $\ln 2=0.6931472$。
$P=y$ 时 loss `1.0e-12`（clip 后的下限，不是真的 0）。

**常见误区**：

- **不缓存中间量，反向传播就得重算甚至算不出来**。
  PyTorch 的 autograd 做的也是这件事，只是替你自动存了。
- **`y` 要 `reshape(-1, 1)`**。否则 `(n,)` 和 `(n,1)` 广播成 `(n,n)`，
  loss 会悄悄变成一个说不通的数，还不报错 —— 这种 bug 只能靠打印 shape 抓。
- **损失是 mean，梯度就得除以 $n$**，14.4 会再强调一次。

**对应练习**：[第 5、6 题](../exercises/ch14_ex.py)（前向 + 缓存、带 clip 的二元交叉熵）

---

<a id="c14-04"></a>
### 14.4 反向传播：只是把链式法则重复几遍（Backpropagation）

**概念定义**：**从损失出发，沿着计算图从右往左，每经过一个节点就乘一次它的局部导数。**
这就是 [ch02 2.8 说的「一串导数相乘」](../../00_foundations/docs/ch02_math_foundations.md#c02-08)，
一层都不多。本章不引入 Jacobian、不写矩阵微分推导。

**数学形式**：每个箭头只写「 upstream 梯度 × 本地导数」，形状自己会对上：

| 步骤 | 在算什么（人话） | 式子 |
|---|---|---|
| ① 输出层 | BCE + sigmoid 合并后，**预测减真值** | $\frac{\partial L}{\partial Z_2}=\frac{P-y}{n}$ |
| ② 第二层参数 | 上游梯度乘这一层的输入 | $\frac{\partial L}{\partial W_2}=A_1^{\top}dZ_2,\quad db_2=\sum_i dZ_{2,i}$ |
| ③ 传回隐藏层 | 沿 $W_2$ 把梯度搬回去 | $dA_1=dZ_2W_2^{\top}$ |
| ④ tanh 本地导数 | 逐元素乘（$\odot$） | $dZ_1=dA_1\odot(1-A_1^2)$ |
| ⑤ 第一层参数 | 同上 | $\frac{\partial L}{\partial W_1}=X^{\top}dZ_1,\quad db_1=\sum_i dZ_{1,i}$ |

第 ① 步是整个反向传播最值得记住的一条：**`dL/dZ2 = (P - y)/n`**。
看着吓人的 $\log$ 和 $\sigma'$ 刚好约干净了，这不是巧合，是 [ch07](../../02_supervised/docs/ch07_linear_models.md) 里
「Sigmoid + 交叉熵」配对的理由。

**先看一个单样本的手工连乘**（和 ch02 那个 `-8.0` 例子同构）。
取 $x=[0.5,0.3]$、$y=0$、$h=2$、随机参数：

```
P = 0.487414          → dL/dZ2 = 0.487414
dL/dA1 = [-0.110314, -0.052543]      1 - A1² = [0.732175, 0.616305]
dL/dZ1 = [-0.080769, -0.032382]
最后乘上 dZ1/dW1[0,0] = x[0] = 0.5
手工连乘 dL/dW1[0,0] = -0.0403845059
中心差分             = -0.0403845060      差 1.4e-10
```

**最小代码**：

```python
def backward(X, y, p, cache):
    Z1, A1, Z2, P = cache
    n = len(X)
    dZ2 = (P - np.asarray(y).reshape(-1, 1)) / n
    dW2 = A1.T @ dZ2
    db2 = dZ2.sum(axis=0)
    dA1 = dZ2 @ p["W2"].T
    dZ1 = dA1 * (1 - A1 ** 2)          # tanh 的本地导数，逐元素
    dW1 = X.T @ dZ1
    db1 = dZ1.sum(axis=0)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}
```

**数值梯度检验**（[ch04 教的习惯](../../01_ml_framework/docs/ch04_training_steps.md)，这里能救命）：
对 17 个参数逐个做中心差分，与解析梯度比：

| 参数 | 形状 | 最大绝对差 |
|---|---|---|
| `W1` | (2,4) | `6.63e-11` |
| `b1` | (4,) | `8.30e-11` |
| `W2` | (4,1) | `6.34e-11` |
| `b2` | (1,) | `4.56e-12` |

ch04 定的警戒线是 `1e-5`，这里小了五个数量级，说明梯度没写错。

**常见误区**：

- **漏掉 `/n`**：loss 用 `mean` 就得除，漏了等于把学习率偷偷放大 $n$ 倍，
  小数据上会直接发散，而且数值梯度检验**立刻**能抓到。
- **转置写反**：用形状自查 —— `dW1` 必须和 `W1` 同形 `(d,h)`，
  `X.T @ dZ1` 是 `(d,n)@(n,h)=(d,h)`，写成 `dZ1 @ X` 形状就对不上。
- **忘了激活的本地导数**：漏掉 `(1 - A1**2)` 就等于把 tanh 当恒等映射，
  网络退化成 14.2 的线性堆叠。
- **数值梯度检验只检一个参数**：符号错常常只出现在某一层，必须全参数扫一遍。
- **梯度对了 ≠ 一定收敛**：检验只能证明「导数算对」，
  证明不了「能跑到好解」，14.5 的 `h=3` 就是卡在局部最优。

> 和 C++ 的差异：手写反向时把 `A1`、`Z1` 留在作用域里，
> 等价于框架替你保存的 activation。C++ 里你会用 `std::vector<float>` 手动管这些缓冲；
> numpy 里放进一个 tuple 返回即可。另外 `dZ1 = dA1 * (1 - A1**2)` 是逐元素乘，
> 不是 `@` —— [ch02 2.2](../../00_foundations/docs/ch02_math_foundations.md#c02-02) 的老坑。

**对应练习**：[第 7~9 题](../exercises/ch14_ex.py)（手写 backward、单项中心差分、全参数梯度检验）

---

<a id="c14-05"></a>
### 14.5 最小代码：NumPy 两层网络（Two-Layer Network）

**概念定义**：把前面四节拼起来，训练循环还是 [ch04 的三步骤](../../01_ml_framework/docs/ch04_training_steps.md)：
**模型**（两层网络）→ **损失**（二元交叉熵）→ **优化**（梯度下降）。
一个字都不用改，只是 `f_theta` 从 $wx+b$ 换成了四行前向。

```python
def train_network(X, y, h=4, lr=0.5, steps=10000, seed=0, scale=0.5):
    p = init_params(X.shape[1], h, 1, seed, scale)
    hist = []
    for t in range(1, steps + 1):
        _, cache = forward(X, p)          # ① 模型前向
        g = backward(X, y, p, cache)      # ② 损失的梯度
        for k in p:
            p[k] -= lr * g[k]             # ③ 优化
        if t in (1, 100, 500, 2000, 5000, steps):
            hist.append((t, bce_loss(y, forward(X, p)[0])))
    return p, hist
```

**实跑数字**：XOR，120 训练 / 40 验证，`h=4`、`lr=0.5`、10000 步、`seed=0`：

| 步数 | 1 | 100 | 500 | 2000 | 5000 | 10000 |
|---|---|---|---|---|---|---|
| loss | 0.690430 | 0.605464 | 0.124686 | 0.056434 | 0.034795 | **0.023061** |

最终 **train `1.0000` / val `1.0000`**。
同一份数据上 `LogisticRegression` 是 train `0.6917` / val **`0.675`**
（和 [ch08 表里那一行](../../02_supervised/docs/ch08_classical_classifiers.md) 完全一致）。
四个象限的验证点给出 `1.0000 / 1.0000 / 0.0000 / 0.0000`，
在 $21\times21$ 网格上与真 XOR 标签一致率 `0.9546` —— 它确实学到了对角结构，不是背答案。

**隐藏层宽度扫描**（同 `seed=0, lr=0.5`，10000 步）：

| $h$ | 1 | 2 | 3 | 4 | 8 |
|---|---|---|---|---|---|
| val 准确率 | 0.6500 | 0.8250 | **0.7500** | **1.0000** | **1.0000** |
| 参数量 | 5 | 9 | 13 | 17 | 33 |

注意 `h=3` 比 `h=2` 还差：**这不是 bug，是局部最优**。
容量够了不代表梯度下降找得到解，初始化和随机种子在这里影响很大 ——
[ch15 15.4](ch15_activation_init.md#c15-04) 用 20 个种子把这件事量到底：
换初始化确实能救 `seed=0`，但整体成功率没稳定提升，主要瓶颈其实是容量。

**学习率扫描**（`h=4`，10000 步）：

| `lr` | 0.05 | 0.2 | 0.5 | 1.0 | 3.0 | 10.0 |
|---|---|---|---|---|---|---|
| 最终 loss | 0.080649 | 0.039336 | 0.023061 | **0.016587** | 0.022029 | **0.923859** |

`lr=10` 直接发散（val 掉到 `0.6250`）；`lr=20` 跑 200 步 loss 就从 `0.692` 涨到 `1.166`。
和 [ch04 发散判定](../../01_ml_framework/docs/ch04_training_steps.md)、
[ch12 AE 第 8 步 `inf`](../../03_unsupervised/docs/ch12_dimensionality.md#c12-03) 是同一个坑，第三次出现了。

**常见误区**：

- **全批量梯度下降撑不住大数据**：这里 120 个样本一把梭没问题，
  真实图像数据要小批量 + 动量 / Adam，那是 [ch16](ch16_training_dnn.md)。
- **别把这套手写网络直接搬去跑图像**：全连接层把 $224\times224\times3$ 拍平会炸参数量，
  图像要 [ch17 的 CNN](ch17_architectures.md#c17-01)。
  [以图搜图终点](../../06_engineering/README.md) 用的是预训练模型抽 embedding，不是从零训这个。
- **`train/val` 都 1.0 不代表通用**：XOR 只有 2 维、160 个点。
  判断泛化还是要看 [ch05 学习曲线](../../01_ml_framework/docs/ch05_error_sources.md) 和
  [ch06 评估协议](../../01_ml_framework/docs/ch06_evaluation_metrics.md)，别被满分骗了。

**对应练习**：[第 10、11 题](../exercises/ch14_ex.py)（训练到收敛、四象限预测）

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| 双重循环累加加权和 | `X @ W + b`，BLAS + 广播 |
| 手写 `std::vector` 存 activation | `forward` 返回 `(P, cache)` 一个 tuple |
| 手动推每一层导数 | 逐段连乘 + 中心差分当场验 |
| `sum/count` 手写归约 | `dZ2.sum(axis=0)`、`X.T @ dZ1` |
| 框架 `.backward()` 一行 | 现在知道它内部就是本章这 6 行 |

| [ch04 三步骤](../../01_ml_framework/docs/ch04_training_steps.md) | 本章对应 |
|---|---|
| 模型 $f_\theta$ | $P=\sigma(\tanh(XW_1+b_1)W_2+b_2)$ |
| 损失 $L$ | 二元交叉熵（带 clip） |
| 优化 | 全批量梯度下降，梯度由反向传播给出 |

> **最容易踩的 3 个坑**：
> 1. **不加激活函数就堆层** —— 两层线性 = 一层线性，实测差 `1.11e-16`，白堆
> 2. **反向传播漏 `/n` 或漏激活导数** —— 用全参数数值梯度检验抓，别靠肉眼
> 3. **学习率拍脑袋** —— `lr=10` 直接发散，`lr=0.5` 才稳；ch04、ch12、本章三次踩同一个坑

**和实践终点的联系**：以图搜图要「预训练模型抽 embedding」，
本章就是理解那个模型内部在算什么的地基。真做项目时不会手写这些 ——
[ch16](ch16_training_dnn.md) 起换 PyTorch，但到那时 `W1`、`dZ2`、缓存不再是黑箱。

## 练习

本章练习统一在 [`ch14_ex.py`](../exercises/ch14_ex.py)：从数值稳定的 sigmoid 与激活导数、
参数初始化、前向传播与缓存、带 clip 的交叉熵，到**手写反向传播 + 全参数数值梯度检验**、
训练到 XOR 收敛、四象限预测，最后亲手验证「两层线性 = 一层线性」，共 12 题。
**全部只用 numpy，不用任何框架**，跑通所有 `assert` 即过关。

上一篇：[第 12 章 降维与表示](../../03_unsupervised/docs/ch12_dimensionality.md)（第 13 章 `[选读]`，已跳过）
下一篇：[第 15 章 激活函数与初始化](ch15_activation_init.md)
