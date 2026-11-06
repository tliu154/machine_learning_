"""
ch01 练习：世界观
──────────────────────────────────────────────────
目标：
  1. 体会"变量是便利贴"（引用语义）
  2. 区分 is 和 ==
  3. 熟悉 input / int 转换
把每个 TODO 的地方补完，然后右键 Run 这个文件。
底部的 assert 全过就 OK。
"""


# ---------- 1. 交换两个变量（不许用临时变量） ----------
def swap(a, b):
    """返回交换顺序后的元组 (b, a)"""
    # TODO: 一行搞定

    return b,a


# ---------- 2. 引用 vs 拷贝 ----------
def make_copy(lst):
    """
    返回 lst 的一个【独立副本】。
    要求：修改返回的列表，绝不能影响传进来的原列表。
    """
    # TODO

    return lst.copy()


# ---------- 3. 判断 None ----------
def describe(x):
    """
    x 是 None 时返回字符串 "空"，
    否则返回 f"值是{x}"
    注意：判断 None 要用 is，不要用 ==
    """
    # TODO
    if x is None:
        return "空"
    else:
        return f"值是{x}"


# ---------- 4. 温度转换 ----------
def celsius_to_fahrenheit(c):
    """摄氏转华氏：F = C * 9/5 + 32，返回浮点数"""
    # TODO

    return c * 9 / 5 + 32


# ---------- 5. 一行读两个整数 ----------
def read_two_ints(line):
    """
    line 是形如 "3 5" 的字符串，返回整数元组 (3, 5)
    提示：split() + map(int, ...) + tuple
    """
    # TODO

    return tuple(map(int, line.split()))



# ---------- 6. 用一行 read_two_ints + 除法做均值 ----------
def average_of_two(line):
    """给定 "3 5" 返回平均值 4.0（注意 Python 的 / 返回什么）"""
    # TODO: 复用上面的函数
    a, b = read_two_ints(line)

    return (a + b) / 2


# ==================== 自测 ====================
if __name__ == "__main__":
    assert swap(1, 2) == (2, 1), "swap 没写对"
    assert swap("a", "b") == ("b", "a")

    src = [1, 2, 3]
    cp = make_copy(src)
    cp.append(99)
    assert src == [1, 2, 3], "make_copy 不是真正的副本，原列表被改了！"
    assert cp == [1, 2, 3, 99]

    assert describe(None) == "空"
    assert describe(0) == "值是0", "注意：业务值 0 不能当成 None"

    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert abs(celsius_to_fahrenheit(37) - 98.6) < 0.01

    assert read_two_ints("3 5") == (3, 5)
    assert read_two_ints("-1 100") == (-1, 100)

    assert average_of_two("3 5") == 4.0
    assert isinstance(average_of_two("3 5"), float), "/ 应该返回 float"

    print("ch01 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def swap(a, b):
    return b, a

def make_copy(lst):
    return lst.copy()          # 或 list(lst) / lst[:]

def describe(x):
    if x is None:
        return "空"
    return f"值是{x}"

def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

def read_two_ints(line):
    return tuple(map(int, line.split()))

def average_of_two(line):
    a, b = read_two_ints(line)
    return (a + b) / 2
"""
# endregion
