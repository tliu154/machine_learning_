# 机器学习教学笔记（Machine Learning Teaching Notes）

一个**按学习依赖组织、长期演进**的机器学习笔记库。当前阶段是框架：
完整章节骨架 + 状态 + 写作规范，具体内容之后按需逐章填充。

- GitHub：https://github.com/tliu154/machine_learning_
- 本地：`D:\我的知识库\develop\machine_learning`（同时是 Obsidian 知识库路径）

## 快速导航

| 文件 | 作用 |
|---|---|
| **[SYLLABUS.md](SYLLABUS.md)** | **完整骨架**：8 篇 / 24 章 / 附录 A~F，每章子概念索引、状态、预定文件。**章节状态只在这里维护** |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 新增章节的命名、锚点、模板、校验规范 |
| [NOTATION.md](NOTATION.md) | 符号约定与术语规范（全仓库统一） |
| [`_templates/`](_templates/) | 章节模板 / 单节模板 / 练习模板 |
| [00_foundations/data_stack/](00_foundations/data_stack/) | 已完成：numpy / pandas / matplotlib 7 篇教学 + 6 份练习 |

## 本次框架调整：采纳什么、改什么

对照给来的 8 篇 23 章大纲做的取舍。**采纳结构，不复制体量**。

| 优点 | 处理 | 理由 |
|---|---|---|
| 子概念索引前置 | **全采纳** | 写进章节模板，索引项链接到各节锚点 |
| 一个概念一个独立小节、标题带英文 | **全采纳** | `### 7.1 线性回归（Linear Regression）` 格式统一 |
| 按学习依赖排序（8 篇） | **全采纳** | 目录重排，并补上原框架缺的 **LLM 篇、工程篇、专题篇** |
| 每节统一模板 | **改造采纳** | 「数学形式」改为**可选**（Git、Jupyter 这类节没有公式）；「练习」不放在每节，改在**每章末尾一份**练习文件，节内只放链接 —— 否则 150 个概念就要 150 份碎片练习 |
| 目录可扩展、先给骨架 | **全采纳，但换实现** | **不建 150 个空壳文件**：完整骨架集中一份 `SYLLABUS.md`，只有真正开写时才建 `chNN_*.md`。空壳文件是最容易烂尾的东西 |
| 锚点稳定 | **加强** | 中文 + 括号 + 英文的标题，GitHub 自动生成的 slug 不稳定（括号被吞、中英混排易变）。**一律用显式 `<a id="c07-01"></a>`**，索引链到显式 ID，不依赖自动 slug |
| 第 0 章前言与符号约定 | **拆分** | 不单独建第 0 章（会和 README 重复维护）：定位/路径 → 本文件，模板 → CONTRIBUTING，符号术语 → `NOTATION.md` |
| 附录 E 练习题与答案 | **只做索引** | 答案统一留在各练习文件的 `# region 参考答案` 里，不在附录重复存一份，避免改一处忘另一处 |
| 第 15 / 16 章 | **保留编号，允许合并** | 激活函数/初始化与训练技巧内容重叠，实际撰写时可合成一章，章号不删以便对照 |
| 原模块前缀命名（np/pd/alg/dl…） | **改为全局章号** | `ch07_linear_models.md` 比 `alg01_xxx.md` 更直观，且章跨篇移动时不用改名 |

**原风格保留不变**：C++ 迁移导向（只讲差异）、一章 150~250 行、教学配练习、
`assert` 自测、`# region` 折叠答案、固定随机种子、不依赖大文件。

## 学习依赖顺序

```mermaid
flowchart LR
    P1["第1篇 基础工具<br/>Python · 数学"] --> P2["第2篇 ML 框架<br/>训练三步骤 · 误差 · 评估"]
    P2 --> P3["第3篇 监督学习<br/>线性 · 分类 · 集成 · 特征"]
    P2 --> P4["第4篇 无监督<br/>聚类 · 降维"]
    P3 --> P5["第5篇 深度学习<br/>反向传播 · CNN · Transformer"]
    P4 --> P5
    P5 --> P6["第6篇 现代 LLM<br/>预训练 · RAG · Agent"]
    P3 --> P7["第7篇 工程实践<br/>项目流程 · 部署监控"]
    P5 --> P7
    P7 --> P8["第8篇 专题<br/>可解释性 · 公平隐私"]
```

不严格按顺序也行 —— 每章开头用「前置」一行点明依赖，按需跳读。
实战项目是**贯穿各篇的实践轨道**（见 [SYLLABUS 第 7 篇](SYLLABUS.md)），不占章号。

## 目录结构

```
machine_learning/
├── README.md              本文件：导航、取舍说明、路径图
├── SYLLABUS.md            完整章节骨架 + 状态（唯一状态源）
├── CONTRIBUTING.md        写作与校验规范
├── NOTATION.md            符号与术语约定
├── _templates/            章节模板 / 单节模板 / 练习模板
├── 00_foundations/        第1篇 基础工具与数学直觉
│   ├── data_stack/        [已完成] numpy/pandas/matplotlib 全套
│   └── python_basics/     [待迁移] 原 ch01~ch12
├── 01_ml_framework/       第2篇 机器学习基础框架
├── 02_supervised/         第3篇 监督学习
├── 03_unsupervised/       第4篇 无监督学习
├── 04_deep_learning/      第5篇 深度学习
├── 05_llm/                第6篇 现代机器学习与 LLM
├── 06_engineering/        第7篇 工程实践（含 projects/ 实践轨道）
├── 07_topics/             第8篇 专题与负责任 ML
└── 90_appendix/           附录 A~F
```

每篇统一含 `README.md`（定位 + 依赖 + 实践方向）、`docs/`、`exercises/`。
章节清单不在篇 README 里重复，一律看 SYLLABUS。

## 单节模板（每节五段，"数学形式"可选）

```
概念定义 → 数学形式（可选）→ 最小代码 → 常见误区 → 对应练习链接
```

外加一节「和 C++ / 已有认知的差异」——这是这套笔记从第一天起的特色，不丢。

## 进度

- **已完成**：7 篇教学 + 6 份练习 + 1 份速查表（第 1 篇的 1.3 / 1.4 / 1.5 节）
- **已规划**：24 章 + 6 个附录，约 150 个概念小节，全部列在 [SYLLABUS.md](SYLLABUS.md)
- **待迁移**：Python 基础语法 ch01~ch12（原 `D:\develop\python` 已重组，文件散落）
- **下一步**：挑一章开写，复制 `_templates/`，写完只更新 SYLLABUS 的状态

## 快速开始

```bash
cd 00_foundations/data_stack/exercises
python np01_ex.py       # 输出 "np01 全部通过 ✓" 即过关
```

依赖：`pip install numpy pandas matplotlib`（后续章节按需加 `scikit-learn`、`torch`）。
仓库不收录数据集和模型权重，练习数据全部现场生成或用临时目录。

## 添加一章的最短路径

1. 在 [SYLLABUS.md](SYLLABUS.md) 找到章号 → 确认该章的预定文件名
2. 复制 `_templates/chapter_template.md` 到对应篇的 `docs/chNN_*.md`
3. 按 `_templates/concept_section.md` 逐节填写（每节显式锚点）
4. 复制 `_templates/exercise_template.py` 到 `exercises/chNN_ex.py`
5. 跑自测、更新 SYLLABUS 状态、commit

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。
