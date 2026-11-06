# 第 4 章 训练三步骤（Three Steps of Training）

> 前置：第 1 章 1.3（numpy 数组与广播）、第 2 章 2.3（梯度，凭直觉即可）
> 对应练习：[`ch04_ex.py`](../exercises/ch04_ex.py) ｜ 状态：`[已完成]` ｜ 所属篇：`01_ml_framework/`

**一句话**：所有监督学习都是同三件事 —— **猜一个带空的函数 → 定义「错得有多离谱」→ 按错误的方向把空填上**。
后面无论换成神经网络还是大语言模型，变的只是这三步里塞进去了什么。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [模型（Model）](#c04-01) · [未知参数（Unknown Parameters）](#c04-01) | 4.1 设定模型 |
| [损失函数（Loss Function）](#c04-02) · [均方误差（Mean Squared Error, MSE）](#c04-02) | 4.2 定义损失 |
| [优化（Optimization）](#c04-03) · [梯度下降（Gradient Descent）](#c04-03) · [学习率（Learning Rate）](#c04-03) | 4.3 优化参数 |
| [训练循环（Training Loop）](#c04-04) · [Epoch / 小批量（Mini-batch）](#c04-04) | 4.4 训练循环 |
| [完整流程（Full Pipeline）](#c04-05) · [数据泄漏（Data Leakage）](#c04-05) | 4.5 从三步骤到完整流程 |

### 全章共用的例子

```python
import numpy as np

rng = np.random.default_rng(42)
x = np.linspace(0, 1, 50)
y = 3 * x + 2 + rng.normal(0, 0.05, 50)   # 真实关系：w=3, b=2，加了噪声
```

假装我们不知道 `3` 和 `2`，要让程序自己找出来。全章所有代码拼起来就是一个完整训练脚本。

---

<a id="c04-01"></a>

### 4.1 设定模型（Model with Unknown Parameters）

**概念定义**：模型就是一个**带未知参数的函数**。训练 = 用数据把这些空的数值填出来。
我们猜数据是一条直线，于是写下 $\hat{y} = wx + b$，其中 $w$（权重）和 $b$（偏置）是未知的。

**数学形式**：
$$\hat{y} = f_{\theta}(x) = wx + b,\qquad \theta = \lbrace w, b \rbrace$$

「$\hat{y}$ 是模型的预测，$y$ 是真实值，$\theta$ 是全部未知参数的集合」。
numpy：`y_pred = w * x + b`（**整列一次算完，没有 for**）。

**最小代码**：
```python
def linear_predict(x, w, b):
    return w * x + b

w, b = 0.0, 0.0             # 先随便猜
y_pred = linear_predict(x, w, b)
print(y_pred[:3])           # [0. 0. 0.]  ← 现在模型啥也不会
```

**常见误区**：**「线性模型」指的是对参数线性，不是对 x 线性**。
$\hat{y} = w_1 x + w_2 x^2 + b$ 依然是线性模型（多项式回归），因为未知的 $w_1, w_2$ 都是一次方。
判断标准只有一条：模型对**参数**是不是线性的。

**对应练习**：[第 1 题](../exercises/ch04_ex.py)

> 和 C++ 的差异：C++ 里你会写 `struct Params { double w, b; };` 再配一个函数，
> 改参数得手动改结构体。Python 里先把参数当两个普通浮点数；
> 往后参数一多，统一打包成一个向量 `theta = np.array([w, b])` ——
> **把参数向量化**是所有 ML 框架（PyTorch 的 `parameters()`）的共同起点。

---

<a id="c04-02"></a>

### 4.2 定义损失（Loss Function）

**概念定义**：损失函数把「模型有多差」压缩成**一个标量**。有了这个数，优化才有方向。
回归问题最常用 MSE：所有样本预测误差平方的平均。

**数学形式**：
$$L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2$$

「把每个样本的误差平方，再取平均」。numpy：`np.mean((y - y_pred) ** 2)`。
为什么用平方而不是绝对值：处处可导、对大误差惩罚更重、且这个形式有闭式解（ch07 会讲）。

**最小代码**：
```python
def mse_loss(y, y_pred):
    return float(np.mean((y - y_pred) ** 2))

print(mse_loss(y, linear_predict(x, 0, 0)))   # 很大，因为 y 在 2 附近
print(mse_loss(y, linear_predict(x, 3, 2)))   # 很小，只剩噪声
```

**常见误区**：**损失函数和梯度公式必须配套**。
有人把损失写成 $\frac{1}{2n}\sum(\cdot)^2$（为了消去梯度里的 2），有人写成 $\frac{1}{n}\sum(\cdot)^2$。
本章统一用后者，对应梯度带系数 $-2/n$。**从别处抄梯度公式前，先确认它的 L 怎么定义的**。

**对应练习**：[第 2 题](../exercises/ch04_ex.py)

---

<a id="c04-03"></a>

### 4.3 优化参数（Optimization）

**概念定义**：梯度下降就是「站在当前参数上，往损失下降最快的方向迈一小步，重复」。
方向由梯度给出，步长由**学习率** $\eta$ 控制。

**数学形式**：
$$\frac{\partial L}{\partial w} = -\frac{2}{n}\sum_{i=1}^{n} x_i\left(y_i - \hat{y}_i\right),\qquad
\frac{\partial L}{\partial b} = -\frac{2}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)$$
$$w \leftarrow w - \eta \frac{\partial L}{\partial w},\qquad b \leftarrow b - \eta \frac{\partial L}{\partial b}$$

「梯度是当前参数下损失对每个参数的偏导；负号表示往减小损失的方向走」。

**最小代码**：
```python
def mse_gradients(x, y, w, b):
    err = y - (w * x + b)              # (n,)
    dw = -2 * np.mean(x * err)
    db = -2 * np.mean(err)
    return dw, db

def gradient_step(x, y, w, b, lr):
    dw, db = mse_gradients(x, y, w, b)  # 用【旧】参数一次算完两个梯度
    return w - lr * dw, b - lr * db     # 再一起更新

w, b = gradient_step(x, y, 0.0, 0.0, lr=0.1)
print(w, b)                             # 离 3 和 2 近了一步
```

**常见误区**：**学习率是最该先调的那个数**。
`lr` 太小几百轮看不出动静，太大会一步跨过最优点、损失越跑越大甚至 `inf`。
同一份数据 `lr=0.1` 收敛，`lr=10` 直接发散 —— 练习里让你亲手看一次。
另一个坑：梯度要**用同一组旧参数算完再一起更新**，别边更新边算（后面换成数值梯度或 autograd 时会立刻出错）。

**对应练习**：[第 3、4、5、10 题](../exercises/ch04_ex.py)（第 5 题即本节的梯度检验）

> 和 C++ 的差异：C++ 里这一步是双重循环累加 Σ；numpy 里是 `np.mean(x * err)`，
> 一行搞定且底层 SIMD。**代价是形状错了不会编译报错**，只在运行时给你一个诡异的结果 ——
> 所以 ML 代码里 `print(x.shape)` 出现频率极高。

#### 工程手段：数值梯度检验（Gradient Checking）

写解析梯度最容易犯的是符号错、系数错。用一个不依赖推导的办法验一遍：

$$\frac{\partial L}{\partial \theta} \approx \frac{L(\theta + \varepsilon) - L(\theta - \varepsilon)}{2\varepsilon}$$

```python
def numerical_gradient(x, y, w, b, eps=1e-6):
    dw = (mse_loss(y, linear_predict(x, w + eps, b))
          - mse_loss(y, linear_predict(x, w - eps, b))) / (2 * eps)
    db = (mse_loss(y, linear_predict(x, w, b + eps))
          - mse_loss(y, linear_predict(x, w, b - eps))) / (2 * eps)
    return dw, db

print(mse_gradients(x, y, 1.0, 0.5))       # 解析
print(numerical_gradient(x, y, 1.0, 0.5))  # 数值，应该几乎一样
```

两个值差到 1e-5 以上，就是解析梯度写错了。这个习惯在 ch14 手写反向传播时能救命。

---

<a id="c04-04"></a>

### 4.4 训练循环（Training Loop）

**概念定义**：把「预测 → 算损失 → 算梯度 → 更新」重复很多次，直到损失不再下降。
跑完一轮**全部**训练数据叫一个 **epoch**；数据太多时每次只取一小批叫 **mini-batch**。

**数学形式**：本节无新公式，只是把 4.1~4.3 装进一个循环。

**最小代码**：
```python
def train_linear(x, y, lr=0.1, epochs=500, w0=0.0, b0=0.0):
    w, b = w0, b0
    losses = []
    for _ in range(epochs):
        loss = mse_loss(y, linear_predict(x, w, b))
        losses.append(loss)             # 记录【更新前】的损失
        dw, db = mse_gradients(x, y, w, b)
        w, b = w - lr * dw, b - lr * db
    return w, b, losses

w, b, losses = train_linear(x, y)
print(round(w, 2), round(b, 2))         # 约 3.0, 2.0
print(losses[0], losses[-1])            # 损失从大变小
```

小批量用生成器写最自然（基础教程 ch08 讲过 `yield`）：

```python
def batch_iterator(x, y, batch_size, shuffle=False, seed=42):
    idx = np.arange(len(x))
    if shuffle:
        np.random.default_rng(seed).shuffle(idx)
    for start in range(0, len(idx), batch_size):
        sel = idx[start:start + batch_size]
        yield x[sel], y[sel]

for xb, yb in batch_iterator(x, y, 16, shuffle=True):
    w, b = gradient_step(xb, yb, w, b, lr=0.05)
```

**常见误区**：**记录 loss 要在参数更新之前**。
放在更新之后，曲线第一项就是「已经走了一步」的损失，和后面的 epoch 对不齐，看收敛会误判。
还有：**收敛不等于损失降到 0** —— 数据里有噪声时，损失会停在噪声方差附近，这是正常的。

**对应练习**：[第 6、7、9 题](../exercises/ch04_ex.py)

---

<a id="c04-05"></a>

### 4.5 从三步骤到完整流程（From Training to Full Pipeline）

**概念定义**：三步骤是引擎，真实项目还要在前后各接一段：

```
划分数据 → 预处理 → 【模型 → 损失 → 优化】循环 → 验证评估 → 保存 → 推理
```

**最小代码**（骨架，细节留给 ch05 / ch06 / ch20）：

```python
# 1. 划分（先划分，再 fit 预处理器！）
n = len(x); k = int(0.8 * n)
x_tr, y_tr, x_va, y_va = x[:k], y[:k], x[k:], y[k:]

# 2. 只在训练集上算均值/标准差
mu, sigma = x_tr.mean(), x_tr.std()
x_tr_s, x_va_s = (x_tr - mu) / sigma, (x_va - mu) / sigma

# 3. 训练三步骤
w, b, losses = train_linear(x_tr_s, y_tr, lr=0.1, epochs=500)

# 4. 验证
print("val MSE:", mse_loss(y_va, linear_predict(x_va_s, w, b)))
```

**常见误区**：**数据泄漏（Data Leakage）** —— 先在全量数据上算 `mu/sigma` 再划分，
测试集的信息就悄悄进了训练过程，验证分数会虚高。
**凡是「从数据里学出来的量」（均值、方差、编码器、特征选择器），都只能在训练集上 fit**。
这是初学者最常犯、也最难自己发现的错，ch06 还会专门量化它。

**对应练习**：[第 8 题（标准化，注意全相等时的除零）](../exercises/ch04_ex.py)

### 三步骤在后面各章长什么样

| | 本章（线性模型） | ch07~ch10 经典算法 | ch14~ch17 神经网络 | ch18~ch19 LLM |
|---|---|---|---|---|
| 模型 $f_\theta$ | $wx + b$ | 树 / 核函数 / 集成 | 多层非线性网络 | Transformer |
| 损失 $L$ | MSE / 交叉熵 | hinge / 对数损失 | 交叉熵 + 正则 | 下一个 token 的交叉熵 |
| 优化 | 手写梯度下降 | 闭式解 / 贪心分裂 | **反向传播 + Adam** | AdamW + 分布式 |
| 参数量 | 2 | 几百~几万 | 百万~亿 | 十亿以上 |

**看穿这张表，后面所有章节都只是在换格子里的东西。**

---

## 小结

| C++ / 已有认知 | 本章写法 |
|---|---|
| `struct Params` + 手写函数 | 参数先是两个 float，往后打包成向量 |
| 双重循环算 Σ | `np.mean(x * err)` 向量化 |
| 编译期检查类型形状 | 运行时才炸，`print(shape)` 是日常 |
| `for` 里手动更新变量 | 训练循环 = 三步骤的重复 |
| 断言验证逻辑 | 数值梯度检验验证数学 |

> **最容易踩的 3 个坑**：
> 1. 损失函数和梯度公式**不配套**（`1/n` 还是 `1/(2n)`）
> 2. 学习率太大直接发散，且不会报错，只会 `inf`
> 3. 先在全量数据上标准化再划分 → 数据泄漏，分数虚高

## 练习

本章练习统一在 [`ch04_ex.py`](../exercises/ch04_ex.py)：从模型前向、损失、解析梯度、
梯度检验，到完整训练循环和发散判定，共 10 题。跑通所有 `assert` 即过关。

上一篇：第 3 章 机器学习是什么（待写，见 [SYLLABUS](../../SYLLABUS.md)）
下一篇：第 5 章 误差来源与模型选择（待写，见 [SYLLABUS](../../SYLLABUS.md)）
