---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch12 递归

> 前置：ch07 函数。递归不需要新语法，只是一种"函数自己调自己"的写法。

## 12.1 递归 = 函数自己调用自己

C++ 里你已经写过，概念完全一致。**唯一的区别是失败时的表现**：

| | C++ | Python |
|---|---|---|
| 递归太深 | 栈溢出 → 程序直接崩溃（段错误） | 抛 `RecursionError` 异常（**可以捕获**） |
| 默认深度 | 取决于栈大小（通常几万层） | **1000 层**（`sys.getrecursionlimit()`） |
| 尾递归优化 | `-O2` 编译器会做 | **CPython 永远不做**，别指望 |

```python
import sys
sys.getrecursionlimit()     # 1000
sys.setrecursionlimit(3000) # 可以改，但改太大真的会崩（C 栈溢出，进程直接挂）
```

## 12.2 两个要素：缺一不可

```python
def factorial(n):
    if n <= 1:              # ① 终止条件 base case —— 不写就无限递归
        return 1
    return n * factorial(n - 1)   # ② 递归步 recursive case —— 必须朝终止条件靠近
```

写递归时心里默念两句：

1. **最简单的情况是什么，直接返回什么？**（n=0/1、空字符串、空列表）
2. **怎么把问题缩小一点点再交给自己？**（n-1、去掉首字符、左右子区间）

## 12.3 调用栈长什么样

`factorial(3)`：

```
factorial(3) → 3 * factorial(2)
                   factorial(2) → 2 * factorial(1)
                                      factorial(1) → 1     ← 触底
                                  2 * 1 = 2
              3 * 2 = 6
```

**先一层层"下去"，再一层层"回来"**。递归的代价就是这 1000 层的栈。

## 12.4 循环 → 递归的思维转换

C++ 党习惯这样：

```python
def sum_list(nums):
    total = 0
    for x in nums:
        total += x
    return total
```

递归版要换一种问法：**"列表的和 = 第一个元素 + 剩下部分的和"**

```python
def sum_list(nums):
    if not nums:              # 空列表 = 0
        return 0
    return nums[0] + sum_list(nums[1:])   # 首元素 + 剩余部分的和
```

看出来了吗？递归的思路是**把问题拆成一个"当前元素"和一个"规模更小的同类问题"**，而不是"一步步累加"。

> ⚠️ 这个例子用切片 `nums[1:]`，每次都产生新列表，是 O(n²)。
> 真正要写求和当然用 `sum(nums)`。这里只是拿来说明思路。
> 想避免切片开销可以传下标，但初学阶段先别纠结效率。

## 12.5 经典例子

### 斐波那契 + 记忆化 —— 必会

```python
def fib(n):                     # 朴素递归
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(35)     # 慢到怀疑人生（O(2^n)，重复计算了几百万次）
```

画一下 `fib(5)` 的调用树就知道有多浪费：`fib(3)` 被算了 2 次，`fib(2)` 算了 3 次……

**一行装饰器解决**：

```python
from functools import lru_cache

@lru_cache(maxsize=None)        # 缓存：算过的参数直接返回记下的结果
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(100)    # 354224848179261915075  瞬间出结果
```

> `@lru_cache` 就是 C++ 里手写 `unordered_map<int, long long> memo` 的平替，而且不污染函数体。
> 注意：被缓存的函数参数必须**可哈希**（int/str/tuple 可以，list 不行）。

### 字符串反转

```python
def reverse(s):
    if len(s) <= 1:
        return s
    return s[-1] + reverse(s[:-1])     # 最后一个字符 + 前面部分的反转
```

### 判断回文

```python
def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])      # 掐头去尾再看
```

### 欧几里得算法（GCD）

```python
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

gcd(48, 18)     # 6
```

### 二分查找

```python
def binary_search(nums, target, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1                       # 没找到
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search(nums, target, mid + 1, hi)
    else:
        return binary_search(nums, target, lo, mid - 1)
```

> 用默认参数 `lo/hi` 传递搜索区间，比每次切片 `nums[mid+1:]` 好（切片会丢掉真实下标）。

## 12.6 递归的两个坑

### 坑 1：忘了终止条件

```python
def bad(n):
    return bad(n + 1)       # 永远到不了底
# RecursionError: maximum recursion depth exceeded
```

### 坑 2：重复计算

见上面的 `fib`。**只要递归树里有重复的子问题，就上 `@lru_cache`**。

### 坑 3：可变默认值 + 递归

```python
# ✗ 和 ch07 一样的坑，递归里更隐蔽
def collect(n, acc=[]):
    ...
# ✓
def collect(n, acc=None):
    if acc is None:
        acc = []
    ...
```

## 12.7 递归 + yield：遍历树形结构

递归遍历目录是最自然的例子：

```python
from pathlib import Path

def walk(path):
    """产出目录下所有文件（含子目录）的 Path"""
    for entry in Path(path).iterdir():
        if entry.is_dir():
            yield from walk(entry)      # yield from = 把子生成器的值直接透传出去
        else:
            yield entry

for f in walk("."):
    print(f)

# 一行统计：
sum(f.stat().st_size for f in walk("."))
```

> `yield from` 在递归里特别好用，比"把结果列表层层 return 回去"清爽得多（ch08 讲过生成器）。

## 12.8 调试递归：打印缩进

递归最烦的是看不清在第几层。加一个 `depth` 参数就够了：

```python
def factorial(n, depth=0):
    print("  " * depth + f"→ factorial({n})")
    if n <= 1:
        print("  " * depth + f"← 返回 1")
        return 1
    result = n * factorial(n - 1, depth + 1)
    print("  " * depth + f"← factorial({n}) = {result}")
    return result
```

输出：

```
→ factorial(3)
  → factorial(2)
    → factorial(1)
    ← 返回 1
  ← factorial(2) = 2
← factorial(3) = 6
```

一眼看清"下去"和"回来"的过程。写完调通再把 print 删掉。

## 12.9 递归 vs 循环：怎么选

| 场景 | 建议 |
|---|---|
| 数据是**树形/嵌套**的（JSON、目录、语法树） | **递归**，循环写起来很痛苦 |
| 问题本身是递归定义的（斐波那契、汉诺塔、组合） | **递归**，思路直接 |
| 深度可能超过几百层（链表 10000+ 节点） | **循环**，Python 会 RecursionError |
| 简单的线性累加/遍历 | **循环**（或内置函数），别为了递归而递归 |
| 需要极致性能 | **循环**，函数调用在 CPython 里不便宜 |

一句话：**能用循环简单写清楚的就别递归；数据天然是嵌套的就别硬写循环。**

## 12.10 三个"能讲明白就出师"的题

1. **汉诺塔**：`hanoi(n)` 返回移动步骤。核心是"把 n-1 个挪到中转柱 → 挪最大的 → 把 n-1 个挪回来"。
2. **快速排序**：选基准 → 小的放左边、大的放右边 → 对左右各自递归。
3. **完全拍平嵌套列表**：`[1,[2,[3,4]],5] → [1,2,3,4,5]`。

这三道题在练习文件里都有，写不出来很正常，先看答案再合上默写一遍。

---

### 小结

- 递归 = base case + 朝着 base case 缩小的 recursive case
- Python 递归上限 1000 层，**没有尾递归优化**，深了会 `RecursionError`
- 有重复子问题就加 `@lru_cache`
- 树形/嵌套结构用递归 + `yield from` 最舒服
- 调试时传个 `depth` 参数打印缩进

下一站：练习文件 [ch12_ex.py](../exercises/ch12_ex.py)
