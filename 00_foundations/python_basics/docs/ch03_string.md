---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
 # ch03 字符串

Python 的字符串 `str` 大致对应 C++ 的 `std::string`，但**不可变**，且 Unicode 天然支持。

## 3.1 不可变！这是首要认知

```cpp
// C++
std::string s = "abc";
s[0] = 'A';        // 合法，原地修改
```

```python
s = "abc"
# s[0] = "A"       # TypeError！str 不支持原地修改
s = "Abc"          # 只能重新赋值（其实是新建了一个对象，把便利贴移过去）
```

**所有"修改"字符串的方法，其实都返回一个新字符串**：

```python
s = "hello"
t = s.upper()      # "HELLO"，但 s 还是 "hello"
print(s)           # hello
s = s.upper()      # 想改就得重新贴标签
```

## 3.2 引号与转义

```python
a = '单引号'
b = "双引号"       # 两者完全等价，随你习惯（社区偏双引号）
c = """三引号
可以换行"""
d = r"C:\new\test"     # r 前缀 = raw 字符串，反斜杠不转义（写正则/Windows 路径神器）
e = "他说\"你好\""      # 转义
```

> C++ 党注意：Python **没有 `char` 类型**。`s[0]` 得到的是一个长度为 1 的 `str`，不是字符。
> 单双引号在 Python 里没有任何区别（不像某些语言里单引号表示 char）。

## 3.3 索引：负数索引是真香之物

```python
s = "Python"
#     P y t h o n
# 正: 0 1 2 3 4 5
# 负:-6-5-4-3-2-1
s[0]      # 'P'
s[-1]     # 'n'   最后一个字符！C++ 要写 s[s.size()-1]
s[-2]     # 'o'
len(s)    # 6     内置函数，不是成员函数 s.length()
```

## 3.4 切片 —— 本章核心技能

```python
s[start:stop:step]      # 左闭右开！包含 start，不包含 stop
```

```python
s = "Python"
s[0:2]      # 'Py'     索引 0,1（不含 2）
s[2:]       # 'thon'   省略 stop = 到末尾
s[:3]       # 'Pyt'    省略 start = 从头
s[:]        # 'Python' 全复制
s[::2]      # 'Pto'    步长 2
s[::-1]     # 'nohtyP' 倒序！经典技巧
s[-3:]      # 'hon'    后三个
s[1:-1]     # 'ytho'   掐头去尾
```

要点：

- **永远左闭右开**，`s[a:b]` 的长度是 `b - a`
- 越界**不报错**，自动夹紧：`s[0:100]` 返回整个串
- 但单个下标越界**会报错**：`s[100]` → IndexError
- 切片产生新对象，`s[:]` 是浅拷贝的常用写法

```python
# 判断回文字符串 —— 一行
def is_palindrome(s):
    return s == s[::-1]
```

## 3.5 f-string（格式化字符串字面值）

Python 3.6+ 的产物，**忘掉 `%` 和 `.format()` 吧**。

```python
name = "涛"
age = 19
score = 95.5

print(f"我叫{name}，今年{age}岁")
print(f"平均分{score:.1f}")             # 95.5      冒号后接格式规范
print(f"明年{age + 1}岁")                # 大括号里可以放表达式
print(f"{'是' if age >= 18 else '否'}成年")
print(f"{[i**2 for i in range(5)]}")     # 甚至可以放推导式
print(f"{{字面大括号}}")                  # 两个括号转义成一个
print(f"{age=}")                        # age=19   调试神器，Python 3.8+
```

对比 C++20 之前只能靠 `printf` / `ostringstream` 拼。

## 3.6 常用字符串方法

```python
s = "  Hello World  "

# 查找 / 判断
s.find("World")        # 8    找不到返回 -1（不像 C++ 的 npos）
s.index("World")       # 8    找不到抛 ValueError
"World" in s           # True   用 in 判断子串最 Pythonic
s.count("l")           # 3
s.startswith("  He")   # True
s.endswith("ld")       # False  尾部还有空格
"abc123".isdigit()     # False  (整体)全是数字？类似的还有 isalpha/isalnum/isspace
"".join               # 见下

# 变换（全部返回新串）
s.strip()              # 'Hello World'   去掉两端空白
s.lstrip() / s.rstrip()
s.lower() / s.upper()
s.title()              # '  Hello World  ' → 首字母大写
s.replace("World", "Python")
s.swapcase()

# 拆分 / 拼接
"a,b,c".split(",")        # ['a', 'b', 'c']
"a  b   c".split()        # ['a', 'b', 'c']   不传参数 = 按任意空白切，自动去空串
"a\nb\nc".splitlines()    # ['a', 'b', 'c']
"-".join(["a","b","c"])   # 'a-b-c'   注意是 join(列表)，不是 列表.join()
" ".join(str(x) for x in [1,2,3])   # '1 2 3'
```

> `join` 的方向反直觉：**分隔符.join(列表)**。
> 记法：你在用 `-` 去粘连 `["a","b","c"]`，所以 `-` 是主语。

还有：

```python
s.zfill(5)          # '00042' 左补零
s.center(10, '*')   # 居中用 * 填充
s.partition("=")    # ('key', '=', 'value')  三段切分，解析配置很好用
s.removeprefix("http://") / s.removesuffix(".txt")   # 3.9+
```

## 3.7 字符串也是序列

```python
for ch in "abc":        # 逐字符遍历
    print(ch)

list("abc")         # ['a','b','c']
sorted("cab")       # ['a','b','c']  返回排序后的列表
max("abc")          # 'c'
"".join(reversed("abc"))    # 'cba'    reversed 返回迭代器，要 join 回来
```

字符串支持 `+` 拼接和 `*` 重复，但**在循环里别用 `+` 累加字符串**（每次都新建对象，O(n²)）。用列表 `append` 最后 `join`。

```python
# 慢
res = ""
for i in range(10000):
    res += str(i)

# 快
parts = []
for i in range(10000):
    parts.append(str(i))
res = "".join(parts)
```

## 3.8 Python 3 的 str 就是 Unicode

```python
s = "你好，世界"        # 源文件默认 UTF-8，直接写中文
len(s)                # 5   数的是字符数，不是字节数
s.encode("utf-8")     # b'\xe4\xbd\xa0...'  转 bytes
b.decode("utf-8")     # bytes → str
```

> 有别于 Python 2（那个年代 `str` 是字节串）—— 你现在学的 Python 3 里 `str` = Unicode 字符序列，`bytes` = 字节序列，界限分明。文件 IO 时才会遇到（ch09）。

---

### 小结

| C++ | Python |
|---|---|
| `char` + `std::string` | 只有 `str`（没有 char 类型） |
| `s.length()` | `len(s)` |
| `s[0] = 'A'` 可以 | 不可变，只能重建 |
| `s.substr(2, 3)` | `s[2:5]`（左闭右开） |
| `ostringstream` / `printf` | f-string |
| `std::string::npos` | `find()` 返回 `-1` |

下一章：[ch04 列表与元组](ch04_list_tuple.md)
