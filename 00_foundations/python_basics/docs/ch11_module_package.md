---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch11 模块、包与虚拟环境

## 11.1 import 的五种形式

```cpp
// C++ 是文本替换式的 #include <iostream>
```

```python
import math                     # 整体导入，用 math.sqrt(2)
from math import sqrt, pi       # 精确导入，直接用 sqrt(2)
from math import sqrt as sq     # 起别名
from math import *              # ✗ 污染命名空间，别用（搞不清哪个名字来自哪）
import numpy as np              # 社区约定的短别名（numpy→np, pandas→pd, matplotlib.pyplot→plt）
```

推荐：

- 优先 `import module`，用 `module.func()` —— 一看就知道从哪来
- 频繁使用某个函数才用 `from x import y`

## 11.2 自己写模块

Python 里**一个 .py 文件就是一个模块**，模块名就是文件名。

```
MathUtils.py        ← 模块名是 MathUtils（文件名建议还是用 snake_case）
```

```python
# mymath.py
"""我的数学工具模块。"""          # 模块级 docstring

PI = 3.14159                    # 模块里的全局变量

def area(r):
    return PI * r * r

def _helper():                  # 下划线开头不会被 from mymath import * 导入
    pass
```

同目录下另一个文件里：

```python
import mymath
mymath.area(2)

from mymath import area, PI
```

> Python **没有头文件/源文件分离**，也不需要前置声明。import 就是把那个 .py 从头到尾执行一遍，然后把里面定义的名字拿过来。

## 11.3 `if __name__ == "__main__"` —— 必懂

```python
# mymath.py
def area(r):
    return 3.14 * r * r

print("模块被加载了")             # ⚠️ 被 import 时也会执行！

if __name__ == "__main__":
    # 只有【直接运行这个文件】时才会执行
    # 被 import 时这里不执行
    print("测试:", area(2))
```

原理：每个模块都有一个 `__name__` 变量

- 直接运行 `python mymath.py` → `__name__ == "__main__"`
- 被 import → `__name__ == "mymath"`（模块名）

**用途**：把测试代码 / 命令行入口放在这个块里，模块既能被 import 又能直接跑。相当于 C++ 里 main 与库的分离。

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

## 11.4 包（package）

包 = **含有 `__init__.py` 的目录**（Python 3.3+ 后可以省略，但建议保留）。

```
myproject/
├── __init__.py          # 可以是空文件，标记这是个包
├── models.py
└── utils.py
```

```python
from myproject import models
from myproject.utils import helper
```

### 相对导入（包内部互相引用）

```python
# 在 myproject/models.py 里
from . import utils              # 一个点 = 当前包
from .submodule import helper
from ..parent import thing       # 两个点 = 上级包
```

> ⚠️ 相对导入只能在**被作为包 import** 时用，直接运行那个文件会报 "attempted relative import beyond top-level package"。所以入口脚本放外面。

## 11.5 PyCharm 与项目结构

在 PyCharm 里：

- 右键目录 → **Mark Directory as → Sources Root**，蓝色目录里的模块可以直接被 import
- **Ctrl+B** 跳到定义（跳到库源码，看实现很有用）
- **Ctrl+Alt+O** 优化 import（删掉没用的）
- **Alt+Enter** 万能键：自动 import 缺失的模块、改名、补 `self` 等

## 11.6 常用标准库速览

```python
# --- 数学 ---
import math, random, statistics
random.randint(1, 10)           # [1,10] 闭区间整数（C++ 的 % 是半开，这里注意）
random.choice(["a","b","c"])
random.sample(range(100), 5)    # 不重复抽 5 个
random.shuffle(lst)             # 原地打乱
statistics.mean/median/stdev([1,2,3])

# --- 时间 ---
import time, datetime
time.time()                     # Unix 时间戳（秒，float）
time.perf_counter()             # 高精度计时，测代码耗时用这个
time.sleep(0.5)
datetime.datetime.now()
datetime.date.today()
datetime.timedelta(days=7)

# --- 系统 ---
import os, sys, subprocess
os.getcwd() / os.chdir(path)
os.environ.get("PATH")
os.path.join("a","b")           # 老写法，现在推荐 pathlib
sys.argv                        # 命令行参数
sys.exit(1)
subprocess.run(["git","status"], capture_output=True, text=True)

# --- 文本处理 ---
import re
re.match(r"\d+", "123abc")      # r 前缀 raw 字符串，写正则必备
re.findall(r"\b\w+@\w+\.\w+", text)
re.sub(r"\s+", " ", text)

# --- 其他高频 ---
import json, csv, logging, unittest
import argparse                 # 命令行工具
import collections              # Counter, defaultdict, deque, namedtuple
import itertools                # ch08
import functools                # lru_cache, reduce, wraps
import dataclasses, typing, pathlib, shutil, copy, pickle, sqlite3
```

## 11.7 虚拟环境 venv

**为什么需要**：不同项目需要不同版本的库，全局装会打架（C++ 大概相当于系统级 /usr/lib 全塞进去）。

```bash
# 创建
python -m venv .venv            # 推荐目录名 .venv，PyCharm 能自动识别

# 激活
# Windows Git Bash:
source .venv/Scripts/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# 激活后命令行前面会出现 (.venv)
pip install requests            # 只装到这个环境里
pip list
pip freeze > requirements.txt   # 导出依赖清单
pip install -r requirements.txt # 别人 clone 后一键还原

# 退出
deactivate
```

**PyCharm 里更简单**：File → Settings → Python Interpreter → Add Interpreter → Virtualenv Environment → New → OK。之后 PyCharm 底部的 Terminal 会自动激活。

> 每个 Python 项目都建一个 venv，这是硬性好习惯。

## 11.8 pip：包管理

```bash
pip install requests            # 安装
pip install requests==2.31.0    # 指定版本
pip install "requests>=2.0"
pip uninstall requests
pip list / pip show requests
pip install -r requirements.txt
```

国内镜像加速（一次性）：

```bash
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

常用第三方库（以后会碰到）：

| 库 | 用途 |
|---|---|
| `numpy` | 数值计算/数组（科学计算基石） |
| `pandas` | 表格数据分析 |
| `matplotlib` | 绘图 |
| `requests` | HTTP 请求 |
| `opencv-python` | 计算机视觉 ← 你做 RoboMaster 视觉会用 |
| `pytest` | 单元测试 |

> RoboMaster/OpenCV 方向的话，`numpy` + `opencv-python` 是必装项，Python 的 OpenCV API 比 C++ 版好写很多。

## 11.9 你走过的路：最终项目结构建议

```
D:\develop\python\
├── .venv/                  ← 虚拟环境（不要提交到 git）
├── docs/                   ← 本套教程
├── exercises/              ← 练习
├── requirements.txt        ← 依赖清单
└── mylib/                  ← 以后自己的代码放这里
    ├── __init__.py
    └── utils.py
```

别忘了 `.gitignore` 里加上 `.venv/` 和 `__pycache__/`。

---

### 小结

| C++ | Python |
|---|---|
| `#include <xxx>` | `import xxx` |
| `.h` 声明 + `.cpp` 实现 | 一个 `.py` 全搞定 |
| 静态库/动态库管理 | pip + venv |
| `cmake` / Makefile | 通常不需要，直接 `python xxx.py` |
| `int main()` | `if __name__ == "__main__":` |

下一站：[ch12 递归](ch12_recursion.md)（专题），或者去 [附录速查表](appendix_cpp_python_cheatsheet.md) 随时复习。
