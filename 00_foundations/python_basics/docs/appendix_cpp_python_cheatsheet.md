---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# 附录：C++ ↔ Python 速查表

忘语法时翻这里。

## 语法骨架

| 操作 | C++ | Python |
|---|---|---|
| Hello World | `cout << "hi";` | `print("hi")` |
| 代码块 | `{ }` | 缩进 + `:` |
| 单行注释 | `//` | `#` |
| 多行注释 | `/* */` | 三引号字符串 |
| 逻辑运算 | `&&` `\|\|` `!` | `and` `or` `not` |
| 三元 | `c ? a : b` | `a if c else b` |
| 自增 | `i++` | `i += 1`（没有 `++`） |
| 交换 | `swap(a,b)` | `a, b = b, a` |
| 幂 | `pow(a,b)` | `a ** b` |
| 交换值时临时变量 | 需要 | 不需要 |
| 主函数 | `int main()` | `if __name__ == "__main__":` |

## 类型

| C++ | Python | 备注 |
|---|---|---|
| `int` | `int` | Python 无限精度 |
| `double/float` | `float` | 都是双精度 |
| `bool` | `bool` | `True`/`False`，是 int 子类 |
| `char` | 无 | `'a'` 就是长度为 1 的 str |
| `std::string` | `str` | 不可变 |
| `std::vector<T>` | `list` | 可放异构元素 |
| `std::array<T,N>` | `tuple` | 不可变 |
| `std::pair` | `tuple` | 可拆包 |
| `std::map` | `dict`（有序） | 字面量 `{}` |
| `std::unordered_map` | `dict` | — |
| `std::set` | `set` | 空集是 `set()` 不是 `{}` |
| `std::queue` | `collections.deque` | 别用 `list.pop(0)` |
| `std::optional<T>` | `T \| None` | — |
| `nullptr` / `NULL` | `None` | 判断用 `is` |

## 容器操作

| 操作 | C++ | Python |
|---|---|---|
| 长度 | `v.size()` `s.length()` | `len(x)` |
| 追加 | `v.push_back(x)` | `v.append(x)` |
| 插入 | `v.insert(it, x)` | `v.insert(i, x)` |
| 尾删 | `v.pop_back()` | `v.pop()` |
| 查找元素 | `std::find` | `x in container` |
| 排序 | `sort(begin,end)` | `v.sort()` / `sorted(v)` |
| 带 key 排序 | 写 lambda 比较器 | `sorted(v, key=lambda x: ...)` |
| 反转 | `reverse(begin,end)` | `v.reverse()` / `v[::-1]` |
| 切片 | 手动 | `v[1:4]` `v[::-1]` `v[::2]` |
| 求和 | `accumulate` | `sum(v)` |
| 最值 | `min_element` | `min(v)` `max(v)` |
| 任意/全部 | — | `any(...)` `all(...)` |
| 去重 | `sort + unique` | `list(set(v))` 或 `dict.fromkeys(v)` |
| 拷贝 | 拷贝构造（深） | `=` 引用 / `copy()` 浅 / `deepcopy()` 深 |

## 字符串

| 操作 | C++ | Python |
|---|---|---|
| 拼接 | `s1 + s2` | `s1 + s2` 或 f-string |
| 子串 | `s.substr(2, 3)` | `s[2:5]`（左闭右开） |
| 查找 | `s.find(x)` → npos | `s.find(x)` → -1 |
| 包含 | `s.find(x) != npos` | `x in s` |
| 替换 | 手写循环 | `s.replace(a, b)` |
| 拆分 | `stringstream` | `s.split(",")` |
| 拼接列表 | — | `",".join(list)` |
| 去空白 | 手写 | `s.strip()` |
| 大小写 | `tolower` 循环 | `s.lower()` / `s.upper()` |
| 格式化 | `printf` / `stringstream` | f-string `f"{x:.2f}"` |
| 逐字符 | `for(char c : s)` | `for c in s` |

## 控制流

| 操作 | C++ | Python |
|---|---|---|
| 条件 | `if () {} else if {}` | `if:` `elif:` `else:` |
| 计数循环 | `for(int i=0;i<n;i++)` | `for i in range(n)` |
| 范围循环 | `for(auto& x : v)` | `for x in v` |
| 带下标 | 手维护 i | `for i, x in enumerate(v)` |
| 并行双序列 | — | `for a, b in zip(xs, ys)` |
| while | `while(){}` | `while:` |
| do-while | `do{}while()` | `while True:` + `break` |
| switch | `switch/case` | `match/case`（3.10+） |
| 空语句 | `;` 或 `{}` | `pass` |
| break 后的 else | 无 | `for...else`（no-break 时执行） |

## 函数

| 操作     | C++                       | Python                   |
| ------ | ------------------------- | ------------------------ |
| 定义     | `int f(int a)`            | `def f(a):`              |
| 返回多值   | `pair` / `tuple` / struct | `return a, b`（自动元组）      |
| 默认值    | `int f(int a=1)`          | `def f(a=1):` ⚠️ 别用可变默认值 |
| 可变参数   | 模板包                       | `*args` / `**kwargs`     |
| 引用传参   | `void f(int& x)`          | 默认行为（但重新绑定无效）            |
| 值传参    | `void f(int x)`           | 对可变对象要显式 copy            |
| lambda | `[](int x){...}`          | `lambda x: ...` 只能单行     |
| 重载     | 支持                        | ❌ 不支持，同名的后者覆盖前者          |

## 类

| 操作 | C++ | Python |
|---|---|---|
| 定义 | `class A { public: ... };` | `class A:` |
| 构造 | `A(int x): x(x) {}` | `def __init__(self, x): self.x = x` |
| this | `this->x` | `self.x`（显式参数） |
| 实例化 | `A a(1);` 或 `new A(1)` | `a = A(1)`（无 new） |
| 析构 | `~A()` | `__del__`（几乎不用） |
| 访问控制 | `public/private/protected` | 约定 `_x` / `__x` |
| 静态成员 | `static` | 类属性（类体内赋值） |
| 继承 | `class B : public A` | `class B(A)` |
| 调父类 | `A::method()` | `super().method()` |
| 虚/纯虚 | `virtual` `= 0` | 天然全虚；`raise NotImplementedError` |
| 运算符重载 | `operator+` | `__add__` |
| 输出 | `operator<<` | `__str__` / `__repr__` |
| const 方法 | `void f() const` | 无对应（靠约定） |
| 数据类 | 手写一堆样板 | `@dataclass` |

## 异常与资源

| 操作 | C++ | Python |
|---|---|---|
| 抛异常 | `throw runtime_error(x)` | `raise ValueError(x)` |
| 捕获 | `catch(const E& e)` | `except E as e:` |
| 兜底 | `catch(...)` | `except Exception:`（别用裸 except） |
| 清理 | RAII 析构 | `with` 语句 |
| 重抛 | `throw;` | `raise` |
| 打开文件 | `ifstream f(path)` | `with open(path, encoding="utf-8") as f` |
| 路径 | `std::filesystem::path` | `pathlib.Path` |

## 组织与工程

| 操作 | C++ | Python |
|---|---|---|
| 引入 | `#include <x>` | `import x` |
| 命名空间 | `namespace n {}` | 模块天然就是命名空间 |
| 编译 | g++ / MSBuild + CMake | 无需编译，直接 `python x.py` |
| 包管理 | vcpkg / conan / 手动 | `pip` |
| 依赖清单 | CMakeLists | `requirements.txt` |
| 环境隔离 | Docker / 系统环境 | `venv` |
| 单元测试 | Google Test / Catch2 | `pytest` / `unittest` |
| 风格规范 | 各家各异 | **PEP 8**（几乎全社区统一） |

## 递归

| 操作 | C++ | Python |
|---|---|---|
| 递归太深 | 栈溢出崩溃（段错误） | 抛 `RecursionError`（可捕获） |
| 默认深度 | 取决于栈大小 | 1000（`sys.getrecursionlimit()`） |
| 尾递归优化 | `-O2` 会做 | **永不做**，别写尾递归求性能 |
| 记忆化 | 手写 `unordered_map` memo | `@functools.lru_cache` |
| 遍历目录树 | `recursive_directory_iterator` | `Path.rglob()` 或 `yield from` 递归 |

## 最容易踩的 9 个坑（复习清单）

1. `b = a` 对 list/dict 是**引用**，改一个另一个跟着变 → 用 `.copy()` / `deepcopy()`
2. 默认参数别用 `[]` 或 `{}` → 用 `None` 然后在函数里创建
3. `/` 永远返回 float，`7/2 == 3.5`；整除是 `//`
4. `input()` 返回的永远是 str，要数字得 `int()`
5. 没有 `++`/`--`，没有 `switch`，没有 `do-while`
6. 循环里读写中文文件要写 `encoding="utf-8"`
7. `is` 只用来判断 `None`；相等用 `==`
8. 函数里给外部变量赋值要 `global` / `nonlocal`
9. 递归超过 1000 层会 `RecursionError`，且 Python 不做尾递归优化

---

> 记不住没关系，用到再回来翻。**真正学会是写出东西来的那一刻**，不是读完教程的时候。
