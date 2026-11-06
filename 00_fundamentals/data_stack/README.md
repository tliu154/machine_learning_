# 数据分析三件套：numpy / pandas / matplotlib

> 本模块是机器学习教程的 00 前置基础，返回 [仓库总纲](../../README.md) ｜ [模块说明](../README.md)
> （仓库内这份为准；`D:\我的知识库\develop\python_data` 为原始副本）

> 前置：Python 基础语法 —— 函数、切片、推导式、生成器、类（之前那套 ch01~ch12 教程）。
> 这里假设你已经会写 Python 函数、切片、推导式，直接进入"用库干活"的阶段。

## 这三个库分别干什么

| 库 | 一句话 | C++ 对照 |
|---|---|---|
| **numpy** | 多维数组 + 全向量化运算 | 自己手搓的 `vector<double>` + SIMD 循环 |
| **pandas** | 表格数据（像带索引的 Excel） | 没有好的对照物，最接近"带列名的结构化容器" |
| **matplotlib** | 画图 | 没有对照物，gnuplot/QCustomPlot 的脚本版 |

对你（RoboMaster 视觉）的优先级：**numpy > matplotlib > pandas**。
OpenCV 的 Python 版里，图像就是 numpy 数组，`cv2` 和 `numpy` 是绑死的；numpy 熟了等于图像处理武器库翻倍。

## 怎么用

1. PyCharm 打开本仓库根目录 `machine_learning/`（或把 `00_fundamentals/data_stack/` 加进解释器范围）。
2. 每个练习文件开头都 `import` 对应库 —— **没装的话先装**：

```bash
pip install numpy pandas matplotlib
# 国内慢就用清华镜像：
pip install numpy pandas matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 读 `docs/` 里的章节，对着 PyCharm 敲；读完做 `exercises/` 里对应文件，跑 assert 自测。
4. 卡住了展开文件末尾的 `# region 参考答案`（PyCharm 可折叠）。

## 核心心法（比语法重要）

**numpy/pandas 的世界和纯 Python 是两套思维**：

```
纯 Python：for 循环逐个处理元素
numpy：     整个数组一次性运算，for 循环几乎消失
```

新手最大的坑就是**用写 C++ 的方式写 numpy** —— 拿着 ndarray 还在下标循环。
记住一条铁律：

> **你写的每一个 `for i in range(len(a))`，在 numpy 里几乎都有一个向量化版本。**
> 速度差 10~100 倍，代码还短一半。

## 章节目录

| 章节 | 主题 | 要点 |
|---|---|---|
| [np01](docs/np01_ndarray.md) | ndarray：数组的本质 | dtype / shape / 视图 vs 拷贝 / 布尔掩码 |
| [np02](docs/np02_broadcast.md) | 广播与向量化 | 广播规则 / axis / 聚合 / reshape —— 干掉 for 循环 |
| [np03](docs/np03_practice.md) | numpy 实战 | 线性代数 / 随机数 / **图像就是数组**（视觉组重点） |
| [pd01](docs/pd01_dataframe.md) | Series 与 DataFrame | 创建 / loc·iloc / 过滤 / 缺失值 |
| [pd02](docs/pd02_groupby.md) | 分组、合并与读写 | groupby / merge / apply / CSV |
| [plt01](docs/plt01_plot.md) | matplotlib 绘图 | 折线 / 散点 / 柱状 / subplots / 中文显示 / 保存 |
| [附录](docs/appendix_cheatsheet.md) | 三件套速查表 | 想不起 API 时翻这里 |

建议顺序：np01 → np02 → np03 → plt01 → pd01 → pd02（pandas 依赖 numpy，但和画图无依赖）。

## 环境自检

```python
import numpy as np
import pandas as pd
import matplotlib
print(np.__version__)   # >= 2.0 都行，本套材料按 2.x API 写
print(pd.__version__)   # >= 2.0
```

> numpy 2.x 和 1.x 有少量 API 差异（比如 `np.float_` 没了），本套按 2.x 写；
> 网上老教程里的 `np.float`、`np.bool` 写法一律过时，别抄。
