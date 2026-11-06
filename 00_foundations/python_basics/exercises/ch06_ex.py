"""
ch06 练习：控制流
──────────────────────────────────────────────────
重点：别写 for i in range(len(x))！ 用 enumerate / zip / 推导式
"""


# ---------- 1. 找出所有素数（用 for-else） ----------
def is_prime(n):
    """
    n < 2 返回 False，否则判断是否为素数。
    必须用 for...else 结构写（练习这个语法）。
    """
    # TODO
    return None


# ---------- 2. FizzBuzz ----------
def fizzbuzz(n):
    """
    1..n，能被 3 整除替换 "Fizz"，5 → "Buzz"，同时能 → "FizzBuzz"
    返回 list（元素是 int 或 str）
    """
    # TODO
    return None


# ---------- 3. 查找第一个满足条件的（用 next + 生成器） ----------
def first_above(nums, threshold):
    """
    返回第一个大于 threshold 的元素，没有返回 None。
    提示：next((x for x in nums if x > threshold), None)
    """
    # TODO
    return None


# ---------- 4. 索引对照表 ----------
def index_map(items):
    """
    ["a","b"] → {"a": 0, "b": 1}
    用 enumerate + 字典推导式一行搞定，不许用 range(len())
    """
    # TODO
    return None


# ---------- 5. 配对求和 ----------
def pairwise_sum(a, b):
    """
    [1,2,3], [10,20,30] → [11,22,33]
    用 zip + 列表推导式
    """
    # TODO
    return None


# ---------- 6. 统计成绩分布 ----------
def grade_distribution(scores):
    """
    >=90 优秀，>=80 良好，>=60 及格，其余 不及格
    返回 dict: {"优秀": n, "良好": n, "及格": n, "不及格": n}
    四个 key 都要有（可以是 0）
    """
    # TODO
    return None


# ---------- 7. 累加直到超过阈值 ----------
def count_until(nums, limit):
    """从头累加 nums，返回累加和首次超过 limit 时用了几个元素（全加完也没超就返回 len）"""
    # TODO
    return None


# ---------- 8. 二分查找 ----------
def binary_search(sorted_nums, target):
    """返回下标，找不到返回 -1。用 while 循环（Python 里 while 相对少见，练一下）"""
    # TODO
    return None


# ---------- 9. 三角形（不需要 ==  comparison chain） ----------
def triangle_type(a, b, c):
    """
    先排序判断能否构成三角形（两小边之和 > 最大边），不能返回 "不是三角形"
    能则返回 "等边"/"等腰"/"普通"
    提示：a, b, c = sorted([a, b, c]) 然后 cin 比较链
    """
    # TODO
    return None


# ---------- 10. 矩阵最大值坐标 ----------
def max_position(matrix):
    """
    [[1,5,2],[9,3,4]] → (1, 0)  最大值 9 在第 1 行第 0 列
    用 enumerate 嵌套 + max(key=...) 或直接遍历
    """
    # TODO
    return None


# ---------- 11. 命令行菜单（练 while True + match） ----------
def process_command(cmd):
    """
    cmd 是字符串命令，返回处理结果字符串：
      "add 1 2 3"  → "和=6"
      "mul 2 3"    → "积=6"
      "max 5 2 9"  → "最大=9"
      其它        → "未知命令"
    用 match + 序列解构（str.split()）
    """
    # TODO
    return None


# ---------- 12. 去重并且在 BG 之后 ----------
def running_max(nums):
    """
    返回等长列表，第 i 项是 nums[:i+1] 的最大值
    [3,1,5,2] → [3,3,5,5]
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    assert [n for n in range(20) if is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19]

    assert fizzbuzz(15)[14] == "FizzBuzz"
    assert fizzbuzz(5) == [1, 2, "Fizz", 4, "Buzz"]
    assert fizzbuzz(3)[2] == "Fizz"

    assert first_above([1, 5, 9], 4) == 5
    assert first_above([1, 2], 10) is None

    assert index_map(["a", "b"]) == {"a": 0, "b": 1}

    assert pairwise_sum([1, 2, 3], [10, 20, 30]) == [11, 22, 33]
    assert pairwise_sum([1], [10, 20]) == [11]

    assert grade_distribution([95, 82, 60, 45]) == {
        "优秀": 1, "良好": 1, "及格": 1, "不及格": 1
    }
    assert grade_distribution([]) == {"优秀": 0, "良好": 0, "及格": 0, "不及格": 0}

    assert count_until([1, 2, 3, 4, 5], 6) == 4      # 1+2+3=6 不算超过，+4=10 才超过
    assert count_until([1, 1, 1], 100) == 3

    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5], 4) == -1
    assert binary_search([], 1) == -1

    assert triangle_type(3, 3, 3) == "等边"
    assert triangle_type(3, 3, 4) == "等腰"
    assert triangle_type(3, 4, 5) == "普通"
    assert triangle_type(1, 2, 3) == "不是三角形"
    assert triangle_type(1, 1, 3) == "不是三角形"

    assert max_position([[1, 5, 2], [9, 3, 4]]) == (1, 0)
    assert max_position([[7]]) == (0, 0)

    assert process_command("add 1 2 3") == "和=6"
    assert process_command("mul 2 3") == "积=6"
    assert process_command("max 5 2 9") == "最大=9"
    assert process_command("foo") == "未知命令"

    assert running_max([3, 1, 5, 2]) == [3, 3, 5, 5]
    assert running_max([]) == []

    print("ch06 全部通过 ✓")


# region 参考答案
"""
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    else:
        return True

def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(i)
    return out

def first_above(nums, threshold):
    return next((x for x in nums if x > threshold), None)

def index_map(items):
    return {item: i for i, item in enumerate(items)}

def pairwise_sum(a, b):
    return [x + y for x, y in zip(a, b)]

def grade_distribution(scores):
    dist = {"优秀": 0, "良好": 0, "及格": 0, "不及格": 0}
    for s in scores:
        if s >= 90:
            dist["优秀"] += 1
        elif s >= 80:
            dist["良好"] += 1
        elif s >= 60:
            dist["及格"] += 1
        else:
            dist["不及格"] += 1
    return dist

def count_until(nums, limit):
    total = 0
    for i, x in enumerate(nums, start=1):
        total += x
        if total > limit:
            return i
    return len(nums)

def binary_search(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == target:
            return mid
        elif sorted_nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def triangle_type(a, b, c):
    a, b, c = sorted([a, b, c])
    if a + b <= c:
        return "不是三角形"
    if a == b == c:
        return "等边"
    if a == b or b == c:
        return "等腰"
    return "普通"

def max_position(matrix):
    best = (-1, (-1, -1))
    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            if v > best[0]:
                best = (v, (i, j))
    return best[1]

def process_command(cmd):
    match cmd.split():
        case ["add", *nums]:
            return f"和={sum(int(n) for n in nums)}"
        case ["mul", *nums]:
            prod = 1
            for n in nums:
                prod *= int(n)
            return f"积={prod}"
        case ["max", *nums]:
            return f"最大={max(int(n) for n in nums)}"
        case _:
            return "未知命令"

def running_max(nums):
    cur = None
    out = []
    for x in nums:
        cur = x if cur is None or x > cur else cur
        out.append(cur)
    return out
"""
# endregion
