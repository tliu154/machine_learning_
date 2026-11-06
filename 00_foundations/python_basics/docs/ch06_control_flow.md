---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch06 控制流

## 6.1 if / elif / else

```python
if score >= 90:
    grade = "A"
elif score >= 80:          # elif，不是 else if！
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"
```

注意：

- 关键字是 `elif`（少写一个空格，多了个 t）
- **不需要括号**，`(score >= 90)` 加了也没错但不符合惯例
- 条件不必是 bool，见 §6.2

### 三元表达式（C++ 的 `?:`）

```cpp
// C++
int m = a > b ? a : b;
```

```python
m = a if a > b else b      # 注意顺序！值 if 条件 else 值
```

读法："取 a，如果 a > b，否则取 b"。语序和自然语言一致，不像 `?:` 那么绕。

## 6.2 真值测试

回看 ch02：这些是"假"，其余都是"真"。

```python
False, None, 0, 0.0, 0j, "", [], (), {}, set()
```

于是 Python 代码可以这么写：

```python
if not name:                # 而不是 if name == "" or name is None
    name = "匿名"

while items:                # 而不是 while len(items) > 0
    items.pop()
```

> 但要注意 **`0` 是假**。如果 0 是合法业务值：
> ```python
> if count is None:      # ✓ 明确判断
> if count:              # ✗ count == 0 也会走这个分支
> ```

## 6.3 for 循环：遍历，不是计数

这是 C++ 党第二个重大思维转变。

```cpp
// C++ 最常见的三段式，Python 里没有对应语法
for (int i = 0; i < n; ++i) { }
```

```python
# Python 的 for 是 for-each：直接给你元素
for item in ["a", "b", "c"]:
    print(item)

# 需要下标 → range
for i in range(10):         # 0,1,...,9   不含 10！
for i in range(2, 10):      # 2..9
for i in range(0, 10, 2):   # 0,2,4,6,8   步长
for i in range(10, 0, -1):  # 10..1       倒着走

# 需要下标+值 → enumerate（ch04）
for i, item in enumerate(lst, start=1):
    print(i, item)

# 并行遍历两个序列 → zip
names = ["a", "b", "c"]
ages = [18, 19, 20]
for name, age in zip(names, ages):
    print(name, age)
# zip 长度以最短的那个为准（想报错就用 strict=True，Python 3.10+）

# 遍历 dict（ch05）
for k, v in d.items():
    ...
```

> 一句话总结：**在 Python 里写 `for i in range(len(x))` 基本是错的**（除非你要改元素）。
> 需要 index？用 `enumerate`。需要两个一起？用 `zip`。

### ⚠️ 遍历时不要修改容器

```python
# ✗ 会跳过元素（因为迭代器内部有下标）
for x in lst:
    if x % 2 == 0:
        lst.remove(x)

# ✓ 遍历副本，或者用推导式过滤
for x in lst[:]:
    ...
lst = [x for x in lst if x % 2 != 0]
```

## 6.4 while

```python
i = 0
while i < 10:
    i += 1
```

### ⚠️ Python 没有 `do...while`

模拟方式：

```python
while True:
    line = input("> ")
    if line == "quit":
        break
    print(line)
```

## 6.5 break / continue / pass

```python
for x in data:
    if x < 0:
        continue        # 跳过本次，进入下一轮
    if x > 100:
        break           # 跳出整个循环
    process(x)
```

`pass` 是**空语句占位符**（C++ 的 `;` 或 `{}`）：

```python
if x > 0:
    pass            # 什么都不做，但不写会 SyntaxError

def todo():         # 先搭骨架，函数体以后再写
    pass

class Empty:
    pass
```

## 6.6 ⭐ 循环的 else 子句（Python 独有）

```python
for x in items:
    if x == target:
        print("找到了")
        break
else:
    print("没找到")      # 只有【没被 break】时才执行！
```

`while` 也一样。**是 `for...break` 配套的"没找到"分支**。

```python
# 经典用法：判断素数
for d in range(2, int(n**0.5) + 1):
    if n % d == 0:
        print(n, "不是素数")
        break
else:
    print(n, "是素数")
```

这个语法反直觉（很多人第一反应以为 else 是"循环没执行"），记住它的意思是 **"no break"** 就够了。

## 6.7 match 语句（Python 3.10+）

真正的 switch-case，而且能做**结构匹配**（远超 C++ 的 switch）。

```python
command = input()
match command.split():
    case ["quit"]:
        print("退出")
    case ["load", filename]:                    # 解构列表，绑到 filename
        print(f"加载 {filename}")
    case ["add", *nums]:                        # 星号收集剩余
        print(f"求和 {sum(int(n) for n in nums)}")
    case _:                                     # 通配符 default
        print("未知命令")
```

匹配字典：

```python
match point:
    case {"x": 0, "y": 0}:
        print("原点")
    case {"x": x, "y": y} if x == y:            # 守卫条件
        print("在 y=x 上")
    case {"x": x, "y": y}:
        print(f"({x}, {y})")
```

## 6.8 海象运算符 `:=`（Python 3.8+）

在表达式内部做赋值，避免重复计算：

```python
# 传统写法要调用两次
if (n := len(data)) > 10:
    print(f"数据太多，有 {n} 条")

while (line := input()) != "":
    print(line)

# 在推导式里复用计算结果
[y for x in data if (y := f(x)) is not None]
```

用得不多，但看到别懵。

---

### 小结

| C++ | Python |
|---|---|
| `for(int i=0;i<n;i++)` | `for i in range(n)` 或 `for x in xs` |
| `for(auto& x : v)` | `for x in v` |
| `auto [i,x]` 无对应 | `enumerate(v)` / `zip(a, b)` |
| `?:` | `a if cond else b` |
| `switch` | `match`（3.10+），功能强得多 |
| `do...while` | 没有，用 `while True` + `break` |
| `{}` 空块 | `pass` |

下一章：[ch07 函数](ch07_function.md)
