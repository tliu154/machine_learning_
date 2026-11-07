# 教学大纲（Syllabus）· 完整骨架

**本文件是整个仓库唯一的章节清单与状态源。** 各篇 README 只写定位和实践方向，
章节增删、状态更新一律改这里，避免多处重复维护。

- 学习依赖顺序：**基础工具 → ML 框架 → 经典算法 → 深度学习 → 现代 LLM → 工程实践 → 专题**
- 章号 0~23 保持稳定，作为跨文件引用的唯一标识；篇只是分组，不参与编号
- 每章只有真正开写时才建 `.md` 文件；本文件里的「文件」列是**预定路径**，不是现存文件

状态：`[已完成]` 教学+练习+自测通过 ｜ `[部分完成]` 只有部分节 ｜ `[待迁移]` 内容写过但不在仓库 ｜
`[待写]` 仅规划 ｜ `[选读]` 低优先级

---

## 第 1 篇 基础工具与数学直觉 → `00_foundations/`

前置：无。目标：能用 Python 数据栈把一串数字变成一张图。

### 第 0 章 前言与使用说明（Preface） · [已落地]

> 不单独建章文件，拆到三处：`README.md`（定位/读者/路径图）、`CONTRIBUTING.md`（模板与规范）、`NOTATION.md`（符号与术语）

**本章子概念索引：** 文档结构（Document Structure）· 学习路径（Learning Path）· 笔记模板（Note Template）· 数学符号约定（Mathematical Notation）

### 第 1 章 Python 与数据栈（Python and Data Stack） · [部分完成]

> 文件：`00_foundations/docs/ch01_python_data_stack.md`（索引页） ｜ 练习：见 `data_stack/exercises/`

**本章子概念索引：** Python 基础语法（Python Basics）· Jupyter Notebook 与环境配置（Environment Setup）· NumPy 数组（NumPy Arrays）· pandas 数据框（DataFrame）· Matplotlib / Seaborn 可视化（Visualization）· Git 与 GitHub（Version Control）

| 节 | 概念 | 状态 | 现有内容 |
|---|---|---|---|
| 1.1 | Python 基础语法 | [已完成] | [python_basics/](00_foundations/python_basics/README.md) 13 篇教学 + 12 份练习 |
| 1.2 | Jupyter / venv / uv / Git | [待写] | — |
| 1.3 | NumPy 数值数组 | [已完成] | `data_stack/docs/np01~np03_*.md` + 3 份练习 |
| 1.4 | pandas 表格处理 | [已完成] | `data_stack/docs/pd01~pd02_*.md` + 2 份练习 |
| 1.5 | Matplotlib 可视化 | [已完成] | `data_stack/docs/plt01_plot.md` + 1 份练习 |
| 1.6 | 最小实践：加载 → 清洗 → 计算 → 可视化 | [待写] | — |

### 第 2 章 数学基础（Mathematical Foundations） · [待写]

> 文件：`00_foundations/docs/ch02_math_foundations.md` ｜ 练习：`ch02_ex.py`

**本章子概念索引：** 向量与矩阵（Vectors and Matrices）· 矩阵乘法（Matrix Multiplication）· 概率分布（Probability Distribution）· 条件概率与贝叶斯（Conditional Probability and Bayes）· 期望与方差（Expectation and Variance）· 导数与偏导（Derivative）· 梯度（Gradient）· 链式法则（Chain Rule）

**节骨架：** 2.1 线性代数直觉 ｜ 2.2 概率与统计直觉 ｜ 2.3 微积分与梯度 ｜ 2.4 数学在 ML 中的位置

---

## 第 2 篇 机器学习基础框架 → `01_ml_framework/`

前置：第 1 篇。**整个教程最重要的一篇**：算法会过时，判断力不会。

### 第 3 章 机器学习是什么（What is Machine Learning） · [待写]

> 文件：`ch03_what_is_ml.md` ｜ 练习：`ch03_ex.py`

**本章子概念索引：** 监督学习（Supervised Learning）· 无监督学习（Unsupervised Learning）· 半监督（Semi-supervised）· 自监督（Self-supervised）· 强化学习（Reinforcement Learning）· 分类（Classification）· 回归（Regression）· 结构化学习（Structured Learning）

**节骨架：** 3.1 定义 ｜ 3.2 学习范式 ｜ 3.3 任务类型 ｜ 3.4 传统编程 vs. 机器学习

### 第 4 章 训练三步骤（Three Steps of Training） · [已完成]

> [教学](01_ml_framework/docs/ch04_training_steps.md) · [练习](01_ml_framework/exercises/ch04_ex.py)

**本章子概念索引：** 模型（Model）· 未知参数（Unknown Parameters）· 损失函数（Loss Function）· 优化（Optimization）· 梯度下降（Gradient Descent）· 学习率（Learning Rate）

**节骨架：** 4.1 设定模型 ｜ 4.2 定义损失 ｜ 4.3 优化参数 ｜ 4.4 训练循环 ｜ 4.5 从三步骤到完整流程

### 第 5 章 误差来源与模型选择（Error Sources and Model Selection） · [待写]

> 文件：`ch05_error_sources.md` ｜ 练习：`ch05_ex.py`

**本章子概念索引：** 偏差（Bias）· 方差（Variance）· 偏差—方差权衡（Bias-Variance Tradeoff）· 过拟合（Overfitting）· 欠拟合（Underfitting）· 模型容量（Model Capacity）· 正则化（Regularization）· 训练/验证/测试集（Train/Val/Test Split）· 交叉验证（Cross-Validation）· 分布不匹配（Distribution Shift）

**节骨架：** 5.1 偏差与方差 ｜ 5.2 权衡 ｜ 5.3 过拟合与欠拟合 ｜ 5.4 正则化 ｜ 5.5 数据划分与交叉验证 ｜ 5.6 分布不匹配 ｜ 5.7 误差诊断流程

### 第 6 章 评估指标（Evaluation Metrics） · [已完成]

> [教学](01_ml_framework/docs/ch06_evaluation_metrics.md) · [练习](01_ml_framework/exercises/ch06_ex.py)

**本章子概念索引：** 准确率（Accuracy）· 精确率（Precision）· 召回率（Recall）· F1 分数（F1 Score）· 混淆矩阵（Confusion Matrix）· ROC / AUC · MAE / MSE / RMSE · R² · 数据泄漏（Data Leakage）

**节骨架：** 6.1 分类指标 ｜ 6.2 回归指标 ｜ 6.3 指标选择与业务代价 ｜ 6.4 数据泄漏与评估陷阱

---

## 第 3 篇 监督学习 → `02_supervised/`

前置：第 2 篇。统一用 sklearn 演示，每章至少有一个练习只用 numpy 手写核心步骤。

### 第 7 章 线性模型（Linear Models） · [已完成]

> [教学](02_supervised/docs/ch07_linear_models.md) · [练习](02_supervised/exercises/ch07_ex.py)

**本章子概念索引：** 线性回归（Linear Regression）· 最小二乘（Least Squares）· 逻辑回归（Logistic Regression）· Sigmoid 函数 · 交叉熵损失（Cross-Entropy Loss）· 梯度下降（Gradient Descent）

**节骨架：** 7.1 线性回归 ｜ 7.2 逻辑回归 ｜ 7.3 正则化线性模型 ｜ 7.4 从 NumPy 实现到 scikit-learn

### 第 8 章 经典分类算法（Classical Classification Algorithms） · [已完成]

> [教学](02_supervised/docs/ch08_classical_classifiers.md) · [练习](02_supervised/exercises/ch08_ex.py)

**本章子概念索引：** K 近邻（KNN）· 决策树（Decision Tree）· 信息增益（Information Gain）· 基尼不纯度（Gini Impurity）· 支持向量机（SVM）· 核方法（Kernel Method）· 朴素贝叶斯（Naive Bayes）

**节骨架：** 8.1 KNN ｜ 8.2 决策树 ｜ 8.3 SVM ｜ 8.4 朴素贝叶斯 ｜ 8.5 算法对比与适用场景

### 第 9 章 集成方法（Ensemble Methods） · [已完成]

> [教学](02_supervised/docs/ch09_ensemble.md) · [练习](02_supervised/exercises/ch09_ex.py)

**本章子概念索引：** Bagging · 随机森林（Random Forest）· Boosting · 梯度提升（Gradient Boosting）· XGBoost / LightGBM · 堆叠（Stacking）

**节骨架：** 9.1 Bagging 与随机森林 ｜ 9.2 Boosting 与梯度提升 ｜ 9.3 偏差—方差视角

### 第 10 章 特征工程（Feature Engineering） · [已完成]

> [教学](02_supervised/docs/ch10_feature_engineering.md) · [练习](02_supervised/exercises/ch10_ex.py)

**本章子概念索引：** 特征缩放（Feature Scaling）· 归一化 / 标准化（Normalization / Standardization）· 缺失值处理（Missing Values）· 类别编码（Categorical Encoding）· 特征选择（Feature Selection）· 特征构造（Feature Construction）· 数据增强（Data Augmentation）

**节骨架：** 10.1 缩放与归一化 ｜ 10.2 缺失值与异常值 ｜ 10.3 类别编码 ｜ 10.4 特征选择与构造

---

## 第 4 篇 无监督学习 → `03_unsupervised/`

前置：第 2 篇（评估）、第 10 章（缩放）。

### 第 11 章 聚类（Clustering） · [待写]

> `ch11_clustering.md` ｜ `ch11_ex.py`

**本章子概念索引：** K-means · 层次聚类（Hierarchical Clustering）· DBSCAN · 聚类评估（Clustering Evaluation）

**节骨架：** 11.1 K-means ｜ 11.2 层次聚类 ｜ 11.3 DBSCAN ｜ 11.4 评估与簇数选择

### 第 12 章 降维与表示（Dimensionality Reduction） · [待写]

> `ch12_dimensionality.md` ｜ `ch12_ex.py`

**本章子概念索引：** 主成分分析（PCA）· t-SNE · UMAP · 自编码器（Autoencoder）

**节骨架：** 12.1 PCA ｜ 12.2 t-SNE 与 UMAP ｜ 12.3 自编码器

### 第 13 章 其他无监督任务（Other Unsupervised Tasks） · [选读]

> `ch13_other_unsupervised.md` ｜ `ch13_ex.py`

**本章子概念索引：** 密度估计（Density Estimation）· 异常检测（Anomaly Detection）· 关联规则（Association Rules）

**节骨架：** 13.1 密度估计 ｜ 13.2 异常检测 ｜ 13.3 关联规则

---

## 第 5 篇 深度学习 → `04_deep_learning/`

前置：第 2 章（梯度与链式法则）、第 7 章（线性模型）。
顺序：**先 numpy 手写，再上 PyTorch**，避免把框架当黑箱。

### 第 14 章 神经网络基础（Neural Network Basics） · [待写]

> `ch14_nn_basics.md` ｜ `ch14_ex.py`

**本章子概念索引：** 神经元（Neuron）· 权重 / 偏置（Weight / Bias）· 激活函数（Activation Function）· 隐藏层 / 输出层（Hidden / Output Layer）· 前向传播（Forward Propagation）· 反向传播（Backpropagation）· 计算图（Computational Graph）

**节骨架：** 14.1 神经元与层 ｜ 14.2 多层叠加 ｜ 14.3 前向传播 ｜ 14.4 反向传播 ｜ 14.5 最小代码：NumPy 两层网络

### 第 15 章 激活函数与初始化（Activation and Initialization） · [待写]

> `ch15_activation_init.md` ｜ `ch15_ex.py`

**本章子概念索引：** Sigmoid · ReLU · Leaky ReLU · GELU · 梯度消失（Vanishing Gradient）· 梯度爆炸（Exploding Gradient）· 权重初始化（Weight Initialization）· Xavier / He 初始化

**节骨架：** 15.1 Sigmoid 与 ReLU ｜ 15.2 梯度消失与爆炸 ｜ 15.3 权重初始化

> 取舍备注：15 与 16 内容接近，实际撰写时**允许合并成一章**，编号保留以便对照。

### 第 16 章 训练深度网络（Training Deep Networks） · [待写]

> `ch16_training_dnn.md` ｜ `ch16_ex.py`

**本章子概念索引：** 优化器（Optimizer）· SGD / Momentum / Adam · 学习率调度（LR Scheduling）· 批归一化 / 层归一化（Batch / Layer Norm）· Dropout · 残差连接（Residual Connection）· 早停（Early Stopping）

**节骨架：** 16.1 优化器 ｜ 16.2 学习率调度 ｜ 16.3 归一化 ｜ 16.4 Dropout 与残差 ｜ 16.5 深层网络退化

### 第 17 章 常见网络结构（Common Architectures） · [待写]

> `ch17_architectures.md` ｜ `ch17_ex.py`

**本章子概念索引：** 卷积神经网络（CNN）· 循环神经网络（RNN）· LSTM / GRU · Transformer · 自注意力（Self-Attention）· 多头注意力（Multi-Head Attention）

**节骨架：** 17.1 CNN ｜ 17.2 RNN / LSTM / GRU ｜ 17.3 Transformer 与自注意力

---

## 第 6 篇 现代机器学习与 LLM → `05_llm/`

前置：第 17 章（Transformer）。**原框架缺这一篇，本次补上。**

### 第 18 章 自监督与预训练（Self-supervision and Pretraining） · [待写]

> `ch18_self_supervised.md` ｜ `ch18_ex.py`

**本章子概念索引：** 自监督学习（Self-supervised Learning）· 掩码语言建模（Masked Language Modeling）· 对比学习（Contrastive Learning）· 预训练（Pretraining）· 微调（Fine-tuning）· 表征学习（Representation Learning）

**节骨架：** 18.1 自监督学习 ｜ 18.2 预训练与微调 ｜ 18.3 表征学习

### 第 19 章 大语言模型应用（LLM Applications） · [待写]

> `ch19_llm_applications.md` ｜ `ch19_ex.py`

**本章子概念索引：** 大语言模型（LLM）· 提示工程（Prompt Engineering）· 检索增强生成（RAG）· 智能体（Agent）· LLM 评估（LLM Evaluation）· 幻觉（Hallucination）

**节骨架：** 19.1 LLM 基本使用 ｜ 19.2 提示工程 ｜ 19.3 RAG ｜ 19.4 Agent 基础 ｜ 19.5 LLM 评估

---

## 第 7 篇 工程实践与部署 → `06_engineering/`

前置：任意一个能跑通的模型。**实践轨道单独放在 `projects/`**，不占章号。

### 第 20 章 机器学习项目流程（ML Project Workflow） · [待写]

> `ch20_project_workflow.md` ｜ `ch20_ex.py`

**本章子概念索引：** 问题定义（Problem Formulation）· 数据收集与清洗（Data Collection / Cleaning）· 基线模型（Baseline Model）· 实验记录（Experiment Tracking）· 模型选择（Model Selection）· 误差分析（Error Analysis）· 可复现性（Reproducibility）

**节骨架：** 20.1 从问题到基线 ｜ 20.2 实验与误差分析 ｜ 20.3 项目复现

### 第 21 章 部署与监控（Deployment and Monitoring） · [待写]

> `ch21_deployment.md` ｜ `ch21_ex.py`

**本章子概念索引：** 模型服务（Model Serving）· API 部署（API Deployment）· Docker · 推理延迟（Inference Latency）· 数据漂移（Data Drift）· 模型监控（Model Monitoring）· MLOps

**节骨架：** 21.1 模型服务与 API ｜ 21.2 容器化 ｜ 21.3 监控与数据漂移 ｜ 21.4 MLOps 基础

### 实践轨道（Projects） · [待写]

| 项目 | 用得到的章 | 目录 |
|---|---|---|
| 表格数据端到端 | 第 3~10 章 | `06_engineering/projects/tabular/` |
| 图像分类（迁移学习） | 第 14~17 章 | `06_engineering/projects/image_classification/` |
| **以图搜图 / 图像检索（终点目标）** | 第 11~12 / 14~19 / 21 章 | `06_engineering/projects/image_retrieval/` |
| 模型服务化 Demo | 第 21 章 | `06_engineering/projects/serving_demo/` |

> 终点目标为**以图搜图（Image Retrieval）**：图像集 → 预训练模型抽 embedding
> → 降维 / 聚类（ch11、ch12）→ 建向量索引 → 查询服务与召回率 / 延迟评估
> → 新图加入后的漂移监控（ch21）。无需标注、无需 GPU，
> 与 `image_classification/` 共用同一份图像集和骨干模型。
> `.gitignore` 已排除数据集与权重，仓库不放大文件。

---

## 第 8 篇 专题与负责任机器学习 → `07_topics/`

优先级低，[选读]。有实际项目踩到坑时再写，不提前铺开。

### 第 22 章 可解释性（Interpretability） · [选读]

**本章子概念索引：** 特征重要性（Feature Importance）· SHAP · LIME · 注意力可视化（Attention Visualization）
**节骨架：** 22.1 全局可解释性 ｜ 22.2 局部可解释性

### 第 23 章 公平性、隐私与安全（Fairness, Privacy, Security） · [选读]

**本章子概念索引：** 算法偏见（Algorithmic Bias）· 公平性约束（Fairness Constraint）· 差分隐私（Differential Privacy）· 对抗攻击（Adversarial Attack）· 数据隐私（Data Privacy）
**节骨架：** 23.1 公平性 ｜ 23.2 隐私 ｜ 23.3 安全与对抗攻击

---

## 附录 → `90_appendix/`

| 附录 | 内容 | 状态 |
|---|---|---|
| A | 术语表（Glossary）中英对照 + 一句话直觉 | [待写] |
| B | 公式速查（Formula Sheet）每式配一段 numpy 实现 | [待写] |
| C | 代码模板（Code Templates）训练循环 / 评估 / 画图 | [待写] |
| D | 常用数据集（Datasets）下载方式、许可、大小 | [待写] |
| E | 练习索引（Exercise Index）**只做索引，不重复存答案** | [已完成] `90_appendix/docs/appE_exercises.md` |
| F | 推荐资源（Resources） | [待写] |
| — | numpy / pandas / matplotlib 速查表 | [已完成] `00_foundations/data_stack/docs/appendix_cheatsheet.md` |

> 取舍：参考答案统一放在各 `chNN_ex.py` 的 `# region 参考答案` 里，附录 E 只给链接。
> 不在两处存答案，避免改一处忘另一处。

---

## 维护约定

1. 章节状态只在本文件更新；根 README 的进度数字按本文件汇总
2. 开写新章时：复制 `_templates/chapter_template.md`，按 `chNN_<短名>.md` 命名，
   放进对应篇的 `docs/`；练习放 `exercises/chNN_ex.py`
3. 章号一旦分配不再变动；废弃章节标 `[已废弃]` 而不是删号
4. 每章开头必须有「本章子概念索引」，用显式锚点链接到各节（见 CONTRIBUTING.md）
