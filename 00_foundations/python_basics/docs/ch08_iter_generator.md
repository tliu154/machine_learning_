---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch08 迭代器与生成器

C++ 有 iterator，但没有生成器。这一章是 Python 最有特色的部分之一。

## 8.1 可迭代对象 vs 迭代器

- **Iterable（可迭代对象）**：能用 `for x in obj` 的东西。`list` `str` `dict` `tuple` `set` `range` `文件对象`
- **Iterator（迭代器）**：带 `__next__()` 的状态对象，迭代器本身也可迭代

```python
lst = [1, 2, 3]         # list 是 iterable，不是 iterator
it = iter(lst)          # 拿到迭代器
next(it)                # 1
next(it)                # 2
next(it)                # 3
next(it)                # StopIteration 异常！
```

`for` 循环的本质就是：

```python
it = iter(lst)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
```

**迭代器是一次性的**，走完就空了：

```python
nums = iter([1,2,3])
list(nums)      # [1,2,3]
list(nums)      # []      已经耗尽
```

```python
list(reversed([1,2,3]))     # reversed 返回迭代器，不 list() 就看不到 contents
list(zip(a, b))             # zip 也是迭代器
list(enumerate(xs))         # 同理
```

## 8.2 生成器函数：yield

带 `yield` 的函数叫生成器函数。调用它**不执行函数体**，而是返回一个生成器对象：

```python
def countdown(n):
    while n > 0:
        yield n         # 交出一个值，函数在这里"暂停"
        n -= 1

gen = countdown(3)          # 什么都不打印，函数没运行
next(gen)                   # 3
next(gen)                   # 2
for x in countdown(3):      # 3 2 1
    print(x)
list(countdown(3))          # [3,2,1]
```

**`return` vs `yield`**：

| | `return` | `yield` |
|---|---|---|
| 返回值 | 直接给调用者，函数结束 | 交出一个值，**函数状态挂起** |
| 再次调用 | 从头开始 | 从上次 `yield` 处继续 |
| 内存 | 一次性算完所有结果 | 按需生成，一个一个给 |

对比 C++20 的 coroutine 概念类似，但 Python 用起来简单一万倍。

### 为什么要用它？惰性求值 + 省内存

```python
def read_huge_file(path):
    with open(path) as f:
        for line in f:          # 文件本身就是迭代器，一行一行读，不占内存
            yield line.strip()

for line in read_huge_file("big.log"):
    process(line)               # 10GB 的文件也不会爆内存
```

```python
# 斐波那契：无限序列
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 取前 10 个
from itertools import islice
list(islice(fib(), 10))     # [0,1,1,2,3,5,8,13,21,34]
```

> 注意 `while True` 的生成器不会死循环 —— 它每次 yield 后就停住了，只有你 next 才继续。

## 8.3 生成器表达式

圆括号版本的小推导式，ch05 见过：

```python
gen = (x**2 for x in range(10))     # 生成器对象，还没算任何东西
sum(gen)                            # 285，边遍历边算，不占内存

# 对比列表推导式
lst = [x**2 for x in range(10)]     # 立刻算出全部 10 个数存起来
```

**生成器 vs 列表何时选**：

| 场景 | 选 |
|---|---|
| 数据量大 / 可能无限 | 生成器表达式 |
| 只要遍历一次，或做 `sum/max/any/all` | 生成器表达式 |
| 需要多次遍历、下标访问、`len()` | 列表推导式 |
| `sum(x for x in xs)` 里 | 括号可以省略（在函数调用里） |

```python
any(x > 10 for x in nums)       # 有没有大于 10 的
all(x > 0 for x in nums)        # 是不是都大于 0
max(x for x in nums if x % 2)   # 奇数里最大的
```

## 8.4 itertools 标准库（偷懒神器）

```python
from itertools import count, cycle, repeat, islice, chain, combinations, permutations, groupby, accumulate

count(10)               # 10,11,12,... 无限累加
cycle("AB")             # A,B,A,B,... 无限循环
repeat(0, 3)            # 0,0,0
islice(fib(), 5)        # 从无限生成器取前 5 个

chain([1,2], [3,4])                     # 1,2,3,4   串接多个可迭代对象
accumulate([1,2,3,4])                   # 1,3,6,10  前缀和
combinations([1,2,3], 2)                # (1,2)(1,3)(2,3)
permutations([1,2,3], 2)                # (1,2)(1,3)(2,1)(2,3)(3,1)(3,2)
product([1,2], "ab")                    # 笛卡尔积

# groupby 注意：必须先按 key 排好序
for key, group in groupby(sorted_words, key=len):
    print(key, list(group))
```

## 8.5 常见"只要/这种"的惯用法

```python
with open("f.txt") as f:
    first = next(f, None)           # 只读第一行，文件不存在时有默认值

import itertools
def chunked(it, n):                 # 每 n 个一组
    it = iter(it)
    while batch := list(islice(it, n)):
        yield batch

list(chunked(range(7), 3))          # [[0,1,2],[3,4,5],[6]]
```

## 8.6 装饰器（进阶，先认识）

```python
import time
from functools import wraps

def timer(func):                    # 装饰器是一个"接收函数、返回函数"的函数
    @wraps(func)                    # 保留原函数的名字和文档
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时 {time.perf_counter()-start:.4f}s")
        return result
    return wrapper

@timer                              # 语法糖，等价于 slow_func = timer(slow_func)
def slow_func():
    time.sleep(0.5)

slow_func()                         # slow_func 耗时 0.5003s
```

`@` 语法等价于 AOP / 中间件。常见用途：计时、日志、权限校验、缓存（`@functools.lru_cache`）、Flask 路由。

不要求你现在会写，**看到 `@xxx` 要知道那是把一个函数包了一层**。

---

### 小结

| 概念 | 说明 |
|---|---|
| Iterable | 能 `for x in` 的对象 |
| Iterator | `next()` 逐个取值，一次性 |
| `iter(obj)` / `next(it)` | 手动推进迭代器 |
| `yield` | 函数暂停并交值，再次调用从原地继续 |
| 生成器表达式 | `(... for ...)`，惰性求值省内存 |
| itertools | 无限序列、组合、累加等现成工具 |

下一章：[ch09 文件 IO 与异常](ch09_file_exception.md)
