# Python 基础语法 · 学习路线（给有 C++ 基础的人）

> **本目录对应 [SYLLABUS](../../SYLLABUS.md) 第 1 章 1.1 节，状态 `[已完成]`。**
> ⚠️ **章号说明**：本目录里的 `chNN` 指的是**这套基础教程自己的章号**（ch01 世界观、ch04 列表元组、ch12 递归），
> 与仓库全局章号（ch04 训练三步骤等 ML 章节）**完全无关**。两套文件在不同目录下，别混。

这份材料不是"从零学编程"，而是**从 C++ 迁移到 Python**。
你已经懂变量、循环、函数、类、指针 —— 所以每一章只讲 **Python 和你已有认知不一样的地方**。

2026-11 从 `D:\我的知识库\develop\Python\python_ex\` 迁入本仓库（原目录保留）。
13 篇教学 + 12 份练习，练习格式与全仓库一致：TODO + `assert` 自测 + `# region` 折叠答案。

## 怎么用

1. 用 PyCharm 打开本目录 `python_basics/`（File → Open），或直接在仓库根项目里跑练习。
2. 打开 `docs/chNN_xxx.md`，**对着 PyCharm 一边读一边敲**（不要复制粘贴，手敲才有肌肉记忆）。
3. 读完一章，打开 `exercises/chNN_ex.py`，把 `TODO` 的地方填完。
4. 跑起来：`chNN_ex.py` 底部有一堆 `assert`，全过 = 这一章过关。右键 → Run，或者 Alt+Shift+F10。
5. 卡住了，展开文件末尾的 `# region 参考答案`（PyCharm 里 `# region` 可以折叠，点左边小三角展开）。

> 练习文件里有自测断言，改完直接跑就行，不用自己造输入。

## 章节目录

| 章节 | 主题 | C++ 对照 / 一句话要点 |
|---|---|---|
| [ch01](docs/ch01_from_cpp_to_python.md) | 世界观：缩进、变量是标签 | 没有 `{}`、没有分号、变量不是盒子而是便利贴 |
| [ch02](docs/ch02_numbers.md) | 数字与运算符 | `int` 无限精度；`**` 是幂不是指针；`//` 整除 |
| [ch03](docs/ch03_string.md) | 字符串 | 不可变；切片是核心技能；f-string 比 `cout` 好用 |
| [ch04](docs/ch04_list_tuple.md) | 列表与元组 | `list` 是 vector+ 万能容器；深浅拷贝是 C++ 党第一大坑 |
| [ch05](docs/ch05_dict_set.md) | 字典与集合 | 哈希 map / set 内置语法；推导式取代手写循环 |
| [ch06](docs/ch06_control_flow.md) | 控制流 | `for x in xs` 取代下标循环；空容器 = False |
| [ch07](docs/ch07_function.md) | 函数 | 可变默认参数是第二大坑；`*args/**kwargs` |
| [ch08](docs/ch08_iter_generator.md) | 迭代器与生成器 | `yield` 是 C++ 没有的东西，但很像协程 |
| [ch09](docs/ch09_file_exception.md) | 文件 IO 与异常 | `with` = RAII 的作用域 guard |
| [ch10](docs/ch10_class.md) | 类与对象 | `self` 就是隐式的 `this`；`__str__` 取代 `operator<<` |
| [ch11](docs/ch11_module_package.md) | 模块、包、虚拟环境 | `import` 取代 `#include`；`if __name__ == "__main__"` |
| [ch12](docs/ch12_recursion.md) | 递归（专题） | 深度上限 1000、无尾递归优化、`@lru_cache` 取代手写 memo |
| [附录](docs/appendix_cpp_python_cheatsheet.md) | C++ ↔ Python 速查表 | 想不起语法时翻这里 |

## 心理建设：三个必须先接受的认知转变

```
1. 变量不是"装数据的盒子"，是"贴在数据上的便利贴"（= C++ 的引用，但没有解引用符号）
2. 类型跟着值走，不跟着变量走          int x = 5;  →  x = 5（x 明天可以是字符串）
3. 缩进就是语法，不是风格              大括号没了，缩进错了代码就错了
```

接受这三点，后面 10 章都是顺水推舟；不接受，会一直觉得 Python"不严谨"。

## 环境自检

```bash
python --version     # 应该 >= 3.10，推荐 3.12+
python -c "print('ok')"
```

PyCharm 里如果提示 "No interpreter"，去 File → Settings → Python Interpreter → Add Interpreter → 选系统 Python 或者新建一个 Virtualenv。**建议一开始就建 venv**（ch11 会讲为什么）。
