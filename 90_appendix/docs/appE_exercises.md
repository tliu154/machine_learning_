# 附录 E 练习索引（Exercise Index）

全仓库 **32 份**练习的总入口。**这里只放链接，不重复存答案** —— 参考答案统一留在各
`chNN_ex.py` 末尾的 `# region 参考答案` / `# endregion` 之间（PyCharm 里可折叠），
改答案只改那一处，不用同步两个地方。

- **单份跑法**：打开练习文件右键 Run，看到 `chNN 全部通过 ✓` 即过关
- **全部跑法**：仓库根执行 `python tools/verify_all.py`（同时验答案、相对链接、显式锚点）
- 写新练习的约定见 [CONTRIBUTING.md](../../CONTRIBUTING.md)，章节状态以 [SYLLABUS.md](../../SYLLABUS.md) 为准

> ⚠️ **章号撞名**：`00_foundations/python_basics/exercises/` 里的 `ch01`~`ch12` 是
> **Python 基础教程自己的章号**，与 ML 全局章号（ch04 训练三步骤、ch06 评估指标……）毫无关系。
> 两套 `ch04_ex.py` / `ch06_ex.py` / `ch07_ex.py` / `ch11_ex.py` / `ch12_ex.py` 等内容完全不同，
> **按下面的完整路径打开，别只搜文件名**。ML 侧练习的 docstring 里也写了这句区分说明。

---

## 第 1 篇 基础工具（`00_foundations/`）

### 数据栈三件套（对应 1.3~1.5 节）

| 练习 | 主题 |
|---|---|
| [np01_ex.py](../../00_foundations/data_stack/exercises/np01_ex.py) | ndarray、dtype、切片视图、布尔掩码 |
| [np02_ex.py](../../00_foundations/data_stack/exercises/np02_ex.py) | 广播规则、`axis`、逐元素乘 vs 矩阵乘 |
| [np03_ex.py](../../00_foundations/data_stack/exercises/np03_ex.py) | numpy 实战与图像：`uint8` 防溢出三连 |
| [pd01_ex.py](../../00_foundations/data_stack/exercises/pd01_ex.py) | Series / DataFrame、`loc` / `iloc`、缺失值 |
| [pd02_ex.py](../../00_foundations/data_stack/exercises/pd02_ex.py) | `groupby().agg()` / `transform()`、merge |
| [plt01_ex.py](../../00_foundations/data_stack/exercises/plt01_ex.py) | 面向对象画图、Agg 无头后端、中文显示 |

### Python 基础语法（对应 1.1 节，自带章号）

| 练习 | 主题 | 练习 | 主题 |
|---|---|---|---|
| [ch01](../../00_foundations/python_basics/exercises/ch01_ex.py) | 从 C++ 到 Python | [ch02](../../00_foundations/python_basics/exercises/ch02_ex.py) | 数字与运算 |
| [ch03](../../00_foundations/python_basics/exercises/ch03_ex.py) | 字符串 | [ch04](../../00_foundations/python_basics/exercises/ch04_ex.py) | 列表与元组 |
| [ch05](../../00_foundations/python_basics/exercises/ch05_ex.py) | 字典与集合 | [ch06](../../00_foundations/python_basics/exercises/ch06_ex.py) | 控制流 |
| [ch07](../../00_foundations/python_basics/exercises/ch07_ex.py) | 函数 | [ch08](../../00_foundations/python_basics/exercises/ch08_ex.py) | 迭代器与生成器 |
| [ch09](../../00_foundations/python_basics/exercises/ch09_ex.py) | 文件与异常 | [ch10](../../00_foundations/python_basics/exercises/ch10_ex.py) | 类与面向对象 |
| [ch11](../../00_foundations/python_basics/exercises/ch11_ex.py) | 模块与包 | [ch12](../../00_foundations/python_basics/exercises/ch12_ex.py) | 递归 |

### 数学基础（对应第 2 章）

| 练习 | 章 | 主题 |
|---|---|---|
| [ch02_ex.py](../../00_foundations/exercises/ch02_ex.py) | 第 2 章 | 向量/矩阵与 `@`、频率收敛、贝叶斯后验、均值方差与 `ddof`、中心差分与偏导、MSE 梯度、负梯度最陡下坡、链式法则数值验证 |

配套速查表：[appendix_cheatsheet.md](../../00_foundations/data_stack/docs/appendix_cheatsheet.md)。

---

## 第 2 篇 机器学习基础框架（`01_ml_framework/`）

| 练习 | 章 | 主题 |
|---|---|---|
| [ch03_ex.py](../../01_ml_framework/exercises/ch03_ex.py) | 第 3 章 | 学阈值 vs 手写规则、漂移后重学、自监督伪标签、2-means、任务类型、自训练 |
| [ch04_ex.py](../../01_ml_framework/exercises/ch04_ex.py) | 第 4 章 | 训练三步骤：前向、MSE、解析/数值梯度、训练循环、发散判定 |
| [ch05_ex.py](../../01_ml_framework/exercises/ch05_ex.py) | 第 5 章 | 多项式与 Ridge、偏差—方差分解、阶数扫描、K 折 CV、外推灾难、误差诊断 |
| [ch06_ex.py](../../01_ml_framework/exercises/ch06_ex.py) | 第 6 章 | 评估指标：混淆矩阵、P/R/F1、ROC-AUC、回归四指标、业务代价、泄漏量化 |

## 第 3 篇 监督学习（`02_supervised/`）

| 练习 | 章 | 主题 |
|---|---|---|
| [ch07_ex.py](../../02_supervised/exercises/ch07_ex.py) | 第 7 章 | 线性模型：正规方程、Sigmoid / 交叉熵、Ridge、R² |
| [ch08_ex.py](../../02_supervised/exercises/ch08_ex.py) | 第 8 章 | 经典分类：KNN、基尼/熵、递归决策树、RBF 核 |
| [ch09_ex.py](../../02_supervised/exercises/ch09_ex.py) | 第 9 章 | 集成方法：Bagging 投票、Bootstrap、梯度提升残差 |
| [ch10_ex.py](../../02_supervised/exercises/ch10_ex.py) | 第 10 章 | 特征工程：fit/apply 分离、编码、IQR 裁剪、亲手量化泄漏 |

## 第 4 篇 无监督学习（`03_unsupervised/`）

| 练习 | 章 | 主题 |
|---|---|---|
| [ch11_ex.py](../../03_unsupervised/exercises/ch11_ex.py) | 第 11 章 | 聚类：距离矩阵、K-means 分配/更新/收敛、缩放前后对比、三种 linkage、DBSCAN 与 eps 扫描、轮廓系数与 K 扫描 |
| [ch12_ex.py](../../03_unsupervised/exercises/ch12_ex.py) | 第 12 章 | 降维：协方差与特征值分解、解释方差比、投影/重构恒等式、白化、保邻域率、Student-t Q 与 KL 梯度、线性 AE 收敛到 PCA、降维检索 recall |

## 第 5 篇 深度学习（`04_deep_learning/`）

| 练习 | 章 | 主题 |
|---|---|---|
| [ch14_ex.py](../../04_deep_learning/exercises/ch14_ex.py) | 第 14 章 | 神经网络基础：数值稳定激活与导数、参数初始化、前向缓存、BCE、手写反向传播、全参数数值梯度检验、XOR 收敛、两层线性退化 |
| [ch15_ex.py](../../04_deep_learning/exercises/ch15_ex.py) | 第 15 章 | 激活函数与初始化：Sigmoid 导数上界与饱和、Leaky ReLU / GELU、8 层前向 std 与逐层梯度范数、梯度消失 / 爆炸量化、死 ReLU、Xavier / He、复现 ch14 卡住的 `seed=0` |
| [ch16_ex.py](../../04_deep_learning/exercises/ch16_ex.py) | 第 16 章 | 训练深度网络：SGD / Momentum / Adam 更新式与偏差修正、cosine / step 调度、BatchNorm / LayerNorm、running stats、inverted dropout、残差恒等支路、用几何平均判断逐层放大 |

---

## 约定

1. 每章**一份**练习文件，节内只放题号链接，不拆成碎片文件
2. 函数桩留 `# TODO` + `return None`，底部 `assert` 覆盖正常输入与边界
3. 参考答案放 `# region 参考答案` 的三引号块里，**反斜杠只写一份**
4. 数据现场生成、固定 `default_rng(42)`、不依赖仓库外文件
5. **练习一律不 import sklearn**；库对照只出现在教学文档里，并标注 `pip install scikit-learn`
