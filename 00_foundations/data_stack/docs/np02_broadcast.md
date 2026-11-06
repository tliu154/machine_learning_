#course/CS #course/数据分析 #topic/Python #type/笔记 
# np02 广播与向量化 —— 干掉 for 循环

## 2.1 向量化：整个数组一起算

```cpp
// C++：你写过一万遍的循环
for (int i = 0; i < n; ++i) c[i] = a[i] + b[i];
```

```python
# numpy：一行，底层是 C + SIMD
c = a + b
```

**所有算术运算符都是逐元素的**：

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b        # [11, 22, 33]
a * b        # [10, 40, 90]   ← 是逐元素乘，不是矩阵点积！
a ** 2       # [1, 4, 9]
a / b        # [0.1, 0.1, 0.1]
a % 2        # [1, 0, 1]
a > b        # [False, False, False]
-a           # [-1, -2, -3]
np.exp(a) / np.log(b) / np.sqrt(a) / np.abs(a) / np.sin(a)   # ufunc 家族
```

> ⚠️ **矩阵乘法是 `@` 不是 `*`**：
> ```python
> A @ B      # 矩阵点积
> A.dot(B)   # 同上
> A * B      # 逐元素（shape 不同会广播或报错）—— 别搞混
> ```

## 2.2 广播（Broadcasting）—— 小数组"自动膨胀"

形状不同的数组运算时，numpy 按规则自动对齐 —— 这是它最强大的机制。

```python
a = np.array([[0, 0, 0],
              [10, 10, 10]])      # shape (2, 3)
b = np.array([1, 2, 3])           # shape (3,)

a + b
# array([[ 1,  2,  3],
#        [11, 12, 13]])            b 被当成两行都加，实际没复制内存
```

对照你的直觉：这就像 C++ 里 `for each row: row + b`，但**零循环零拷贝**。

### 广播规则（背下来）

两个数组从**最后一维向前**逐维比较：

1. 维度相等 → OK
2. 其中一个是 1 → 该维"拉伸"成另一个的长度 → OK
3. 其它情况 → 报错

```
(2, 3) + (3,)     → (3,) 视作 (1, 3) → 拉伸 → (2, 3)  ✓
(2, 3) + (2, 1)   → 第二维 1 拉成 3    → (2, 3)      ✓
(2, 3) + (2,)     → (2,) 视作 (1,2)，第二维 2 vs 3    ✗ ValueError
(3, 1) + (1, 4)   → 双向拉伸           → (3, 4)      ✓
(5,)   + ()       → 标量全员广播                      ✓
```

经典应用 —— 列向量 + 行向量 = 网格：

```python
rows = np.arange(3).reshape(3, 1)    # [[0],[1],[2]]
cols = np.arange(4).reshape(1, 4)    # [[0,1,2,3]]
rows + cols                           # 3×4 的加法表，广播双向拉伸
rows * 10 + cols
```

### 常见坑

```python
a = np.ones((3, 4))
a + np.array([1, 2, 3])     # ✗ 报错！(4) vs (3,4) 最后一维 4≠3
a + np.array([1, 2, 3]).reshape(3, 1)   # ✓ 想按行加，先整成列向量
```

> 排查形状问题的万能三步：`print(a.shape)` → 心里过一遍广播规则 → 手动 reshape 对齐。
> **(n,) 和 (n,1) 不等价**，broadcast 时表现完全不同，这是新手错误第一名。

## 2.3 axis —— 聚合沿哪个方向

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])     # shape (2, 3)
```

```python
m.sum()          # 21           全部加起来
m.sum(axis=0)    # [5, 7, 9]    沿行的方向压 → 每列一个和（结果 shape (3,)）
m.sum(axis=1)    # [6, 15]      沿列的方向压 → 每行一个和（结果 shape (2,)）
m.mean(axis=0)   # [2.5, 3.5, 4.5]  每列均值
m.max(axis=1)    # [3, 6]       每行最大
m.argmax(axis=1) # [2, 2]
m.cumsum()       # 累加 [1,3,6,10,15,21]
m.std() / m.var()  # 标准差 / 方差
```

**记忆法：axis=k 就是"第 k 个下标被消掉"**。

- `sum(axis=0)`：结果的第 0 个下标没了 → 剩 (3,) → 每列一个数
- `sum(axis=1)`：第 1 个下标没了 → 剩 (2,) → 每行一个数

所有聚合函数都有个保底参数 `keepdims`：

```python
m.sum(axis=1, keepdims=True)    # shape (2, 1)，方便继续广播
```

## 2.4 拼接与拆分

```python
a = np.arange(6).reshape(2, 3)
b = np.ones((2, 3))

np.concatenate([a, b], axis=0)     # 上下拼 → (4, 3)   像 vstack
np.concatenate([a, b], axis=1)     # 左右拼 → (2, 6)   像 hstack
np.vstack([a, b])                  # 竖着堆 = axis=0
np.hstack([a, b])                  # 横着堆 = axis=1
np.stack([a, b])                   # 新增一维 → (2, 2, 3)  注意和 vstack 不同！

np.split(a, 2, axis=0)             # 切两份 → [array, array]
np.hsplit(a, 3)                    # 按列切 3 份
```

> `stack` vs `vstack`：
> `stack` 把 n 个 (2,3) 变成 (n,2,3) —— **多了一层**；
> `vstack` 把 n 个 (2,3) 变成 (n·2, 3) —— 平铺。
> 把一组同形状数组"叠成一摞"用 `stack`。

## 2.5 随机数（np.random）

```python
rng = np.random.default_rng(42)    # 现代写法：显式生成器 + 种子（可复现）

rng.integers(0, 10, size=5)                # 5 个 [0,10) 整数
rng.random(5)                             # 5 个 [0,1) 均匀浮点
rng.random((3, 4))                        # 3×4
rng.normal(0, 1, size=1000)               # 正态分布 (均值, 标准差)
rng.uniform(-5, 5, 100)                   # 均匀分布
rng.shuffle(arr)                          # 原地打乱
rng.permutation(10)                       # 返回打乱副本
rng.choice([1,2,3], size=5, replace=True, p=[.1,.2,.7])   # 加权抽样
```

> 老教程里的 `np.random.seed(42)` + `np.random.rand()` 是旧全局风格，能用但过时；
> 新代码用 `default_rng` —— 种子跟着生成器走，不污染全局状态。

## 2.6 向量化重构实战

一个真实重构例子（视觉方向常见）—— 灰度图阈值分割：

```python
# ✗ C++ 思维的 Python（能用，但慢、丑）
out = np.zeros_like(gray)
for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        if gray[i, j] > 127:
            out[i, j] = 255
        else:
            out[i, j] = 0

# ✓ numpy 正确姿势
out = np.where(gray > 127, 255, 0).astype(np.uint8)
# 或者
out = ((gray > 127) * 255).astype(np.uint8)
```

再如 —— 一组点绕原点旋转 30°：

```python
theta = np.deg2rad(30)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
pts = rng.random((1000, 2))       # 1000 个点
rotated = pts @ R.T               # 一行旋转全部点！(1000,2)@(2,2)
```

> `pts @ R.T`：1000 个点各自的旋转，全在一次矩阵乘法里完成。
> C++ 里这是双层循环 × 4 次乘加；numpy 里是 BLAS 调用。

---

### 小结

| 你想干的事 | numpy 写法 |
|---|---|
| 逐元素运算 | 直接 `+ - * /`（`*` 是逐元素！） |
| 矩阵乘 | `A @ B` |
| 小数组作用到大数组 | 广播（规则：尾维对齐，1 可拉伸） |
| 每行/每列求和 | `sum(axis=)`，第 k 个下标被消掉 |
| 条件筛选 | `a[mask]`、`np.where` |
| 一摞数组堆叠 | `np.stack`（新增维度）/ `vstack`（平铺） |
| 随机数 | `rng = np.random.default_rng(seed)` |

下一章：[np03 实战与图像](np03_practice.md)
