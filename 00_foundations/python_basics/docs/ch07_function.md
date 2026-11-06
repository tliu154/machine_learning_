---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch07 函数

## 7.1 定义与调用

```cpp
// C++
int add(int a, int b) { return a + b; }
```

```python
def add(a, b):
    """返回两数之和。           ← docstring，三引号，第一行就是它才会被 IDE 识别"""
    return a + b

result = add(1, 2)
print(add.__doc__)      # 打印文档字符串
help(add)               # 交互式帮助
```

要点：

- `def` 关键字，缩进定函数体，**没有返回类型声明**
- 没有 `return` 或 `return` 后面没值 → 返回 `None`
- docstring 不是注释，它是运行时可访问的字符串（PyCharm 悬浮会显示）
- **函数必须先定义后调用**（Python 从上往下执行，不像 C++ 可以前置声明）

```python
greet()             # ✗ NameError，因为下面才定义
def greet():
    print("hi")
```

但如果在 `main()` 里调用就没问题：

```python
def main():
    greet()             # ✓ 运行时 greet 已经定义好了

def greet():
    print("hi")

if __name__ == "__main__":
    main()
```

## 7.2 返回多个值

```cpp
// C++ 要么用 struct，要么用 std::pair / tuple
std::pair<int,int> divmod(int a, int b);
```

```python
def divmod_custom(a, b):
    return a // b, a % b      # 逗号分隔，实际返回的是一个 tuple

q, r = divmod_custom(17, 5)   # 自动拆包
```

本质是元组打包，写法上看起来像多返回值。

## 7.3 参数传递：传对象引用

理解这个就能解释很多"灵异现象"：

```python
def modify(n, lst):
    n = n + 1           # int 不可变 → 只是把局部的便利贴撕下来贴到新对象，外面看不到
    lst.append(99)      # list 可变 → 原地改了同一个对象，外面看得到！

x, mylist = 1, []
modify(x, mylist)
print(x, mylist)        # 1 [99]
```

规则：

- 传入的是**对象的引用**（不是拷贝，也不是 C++ 的引用 `&` 那么强）
- **重新绑定形参**（`n = ...`）对外部无影响
- **原地修改对象**（`lst.append/[]= /d.update`）对外部有影响

想要不影响外部的列表：

```python
def safe_modify(lst):
    lst = lst.copy()    # 或者接收时就 list(lst)
    ...
```

> C++ 对照：`void f(std::vector<int> v)` 拷贝，`void f(std::vector<int>& v)` 引用。
> Python 永远是"传引用"，区别只在于你的操作是「改对象」还是「换对象」。

## 7.4 默认参数 ⚠️ 第二大坑

```python
def greet(name, greeting="你好"):
    print(f"{greeting}, {name}")

greet("涛")                  # 你好, 涛
greet("涛", "Hi")            # Hi, 涛
greet(name="涛", greeting="Hi")   # 关键字参数，可以乱序
```

**坑在这里**：

```python
# ✗✗✗ 千万不要用可变对象做默认值
def add_item(x, items=[]):
    items.append(x)
    return items

add_item(1)     # [1]
add_item(2)     # [1, 2]     ← 默认值只会在函数定义时创建一次，之后一直复用！
add_item(3)     # [1, 2, 3]
```

正确写法：

```python
def add_item(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items
```

**规则：默认参数永远用不可变值（`None` / 数字 / 字符串 / tuple）**。

## 7.5 `*args` 与 `**kwargs`

```python
def total(*args):           # args 是一个 tuple
    return sum(args)

total(1, 2, 3, 4)           # 10
```

```python
def show_info(**kwargs):    # kwargs 是一个 dict
    for k, v in kwargs.items():
        print(k, v)

show_info(name="涛", age=19)     # 关键字参数收集成字典
```

组合使用的标准签名顺序：

```python
def f(pos1, pos2, default=10, *args, **kwargs):
    ...
```

调用时也能用 `*` / `**` **拆包传参**：

```python
nums = [1, 2, 3]
total(*nums)                    # 等价于 total(1,2,3)
conf = {"name": "涛", "age": 19}
show_info(**conf)               # 等价于 show_info(name="涛", age=19)
```

## 7.6 参数类型限制（Python 3.8+）

```python
def f(a, b, /, c, d, *, e, f2):
    ...
#   ↑斜杠前：只能按位置传    ↑中间：都行   ↑星号后：只能按关键字传
```

```python
def greet(name, /, greeting="你好", *, punct="!"):
    print(f"{greeting}{punct} {name}")

greet("涛")                          # ✓
greet("涛", greeting="Hi")           # ✓
greet(name="涛")                     # ✗ name 只能位置传
greet("涛", "Hi", "?")               # ✗ punct 必须写成 punct="?"
```

自己写代码一般用不到，但读标准库源码时能看到。

## 7.7 lambda：单行匿名函数

```cpp
// C++11 lambda
auto square = [](int x) { return x * x; };
```

```python
square = lambda x: x * x        # 只能有一个表达式，不能有语句，自动 return
```

**Python 的 lambda 比 C++ 弱很多** —— 不能写多行、不能有 `if/for/return`。所以只用在很短的地方：

```python
sorted(students, key=lambda s: s["score"])          # 最常见用途
list(map(lambda x: x * 2, nums))
```

需要多行逻辑就用 `def`。**永远不要把 lambda 赋值给变量**（上面 `square = lambda...` 是不推荐的写法，PEP8 让你用 def）。

## 7.8 作用域 LEGB

```python
x = 10              # 全局

def outer():
    y = 20          # 外层函数的局部（enclosing）

    def inner():
        z = 30      # 局部
        print(x, y, z)      # 读：往外层一层层找，都能读到

    # y = y + 1     # ✗ UnboundLocalError！
```

**在函数里给变量赋值 = 声明它是局部变量**。所以 `y = y + 1` 会让 `y` 变成局部的，然后读到一个还没定义的局部变量 → 报错。

解决：

```python
count = 0
def increment():
    global count        # 声明：我要改的是全局那个 count
    count += 1

def outer():
    n = 0
    def inner():
        nonlocal n      # 声明：我要改的是外层函数的 n（不是全局）
        n += 1
    inner()
    print(n)            # 1
```

> 只**读**不用 `global`；要**改**才需要。

## 7.9 类型注解（Type Hints）

Python 3.5+ 可以给函数标注类型 —— **解释器不检查**（纯注释性质），但 PyCharm 会用它做补全和报错提示。

```python
def add(a: int, b: int) -> int:
    return a + b

from typing import Optional, Union

def find(name: str) -> Optional[int]:       # Optional[int] = int | None
    ...

Vector = list[float]        # Python 3.9+ 起，内置类型可以直接下标

def scale(v: Vector, k: float) -> Vector:
    return [x * k for x in v]
```

Python 3.10+ 可以用 `|`：`int | str` 代替 `Union[int, str]`。

想真正做静态检查，用 `mypy`：

```bash
pip install mypy
mypy my_script.py
```

> 建议：**写类型注解**。PyCharm 靠它能给你准确补全，写大项目时价值很高。

## 7.10 高阶函数内置三件套

```python
nums = [1, 2, 3, 4]

list(map(lambda x: x*2, nums))              # [2,4,6,8]   map ≈ <algorithm> 的 transform
list(filter(lambda x: x%2==0, nums))        # [2,4]       filter ≈ copy_if
import functools
functools.reduce(lambda a,b: a+b, nums)     # 10         reduce ≈ accumulate
```

但实际中 Python 社区更推荐推导式：

```python
[x*2 for x in nums]                 # 比 map+lambda 更清晰
[x for x in nums if x % 2 == 0]
```

---

### 小结

| C++ | Python |
|---|---|
| `int f(int a, int b)` | `def f(a, b):`（返回值无类型） |
| 前置声明 / 头文件 | 必须先 def 再调用（或放进 main） |
| 引用传参 `T&` | 默认传对象引用，看你是否原地改 |
| 默认实参求值时机 | **只求值一次**，别用可变默认值 |
| 可变参数模板 | `*args` / `**kwargs` |
| lambda 支持多语句 | lambda 只能单行表达式 |

下一章：[ch08 迭代器与生成器](ch08_iter_generator.md)
