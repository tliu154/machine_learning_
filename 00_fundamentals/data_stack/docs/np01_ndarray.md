#course/CS #course/数据分析 #topic/Python #type/笔记 
# np01 ndarray：数组的本质

## 1.1 ndarray 是什么

```cpp
// C++ 里你熟悉的东西：一段连续内存 + 固定元素类型
double a[1000];
std::vector<double> v(1000);
```

```python
import numpy as np                # 社区约定俗成的别名，全宇宙都叫 np

a = np.array([1, 2, 3])           # 一维数组
m = np.array([[1, 2, 3],
              [4, 5, 6]])         # 二维（2×3）
```

和 `list` 的本质区别：

| | `list` | `ndarray` |
|---|---|---|
| 元素类型 | 任意（存引用） | **单一 dtype**（存值本身，连续内存） |
| 性能 | 慢（每元素都是 PyObject） | 快（紧挨着的 C 数组，SIMD 加速） |
| 维度 | 只有 1 维（套娃做 2 维） | 原生多维，带 shape |
| 运算 | 逐个循环 | **整体运算** |

**一个 ndarray = 一块连续内存 + dtype + shape + strides**，这就是它快的全部秘密。
写视觉/科学计算，看到 `list of list` 想转 `np.array`，看到双层 for 想找向量化。

## 1.2 创建数组的各种姿势

```python
np.array([1, 2, 3], dtype=np.float64)   # 从 list 转，可指定 dtype
np.zeros(5)                             # [0,0,0,0,0]
np.zeros((3, 4))                        # 3×4 全零矩阵（注意传的是元组）
np.ones((2, 2), dtype=np.int32)
np.full((2, 2), 7)                      # 全是 7
np.eye(3)                               # 单位矩阵
np.arange(10)                           # 像 range：0..9
np.arange(2, 10, 2)                     # 2,4,6,8
np.linspace(0, 1, 5)                    # [0, 0.25, 0.5, 0.75, 1.0]  均匀切 5 点（含端点！）
np.empty(3)                             # 未初始化（值是内存垃圾，别直接用）
np.zeros_like(x)                        # 和 x 同 shape 同 dtype 的全零

np.array([[1, 2], [3, 4]], dtype=np.float32)     # 图像常用 float32
```

> `arange` 用整数步长，`linspace` 用"要几个点"。
> 图像坐标、采样频率这类"均匀取 N 个点"的场景一律 `linspace`。

### dtype —— 没有"默认万能类型"

```python
np.array([1, 2])              # int64
np.array([1.0, 2.0])          # float64
np.array([1, 2.0])            # float64   混了会自动提升
np.zeros(3)                   # float64   ← 注意！不是 int
np.array([1, 2], dtype=np.uint8)    # 0~255，图像像素的标准类型

a.dtype          # 查看
a.astype(np.int32)   # 转换（返回新数组）
```

**整数溢出不会报错，会回绕**（和 C++ 一模一样）：

```python
a = np.array([250], dtype=np.uint8)
a + 10          # array([4], dtype=uint8)   260 % 256 = 4，静默溢出！
```

C++ 党对这个应该很亲切 —— uint8 就是 `unsigned char`。

## 1.3 shape / ndim / size —— 数组的"户口本"

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
m.shape     # (2, 3)   行数×列数
m.ndim      # 2        维数
m.size      # 6        元素总数
m.dtype     # dtype('int64')
len(m)      # 2        第一维的长度（行数）
```

### reshape —— 重新排布（元素不动）

```python
a = np.arange(12)         # 0..11
a.reshape(3, 4)           # 3×4
a.reshape(4, -1)          # -1 = 自动推算 → 4×3
a.reshape(-1)             # 拍平成 1 维
a.reshape(12, 1)          # 列向量（和 (12,) 不一样！）
a.T                       # 转置（二维：行列互换）

m.ravel()                 # 拍平（尽量返回视图）
np.ravel(m)               # 同上
```

> `(3,)` 和 `(3, 1)` 和 `(1, 3)` 是三个不同的东西：
> `(3,)` 一维向量；`(3,1)` 三行一列；`(1,3)` 一行三列。矩阵运算时这个区别经常坑人。

```python
a.reshape(3, 4).T
```

## 1.4 索引与切片 —— ⚠️ 全章最重要：切片是"视图"

```python
m = np.arange(12).reshape(3, 4)
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]])

m[1, 2]        # 6      —— 注意是 m[1, 2]，不是 m[1][2]（虽然后者也行，但慢且丑）
m[0]           # 第一行 array([0,1,2,3])
m[:, 1]        # 第二列 array([1,5,9])   冒号 = 整个维度
m[0:2, 1:3]    # 前两行、第 2~3 列构成的子矩阵
m[-1]          # 最后一行
m[:, -1]       # 最后一列
```

**切片返回视图（view），不是拷贝** —— 就是 ch01 说的"便利贴"语义在数组上的翻版：

```python
sub = m[0:2, 0:2]      # 左上角 2×2
sub[0, 0] = 99
print(m[0, 0])         # 99    ← 原数组被改了！
```

> C++ 对照：你拿到的是 `double*` 指针指向原内存，不是拷贝。
> 修改和被修改都是零拷贝、共享内存的。

想要独立副本：

```python
sub = m[0:2, 0:2].copy()      # 显式 copy，之后随便改
```

**赋值也是这个语义**：

```python
b = a              # ✗ 两个名字指向同一个数组！
b = a.copy()       # ✓
b = a[:]           # ✓（一维时）但二维要用 .copy() 才靠谱
```

## 1.5 花式索引与布尔掩码

### 花式索引（传入下标数组）→ 返回拷贝

```python
a = np.arange(10)
a[[3, 1, 7]]           # array([3, 1, 7])   按给定顺序取

m[[0, 2]]              # 第 0 行和第 2 行（拷贝！和切片不同）
m[[0, 2], [1, 3]]      # (m[0,1], m[2,3]) → array([1, 11])   配对取，不是矩形
m[np.ix_([0, 2], [1, 3])]  # 矩形区域 [[1,3],[9,11]]
```

### 布尔掩码 —— numpy 的灵魂 ⭐

```python
a = np.array([3, -1, 7, -5, 2])

a > 0                  # array([True, False, True, False, True])  逐元素比较
a[a > 0]               # array([3, 7, 2])    筛出正数
a[(a > 0) & (a < 5)]   # array([3, 2])       组合条件
a[a % 2 == 0]          # 偶数

a[a < 0] = 0           # 负数清零（原地修改，这个超常用）
a[a > 5] = 5           # 截断 clip
np.where(a > 0, a, 0)  # 三元：正数保留，否则 0 → 新数组
a.clip(0, 5)           # 等价写法

# np.where 的"下标版"：找位置
np.where(a == 7)       # (array([2]),)   7 在下标 2 处
np.nonzero(a)          # 非零元素的下标
```

> ⚠️ 逻辑运算符是 `&` `|` `~`，**不是 and/or/not**（向量的与或非）。
> 且因为优先级问题，**组合条件必须加括号**：`(a > 0) & (a < 5)`。

这套东西对应 C++ 里你手写的：

```cpp
for (double x : v) if (x > 0 && x < 5) out.push_back(x);
```

一行 `a[(a > 0) & (a < 5)]` 就是它的全部。

### 多维掩码

```python
m = np.arange(12).reshape(3, 4)
m[m % 3 == 0]          # 拍平后筛出所有能被 3 整除的元素（返回一维）
m[m > 5] = 0           # 大于 5 的全部清零
np.where(m > 5, 1, 0)  # 阈值化（二值图！）
```

## 1.6 常用属性/函数速查

```python
a.min(), a.max(), a.sum(), a.mean()
a.argmax(), a.argmin()    # 最大/最小值的下标（不是值！）
a.sort()                  # 原地排序
np.sort(a)                # 返回排序后的新数组
np.argsort(a)             # 排序后的下标顺序 —— 按 a 排序 b 的经典操作
a.unique → np.unique(a)   # 去重（返回排序后的）
np.unique(a, return_counts=True)   # 顺便给计数
np.intersect1d(a, b)      # 交集
np.concatenate([a, b])    # 拼接
np.stack([a, b])          # 堆叠出新维度
```

`np.argsort` 用法（很常用）：

```python
scores = np.array([88, 95, 60])
names = ["涛", "李", "王"]
order = np.argsort(-scores)      # 降序 → [1, 0, 2]
[names[i] for i in order]        # ['李', '涛', '王']
```

---

### 小结

| C++ | numpy |
|---|---|
| `double a[N]` 连续内存 | `ndarray`（多了 shape/stride/广播） |
| `unsigned char` | `np.uint8`（都会静默溢出回绕） |
| 手写 for 筛选 | `a[条件]` 布尔掩码 |
| 指针/引用传内存 | 切片是**视图**；`.copy()` 才是拷贝 |
| 手写比较循环 | `np.where` / `clip` |

下一章：[np02 广播与向量化](np02_broadcast.md)
