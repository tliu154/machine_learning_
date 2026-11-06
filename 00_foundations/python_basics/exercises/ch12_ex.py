"""
ch12 练习：递归
──────────────────────────────────────────────────
先读 docs/ch12_recursion.md。
写递归前先问自己两句：
    1. 最简单的情况是什么（终止条件）？
    2. 怎么把问题缩小一点点再交给自己？
"""

from functools import lru_cache
from pathlib import Path


# ---------- 1. 阶乘（递归版） ----------
def factorial(n):
    """
    n! 的递归实现。
    n <= 1 返回 1；n < 0 抛 ValueError("负数没有阶乘")
    """
    # TODO
    if n<=1: return 1
    if n<0: return None
    return n*factorial(n-1)




# ---------- 2. 阶乘（循环版，做对照） ----------
def factorial_iter(n):
    """用 while 实现同样的功能，体会两种写法的差别。n < 0 同样抛 ValueError"""
    # TODO
    if n < 0:
        raise ValueError("负数没有阶乘")
    result = 1
    while n > 1:
        result *= n
        n -= 1
    return result


# ---------- 3. 最大公约数（欧几里得） ----------
def gcd(a, b):
    """
    递归版：gcd(a, b) = gcd(b, a % b)，b == 0 时返回 a
    gcd(48, 18) → 6
    """
    # TODO
    if b == 0:
        return a
    return gcd(b, a % b)



# ---------- 4. 幂运算 ----------
def power(base, exp):
    """base 的 exp 次方，exp 是非负整数。递归实现，不许用 **"""
    # TODO
    if exp == 0:
        return 1
    return base*power(base, exp - 1)


# ---------- 5. 斐波那契（递归 + 缓存） ----------
@lru_cache(maxsize=None)
def fib(n):
    """
    fib(0)=0, fib(1)=1, fib(n)=fib(n-1)+fib(n-2)
    必须用 @lru_cache，否则 fib(35) 要跑很久
    """
    # TODO
    if n < 0: return None
    elif n == 0: return 0
    elif n == 1: return 1
    return fib(n-1)+fib(n-2)


# ---------- 6. 反转字符串 ----------
def reverse(s):
    """递归版：最后一个字符 + 前面部分的反转。不许用切片 [::-1]"""
    # TODO
    if len(s)<=1:
        return s

    return s[-1]+reverse(s[:-1])


# ---------- 7. 判断回文 ----------
def is_palindrome(s):
    """递归版：首尾字符相同 且 去掉首尾后仍是回文。长度 <= 1 算回文"""
    # TODO
    if len(s)<=1: return True

    return is_palindrome(s[1:-1]) and s[0]==s[-1]



# ---------- 8. 完全拍平嵌套列表 ----------
def flatten(nested):
    """
    [1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]
    任意深度都要能拍平。
    """
    # TODO
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# ---------- 9. 二分查找（递归版） ----------
def binary_search(nums, target, lo=0, hi=None):
    """
    在【已排序】的 nums 中找 target，返回下标，找不到返回 -1。
    hi 为 None 时表示第一次调用，自动设为 len(nums)-1。
    用默认参数 lo/hi 传区间，别用切片（切片会丢掉真实下标）。
    """
    # TODO
    if hi is None: hi = len(nums)-1
    if lo>hi: return -1

    mid=(hi+lo)//2
    if nums[mid]==target: return mid
    elif nums[mid]>target: return binary_search(nums, target, lo, mid-1)
    else: return binary_search(nums, target, mid + 1, hi)





# ---------- 10. 汉诺塔 ----------
def hanoi(n, src="A", dst="C", aux="B"):
    """
    返回移动步骤列表，每步是 (从哪根柱子, 到哪根柱子) 的元组。Z
    hanoi(1) → [("A", "C")]
    hanoi(2) → [("A","B"), ("A","C"), ("B","C")]
    思路：把 n-1 个挪到中转柱 → 挪最大的那个 → 把 n-1 个从中转柱挪到目标柱
    """
    # TODO
    if n<=0:
        return []
    step=[]
    step.extend(hanoi(n-1, src, aux, dst))
    step.append((src,dst))
    step.extend(hanoi(n-1, aux, dst, src))
    return step


# ---------- 11. 快速排序（递归版） ----------
def quicksort(nums):
    """
    返回排序后的【新列表】，不要改原列表。
    思路：选一个基准 → 小的放左边、相等的放中间、大的放右边 → 左右各自递归
    """
    # TODO
    return None


# ---------- 12. 递归遍历目录 ----------
def walk_files(root):
    """
    生成器：产出 root 下所有文件（含子目录里的），每个是 Path 对象。
    提示：is_dir() 判断目录，用 yield from 递归
    """
    # TODO
    return None


def dir_stats(root):
    """返回 {"files": 文件数, "bytes": 总字节数}，复用 walk_files"""
    # TODO
    return None


# ---------- 13. 感受递归深度上限 ----------
def recursion_limit_demo():
    """
    写一个必定无法终止的递归去触发 RecursionError，
    然后捕获它并返回异常的类型名字符串 "RecursionError"。
    （如果没触发，返回 "没触发"）
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    import tempfile


    assert gcd(48, 18) == 6
    assert gcd(17, 5) == 1
    assert gcd(0, 5) == 5
    assert gcd(12, 12) == 12

    assert power(2, 10) == 1024
    assert power(3, 0) == 1
    assert power(2, 1) == 2
    assert power(5, 3) == 125

    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55
    assert fib(35) == 9227465, "fib(35) 太慢说明忘了加 @lru_cache"

    assert reverse("abcdef") == "fedcba"
    assert reverse("") == ""
    assert reverse("你") == "你"
    assert reverse("中a文") == "文a中"

    assert is_palindrome("abcba") is True
    assert is_palindrome("abba") is True
    assert is_palindrome("abc") is False
    assert is_palindrome("") is True

    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert flatten([]) == []
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([[[[1]]]]) == [1]

    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5, 7, 9], 1) == 0
    assert binary_search([1, 3, 5, 7, 9], 9) == 4
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    assert binary_search([], 1) == -1

    assert hanoi(1) == [("A", "C")]
    assert hanoi(2) == [("A", "B"), ("A", "C"), ("B", "C")]
    assert len(hanoi(3)) == 7
    assert len(hanoi(10)) == 1023      # 2^n - 1 步

    assert quicksort([3, 6, 1, 8, 2]) == [1, 2, 3, 6, 8]
    assert quicksort([]) == []
    assert quicksort([1]) == [1]
    assert quicksort([5, 5, 3, 5]) == [3, 5, 5, 5]
    original = [3, 1, 2]
    assert quicksort(original) == [1, 2, 3]
    assert original == [3, 1, 2], "quicksort 不应该修改原列表"

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.txt").write_text("12345", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "b.txt").write_text("12", encoding="utf-8")
        (root / "sub" / "deep").mkdir()
        (root / "sub" / "deep" / "c.txt").write_text("x", encoding="utf-8")
        stats = dir_stats(root)
        assert stats["files"] == 3, stats
        assert stats["bytes"] == 5 + 2 + 1, stats
        assert len(list(walk_files(root))) == 3

    assert recursion_limit_demo() == "RecursionError"

    print("ch12 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def factorial(n):
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def factorial_iter(n):
    if n < 0:
        raise ValueError("负数没有阶乘")
    result = 1
    while n > 1:
        result *= n
        n -= 1
    return result

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def reverse(s):
    if len(s) <= 1:
        return s
    return s[-1] + reverse(s[:-1])

def is_palindrome(s):
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])

def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def binary_search(nums, target, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return binary_search(nums, target, mid + 1, hi)
    else:
        return binary_search(nums, target, lo, mid - 1)

def hanoi(n, src="A", dst="C", aux="B"):
    if n <= 0:
        return []
    steps = []
    steps.extend(hanoi(n - 1, src, aux, dst))
    steps.append((src, dst))
    steps.extend(hanoi(n - 1, aux, dst, src))
    return steps

def quicksort(nums):
    if len(nums) <= 1:
        return list(nums)
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quicksort(left) + mid + quicksort(right)

def walk_files(root):
    for entry in Path(root).iterdir():
        if entry.is_dir():
            yield from walk_files(entry)
        else:
            yield entry

def dir_stats(root):
    files = list(walk_files(root))
    return {"files": len(files), "bytes": sum(f.stat().st_size for f in files)}

def recursion_limit_demo():
    def forever(n):
        return forever(n + 1)
    try:
        forever(0)
    except RecursionError:
        return "RecursionError"
    return "没触发"
"""
# endregion
