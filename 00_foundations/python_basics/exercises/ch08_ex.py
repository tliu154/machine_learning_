"""
ch08 练习：迭代器与生成器
──────────────────────────────────────────────────
重点：yield 的暂停恢复机制、惰性求值、itertools
"""

from itertools import islice, accumulate, chain, combinations, count


# ---------- 1. 手动实现 range ----------
def my_range(start, stop=None, step=1):
    """
    生成器版本的 range：
    my_range(3) → 0,1,2
    my_range(1, 5) → 1,2,3,4
    my_range(0, 10, 3) → 0,3,6,9
    用 yield，不许用 range()
    """
    # TODO
    return None


# ---------- 2. 无限偶数序列 ----------
def evens():
    """无限生成 0, 2, 4, 6, ...  用 while True + yield"""
    # TODO
    return None


# ---------- 3. 批量读取聊天记录 ----------
def take_from_source(source_iter, n):
    """
    从任意迭代器取前 n 个元素返回成列表，不足则返回全部。
    不许用 for 循环逐步 append —— 直接用 islice
    """
    # TODO
    return None


# ---------- 4. 分批 ----------
def batches(items, size):
    """
    生成器：把 items 切成若干长度为 size 的列表。
    list(batches([1,2,3,4,5], 2)) → [[1,2],[3,4],[5]]
    """
    # TODO
    return None


# ---------- 5. 惰性求和 ----------
def first_n_squares_sum(n):
    """
    前 n 个平方数的和，但【不能】先建列表。
    提示：生成器表达式直接喂给 sum
    """
    # TODO
    return None


# ---------- 6. 素数生成器 ----------
def primes():
    """无限[]生成素数序列：2,3,5,7,11,... 用试除法 + yield"""
    # TODO
    return None


# ---------- 7. 滑动窗口 ----------
def sliding_window(items, size):
    """
    生成器：产出相邻的长度为 size 的窗口（tuple）
    list(sliding_window([1,2,3,4], 2)) → [(1,2),(2,3),(3,4)]
    """
    # TODO
    return None


# ---------- 8. 链式处理 pipeline ----------
def pipeline(nums):
    """
    对 nums 做三步处理并返回生成器：
      过滤出偶数 → 平方 → 只保留小于 100 的
    用 yield from 或者生成器表达式串联
    """
    # TODO
    return None


# ---------- 9. 文件行数统计（用生成器，不占内存） ----------
def count_lines(lines):
    """
    lines 是行组成的迭代器（比如打开的文件对象）
    返回非空行的数量（strip 后长度 > 0）
    """
    # TODO
    return None


# ---------- 10. itertools 实战 ----------
def prefix_sums(nums):
    """返回前缀和列表，用 accumulate：[1,2,3] → [1,3,6]"""
    # TODO
    return None


def all_pairs(items):
    """返回所有两两组合的列表，用 combinations：[1,2,3] → [(1,2),(1,3),(2,3)]"""
    # TODO
    return None


def flatten_all(nested_lists):
    """[[1,2],[3],[4,5]] → [1,2,3,4,5]，用 chain"""
    # TODO
    return None


# ---------- 11. 记忆 Moment：生成器是一次性的 ----------
def demonstrate_exhaustion():
    """
    返回一个字典展示这个行为：
    gen = (x for x in range(3))
    第一次 list(gen) → [0,1,2]
    第二次 list(gen) → []
    返回 {"first": ..., "second": ...}
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    assert list(my_range(3)) == [0, 1, 2]
    assert list(my_range(1, 5)) == [1, 2, 3, 4]
    assert list(my_range(0, 10, 3)) == [0, 3, 6, 9]
    assert list(my_range(5, 0, -1)) == [5, 4, 3, 2, 1]

    assert list(islice(evens(), 5)) == [0, 2, 4, 6, 8]

    assert take_from_source(iter(range(10)), 3) == [0, 1, 2]
    assert take_from_source(iter([1, 2]), 5) == [1, 2]

    assert list(batches([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(batches([], 3)) == []

    assert first_n_squares_sum(5) == 30        # 0+1+4+9+16

    assert list(islice(primes(), 10)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(sliding_window([1], 2)) == []

    assert list(pipeline(range(20))) == [0, 4, 16, 36, 64]
    #  偶数 0,2,4,...,18 → 平方 0,4,16,36,64,100,... → <100 的: 0,4,16,36,64

    assert count_lines(iter(["a", "", "  ", "b\n"])) == 2

    assert prefix_sums([1, 2, 3]) == [1, 3, 6]
    assert all_pairs([1, 2, 3]) == [(1, 2), (1, 3), (2, 3)]
    assert flatten_all([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]

    assert demonstrate_exhaustion() == {"first": [0, 1, 2], "second": []}

    print("ch08 全部通过 ✓")


# region 参考答案
"""
def my_range(start, stop=None, step=1):
    if stop is None:
        start, stop = 0, start
    if step == 0:
        raise ValueError("step 不能为 0")
    cur = start
    while (cur < stop) if step > 0 else (cur > stop):
        yield cur
        cur += step

def evens():
    n = 0
    while True:
        yield n
        n += 2

def take_from_source(source_iter, n):
    return list(islice(source_iter, n))

def batches(items, size):
    it = iter(items)
    while True:
        batch = list(islice(it, size))
        if not batch:
            return
        yield batch

def first_n_squares_sum(n):
    return sum(x ** 2 for x in range(n))

def primes():
    def is_prime(n):
        if n < 2:
            return False
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                return False
        return True
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

def sliding_window(items, size):
    it = iter(items)
    try:
        window = tuple(islice(it, size))
    except TypeError:
        return
    if len(window) < size:
        return
    yield window
    for item in it:
        window = window[1:] + (item,)
        yield window

def pipeline(nums):
    return (x2 for x in nums if x % 2 == 0
            for x2 in [x ** 2] if x2 < 100)

def count_lines(lines):
    return sum(1 for line in lines if line.strip())

def prefix_sums(nums):
    return list(accumulate(nums))

def all_pairs(items):
    return list(combinations(items, 2))

def flatten_all(nested_lists):
    return list(chain.from_iterable(nested_lists))

def demonstrate_exhaustion():
    gen = (x for x in range(3))
    return {"first": list(gen), "second": list(gen)}
"""
# endregion
