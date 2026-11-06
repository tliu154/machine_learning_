"""
np01 练习：ndarray 基础
──────────────────────────────────────────────────
重点：dtype/shape、切片是视图、布尔掩码
前置：import numpy as np —— 没装先 pip install numpy
"""

import numpy as np


# ---------- 1. 创建数组 ----------
def make_board(rows, cols):
    """返回 rows×cols 的二维数组，元素 = 行号*cols + 列号。不许用双重 for"""
    # TODO: 提示 reshape + arange
    return None


def even_space(n):
    """返回 [0, 1] 上均匀分布的 n 个点（含两端）。n=1 时返回 [0.0]"""
    # TODO
    return None


# ---------- 2. 形状报告 ----------
def describe(a):
    """
    返回 dict: {"shape": 元组, "ndim": int, "size": int,
                "dtype": str(a.dtype)}
    """
    # TODO
    return None


# ---------- 3. 视图 vs 拷贝 ----------
def make_copy(a):
    """返回 a 的独立副本：修改返回值绝不能影响 a（注意切片是视图！）"""
    # TODO
    return None


# ---------- 4. 布尔掩码 ----------
def positives(a):
    """返回 a 中所有正数组成的一维数组（顺序保持）"""
    # TODO
    return None


def count_between(a, lo, hi):
    """返回 a 中值在 [lo, hi] 区间内的元素个数（含端点）。不许写 for"""
    # TODO
    return None


def zero_negatives_inplace(a):
    """把 a 中所有负数【原地】清零，返回 a 本身"""
    # TODO
    return None


# ---------- 5. 取列 / 取行 ----------
def get_column(m, j):
    """返回二维数组 m 的第 j 列（一维数组）"""
    # TODO
    return None


def last_row(m):
    """返回二维数组 m 的最后一行"""
    # TODO
    return None


# ---------- 6. argsort ----------
def sort_by(scores, names):
    """
    scores 是数组，names 是等长列表。
    返回按 scores 降序排列后的 names 列表。
    提示：np.argsort(-scores)
    """
    # TODO
    return None


# ---------- 7. 排序下标去重统计 ----------
def value_stats(a):
    """
    返回 dict: {"unique": 去重升序列表, "counts": 对应出现次数列表}
    提示：np.unique(a, return_counts=True)
    """
    # TODO
    return None


# ---------- 8. 溢出实验 ----------
def saturating_add_u8(a, b):
    """
    a, b 都是 uint8 数组。返回 (a + b) 但【不回绕】——超过 255 的截到 255。
    提示：先 astype 升位再 clip 再转回 uint8
    """
    # TODO
    return None


# ---------- 9. 花式索引 ----------
def take_rows(m, order):
    """按 order 给出的行号顺序重排 m 的行（order 是行号列表）。返回新数组"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    b = make_board(3, 4)
    assert b.shape == (3, 4)
    assert b[0].tolist() == [0, 1, 2, 3]
    assert b[2, 3] == 11
    assert b[1, 0] == 4

    assert np.allclose(even_space(5), [0, 0.25, 0.5, 0.75, 1.0])
    assert even_space(1).tolist() == [0.0]
    assert len(even_space(100)) == 100

    a = np.arange(12).reshape(3, 4)
    info = describe(a)
    assert info == {"shape": (3, 4), "ndim": 2, "size": 12, "dtype": "int64"}
    assert describe(np.zeros(3))["dtype"] == "float64"

    src = np.array([1, 2, 3])
    cp = make_copy(src)
    cp[0] = 99
    assert src[0] == 1, "副本影响了原数组！"
    m2 = np.arange(6).reshape(2, 3)
    cp2 = make_copy(m2)
    cp2[0, 0] = -1
    assert m2[0, 0] == 0

    assert positives(np.array([3, -1, 7, -5, 2])).tolist() == [3, 7, 2]
    assert positives(np.array([-1, -2])).tolist() == []

    assert count_between(np.array([1, 5, 9, 12, 7]), 5, 10) == 3
    assert count_between(np.arange(10), 3, 3) == 1

    t = np.array([2, -3, 5, -1])
    out = zero_negatives_inplace(t)
    assert out is t, "必须原地修改（返回同一个对象）"
    assert t.tolist() == [2, 0, 5, 0]

    m = np.arange(12).reshape(3, 4)
    assert get_column(m, 1).tolist() == [1, 5, 9]
    assert last_row(m).tolist() == [8, 9, 10, 11]

    assert sort_by(np.array([88, 95, 60]), ["涛", "李", "王"]) == ["李", "涛", "王"]
    assert sort_by(np.array([1, 2]), ["a", "b"]) == ["b", "a"]

    vs = value_stats(np.array([3, 1, 3, 2, 1, 3]))
    assert vs["unique"] == [1, 2, 3]
    assert vs["counts"] == [2, 1, 3]

    x = np.array([200, 250], dtype=np.uint8)
    y = np.array([100, 100], dtype=np.uint8)
    r = saturating_add_u8(x, y)
    assert r.dtype == np.uint8
    assert r.tolist() == [255, 255], "uint8 回绕了！300%256=44 说明忘了升位"

    assert take_rows(m, [2, 0, 1]).tolist() == [[8, 9, 10, 11], [0, 1, 2, 3], [4, 5, 6, 7]]

    print("np01 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def make_board(rows, cols):
    return np.arange(rows * cols).reshape(rows, cols)

def even_space(n):
    if n == 1:
        return np.array([0.0])
    return np.linspace(0, 1, n)

def describe(a):
    return {"shape": a.shape, "ndim": a.ndim, "size": a.size, "dtype": str(a.dtype)}

def make_copy(a):
    return a.copy()

def positives(a):
    return a[a > 0]

def count_between(a, lo, hi):
    return int(((a >= lo) & (a <= hi)).sum())

def zero_negatives_inplace(a):
    a[a < 0] = 0
    return a

def get_column(m, j):
    return m[:, j]

def last_row(m):
    return m[-1]

def sort_by(scores, names):
    order = np.argsort(-np.asarray(scores))
    return [names[i] for i in order]

def value_stats(a):
    vals, counts = np.unique(a, return_counts=True)
    return {"unique": vals.tolist(), "counts": counts.tolist()}

def saturating_add_u8(a, b):
    result = a.astype(np.int32) + b.astype(np.int32)
    return np.clip(result, 0, 255).astype(np.uint8)

def take_rows(m, order):
    return m[list(order)]
"""
# endregion
