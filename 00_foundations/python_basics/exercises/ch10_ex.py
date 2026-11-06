"""
ch10 练习：类与对象
──────────────────────────────────────────────────
重点：self、__init__、魔法方法、property、dataclass、继承
"""

from dataclasses import dataclass, field


# ---------- 1. 基础类：银行账户 ----------
class BankAccount:
    """
    要求：
      - __init__(self, owner, balance=0.0)
      - deposit(amount)：amount > 0 才生效，返回新的余额；否则抛 ValueError
      - withdraw(amount)：余额足够才扣，返回新余额；不足则抛 ValueError("余额不足")
      - __str__：返回 f"<账户 {owner}: {balance:.2f}>"
    属性 balance 用普通实例属性即可。
    """

    # TODO: 实现类
    pass


# ---------- 2. 魔法方法：二维向量 ----------
class Vector:
    """
    实现：
      __init__(x, y)
      __repr__  → "Vector(1, 2)"
      __str__   → "(1, 2)"
      __eq__    → 坐标相等即相等（非 Vector 返回 NotImplemented）
      __add__   → 返回新 Vector
      __sub__   → 返回新 Vector
      __mul__(self, k) → 数乘，返回新 Vector
      __rmul__(self, k) → 支持 2 * v 这种写法
      __abs__   → 返回模长（float）
      __bool__  → 零向量为 False
      __iter__  → 让它可以 x, y = v 拆包
    """

    # TODO: 实现类
    pass


# ---------- 3. property：摄氏度 ----------
class Temperature:
    """
    内部存 _celsius。
      celsius 属性可读可写，写入低于 -273.15 时抛 ValueError
      fahrenheit 只读属性 = c * 9/5 + 32
      kelvin 只读属性 = c + 273.15
    """

    # TODO: 实现类
    pass


# ---------- 4. 继承：图形体系 ----------
class Shape:
    """基类：area() 和 perimeter() 都抛 NotImplementedError"""

    # TODO
    pass


class Rectangle(Shape):
    """__init__(width, height)；实现 area / perimeter / __str__ → "Rectangle(3x4)" """

    # TODO
    pass


class Circle(Shape):
    """__init__(radius)；area = πr²，perimeter = 2πr；__str__ → "Circle(r=2)" """

    # TODO
    pass


def total_area(shapes):
    """多态：接受任意 Shape 列表，返回面积之和"""
    # TODO
    return None


# ---------- 5. dataclass：学生成绩 ----------
@dataclass
class Student:
    """
    字段：name (str), score (int, 默认 0), tags (list[str], 默认空列表，不许共享！)
    方法：
      is_pass() → score >= 60
    要求：能比较相等、能直接用 print 看。
    """

    name: str
    score: int = 0
    tags: list = field(default_factory=list)

    # TODO: 加 is_pass
    pass


# ---------- 6. 栈（用魔法方法实现容器协议） ----------
class Stack:
    """
    push(item) / pop()（空栈抛 IndexError("栈空")） / peek() / is_empty() / __len__ / __bool__
    内部用 list。
    """

    # TODO: 实现类
    pass


# ---------- 7. 计数器（用 __call__） ----------
class Counter:
    """
    c = Counter(); c() → 1; c() → 2
    reset() 归零
    """

    # TODO: 实现类
    pass


# ---------- 8. 词频字典（继承 dict） ----------
class WordBag(dict):
    """
    继承内建 dict：
      add(word, n=1) → 累加计数
      top(n) → 返回频率最高的 n 个 (word, count) 列表
    """

    # TODO: 实现类
    pass


# ---------- 9. __slots__ 内存优化类 ----------
class Point:
    """用 __slots__ 限制只有 x, y 两个属性；实现 __eq__ 和 __repr__"""

    __slots__ = ("x", "y")

    # TODO
    pass


# ---------- 10. 上下文管理器（配合 ch09 的 with） ----------
class Timer:
    """
    with Timer() as t:
        do_something()
    print(t.elapsed)   # 耗时秒数（float）
    实现 __enter__ 返回 self，__exit__ 记录时间。
    """

    # TODO: 实现类
    pass


# ==================== 自测 ====================
if __name__ == "__main__":
    acct = BankAccount("涛", 100)
    assert str(acct) == "<账户 涛: 100.00>"
    acct.deposit(50)
    assert acct.balance == 150.0
    for bad_call in [lambda: acct.deposit(-1), lambda: acct.withdraw(1000)]:
        try:
            bad_call()
            raise AssertionError("应该抛 ValueError")
        except ValueError:
            pass
    assert acct.withdraw(50) == 100.0

    v1, v2 = Vector(1, 2), Vector(3, 4)
    assert repr(v1) == "Vector(1, 2)"
    assert str(v1) == "(1, 2)"
    assert v1 + v2 == Vector(4, 6)
    assert v2 - v1 == Vector(2, 2)
    assert v1 * 3 == Vector(3, 6)
    assert 3 * v1 == Vector(3, 6)
    assert abs(Vector(3, 4)) == 5.0
    assert bool(Vector(0, 0)) is False
    assert bool(Vector(0, 1)) is True
    x, y = v1
    assert (x, y) == (1, 2)
    assert v1 != "不是向量"

    t = Temperature(100)
    assert abs(t.fahrenheit - 212.0) < 1e-9
    assert abs(t.kelvin - 373.15) < 1e-9
    t.celsius = 0
    assert t.fahrenheit == 32.0
    try:
        t.celsius = -300
        raise AssertionError("应该抛 ValueError")
    except ValueError:
        pass

    shapes = [Rectangle(3, 4), Circle(1)]
    assert Rectangle(3, 4).area() == 12
    assert Rectangle(3, 4).perimeter() == 14
    assert str(Rectangle(3, 4)) == "Rectangle(3x4)"
    assert str(Circle(2)) == "Circle(r=2)"
    import math
    assert abs(Circle(1).area() - math.pi) < 1e-9
    assert abs(Circle(1).perimeter() - 2 * math.pi) < 1e-9
    assert abs(total_area(shapes) - (12 + math.pi)) < 1e-9

    s1, s2 = Student("涛", 95), Student("涛", 95)
    assert s1 == s2, "dataclass 应自动生成 __eq__"
    assert "95" in str(s1), "dataclass 应自动生成 __repr__"
    assert s1.is_pass() is True
    assert Student("李").is_pass() is False
    assert Student("a").tags is not Student("b").tags, "tags 不能共享同一个列表！"

    st = Stack()
    assert len(st) == 0 and not st
    st.push(1)
    st.push(2)
    assert len(st) == 2 and bool(st)
    assert st.pop() == 2 and st.peek() == 1
    try:
        Stack().pop()
        raise AssertionError("应该抛 IndexError")
    except IndexError:
        pass

    cnt = Counter()
    assert cnt() == 1 and cnt() == 2
    cnt.reset()
    assert cnt() == 1

    bag = WordBag()
    bag.add("a")
    bag.add("a")
    bag.add("b")
    assert bag["a"] == 2
    assert bag.top(1) == [("a", 2)]

    p1, p2 = Point(1, 2), Point(1, 2)
    assert p1 == p2
    assert repr(p1) == "Point(1, 2)"
    try:
        p1.z = 3
        raise AssertionError("__slots__ 应该禁止新增属性")
    except AttributeError:
        pass

    with Timer() as timer:
        _ = sum(range(100000))
    assert isinstance(timer.elapsed, float) and timer.elapsed >= 0

    print("ch10 全部通过 ✓")


# region 参考答案
"""
class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款必须为正")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"<账户 {self.owner}: {self.balance:.2f}>"

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        return bool(self.x or self.y)

    def __iter__(self):
        return iter((self.x, self.y))

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius          # 会走 setter 校验

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self):
        return self._celsius + 273.15

class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def __str__(self):
        return f"Circle(r={self.radius})"

def total_area(shapes):
    return sum(s.area() for s in shapes)

@dataclass
class Student:
    name: str
    score: int = 0
    tags: list = field(default_factory=list)

    def is_pass(self) -> bool:
        return self.score >= 60

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("栈空")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("栈空")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return bool(self._items)

class Counter:
    def __init__(self):
        self._n = 0

    def __call__(self):
        self._n += 1
        return self._n

    def reset(self):
        self._n = 0

class WordBag(dict):
    def add(self, word, n=1):
        self[word] = self.get(word, 0) + n

    def top(self, n):
        return sorted(self.items(), key=lambda kv: kv[1], reverse=True)[:n]

class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Timer:
    def __enter__(self):
        import time
        self._start = time.perf_counter()
        self.elapsed = 0.0
        return self

    def __exit__(self, exc_type, exc, tb):
        import time
        self.elapsed = time.perf_counter() - self._start
        return False
"""
# endregion
