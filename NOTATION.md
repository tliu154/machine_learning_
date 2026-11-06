# 符号约定与术语规范（Notation and Terminology）

全仓库统一。**写新章节前扫一眼，避免同一个概念三章三种写法。**

## 1. 数学符号

| 符号 | 含义 | 代码里 |
|---|---|---|
| $x$ / $\mathbf{x}$ | 标量 / 单个样本的特征向量 | `x` / `x_i` |
| $X$ | 设计矩阵，形状 $(n, d)$ | `X` |
| $y$ / $\hat{y}$ | 真实标签 / 模型预测 | `y` / `y_pred` |
| $n$ / $d$ / $K$ | 样本数 / 特征数 / 类别数或簇数 | `n_samples` / `n_features` / `n_classes` |
| $w$, $b$, $\theta$ | 权重 / 偏置 / 参数全体 | `w` / `b` / `theta` |
| $f_\theta(\cdot)$ | 模型（带参数） | `model(X)` |
| $L(\theta)$ / $\ell$ | 损失函数 / 单个样本的损失 | `loss` / `loss_i` |
| $\nabla_\theta L$ | 损失函数对参数的梯度 | `grad` |
| $\eta$ | 学习率 | `lr` |
| $\lambda$ | 正则化强度 | `alpha`（跟随 sklearn）/ `l2` |
| $\mathbb{E}[\cdot]$, $\mathrm{Var}$ | 期望 / 方差 | `np.mean` / `np.var` |
| $\sigma(\cdot)$ | Sigmoid 函数 | `sigmoid(z)` |
| $\lbrace (x_i, y_i) \rbrace_{i=1}^{n}$ | 数据集 | `X, y` |

**形状约定**（最容易混的地方，每章代码里都要写清）：

- numpy 图像：`(H, W, C)`，BGR，`uint8`，下标 `[y, x]`
- PyTorch 张量：`(N, C, H, W)`，RGB，`float32`
- sklearn 输入：`X` 恒为 `(n_samples, n_features)`，**一维特征也要 reshape 成 `(-1, 1)`**

## 2. 公式排版

- 行内公式 `$...$`，独立成块用 `$$...$$`（GitHub / Obsidian 都渲染）
- 每个公式后面**必须跟一句自然语言解释它「在算什么」**和一段 numpy 实现
- 不写大段推导，需要时链到附录 B 公式速查

```markdown
$$L(\theta) = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2$$

即「所有样本预测误差平方的平均」。numpy：`np.mean((y - y_pred) ** 2)`
```

## 3. 术语规范

- **首次出现**：中文（English），如「偏差（Bias）」「梯度下降（Gradient Descent）」
- 之后再出现用中文；约定俗成的缩写（PCA、CNN、RAG、mAP）直接用缩写
- 标题一律「中文（English）」，英文首字母实词大写
- 中英之间**不加空格**由排版决定，代码/公式前后留半角空格

### 易混词（写错会误导，重点核对）

| 词 | 别写成 | 说明 |
|---|---|---|
| 偏置（Bias） | 偏差 | 参数 $b$；**偏差（Bias）**是误差分解里的概念，同词不同义，出现时标明语境 |
| 精确率（Precision） | 准确率 | `TP/(TP+FP)`；准确率是 `Accuracy` |
| 召回率（Recall） | 查全率混用 | 全仓库统一「召回率」 |
| 验证集（Validation） | 测试集 | 调参用验证集，测试集只在最后用一次 |
| 参数（Parameter） | 超参数 | 训练学到的 vs 人手动设的 |
| 损失（Loss） | 代价/目标函数混用 | 统一「损失函数」，单个样本用「损失」 |
| 推断 / 推理（Inference） | 预测混用 | 部署语境用「推理」，模型语境用「预测」 |

### 缩写表

`ML` 机器学习 ｜ `DL` 深度学习 ｜ `LLM` 大语言模型 ｜ `SGD` 随机梯度下降 ｜
`CNN` 卷积神经网络 ｜ `RNN` 循环神经网络 ｜ `PCA` 主成分分析 ｜
`SVM` 支持向量机 ｜ `KNN` K 近邻 ｜ `ROC/AUC` 受试者工作特征曲线下面积 ｜
`mAP` 平均精度均值 ｜ `RAG` 检索增强生成 ｜ `MLOps` 机器学习运维

## 4. 代码与命名

- 变量：`snake_case`；常量：`UPPER_CASE`；类：`PascalCase`
- 章文件：`chNN_<短名>.md`（NN 为两位章号，全局唯一）
- 练习文件：`chNN_ex.py`，与章文件同号
- 显式锚点：`c<章号>-<节号>`，如 `<a id="c07-02"></a>` → 索引链 `#c07-02`
- 随机种子：一律 `np.random.default_rng(42)` 或 `torch.manual_seed(42)`

## 5. 语言与风格

- 中文叙述，代码/术语保留英文
- **不重复讲编程基础**，只讲与 C++ / 已有认知的差异
- 一章 150~250 行；一节五段模板见 [`_templates/concept_section.md`](_templates/concept_section.md)
- 章节状态只在 [SYLLABUS.md](SYLLABUS.md) 维护
