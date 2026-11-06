# 00 前置基础

进机器学习之前要顺手的东西。**本模块是目前唯一有完整内容的部分**，其余模块只有规划。

## 章节清单

| 编号 | 章节 | 教学 | 练习 | 状态 |
|---|---|---|---|---|
| 00.0 | 环境与工具（venv / uv / PyCharm / Jupyter） | — | — | [待写] |
| 00.1 | Python 基础语法 ch01~ch12 | — | — | [待迁移] |
| 00.2 | numpy 01 ndarray 基础 | [np01](data_stack/docs/np01_ndarray.md) | [np01_ex.py](data_stack/exercises/np01_ex.py) | [已完成] |
| 00.3 | numpy 02 广播与向量化 | [np02](data_stack/docs/np02_broadcast.md) | [np02_ex.py](data_stack/exercises/np02_ex.py) | [已完成] |
| 00.4 | numpy 03 线代与图像 | [np03](data_stack/docs/np03_practice.md) | [np03_ex.py](data_stack/exercises/np03_ex.py) | [已完成] |
| 00.5 | pandas 01 DataFrame | [pd01](data_stack/docs/pd01_dataframe.md) | [pd01_ex.py](data_stack/exercises/pd01_ex.py) | [已完成] |
| 00.6 | pandas 02 分组与读写 | [pd02](data_stack/docs/pd02_groupby.md) | [pd02_ex.py](data_stack/exercises/pd02_ex.py) | [已完成] |
| 00.7 | matplotlib 绘图 | [plt01](data_stack/docs/plt01_plot.md) | [plt01_ex.py](data_stack/exercises/plt01_ex.py) | [已完成] |
| 00.8 | 三件套速查表 | [appendix](data_stack/docs/appendix_cheatsheet.md) | — | [已完成] |

## 收录说明

`data_stack/` 是之前那套「numpy / pandas / matplotlib」教程的完整副本
（原目录：`D:\我的知识库\develop\python_data`，保留不动）。
副本收录进仓库是为了 clone 下来就能自包含地读和跑。
**两边若都要改，以仓库内这份为准**，原目录视为历史快照。

7 篇教学 + 6 份练习 + 1 份速查表，全部参考答案已跑过 assert 自测。

## python_basics（待迁移）

之前的 Python 基础教程 ch01~ch12（变量与引用、字符串、容器、控制流、函数、生成器、
文件异常、类、模块、递归）因为 `D:\develop` 目录重组，目前只剩零散文件，尚未收录。
找到后按下面结构放进来：

```
python_basics/
├── README.md
├── docs/        ch01_*.md ... ch12_*.md
└── exercises/   ch01_ex.py ... ch12_ex.py
```

## 跑一遍

```bash
cd data_stack/exercises
python np01_ex.py
python pd02_ex.py
python plt01_ex.py
```

依赖：`pip install numpy pandas matplotlib`
（matplotlib 练习用 Agg 无头后端，不弹窗，图片存临时目录。）

---

模块规范见 [CONTRIBUTING.md](../CONTRIBUTING.md)
