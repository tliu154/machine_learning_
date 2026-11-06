# 第 1 篇 基础工具与数学直觉（Foundations）

**章号 00~02** ｜ 前置：无 ｜ 目标：能用 Python 数据栈把一串数字变成一张图。

章节清单与状态一律看 [SYLLABUS 第 1 篇](../SYLLABUS.md)。本文件只记本篇特有的资产。

## 已完成：data_stack/

`data_stack/` 是之前那套「numpy / pandas / matplotlib」教程的完整副本
（原始目录 `D:\我的知识库\develop\python_data` 保留不动，**以仓库内这份为准**）。
它对应第 1 章的 1.3 / 1.4 / 1.5 节：

| 节 | 教学 | 练习 |
|---|---|---|
| 1.3 NumPy | [np01](data_stack/docs/np01_ndarray.md) · [np02](data_stack/docs/np02_broadcast.md) · [np03](data_stack/docs/np03_practice.md) | [np01](data_stack/exercises/np01_ex.py) · [np02](data_stack/exercises/np02_ex.py) · [np03](data_stack/exercises/np03_ex.py) |
| 1.4 pandas | [pd01](data_stack/docs/pd01_dataframe.md) · [pd02](data_stack/docs/pd02_groupby.md) | [pd01](data_stack/exercises/pd01_ex.py) · [pd02](data_stack/exercises/pd02_ex.py) |
| 1.5 Matplotlib | [plt01](data_stack/docs/plt01_plot.md) | [plt01](data_stack/exercises/plt01_ex.py) |
| — | [三件套速查表](data_stack/docs/appendix_cheatsheet.md) | — |

7 篇教学 + 6 份练习，参考答案全部跑过 `assert` 自测。
这些文件沿用旧命名（`np01` 而非 `ch01`），是历史资产，不强行改号。

## 已完成：python_basics/

Python 基础语法 ch01~ch12（变量与引用、容器、函数、生成器、异常、类、模块、递归）
已于 2026-11 从 `D:\我的知识库\develop\Python\python_ex\` 迁入（原目录保留）：
**13 篇教学 + 12 份练习**，参考答案全部通过自测。详见 [python_basics/README.md](python_basics/README.md)。

> 注意该目录里的 `chNN` 是基础教程**自己的章号**，和本仓库 ML 章号无关（两个 `ch04_ex.py` 内容完全不同）。

## 本篇写作提醒

- 第 2 章数学基础**够用就好**：只求能看懂损失函数、能自己推梯度下降
- 所有公式用 numpy 落地成代码，别停在纸面（见 [NOTATION.md](../NOTATION.md)）
- 1.2 环境配置节要覆盖 `venv` / `uv` / Jupyter / Git 四件套

```bash
# 跑一遍已有练习
cd data_stack/exercises && python np01_ex.py
```
