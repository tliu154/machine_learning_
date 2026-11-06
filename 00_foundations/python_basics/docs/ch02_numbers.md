---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch02 数字与运算

## 2.1 三种数字类型

```python
i = 42          # int   —— 任意精度！不会溢出
f = 3.14        # float —— 底层是 C 的 double（IEEE754 双精度）
c = 1 + 2j      # complex —— 虚数单位是 j 不是 i
```

```python
2 ** 100
# 1267650600228229401496703205376   ← int 无限精度，C++ 里早就溢出了
0.1 + 0.2
# 0.30000000000000004               ← float 精度问题和 C++ 一模一样
```

> `bool` 也是数字：`True == 1`，`False == 0`（它是 `int` 的子类）。
> `int(True) + True` 结果是 2。别滥用，但要知道。

### 类型转换

```python
int("123")      # 123        字符串转 int，失败抛 ValueError
int(3.9)        # 3          向零截断，不是四舍五入！
float("3.14")   # 3.14
str(123)        # "123"
round(3.14159, 2)   # 3.14   四舍五入到 2 位（注意用的是"银行家舍入"）
round(2.5)      # 2          ← 银行家舍入是"四舍六入五取偶"，不是 C++ round() 的远离零
abs(-7)         # 7
ord("a")        # 97         转到ASCII码，
ord(c)-ord("a")+1          # 把字符转到1~26
```

> C++ 的隐式转换没了：`3 + "4"` 会 TypeError，**必须显式转**。这是好事。

## 2.2 运算符差异对照

| Python | 含义 | C++ 对照 |
|---|---|---|
| `+ - *` | 加减乘 | 一样 |
| `/` | **真除法，永远返回 float** | C++ 里整数除法会截断，这里不会！ |
| `//` | 整除，向下取整 | `7 / 2`（整数时） |
| `%` | 取模 | `%`（Python 结果符号跟除数，跟 C++ 不同） |
| `**` | **幂运算** | 没有，要 `pow()` |
| `+= -= *= /= //= **=` | 复合赋值 | 有（`**=` C++ 没有） |

```python
7 / 2     # 3.5    ← 注意！不是 3
7 // 2    # 3
7 % 3     # 1
-7 // 2   # -4     ← 向下取整，不是向零取整！C++ 的 -7/2 是 -3
2 ** 10   # 1024
10 ** -1  # 0.1
9 ** 0.5  # 3.0    开平方可以用这个
```

**坑**：`-7 // 2 == -4`，`-7 % 2 == 1`。Python 保证 `(a // b) * b + (a % b) == a` 且余数非负（除数为正时），这是数学上更自洽的定义。

### 一个好用的内置：`divmod`

```python
q, r = divmod(17, 5)    # (3, 2)  同时拿到商和余数
```

### 多返回值 / 交换

```python
a, b = b, a             # 交换！不需要临时变量（右边先整体求值成元组再拆包）
q, r = divmod(x, y)
```

## 2.3 比较运算符可以连写

```cpp
// C++
if (a < b && b < c) { }
```

```python
if a < b < c:           # Python 独有，等价于 a < b and b < c
    ...
if 0 <= score <= 100:   # 判断区间，很符合直觉
```

Python 的逻辑运算符是**英文单词**：

```python
and   or   not        # 代替 && || !
```

而且是**短路求值**，返回值是操作数本身而不是 bool：

```python
name = user_input or "匿名"      # input 为空字符串时用默认值（惯用法！）
result = a and b                 # a 为真返回 b，a 为假返回 a
```

## 2.4 math 模块

```python
import math

math.sqrt(2)      # 1.414...
math.floor(3.7)   # 3    向下取整，返回 int
math.ceil(3.2)    # 4
math.trunc(-3.7)  # -3   向零取整
math.pi, math.e
math.log(x)       # 自然对数 ln
math.log2(x), math.log10(x)
math.sin/cos/tan(r)   # 弧度！不是角度
math.radians(180) # 角度 → 弧度
math.inf          # 无穷大
math.isnan(x)
math.gcd(12, 18)  # 6
math.comb(5, 2)   # 10   组合数 C(5,2)，Python 3.8+
math.perm(5, 2)   # 20   排列数
```

也可以 `from math import sqrt, pi` 然后直接用 `sqrt(2)`。区别见 ch11。

### 精确小数：decimal 与 fractions

金融/高精度场景别用 float：

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")     # Decimal('0.3')  精确！
# 注意：Decimal(0.1) 传 float 会带上误差，必须传字符串

from fractions import Fraction
Fraction(1, 3) + Fraction(1, 6)     # Fraction(1, 2)
```

## 2.5 输出格式化

```python
pi = 3.14159265
print(f"{pi:.2f}")          # 3.14        保留 2 位小数
print(f"{pi:>10.2f}")       # '      3.14'  宽度 10 右对齐
print(f"{255:#x}")          # 0xff        十六进制（带 0x 前缀）
print(f"{255:b}")           # 11111111    二进制
print(f"{1000000:,}")       # 1,000,000   千分位
print(f"{0.25:.1%}")        # 25.0%       百分比
```

格式规范迷你表：`{[填充][对齐][符号][宽度][,][.精度][类型]}`

```python
f"{x:0>5d}"     # 宽度 5，左边补 0
f"{s:*^10}"     # 宽度 10，居中，用 * 填充
f"{x:+d}"       # 强制带正负号
```

这部分不需要背，用到再查。ch03 还会详细讲 f-string。

## 2.6 布尔上下文：什么算"假"

C++ 里只有 `0` 是假。Python 里以下**全部为假**（其余都算真）：

```python
False, None, 0, 0.0, 0j
""            # 空字符串
[] () {} set()  # 空容器（后面学）
```

```python
if not lst:         # 判断列表非空，惯用法。不要写 len(lst) == 0
    print("空了")
```

---

### 小结

- `/` 返回 float，`//` 整除且向下取整，`**` 是幂
- `int` 无限精度，`float` 有精度误差，精确计算用 `Decimal`
- 比较可以连写：`a < b < c`
- 逻辑运算符是 `and or not`，且返回操作数而非 bool

下一章：[ch03 字符串](ch03_string.md)
