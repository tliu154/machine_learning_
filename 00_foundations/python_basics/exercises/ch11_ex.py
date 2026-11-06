"""
ch11 练习：标准库与项目组织
──────────────────────────────────────────────────
这一章没有太多新语法，重点是"知道有这些现成工具"。
每个函数用标准库解决，不要重复造轮子。
"""

import argparse
import collections
import datetime
import random
import re
from pathlib import Path


# ---------- 1. datetime：日期计算 ----------
def days_between(d1, d2):
    """
    d1, d2 是 "YYYY-MM-DD" 格式字符串。
    返回相差天数（绝对值 int）。
    提示：datetime.date.fromisoformat + abs((a-b).days)
    """
    # TODO
    return None


def next_weekday(d, target_weekday):
    """
    返回 d 之后（不含 d 当天）最近的那个 target_weekday 的日期对象。
    weekday 用 Monday=0 ... Sunday=6（Python 惯例，和你的直觉对齐了吗？）
    """
    # TODO
    return None


def format_stamp(dt):
    """dt 是 datetime，返回 "2026-10-08 15:30:45" 格式字符串"""
    # TODO
    return None


# ---------- 2. random：随机 ----------
def shuffle_deterministic(items, seed):
    """
    用固定随机种子打乱 items 的副本，返回打乱后的新列表。
    要求同样的 seed 必须得到同样的结果（可复现，调试很有用）。
    不许改原列表。
    """
    # TODO
    return None


def weighted_pick(options, weights):
    """按权重随机挑一个。用 random.choices(..., k=1)"""
    # TODO
    return None


# ---------- 3. re：正则 ----------
def extract_numbers(text):
    r"""
    提取所有整数（含负数），返回 int 列表。
    "温度 -5 到 12 度" → [-5, 12]
    提示：r"-?\d+"
    """
    # TODO
    return None


def is_valid_email(email):
    """简单校验：xxx@xxx.xxx 形式。用 re.fullmatch"""
    # TODO
    return None


def mask_digits(text):
    """把字符串里连续的数字串替换成相同长度的 * 。例：'卡号1234' → '卡号****'"""
    # TODO: re.sub 里可以用 lambda 控制替换内容
    return None


# ---------- 4. collections ----------
def top_n_frequent(items, n):
    """返回出现频率最高的 n 个元素列表（降序），用 collections.Counter"""
    # TODO
    return None


def build_index(records):
    """
    records 是 dict 列表，每个有 "category" 键。
    按 category 分组：{"A": [rec, ...], "B": [...]}
    用 defaultdict
    """
    # TODO
    return None


def moving_average(nums, window):
    """
    返回滑动平均列表，长度 = len(nums) - window + 1。
    用 collections.deque 维护窗口。
    nums=[1,2,3,4,5], window=3 → [2.0, 3.0, 4.0]
    """
    # TODO
    return None


# ---------- 5. argparse：命令行解析 ----------
def build_parser():
    """
    构造并返回 ArgumentParser，要求：
      位置参数 input（输入文件）
      可选参数 -o/--output，默认 "out.txt"
      可选参数 -n/--count，int 类型，默认 10
      开关参数 -v/--verbose（store_true）
    """
    # TODO
    return None


# ---------- 6. pathlib 实战 ----------
def organize_info(path_str):
    """
    返回 dict：
      {" exists": Path(...).exists(),
       "name": 文件名（含扩展）,
       "stem": 不带扩展的文件名,
       "suffix": 扩展名（含点）,
       "parent": 父目录字符串,
       "size_ok": 如果存在且大小 > 0 否则 False}
    注意 prefix 里的键名别写错了（这里特意留个坑测试你的细心）
    """
    # TODO
    return None


# ---------- 7. 环境变量与系统信息 ----------
def get_env_or(key, default=None):
    """读环境变量，不存在返回 default。用 os.environ.get"""
    import os

    # TODO
    return None


# ---------- 8. 主入口写法 ----------
def main(argv=None):
    """
    用 build_parser() 解析 argv（None 表示用真实的 sys.argv），
    然后返回一个描述性的字符串：
        f"处理 {input} → {output}，条数 {count}，{'详细' if verbose else '静默'}"
    这就是真实项目里 main 的样子（把 argparse 和业务逻辑串起来）。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    random.seed(0)

    assert days_between("2026-01-01", "2026-01-31") == 30
    assert days_between("2026-03-01", "2026-02-01") == 28

    d = next_weekday(datetime.date(2026, 10, 8), 0)      # 2026-10-08 是周四
    assert d.weekday() == 0 and d > datetime.date(2026, 10, 8)
    assert next_weekday(datetime.date(2026, 10, 8), 3) == datetime.date(2026, 10, 15)

    assert format_stamp(datetime.datetime(2026, 10, 8, 15, 30, 45)) == "2026-10-08 15:30:45"

    src = list(range(10))
    a1 = shuffle_deterministic(src, 42)
    a2 = shuffle_deterministic(src, 42)
    assert a1 == a2, "同样的 seed 必须得到同样的结果"
    assert sorted(a1) == src
    assert src == list(range(10)), "不能改原列表"

    assert weighted_pick(["a"], [1]) == "a"

    assert extract_numbers("温度 -5 到 12 度") == [-5, 12]
    assert extract_numbers("没有数字") == []

    assert is_valid_email("a@b.com") is True
    assert is_valid_email("a@b") is False
    assert is_valid_email("@b.com") is False

    assert mask_digits("卡号1234密码56") == "卡号****密码**"

    assert top_n_frequent(["a", "b", "a", "c", "b", "a"], 2) == ["a", "b"]

    records = [
        {"category": "A", "id": 1},
        {"category": "B", "id": 2},
        {"category": "A", "id": 3},
    ]
    idx = build_index(records)
    assert len(idx["A"]) == 2 and len(idx["B"]) == 1

    assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    assert moving_average([1, 2], 3) == []

    parser = build_parser()
    args = parser.parse_args(["in.txt", "-o", "res.txt", "-n", "5", "-v"])
    assert args.input == "in.txt"
    assert args.output == "res.txt"
    assert args.count == 5 and isinstance(args.count, int)
    assert args.verbose is True
    args2 = parser.parse_args(["data.csv"])
    assert args2.output == "out.txt" and args2.count == 10 and args2.verbose is False

    info = organize_info(r"D:\a\b\c.txt")
    assert info["name"] == "c.txt"
    assert info["stem"] == "c"
    assert info["suffix"] == ".txt"

    import os
    os.environ["MY_TEST_KEY"] = "hello"
    assert get_env_or("MY_TEST_KEY") == "hello"
    assert get_env_or("DEFINITELY_NOT_SET_123", "x") == "x"

    assert main(["in.txt"]) == "处理 in.txt → out.txt，条数 10，静默"
    assert main(["in.txt", "-o", "o.txt", "-n", "3", "-v"]) == "处理 in.txt → o.txt，条数 3，详细"

    print("ch11 全部通过 ✓")


# region 参考答案
"""
def days_between(d1, d2):
    a = datetime.date.fromisoformat(d1)
    b = datetime.date.fromisoformat(d2)
    return abs((a - b).days)

def next_weekday(d, target_weekday):
    delta = (target_weekday - d.weekday()) % 7
    if delta == 0:
        delta = 7
    return d + datetime.timedelta(days=delta)

def format_stamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def shuffle_deterministic(items, seed):
    rng = random.Random(seed)          # 独立的 Random 实例，不污染全局状态
    result = list(items)
    rng.shuffle(result)
    return result

def weighted_pick(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

def extract_numbers(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]

def is_valid_email(email):
    return re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", email) is not None

def mask_digits(text):
    return re.sub(r"\d+", lambda m: "*" * len(m.group()), text)

def top_n_frequent(items, n):
    return [item for item, _ in collections.Counter(items).most_common(n)]

def build_index(records):
    index = collections.defaultdict(list)
    for rec in records:
        index[rec["category"]].append(rec)
    return dict(index)          # 转回普通 dict，避免外部意外创建 key

def moving_average(nums, window):
    if window > len(nums):
        return []
    win = collections.deque(nums[:window], maxlen=window)
    result = [sum(win) / window]
    for x in nums[window:]:
        win.append(x)
        result.append(sum(win) / window)
    return result

def build_parser():
    p = argparse.ArgumentParser(description="一个简单的命令行工具")
    p.add_argument("input", help="输入文件")
    p.add_argument("-o", "--output", default="out.txt")
    p.add_argument("-n", "--count", type=int, default=10)
    p.add_argument("-v", "--verbose", action="store_true")
    return p

def organize_info(path_str):
    p = Path(path_str)
    return {
        "exists": p.exists(),
        "name": p.name,
        "stem": p.stem,
        "suffix": p.suffix,
        "parent": str(p.parent),
        "size_ok": p.exists() and p.stat().st_size > 0,
    }

def get_env_or(key, default=None):
    import os
    return os.environ.get(key, default)

def main(argv=None):
    args = build_parser().parse_args(argv)
    return f"处理 {args.input} → {args.output}，条数 {args.count}，{'详细' if args.verbose else '静默'}"
"""
# endregion
