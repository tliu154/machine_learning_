---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch05 字典与集合

C++ 的 `std::map` / `std::unordered_map` 是库，Python 的字典是**内置语法**，写起来跟写 JSON 一样自然。

## 5.1 dict ≈ std::unordered_map

```python
d = {}                          # 空字典
scores = {"涛": 95, "李": 88}    # key 是字符串，自动哈希
mixed = {1: "one", "2": 2, (3,3): "tuple key"}   # key 可以是任意可哈希类型

# 增 / 改
scores["王"] = 77
scores["涛"] = 100              # 已存在则是修改

# 查
scores["涛"]                    # 100   不存在会 KeyError！
scores.get("赵", 0)             # 0     不存在返回默认值（推荐）

# 删
del scores["李"]
scores.pop("王")                # 删除并返回值
scores.pop("不存在", 0)          # 带默认值，不抛异常
scores.clear()

# 判断
"涛" in scores                  # True   判断 key 是否存在
"涛" not in scores
len(scores)
```

> ⚠️ C++ 党注意：**没有 `[]` 运算符的"自动插入"语义**。
> `scores["陌生人"]` 在 C++ 的 map 里会插入一个默认值 0，在 Python 里直接 **KeyError**。

### 遍历

```python
for key in scores:              # 默认遍历 key
    print(key, scores[key])

for key, value in scores.items():       # 推荐，items() 返回 (k, v) 元组
    print(key, value)

for value in scores.values():   pass
```

dict 从 Python 3.7 起**保证保持插入顺序**（C++ 的 unordered_map 不保证）。

### 好用的方法

```python
scores.setdefault("赵", 60)     # 不存在就设为 60，存在就什么都不做
scores.update({"a": 1, "b": 2}) # 批量更新

# get_or_create 手动版
other = {}
other.setdefault("k", []).append(1)     # 值为列表时特别好用

# 按值排序
sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

# 反转字典（值必须唯一）
{v: k for k, v in d.items()}

# 合并（Python 3.9+）
merged = d1 | d2
d1 |= d2
```

### defaultdict / Counter

```python
from collections import defaultdict, Counter

# 统计词频：C++ 要写 map<string,int> + 判空，Python 一行
cnt = Counter("abracadabra")
cnt.most_common(2)              # [('a', 5), ('b', 2)]

words = ["apple","banana","avocado","cherry"]
by_letter = defaultdict(list)   # 不存在的 key 自动给个空 list
for w in words:
    by_letter[w[0]].append(w)
# {'a': ['apple','avocado'], 'b': ['banana'], 'c': ['cherry']}
```

## 5.2 set ≈ std::unordered_set

```python
s = {1, 2, 3}
empty = set()          # ⚠️ {} 是空字典不是空集合！
set("abracadabra")     # {'a','b','r','c','d'}  自动去重
```

### 集合运算（对应 `<algorithm>` 里的 set_* ）

| Python | 含义 | C++ |
|---|---|---|
| `a \| b` | 并集 | `set_union` |
| `a & b` | 交集 | `set_intersection` |
| `a - b` | 差集 | `set_difference` |
| `a ^ b` | 对称差 | `set_symmetric_difference` |
| `a <= b` | 子集 | `includes` |

```python
a = {1,2,3}; b = {3,4,5}
print(a | b)    # {1,2,3,4,5}
print(a & b)    # {3}
print(a - b)    # {1,2}
print(1 in a)   # O(1) 查找，比 list 的 O(n) 快得多
```

方法版本：`a.union(b)`, `a.intersection(b)`, `a.add(x)`, `a.remove(x)`（不存在报错）, `a.discard(x)`（不报错）。

> 需要"去重"或"快速判断存在与否"时，第一反应应该是 set，不是 list。
> **set 无序**，别指望顺序。

## 5.3 ⭐ 推导式 Comprehension —— 本章核心

推导式是 Python 的招牌语法，**用一行表达式取代一个循环**。C++ 没有对应物。

```python
# 列表推导式：[表达式 for 变量 in 可迭代对象 if 条件]
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
words   = [w.strip().lower() for w in line.split(",")]

# 等价的传统写法
squares = []
for x in range(10):
    squares.append(x**2)
```

嵌套与多重循环：

```python
pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
matrix2 = [[row[i] for row in matrix] for i in range(3)]   # 转置
flat = [x for row in matrix for x in row]                   # 拍平
```

带 if/else 的三元（注意位置不同！）：

```python
# if 在后面 = 过滤；if 在前面 = 三元表达式
[f"{x}是偶数" if x % 2 == 0 else f"{x}是奇数" for x in range(5)]
```

字典推导式、集合推导式：

```python
{x: x**2 for x in range(5)}             # {0:0, 1:1, 2:4, 3:9, 4:16}
{v: k for k, v in d.items()}            # 反转字典
{len(w) for w in words}                 # 集合：所有单词长度（去重）

# 按条件切分字典
{k: v for k, v in scores.items() if v >= 60}
```

生成器表达式（圆括号）——ch08 会细讲：

```python
sum(x**2 for x in range(1000))     # 不建中间列表，省内存，sum() 里连括号都能省
max(len(w) for w in words)
",".join(str(x) for x in nums)
```

### 什么时候别用推导式

```python
# ✗ 副作用操作不该用推导式（结果列表会被丢弃，纯属浪费）
[print(x) for x in range(10)]

# ✗ 嵌套超过两层就该拆成循环了，可读性崩坏
[[[复杂表达式 for ...] for ...] for ...]
```

## 5.4 可哈希：什么能当 key

- 能当 dict key / set 元素的必须是**可哈希**（hashable）= 生命周期内 hash 值不变
- ✅ `int` `float` `str` `tuple`（所有元素都可哈希时）`None` `bool`
- ❌ `list` `dict` `set`（可变）

```python
{[1,2]: "a"}        # TypeError: unhashable type: 'list'
{(1,2): "a"}        # ✓
```

---

### 小结

| C++ | Python |
|---|---|
| `std::map<K,V>` / `unordered_map` | `dict`，字面量 `{k: v}` |
| `m[key]` 自动插入默认值 | `m[key]` 不存在则 KeyError → 用 `.get()` |
| `set_union` 等 `<algorithm>` 函数 | 运算符 `\| & - ^` |
| 手写循环 push_back | 推导式 `[... for ... if ...]` |

下一章：[ch06 控制流](ch06_control_flow.md)
