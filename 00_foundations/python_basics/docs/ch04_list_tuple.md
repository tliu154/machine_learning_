---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch04 列表与元组

## 4.1 list ≈ std::vector<任意类型>

```python
a = []                      # 空列表
b = [1, 2, 3]
c = [1, "two", 3.0, None]   # 元素可以是不同类型！（底层存放的是对象的引用）
d = list(range(5))          # [0,1,2,3,4]
e = list("abc")             # ['a','b','c']
```

底层是**动态数组**（和 vector 一样），尾插 O(1)，中间插入 O(n)。

## 4.2 增删改查

```python
lst = [10, 20, 30]

lst.append(40)          # [10,20,30,40]          尾部加
lst.insert(1, 15)       # [10,15,20,30,40]       指定位置插（O(n)，少用）
lst.extend([50, 60])    # [10,15,20,30,40,50,60] 批量追加
lst += [70]             # 等价 extend
lst.remove(15)          # 删除第一个值为 15 的元素（找不到 → ValueError）
lst.pop()               # 删除并返回最后一个元素
lst.pop(0)              # 删除并返回索引 0 的元素（O(n)，少用）
lst.clear()             # 清空
lst.index(20)           # 找到 20 的第一个下标（没有 → ValueError）
lst.count(20)           # 出现次数
lst.sort()              # 原地排序
lst.reverse()           # 原地反转
```

返回新列表的版本：

```python
sorted(lst)                     # 排序后的新列表，lst 不变
sorted(lst, reverse=True)       # 降序
sorted(lst, key=abs)            # 按元素绝对值排序（key 函数！C++ 要写 lambda 比较器）
sorted(lst, key=lambda s: len(s))
sorted(words, key=str.lower)    # 忽略大小写排
reversed(lst)                   # 反向迭代器，要 list() 包一下
```

> C++ 的 `sort(vec.begin(), vec.end(), cmp)` 需要写比较器；
> Python 的 `key=` 只需要一个"把一个元素映射成排序依据"的函数，简单得多。

### del 语句

```python
del lst[0]          # 按下标删
del lst[1:3]        # 按切片删
```

## 4.3 切片（同字符串，且能做更多）

```python
nums = [0,1,2,3,4,5,6,7,8,9]
nums[2:5]       # [2,3,4]
nums[:3]        # [0,1,2]
nums[-3:]       # [7,8,9]
nums[::2]       # [0,2,4,6,8]
nums[::-1]      # 倒序，产生新列表
nums[1::2]      # [1,3,5,7,9]
nums[:]         # 浅拷贝！
```

列表**可变**，所以切片可以放在赋值左边：

```python
lst = [1,2,3,4,5]
lst[1:3] = [9, 9, 9]     # [1,9,9,9,4,5]  长度可以不等！
lst[1:4] = []            # [1,4,5]        用空列表删除一段
lst[::2] = [0,0,0,0,0]   # 步长切片赋值时长度必须匹配
```

## 4.4 ⚠️ 深浅拷贝 —— C++ 党第一大坑

```python
a = [1, 2, 3]
b = a               # ✗ 引用同一个列表（想想便利贴）
c = a.copy()        # ✓ 浅拷贝（等价于 list(a) 或 a[:]）
c[0] = 99
print(a)            # [1,2,3] 没有被改 ✓
```

**浅**拷贝的意思是：只拷一层，里面的元素还是共享的。

```python
matrix = [[0,0], [0,0]]
m2 = matrix.copy()
m2[0][0] = 99
print(matrix)       # [[99,0],[0,0]]  ← matrix 被改了！
                    # 因为 copy() 只拷了外层，两个列表共享同样的两个子列表
```

解决：

```python
import copy
m2 = copy.deepcopy(matrix)      # 递归深拷贝
# 或者自己写 list 推导式：[row[:] for row in matrix]
```

> 什么时候需要深拷贝？只有当容器里**嵌套了可变对象**（列表套列表、列表套字典）时。
> 全是数字/字符串的话 `.copy()` 就够用了。

### 乘法创建的陷阱

```python
zeros = [[0] * 3] * 4    # ✗✗ 四行是同一个列表对象！改一个改全部
zeros = [[0] * 3 for _ in range(4)]   # ✓ 写法正确
```

但 `[0] * 3` 本身没问题（`int` 不可变）：
```python
a = [0] * 3     # [0,0,0]  可以，0 是不可变对象
```

## 4.5 tuple：不可变的列表

```python
t = (1, 2, 3)
single = (1,)         # ⚠️ 单元素元组必须加逗号！(1) 只是加了括号的整数 1
empty = ()
t[0]                  # 1   支持索引和切片
# t[0] = 9            # ✗ 不可变
a, b, c = t           # 拆包 unpack
x, y = y, x           # 交换变量用的就是这个机制
t.count(1), t.index(2)
list(t) / tuple([1,2]) # 互相转换
```

**为什么需要 tuple？**

1. 不可变 → 可哈希 → **能当 dict 的 key**、能放进 set（list 不行）
2. 数据不会被意外修改
3. 函数返回多个值的底层机制

### 拆包（解构）的各种姿势

```python
first, second, third = [1, 2, 3]
first, *rest = [1, 2, 3, 4]         # first=1, rest=[2,3,4]    星号收集剩余！
*a, last = [1, 2, 3, 4]             # a=[1,2,3], last=4
head, *mid, tail = [1,2,3,4,5]
a, b = "XY"                          # 字符串也能拆

for i, value in enumerate(["a","b"]):   # enumerate 生成 (index, value) 元组
    print(i, value)
```

```cpp
// C++17 的结构化绑定 std::tie / auto [a,b]，Python 从一开始就支持且更灵活
```

## 4.6 list 作为栈/队列

```python
stack = []
stack.append(1)     # push
stack.pop()         # pop 尾部 → 栈

from collections import deque
q = deque()
q.append(1)         # 右侧入
q.popleft()         # 左侧出 → 队列，O(1)
q.appendleft(0)

# 别用 list.pop(0) 做队列！那是 O(n)
```

## 4.7 遍历的正确姿势

```cpp
// C++ 你可能习惯这样
for (int i = 0; i < v.size(); ++i) { std::cout << v[i]; }
```

```python
# ✗ 不推荐（Python 里几乎不需要下标）
for i in range(len(lst)):
    print(lst[i])

# ✓ 推荐
for item in lst:
    print(item)

# ✓ 需要下标时
for i, item in enumerate(lst):
    print(i, item)

# ✓ 需要下标且从 1 开始
for i, item in enumerate(lst, start=1):
    print(i, item)
```

---

### 小结

| C++ | Python |
|---|---|
| `std::vector<T>` | `list`（可放任意类型） |
| `v.push_back(x)` | `v.append(x)` |
| `v.size()` | `len(v)` |
| 拷贝构造 = 深拷贝 | `=` 是引用，`copy()` 浅、`deepcopy()` 深 |
| `std::tuple` | `tuple`，但语法更轻、能拆包 |
| 下标遍历 | `enumerate()` |

下一章：[ch05 字典与集合](ch05_dict_set.md)
