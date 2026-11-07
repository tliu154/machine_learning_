# 第 4 篇 无监督学习（Unsupervised Learning）

**章号 11~13** ｜ 前置：[ch05 误差诊断](../01_ml_framework/docs/ch05_error_sources.md)、
[ch06 评估指标](../01_ml_framework/docs/ch06_evaluation_metrics.md)、
[ch10 特征缩放](../02_supervised/docs/ch10_feature_engineering.md)

章节清单与状态看 [SYLLABUS 第 4 篇](../SYLLABUS.md)。原框架把聚类和降维塞在「经典算法」末尾，
这次按学习依赖独立成篇 —— 没有标签之后，「什么叫好」这件事本身要重新定义。

## 本篇的核心难点

- **没有真值，指标就不可靠**：轮廓系数、肘部法都只是启发式，要讲清它们的局限
- **尺度决定一切**：K-means、PCA 对特征缩放极度敏感，先标准化再谈结果
- **降维 ≠ 丢信息**：PCA 是从方差角度做投影，t-SNE/UMAP 是保局部结构做可视化，别混用

## 练习设计方向

- ch11：手工迭代一轮 K-means 验证质心更新；在环形数据上看 K-means 如何失败、DBSCAN 如何成功
- ch12：PCA 手写（协方差 → 特征值分解）对照 sklearn；观察解释方差比
- ch13：[选读] 用 Isolation Forest 做异常检测，画决策边界

## 取舍说明

第 13 章标为 `[选读]`，密度估计/关联规则在视觉方向用得少。
真遇到项目需求再写，别为了目录完整而提前铺开。
