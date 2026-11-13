# 第 4 篇 无监督学习（Unsupervised Learning）

**章号 11~13** ｜ 前置：[ch05 误差诊断](../01_ml_framework/docs/ch05_error_sources.md)、
[ch06 评估指标](../01_ml_framework/docs/ch06_evaluation_metrics.md)、
[ch10 特征缩放](../02_supervised/docs/ch10_feature_engineering.md)

章节清单与状态看 [SYLLABUS 第 4 篇](../SYLLABUS.md)。原框架把聚类和降维塞在「经典算法」末尾，
这次按学习依赖独立成篇 —— 没有标签之后，「什么叫好」这件事本身要重新定义。

## 已完成：第 11 章 聚类（docs/ + exercises/）

[ch11 教学](docs/ch11_clustering.md) + [ch11 练习](exercises/ch11_ex.py)，12 题，参考答案通过自测。
4 节：K-means、层次聚类（三种 linkage）、DBSCAN、聚类评估与簇数选择；
**全部只用 numpy**，教学里的 sklearn 对照代码需 `pip install scikit-learn`。

本章刻意把「指标会把错结果夸成更好」做成可复现的实测：两同心环上 K-means
ARI ≈ 0 却拿到更高的轮廓系数（`0.3280` vs DBSCAN `0.1574`），缩放前后准确率 `0.5000 → 1.0000`。

> ⚠️ `exercises/ch11_ex.py` 与 `00_foundations/python_basics/exercises/ch11_ex.py`
> （基础教程「模块与包」）撞名，内容完全不同，按完整路径打开。

## 已完成：第 12 章 降维与表示（docs/ + exercises/）

[ch12 教学](docs/ch12_dimensionality.md) + [ch12 练习](exercises/ch12_ex.py)，12 题，参考答案通过自测。
4 节：PCA（协方差 → 特征值分解 → 解释方差比 / 重构误差恒等式 / 白化）、
t-SNE 与 UMAP（KL 梯度 + 保邻域率）、自编码器（线性 AE ≡ PCA）、
**降维的工程收益**（以图搜图里 64→16 维 recall@5 `0.740→0.700`、计算量 `1/4`）。
**全部只用 numpy**；教学里的 sklearn 对照代码需 `pip install scikit-learn`。

结构备注：12.4 是撰写时补入的第 4 节（原骨架 3 节），把实践轨道的召回率 / 计算量权衡
独立成节便于跳转。数学部分照顾基础薄弱：特征值、KL 梯度都配了读法与人话，不写推导；
线性 AE 只用 ch02 链式法则 + ch04 梯度下降，反向传播留给第 14 章。

> ⚠️ `exercises/ch12_ex.py` 与 `00_foundations/python_basics/exercises/ch12_ex.py`
> （基础教程「递归」）撞名，内容完全不同，按完整路径打开。

## 本篇的核心难点

- **没有真值，指标就不可靠**：轮廓系数、肘部法都只是启发式，要讲清它们的局限
- **尺度决定一切**：K-means、PCA 对特征缩放极度敏感，先标准化再谈结果
- **降维 ≠ 丢信息**：PCA 是从方差角度做投影，t-SNE/UMAP 是保局部结构做可视化，别混用

## 练习设计方向

- [ch11](exercises/ch11_ex.py)（已完成）：手工迭代一轮 K-means 验证质心更新；在环形数据上看 K-means 如何失败、DBSCAN 如何成功
- [ch12](exercises/ch12_ex.py)（已完成）：PCA 手写（协方差 → 特征值分解）对照 sklearn；观察解释方差比与重构误差恒等式；跑降维检索的 recall / 计算量权衡
- ch13：[选读] 用 Isolation Forest 做异常检测，画决策边界

## 取舍说明

第 13 章标为 `[选读]`，密度估计/关联规则在视觉方向用得少。
真遇到项目需求再写，别为了目录完整而提前铺开。
