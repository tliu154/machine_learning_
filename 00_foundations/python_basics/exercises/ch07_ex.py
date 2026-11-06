"""
ch07 练习：函数
──────────────────────────────────────────────────
重点：可变默认参数陷阱、*args/**kwargs、参数传递语义
"""


# ---------- 1. ⚠️ 正确的累加器（避开可变默认参数陷阱） ----------
def append_to(value, target=None):
    """
    把 value 追加到 target 并返回。
    target 为 None 时新建一个列表。
    要求：连续多次不传 target 调用，结果互不影响！
    """
    # TODO
    return None


# ---------- 2. 灵活的求和 ----------
def flexible_sum(*args, start=0):
    """任意个数字求和，还能加起始值。用 *args"""
    # TODO
    return None


# ---------- 3. 构建查询串 ----------
def build_query(base, **params):
    """
    build_query("/search", q="python", page=2)
    → "/search?q=python&page=2"
    没有参数时返回 base 原样。
    """
    # TODO
    return None


# ---------- 4. 参数传递语义测验 ----------
def mutate_test(n, lst, s):
    """
    在函数内部：
      n = n * 2
      lst.append(n)
      s = s.upper()
    然后返回这三个值组成的元组 (n, lst, s)
    做完这题请解释：调用后外层的那个 int 和那个 str 变了吗？为什么？
    """
    # TODO
    return None


# ---------- 5. 计算统计量 ----------
def stats(nums):
    """
    返回 dict: {"count": n, "sum": , "avg": , "min": , "max": }
    avg 保留 2 位小数。空列表时 avg/min/max 为 None。
    """
    # TODO
    return None


# ---------- 6. 装饰器做不到就手写：计时包装 ----------
def repeat(times):
    """
    返回一个装饰器：让被装饰的函数执行 times 次，返回最后一次的结果。
    @repeat(3)
    def f(): ...
    """
    # TODO: 实现一个带参数的装饰器
    def decorator(func):
        # TODO
        return None
    return decorator


# ---------- 7. lambda 排序 ----------
def sort_words_by_vowel_count(words):
    """
    按元音（aeiou，不区分大小写）个数升序排序；
    元音数相同则按字母序升序。返回新列表。
    """
    # TODO
    return None


# ---------- 8. 缓存装饰器（用 functools.lru_cache） ----------
def fib(n):
    """
    返回第 n 项斐波那契数（fib(0)=0, fib(1)=1）
    用 @functools.lru_cache 装饰，否则 fib(35) 会很慢
    """
    # TODO: 递归 + 缓存
    return None


# ---------- 9. 闭包：累加计数器 ----------
def make_counter(start=0):
    """
    返回一个函数，每次调用返回自增后的计数。
    c = make_counter(10); c() → 11; c() → 12
    需要用 nonlocal
    """
    # TODO
    return None


# ---------- 10. 类型注解练习 ----------
def normalize(values: list[float]) -> list[float]:
    """把列表线性缩放到 [0, 1] 区间。全相等时返回全 0 列表"""
    # TODO: 给的类型注解写好了，把实现补上
    return None


# ---------- 11. 高阶函数：apply_to_all ----------
def apply_to_all(func, items):
    """对 items 里每个元素调用 func，返回结果列表。不许用 map（就用一次循环或推导式）"""
    # TODO
    return None


# ---------- 12. 参数校验 ----------
def divide(a, b):
    """
    b 为 0 时抛 ZeroDivisionError("除数不能为零")
    非数字类型时抛 TypeError("参数必须是数字")
    正常返回 a / b
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    assert append_to(1) == [1]
    assert append_to(2) == [2], "⚠️ 这就是可变默认参数的坑！"
    lst = []
    append_to(1, lst)
    append_to(2, lst)
    assert lst == [1, 2]

    assert flexible_sum(1, 2, 3) == 6
    assert flexible_sum(1, start=10) == 11
    assert flexible_sum() == 0

    assert build_query("/search", q="python", page=2) == "/search?q=python&page=2"
    assert build_query("/") == "/"

    assert mutate_test(5, [1], "ab") == (10, [1, 10], "AB")

    s = stats([1, 2, 3, 4])
    assert s == {"count": 4, "sum": 10, "avg": 2.5, "min": 1, "max": 4}
    assert stats([])["avg"] is None

    @repeat(3)
    def add_one():
        add_one.calls = getattr(add_one, "calls", 0) + 1
        return add_one.calls
    assert add_one() == 3

    assert sort_words_by_vowel_count(["rhythm", "apple", "bee", "cat"]) == [
        "rhythm", "cat", "apple", "bee"
    ]

    assert fib(10) == 55
    assert fib(35) == 9227465

    c = make_counter(10)
    assert c() == 11 and c() == 12 and c() == 13
    c2 = make_counter()
    assert c2() == 1

    assert normalize([1, 2, 3]) == [0.0, 0.5, 1.0]
    assert normalize([5, 5, 5]) == [0.0, 0.0, 0.0]

    assert apply_to_all(str, [1, 2]) == ["1", "2"]
    assert apply_to_all(lambda x: x * 2, [1, 2, 3]) == [2, 4, 6]

    assert divide(6, 3) == 2.0
    try:
        divide(1, 0)
        assert False, "应该抛异常"
    except ZeroDivisionError as e:
        assert str(e) == "除数不能为零"
    try:
        divide(1, "a")
        assert False, "应该抛异常"
    except TypeError:
        pass

    print("ch07 全部通过 ✓")


# region 参考答案
"""
def append_to(value, target=None):
    if target is None:
        target = []
    target.append(value)
    return target

def flexible_sum(*args, start=0):
    return start + sum(args)

def build_query(base, **params):
    if not params:
        return base
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{qs}"

def mutate_test(n, lst, s):
    n = n * 2
    lst.append(n)
    s = s.upper()
    return (n, lst, s)
    # 外层的 int 和 str 都没变：它们不可变，"修改"只是把局部便利贴撕到新对象上。
    # list 变了：append 是原地修改同一个对象。

def stats(nums):
    if not nums:
        return {"count": 0, "sum": 0, "avg": None, "min": None, "max": None}
    return {
        "count": len(nums),
        "sum": sum(nums),
        "avg": round(sum(nums) / len(nums), 2),
        "min": min(nums),
        "max": max(nums),
    }

def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def sort_words_by_vowel_count(words):
    def vowels(w):
        return sum(1 for ch in w.lower() if ch in "aeiou")
    return sorted(words, key=lambda w: (vowels(w), w))

from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def make_counter(start=0):
    count = start
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

def normalize(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0] * len(values)
    return [(v - lo) / (hi - lo) for v in values]

def apply_to_all(func, items):
    return [func(item) for item in items]

def divide(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("参数必须是数字")
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b
"""
# endregion
