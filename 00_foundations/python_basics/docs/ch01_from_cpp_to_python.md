---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch01 从 C++ 到 Python：世界观

## 1.1 第一个程序

```cpp
// C++
#include <iostream>
int main() {
    std::cout << "Hello" << std::endl;
    return 0;
}
```

```python
# Python
print("Hello")
```

没了。没有 `main`，没有头文件，没有分号，没有大括号。

> 一个 `.py` 文件就是从第一行执行到最后一行。不用 `main()`。

## 1.2 缩进 = 语法

Python 用**缩进**表示代码块，代替 `{}`。约定 4 个空格（PyCharm 里 Tab 会自动转 4 空格）。

```python
x = 10
if x > 5:          # 冒号 : 表示"下面是一块代码"
    print("大")
    print("这一行还在 if 里面")
print("这一行已经在 if 外面了")
```

C++ 党最容易犯的错：

| 错误 | 后果 |
|---|---|
| 忘记冒号 `:` | SyntaxError |
| 混用空格和 Tab | TabError（PyCharm 一般自动避免） |
| 缩进层级写错 | 逻辑错误，**编译器不会报错**，静默跑错 |

**没有 `switch`、没有 `do...while`、没有 `++`/`--`**。写 `i++` 会 SyntaxError，要写 `i += 1`。

## 1.3 注释与打印

```python
# 单行注释
# Python 没有 /* 多行注释 */，多行注释用三个引号的字符串：
"""
这三行其实是字符串字面量，
放在这里不会被解释器执行，充当多行注释。
放在函数第一行它就是 docstring（见 ch07）。
"""

print("a", "b", 123)        # 逗号分隔 → 自动空格连起来：a b 123
print("a", end="")          # end 控制结尾，默认 "\n"
print(f"x={x}")             # f-string，ch03 讲
```

## 1.4 变量是"便利贴"，不是"盒子"

这是**最重要的一节**。

C++ 里：`int a = 5;` → 内存中有一个 int 大小的盒子，名叫 a，里面放着 5。
Python 里：`a = 5` → **先在内存某处创建一个 int 对象 5，然后把便利贴 `a` 贴上去**。

```python
a = 5
b = a        # 不是拷贝值！是把 b 这张便利贴也贴到同一个 5 上
a = a + 1    # 不是"修改盒子里的值"，而是新建一个对象 6，把便利贴 a 撕下来贴到 6 上
print(a, b)  # 6 5
```

等价于 C++ 的：

```cpp
int value = 5;
int& a = value;   // b = a 之后 b 也是 value 的引用
a = a + 1;        // 这里 C++ 会真的改 value
                  // 而 Python 不会改，它另建一个 6
```

**推论**：Python 里"赋值"永远是贴标签，永不拷贝数据。

```python
lst = [1, 2, 3]
lst2 = lst          # 两个名字指向同一个列表对象！
lst2.append(4)
print(lst)          # [1, 2, 3, 4]  ← lst 也被改了！
```

C++ 党第一次看到这个会懵。**这是 C++ 里 `std::vector<int>& lst2 = lst;` 的效果**。想要真正的拷贝：

```python
lst2 = lst.copy()      # 或者 list(lst) 或者 lst[:]（切片产生新对象）
```

## 1.5 动态类型

```cpp
int x = 5;
// x = "hello";      // C++ 编译错误
```

```python
x = 5
print(type(x))      # <class 'int'>
x = "hello"
print(type(x))      # <class 'str'>   ← 合法！x 此刻撕下来贴到字符串上了
```

- 类型属于**对象**，不属于变量
- 不用声明类型，也不能声明类型（能写"类型提示"，见 ch07，但解释器不强制）
- 代价：拼写错误要等到运行那一刻才炸

### `is` vs `==`

```python
a == b    # 值相等（对应 C++ 的 == 或 strcmp，具体看类型有没有 __eq__）
a is b    # 是不是同一个对象（对应 C++ 里比较地址！）
```

```python
x = [1,2]; y = [1,2]
print(x == y)   # True  值一样
print(x is y)   # False 两个不同的对象

a = None
if a is None:   # 判断 None 必须用 is，社区惯例
    ...
```

> **只在判断 `None` 时用 `is`**。判断数字/字符串相等一律用 `==`。
> `is` 对小整数（-5~256）和短字符串会返回 True，那是 CPython 的缓存优化，别依赖它。

## 1.6 变量名

- 字母/下划线开头，可含数字，区分大小写
- **社区惯例**（不像 C++ 有各种流派，Python 基本统一）：
  - `snake_case` 用于变量和函数：`student_count`
  - `UPPER_CASE` 用于常量：`MAX_SIZE`
  - `PascalCase` 用于类：`StudentRecord`
  - `_name` 单下划线开头 = "内部用的，别外部访问"（约定，不强制）
- Python 没有 `const`，常量靠自觉 + 大写命名

## 1.7 输入

```python
name = input("请输入名字: ")   # input 永远返回 str！
age = int(input("年龄: "))     # 要数字必须显式转换
```

对比 `cin >> n` 会自动转类型 —— Python 不会。`input` 得到的**永远是字符串**。

```python
# 一行读多个整数
a, b = map(int, input().split())    # 输入 "3 5" → a=3, b=5
```

## 1.8 删除名字 / 垃圾回收

```python
x = 5
del x        # 撕掉便利贴，不是释放对象
             # 当对象身上一张便利贴都没有，解释器自动回收（引用计数 + GC）
```

对比 C++ 的手动 `delete` / RAII：Python 里你几乎不用管内存。

## 1.9 REPL 与 PyCharm 技巧

- PyCharm 底部 **Python Console** = 交互式解释器，可以随手验证语法（输入一行执行一行）
- 选中代码 → **Alt+Shift+E** 在 console 里执行选中的片段
- **Ctrl+/** 注释/取消注释选中行
- **Ctrl+Alt+L** 格式化代码
- `# TODO` 标记会在 PyCharm 的 TODO 工具窗里列出来

---

### 小结

| C++ | Python |
|---|---|
| `{}` 界定代码块 | 缩进界定，块开头加 `:` |
| 静态类型，变量有类型 | 动态类型，值有类型，变量是标签 |
| 赋值 = 拷贝值 | 赋值 = 绑定引用 |
| `int x;` 声明后使用 | 不用声明，赋值即诞生 |
| 手动 `new/delete` | 自动垃圾回收 |
| `NULL` / `nullptr` | `None` |
| `i++` | `i += 1` |

下一章：[ch02 数字与运算](ch02_numbers.md)
