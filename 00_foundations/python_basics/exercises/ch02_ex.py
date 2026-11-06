"""
ch02 练习：数字与运算
──────────────────────────────────────────────────
目标：整除/真除/幂、比较链、格式化输出、math 模块
"""


# ---------- 1. 一元二次方程求根 ----------
def quad_roots(a, b, c):
    """
    返回 ax^2+bx+c=0 的两个实根组成的元组 (x1, x2)，x1 <= x2。
    题目保证判别式 >= 0。
    提示：判别式要用 ** 0.5 或 math.sqrt
    """
    # TODO
    delta = b ** 2 - 4 * a * c
    x1 = (-b - delta**0.5) / (2 * a)
    x2 = (-b + delta**0.5) / (2 * a)
    return x1, x2


# ---------- 2. 秒 → 时分秒 ----------
def hms(total_seconds):
    """
    传入整数秒，返回 (小时, 分钟, 秒) 的元组。
    例：hms(3661) → (1, 1, 1)
    提示：divmod 是这里最好用的东西
    """
    # TODO
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


# ---------- 3. 判断闰年 ----------
def is_leap(year):
    """
    能被 4 整除且不能被 100 整除，或者能被 400 整除。
    返回 bool。
    提示：试着用一行 return + 逻辑运算符，体会 and/or/not
    """
    # TODO
    return year%4==0 and year%100!=0 or year%400==0


# ---------- 4. 数字格式化 ----------
def format_money(amount):
    """
    返回带千分位和两位小数的字符串。
    例：format_money(1234567.891) → "1,234,567.89"
    提示：f-string 里用 ,
    """
    # TODO

    return f"{amount:,.2f}"


# ---------- 5. 计算圆的周长面积 ----------
def circle(r):
    """返回 (周长, 面积) 的浮点数元组，用 math.pi"""
    import math

    # TODO
    area = math.pi * r**2

    return 2*math.pi*r, area


# ---------- 6. 阶乘（用 math 模块版和手写版各写一次） ----------
def factorial(n):
    """n >= 0，返回 n! （int）。不许用 math.factorial"""
    # TODO: 用循环
    if n == 0:
        return 1
    elif n>0:
        res=1
        for i in range(n):
            res*=i+1
        return res
    else:
        return 1



# ---------- 7. 等比数列求和 ----------
def geo_sum(a, r, n):
    """
    等比数列前 n 项和：a + ar + ar^2 + ... + ar^(n-1)
    r != 1 时用公式 a*(r**n - 1)/(r-1)；r == 1 时是 a*n
    """
    # TODO
    return a*n if r==1 else a*(r**n - 1)/(r-1)


# ---------- 8. 找出最大值和最小值 ----------
def min_max(nums):
    """返回元组 (最小值, 最大值)。空列表返回 (None, None)"""
    # TODO: 优先用内置函数，别手搓循环
    if not nums:
        return (None, None)
    return (min(nums), max(nums))


# ==================== 自测 ====================
if __name__ == "__main__":
    import math

    x1, x2 = quad_roots(1, -3, 2)
    assert abs(x1 - 1) < 1e-9 and abs(x2 - 2) < 1e-9

    assert hms(3661) == (1, 1, 1)
    assert hms(0) == (0, 0, 0)
    assert hms(59) == (0, 0, 59)
    assert hms(3600) == (1, 0, 0)

    assert is_leap(2024) is True
    assert is_leap(1900) is False
    assert is_leap(2000) is True
    assert is_leap(2023) is False

    assert format_money(1234567.891) == "1,234,567.89"
    assert format_money(0.5) == "0.50"
    assert format_money(-1234.5) == "-1,234.50"

    c, a = circle(1)
    assert abs(c - 2 * math.pi) < 1e-9
    assert abs(a - math.pi) < 1e-9

    assert factorial(0) == 1
    assert factorial(5) == 120
    assert factorial(20) == 2432902008176640000, "int 无限精度，别担心溢出"

    assert geo_sum(1, 2, 4) == 15       # 1+2+4+8
    assert geo_sum(3, 1, 5) == 15       # 3*5
    assert geo_sum(2, 3, 3) == 26       # 2+6+18

    assert min_max([3, 1, 4, 1, 5]) == (1, 5)
    assert min_max([-2.5]) == (-2.5, -2.5)
    assert min_max([]) == (None, None)

    print("ch02 全部通过 ✓")


# region 参考答案
"""
def quad_roots(a, b, c):
    d = (b * b - 4 * a * c) ** 0.5
    x1 = (-b - d) / (2 * a)
    x2 = (-b + d) / (2 * a)
    return (x1, x2) if x1 <= x2 else (x2, x1)

def hms(total_seconds):
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)
    return (h, m, s)

def is_leap(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

def format_money(amount):
    return f"{amount:,.2f}"

def circle(r):
    import math
    return (2 * math.pi * r, math.pi * r ** 2)

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def geo_sum(a, r, n):
    return a * n if r == 1 else a * (r ** n - 1) / (r - 1)

def min_max(nums):
    if not nums:
        return (None, None)
    return (min(nums), max(nums))
"""
# endregion
