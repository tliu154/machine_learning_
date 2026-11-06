#course/CS #course/数据分析 #topic/Python #type/笔记 
# np03 numpy 实战：线性代数、随机与图像

> 最后一章 numpy，重点照顾你的方向：视觉。**OpenCV 的 Python 图像就是 ndarray**。

## 3.1 线性代数

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B                # 矩阵乘
A.dot(B)             # 同上
A.T                  # 转置（视图！）
np.linalg.inv(A)     # 逆矩阵
np.linalg.det(A)     # 行列式
np.linalg.norm(v)    # 向量/矩阵范数
np.linalg.eig(A)     # 特征值/特征向量
np.linalg.svd(A)     # SVD 分解
np.trace(A)          # 迹

# 解线性方程组 Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = np.linalg.solve(A, b)        # [2, 3]   等价手工求逆再乘，但快且稳
np.allclose(A @ x, b)            # True     浮点比较用 allclose，别用 ==
```

> ⚠️ 浮点数比较是老生常谈：**永远 `np.allclose(a, b)`，永远不要 `a == b`**。
> 练习里的 assert 也用这个。

```python
# 最小二乘拟合（直线 y = kx + b）
x = np.array([0, 1, 2, 3, 4])
y = np.array([0.9, 2.1, 2.9, 4.2, 4.8])
k, b = np.polyfit(x, y, 1)       # 一次多项式拟合，返回系数
y_pred = np.polyval([k, b], x)   # 或 k * x + b
```

`polyfit` 做参数拟合 / 相机标定时的直线检测都常用，一行顶 C++ 半页。

## 3.2 随机与统计

```python
rng = np.random.default_rng(0)

data = rng.normal(100, 15, size=10000)    # 模拟 10000 个成绩

data.mean()           # ~100
data.std()            # ~15
np.percentile(data, [25, 50, 75])         # 四分位数
np.median(data)
np.histogram(data, bins=20)               # 直方图（pandas/matplotlib 会用它）
np.corrcoef(a, b)                         # 相关系数矩阵
np.cov(a, b)                              # 协方差
```

**固定种子是可复现的关键** —— 调试视觉算法时，同一组随机测试数据必须每次一样：

```python
rng = np.random.default_rng(42)   # 每次 new 一个带种子的生成器
pts = rng.random((100, 2))
```

## 3.3 ⭐ 图像就是 ndarray（视觉组重点）

OpenCV 读取的图像在 Python 里就是一个三维数组：

```python
# 彩色图 shape = (高 H, 宽 W, 通道 3)，dtype=uint8
img = np.zeros((480, 640, 3), dtype=np.uint8)   # 一张黑色 640×480 彩图

# 灰度图 shape = (H, W)
gray = np.zeros((480, 640), dtype=np.uint8)
```

**约定：shape 前两维是 (行数, 列数) = (高, 宽)，和数学坐标 (x, y) 是反的**：

```python
img[100, 200]              # 第 100 行、第 200 列 → 屏幕坐标约 (x=200, y=100)
img[100, 200] = [255, 0, 0]    # 给这个像素上色（BGR 顺序，OpenCV 惯例）
```

> 坐标反着来是所有初学者的痛：**数组 [y, x]，数学/鼠标 (x, y)**。
> 记不住就在代码里写 `img[y, x]` 让变量名替你记。

不用 OpenCV，纯 numpy 也能演示常见图像操作（这里用 0~255 的 uint8 灰度图）：

```python
gray = np.random.default_rng(1).integers(0, 256, (16, 16)).astype(np.uint8)

# ① 灰度化：加权平均（彩色 → 灰度）
#    (H,W,3) → (H,W)：沿最后一维做加权求和
gray = (color @ np.array([0.114, 0.587, 0.299])).astype(np.uint8)   # BGR 权重

# ② 反色：255 - x
neg = 255 - gray                # uint8 直接整体减，不用循环

# ③ 二值化（阈值分割）
binary = np.where(gray > 127, 255, 0).astype(np.uint8)

# ④ 裁剪 ROI（感兴趣区域）—— 就是切片！
roi = gray[2:10, 3:15]          # 高 2~9、宽 3~14 的矩形区域

# ⑤ 水平翻转
flip_h = gray[:, ::-1]          # 列倒序（视图）

# ⑥ 通道分离（彩图）
b, g, r = color[:, :, 0], color[:, :, 1], color[:, :, 2]

# ⑦ 亮度提升（小心溢出！）
bright = np.clip(gray.astype(np.int16) + 50, 0, 255).astype(np.uint8)
#   uint8 + 50 会回绕（ch01 说过），先升位再 clip 再转回去 —— 图像处理标准三连

# ⑧ 下采样（缩小一半）
small = gray[::2, ::2]          # 隔行隔列取，shape 减半

# ⑨ 逐行/逐列统计
gray.mean(axis=0)               # 每列均值（投影！可做简单目标定位）
(gray > 127).sum(axis=1)        # 每行亮像素数

# ⑩ 归一化到 0~1（喂神经网络前的标准动作）
x = gray.astype(np.float32) / 255.0
```

> ⑦ 是个小陷阱：`uint8 + 50` numpy 2.x 里仍是 uint8 溢出（和 C++ 一样回绕）。
> 涉及"可能越界"的算术，**先 `astype` 升位**。`np.clip` 则保证压回合法区间。

装了 OpenCV 之后的真实版（只是让你混个眼熟）：

```python
import cv2
img = cv2.imread("test.jpg")        # ndarray, (H, W, 3), BGR, uint8
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
resized = cv2.resize(img, (640, 480))
cv2.imwrite("out.png", gray)
# img 就是普通 ndarray，上面所有 numpy 操作随便用
```

## 3.4 性能直觉：为什么必须向量化

同一件事（给 1000 万个数字 +1）的三种写法：

```python
# Python 循环：            ~4 秒
# ndarray 向量化 a + 1：   ~0.01 秒
# 差距 400 倍，而且代码更短
```

原因：ndarray 的循环发生在 C 层，数据是连续内存、SIMD 并行；
Python 的 `for` 每一步都要处理 PyObject 装箱、下标检查、动态分发。

> C++ 党反而最容易"感觉不到痛"——因为你手写循环也很快。
> 但 Python 里**只有向量化才快**，写 for 就是慢 100 倍。
> 判断标准很简单：**数组操作里每出现一个 `for`，先问自己能不能消掉**。

## 3.5 调试三件套

```python
a.shape      # 第一步永远是看形状
a.dtype      # 第二步看类型（uint8 溢出 / int vs float 的坑）
a[:3, :3]    # 第三步打印左上角一小块，肉眼看看对不对

# 广播报错时，心里过一遍规则，手动 reshape 对齐
```

---

### 小结

- 矩阵乘 `@`，解方程 `np.linalg.solve`，浮点比较 `np.allclose`
- 随机数用 `default_rng(种子)`，可复现
- **图像 = (H, W[, C]) 的 uint8 数组**，数组是 [y, x]
- 涉及可能溢出的算术：`astype` 升位 → 运算 → `clip` → 转回 uint8
- 数组操作里每出现一个 for，都要问能不能消掉

下一章：[pd01 Series 与 DataFrame](pd01_dataframe.md)
