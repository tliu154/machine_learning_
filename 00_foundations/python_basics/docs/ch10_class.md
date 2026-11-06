---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch10 类与对象

Python 的 OOP 和 C++ 差别很大：**没有 public/private 强制、没有头文件分离、支持多继承、还有一堆魔法方法**。

## 10.1 最简类

```cpp
// C++
class Student {
public:
    std::string name;
    int score;
    Student(std::string n, int s) : name(n), score(s) {}
    void print() { std::cout << name << " " << score; }
};
```

```python
class Student:
    def __init__(self, name, score):    # 构造函数
        self.name = name                # self 就是 this，不过是显式第一个参数
        self.score = score

    def print_info(self):               # 成员函数的第一个参数必须是 self
        print(f"{self.name}: {self.score}")

s = Student("涛", 95)        # 不需要 new！
s.print_info()
```

要点：

- `__init__` 是构造函数（`__init__` 不是 `__construct__`）
- **`self` 必须手写**，调用时不用传（解释器自动传）
- 创建对象不用 `new`，直接 `类名()`。Python 没有 `delete`
- 没有声明 {} 包裹的成员列表，属性在 `__init__` 里赋值就有了

```python
s.age = 19          # 可以随时给对象加新属性！C++ 想都不敢想
del s.age
```

> 这种动态加属性的能力很灵活，但也很危险（拼错名字就悄悄创建了一个新属性）。
> 想限制住就用 `__slots__`，见 §10.7。

## 10.2 类属性 vs 实例属性

```python
class Dog:
    species = "Canis lupus"       # 类属性：所有实例共享（类似 C++ static 成员）
    count = 0

    def __init__(self, name):
        self.name = name          # 实例属性：每个对象一份
        Dog.count += 1            # 访问类属性要带类名

a = Dog("小黑"); b = Dog("小白")
print(a.species, b.species)       # 共享同一个
print(Dog.count)                  # 2

# ⚠️ 陷阱
a.species = "Cat"                 # 这不是改类属性！是给 a 创建了一个同名实例属性
Dog.species                       # 还是 "Canis lupus"
```

## 10.3 访问控制：靠约定

Python **没有** `public:` / `private:` 关键字。

```python
class BankAccount:
    def __init__(self):
        self._balance = 0           # 单下划线：约定"内部用，别外部访问"（不强制）
        self.__password = "123456"  # 双下划线：名称改写，外部难以直接访问

    def deposit(self, n):
        self._balance += n

    def get_balance(self):
        return self._balance

acc = BankAccount()
acc._balance            # 能访问（只是告诉你不该访问）
acc.__password          # AttributeError
acc._BankAccount__password      # 还是能访问（名称改写成了 _类名__属性）
```

> Python 的哲学："我们都成年人了"。真要限制用 `@property`（§10.5）。

PyCharm 里输入时不提示 `_xxx`，算是软性约束。

## 10.4 魔法方法（Dunder Methods）

Python 用双下划线方法重载运算符，对应 C++ 的 `operator+` 等。

```cpp
// C++
std::ostream& operator<<(std::ostream& os, const Vec2& v);
bool operator==(const Vec2& a, const Vec2& b);
```

```python
class Vec2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):                  # str() / print() 时调用 → 给用户看的
        return f"Vec2({self.x}, {self.y})"

    def __repr__(self):                 # repr() / 控制台回显 → 给开发者看的，应该尽量能 eval
        return f"Vec2({self.x!r}, {self.y!r})"

    def __eq__(self, other):            # ==
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):            # <  （有了它就能直接 sorted()）
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

    def __add__(self, other):           # +
        return Vec2(self.x + other.x, self.y + other.y)

    def __neg__(self):                  # 一元 -
        return Vec2(-self.x, -self.y)

    def __len__(self):                  # len(obj)
        return 2

    def __getitem__(self, i):           # obj[i]  → 有了就能下标访问、能切片、能迭代
        return (self.x, self.y)[i]

    def __contains__(self, v):          # v in obj
        return v in (self.x, self.y)

    def __hash__(self):                 # 定义 __eq__ 后还想放进 set/dict 就得定义这个
        return hash((self.x, self.y))

    def __bool__(self):                 # bool(obj)
        return self.x != 0 or self.y != 0

    def __call__(self):                 # obj()  让对象可以像函数一样被调用
        return self.x + self.y

v = Vec2(3, 4)
print(v)            # Vec2(3, 4)
len(v)              # 2
v[0]                # 3
```

常用表：

| 方法 | 触发 |
|---|---|
| `__init__` | 构造 |
| `__str__` / `__repr__` | `print()` / 交互式回显 |
| `__eq__` `__lt__` `__le__` `__gt__` `__ge__` `__ne__` | 比较运算符 |
| `__add__` `__sub__` `__mul__` `__truediv__` `__floordiv__` `__mod__` `__pow__` | `- * / // % **` |
| `__iadd__` 等 | `+=` 等复合赋值 |
| `__len__` `__getitem__` `__setitem__` `__iter__` `__contains__` | 容器协议 |
| `__hash__` | `hash()`，进 set/dict |
| `__enter__` `__exit__` | `with`（ch09） |
| `__call__` | `obj()` |

> `functools.total_ordering` 装饰器可以让你只写 `__eq__` 和 `__lt__` 就自动补齐其它比较方法。

## 10.5 @property：伪装成属性的方法

```cpp
// C++ 需要 getBalance() / setBalance() 这样的方法
```

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):                  # 读：像属性一样访问 temp.celsius
        return self._celsius

    @celsius.setter
    def celsius(self, value):           # 写：temp.celsius = 100
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):               # 只读计算属性，不用括号
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.celsius)        # 25       ← 调用的是方法，但语法像属性
t.celsius = 30          # 走 setter，带校验
print(t.fahrenheit)     # 86.0
# t.fahrenheit = 100    # ✗ AttributeError，没有 setter 就是只读
```

好处：一开始用普通属性，以后想加校验逻辑，改成 `@property` 时**外部调用代码不用动**。

## 10.6 继承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("子类必须实现")     # 相当于 C++ 纯虚函数

class Dog(Animal):                      # 括号里写父类
    def speak(self):
        return f"{self.name}: 汪汪"

class Cat(Animal):
    def speak(self):
        return f"{self.name}: 喵喵"

# 用继承 + super
class Puppy(Dog):
    def __init__(self, name, months):
        super().__init__(name)          # 调父类 __init__（必须显式调用！）
        self.months = months
```

要点：

- 单继承或多继承都支持：`class C(A, B)`
- **没有虚函数/纯虚函数关键字**，所有方法天然是"虚"的（动态绑定）
- `super().__init__()` **必须自己调用**，不像 C++ 自动调基类构造
- Python 没有重载（同名多签名），后定义的同名方法覆盖前面的

```python
isinstance(dog, Animal)     # True   类似 C++ 的 dynamic_cast 检查
issubclass(Dog, Animal)     # True
type(dog) is Dog            # 精确类型判断（不考虑继承）
```

### MRO（多继承的方法查找顺序）

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...

D.__mro__       # 打印查找顺序：D → B → C → A → object
```

## 10.7 __slots__：省内存 + 禁止乱加属性

```python
class Point:
    __slots__ = ("x", "y")          # 只允许这两个属性

    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
p.z = 3         # AttributeError
```

每个实例不再有 `__dict__`，对象数量多时能省可观内存（几十万个对象时有意义）。日常小项目用不上。

## 10.8 dataclass：数据类的救星（Python 3.7+）

写纯数据类时不用手搓 `__init__`/`__repr__`/`__eq__`：

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    score: int = 0
    tags: list[str] = field(default_factory=list)   # 可变默认值必须用 factory！

    def is_pass(self) -> bool:
        return self.score >= 60

s = Student("涛", 95)
print(s)                # Student(name='涛', score=95, tags=[])  自动生成 __repr__
Student("a", 60) == Student("a", 60)    # True   自动生成 __eq__

@dataclass(frozen=True)     # 不可变，可哈希 → 能进 set/dict
class Config:
    host: str
    port: int = 8080

@dataclass(order=True)      # 自动生成比较方法，可直接 sorted()
class Task:
    priority: int
    name: str = field(compare=False)    # name 不参与比较
```

> 对应 C++ 里一堆样板 getter/setter/构造函数。写 DTO、配置项时用它，能省一大堆行。

---

### 小结

| C++ | Python |
|---|---|
| `public:` / `private:` | 靠约定（单/双下划线），无强制 |
| `this->x` | `self.x`，且必须写在参数列表里 |
| `new Student()` | `Student()`，无 new / delete |
| `operator<<` `operator==` | `__str__` `__eq__` 等魔法方法 |
| 构造函数初始化列表 | 在 `__init__` 里赋值 |
| 自动调基类构造 | 必须手写 `super().__init__()` |
| 虚函数 / 纯虚函数 | 天然都是虚的；`raise NotImplementedError` |
| 一堆 getter/setter 样板 | `@dataclass` 一行搞定 |

下一章：[ch11 模块、包与虚拟环境](ch11_module_package.md)
