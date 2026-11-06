"""
ch04 练习：列表与元组
──────────────────────────────────────────────────
这里专门布置了几道"深拷贝陷阱"题 —— C++ 转 Python 的人在这里摔得最惨。
"""


# ---------- 1. 移除重复元素并保持顺序 ----------
def dedup(lst):
    """
    [3,1,3,2,1] → [3,1,2]
    不许用 set() 直接转（那会丢顺序），自己判重。
    """
    # TODO
    seen=set()
    result=[]
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


# ---------- 2. 找出出现次数最多的元素 ----------
def most_common(lst):
    """返回出现次数最多的元素。空列表返回 None"""
    # TODO
    if not lst:
        return None
    return max(set(lst), key=lst.count)


# ---------- 3. 分块 ----------
def chunk(lst, size):
    """
    [1,2,3,4,5], 2 → [[1,2],[3,4],[5]]
    提示：切片 + range(0, len, size)
    """
    # TODO
    result = []
    for i in range(0, len(lst), size):
        result.append(lst[i:i + size])
    return result


# ---------- 4. 转置矩阵 ----------
def transpose(matrix):
    """
    [[1,2,3],[4,5,6]] → [[1,4],[2,5],[3,6]]
    提示：列表推导式嵌套一行搞定
    """
    # TODO
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


# ---------- 5. ⚠️ 创建正确的二维数组 ----------
def make_matrix(rows, cols, value=0):
    """
    返回 rows×cols 的二维列表，每行都是【独立的】列表。
    修改 matrix[0][0] 绝不能影响 matrix[1][0]。
    这就是文档里说的 [[0]*n]*m 陷阱 —— 别踩。
    """
    # TODO
    return [[value]*cols for _ in range(rows)]


# ---------- 6. ⚠️ 深拷贝 ----------
def deep_copy(matrix):
    """手工实现二维列表的深拷贝（不许 import copy）"""
    # TODO
    return [row[:] for row in matrix]


# ---------- 7. 原地去重（不用新列表） ----------
def remove_evens_inplace(lst):
    """
    原地删除 lst 中所有偶数，不返回新列表（返回值随意）。
    提示：倒序遍历可以避免因删除导致的下标错位；或者用 while。
    """
    # TODO
    for x in lst:
        if x % 2 == 0:
            lst.remove(x)

    return lst


# ---------- 8. 排序 ----------
def sort_students(students):
    """
    students 是若干 tuple: (姓名, 成绩, 年龄)
    按成绩降序；成绩相同按年龄升序。
    返回排序后的新列表，不要改原列表。
    提示：sorted 的 key 返回一个元组即可
    """
    # TODO

    return sorted(students,key=lambda x:(-x[1],x[2]))


# ---------- 9. 扁平化 ----------
def flatten(nested):
    """[[1,2],[3,[4,5]],6] → [1,2,3,[4,5],6]  只拍平一层"""
    # TODO
    res=[]
    for x in nested:
        if isinstance(x, list):
            for y in x:
                res.append(y)
        else:
            res.append(x)
    return res


# ---------- 10. 旋转列表 ----------
def rotate(lst, k):
    """
    循环右移 k 位（k 可能大于 len）。
    [1,2,3,4,5], 2 → [4,5,1,2,3]
    返回新列表，原列表不变。
    """
    # TODO: 用切片
    if not lst:
        return []

    k%=len(lst)
    return lst[-k:]+lst[:-k]


# ---------- 11. 两个列表求交集/差集（保持顺序） ----------
def list_diff(a, b):
    """返回在 a 中但不在 b 中的元素列表，保持 a 的原顺序"""
    # TODO
    return [x for x in a if x not in b]


# ==================== 自测 ====================
if __name__ == "__main__":
    assert dedup([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dedup([]) == []

    assert most_common([1, 2, 2, 3, 3, 3]) == 3
    assert most_common([]) is None

    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([1], 5) == [[1]]

    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

    m = make_matrix(3, 4)
    assert m == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    m[0][0] = 99
    assert m[1][0] == 0, "行之间串了！这就是 [[0]*n]*m 的坑"
    assert m == [[99, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    src = [[1, 2], [3, 4]]
    cp = deep_copy(src)
    cp[0][0] = 99
    assert src == [[1, 2], [3, 4]], "deep_copy 应该彻底独立"

    tmp = [1, 2, 3, 4, 5, 6]
    assert remove_evens_inplace(tmp) == [1, 3, 5]

    students = [("涛", 90, 19), ("李", 90, 18), ("王", 85, 20)]
    assert sort_students(students) == [("李", 90, 18), ("涛", 90, 19), ("王", 85, 20)]
    assert students[0][0] == "涛", "不应该修改原列表"

    assert flatten([[1, 2], [3, [4, 5]], 6]) == [1, 2, 3, [4, 5], 6]

    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert rotate([1, 2, 3], 5) == [2, 3, 1]

    assert list_diff([1, 2, 3, 2, 4], [2, 4]) == [1, 3]

    print("ch04 全部通过 ✓")


# region 参考答案
"""
def dedup(lst):
    seen = set()
    result = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

def most_common(lst):
    if not lst:
        return None
    return max(set(lst), key=lst.count)

def chunk(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def make_matrix(rows, cols, value=0):
    return [[value] * cols for _ in range(rows)]

def deep_copy(matrix):
    return [row[:] for row in matrix]

def remove_evens_inplace(lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] % 2 == 0:
            del lst[i]
    return lst

def sort_students(students):
    return sorted(students, key=lambda s: (-s[1], s[2]))

def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out

def rotate(lst, k):
    if not lst:
        return []
    k %= len(lst)
    return lst[-k:] + lst[:-k]

def list_diff(a, b):
    bs = set(b)
    return [x for x in a if x not in bs]
"""
# endregion
