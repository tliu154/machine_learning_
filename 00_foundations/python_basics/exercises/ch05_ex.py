"""
ch05 练习：字典、集合与推导式
──────────────────────────────────────────────────
目标：把 C++ 里"手写 for 循环填 map"的习惯换成推导式
"""


# ---------- 1. 词频统计 ----------
def word_count(text):
    """
    返回 dict：单词 → 出现次数。
    不区分大小写，标点算作单词的一部分（先别用正则）。
    "Hello hello world" → {"hello": 2, "world": 1}
    """
    # TODO
    cnt={}
    for word in text.lower().split():
        if word not in cnt:
            cnt[word] = 1
            continue
        else:
            cnt[word] += 1

    return cnt


# ---------- 2. 反转映射 ----------
def invert(d):
    """{"a":1, "b":2} → {1:"a", 2:"b"}，题目保证值唯一"""
    # TODO: 字典推导式一行
    return {v:k for k,v in d.items()}


# ---------- 3. 分组 ----------
def group_by_length(words):
    """
    按字符串长度分组。
    ["ab","cd","xyz","q"] → {2: ["ab","cd"], 3: ["xyz"], 1: ["q"]}
    保持每个分组内部的原顺序。
    """
    # TODO
    dict={}
    for word in words:
        dict.setdefault(len(word), []).append(word)

    return dict


# ---------- 4. 合并两个字典（值相加） ----------
def merge_sum(d1, d2):
    """
    {"a":1,"b":2}, {"b":3,"c":4} → {"a":1,"b":5,"c":4}
    """
    # TODO
    result = dict(d1)
    for k, v in d2.items():
        result[k] =result.get(k, 0) + v
    return result


# ---------- 5. 安全取值 ----------
def safe_get(d, key, default="N/A"):
    """用 .get() 实现，d 里没有 key 就返回 default。不许用 if key in d"""
    # TODO
    return None


# ---------- 6. 筛选字典 ----------
def filter_dict(d, threshold):
    """保留值 >= threshold 的键值对，返回新 dict"""
    # TODO: 字典推导式
    return None


# ---------- 7. 扁平化数字矩阵求平方和 ----------
def sum_of_squares(nums):
    """返回 [x**2 for x in nums] 的总和，用生成器表达式传给 sum"""
    # TODO
    return None


# ---------- 8. 找出两个列表的共同元素 ----------
def common_elements(a, b):
    """返回共同元素组成的 set（去重）"""
    # TODO
    return None


# ---------- 9. 找出只出现一次的数字 ----------
def single_number(nums):
    """
    其他数字都出现两次，只有一个出现一次，找出来。
    [4,1,2,1,2] → 4
    不许用 dict！用集合的消去法。
    """
    # TODO
    return None


# ---------- 10. 字符异位词分组 ----------
def group_anagrams(words):
    """
    ["eat","tea","tan","ate","nat","bat"]
    返回 List[List[str]]，每组字母异位：
    [["eat","tea","ate"],["tan","nat"],["bat"]]
    组内顺序随意。
    提示：sorted(word) 得到字母列表 → tuple(sorted(word)) 做 key
    """
    # TODO
    return None


# ---------- 11. 矩阵坐标字典 ----------
def build_grid(rows, cols):
    """
    返回 dict：{(r, c): r*cols+c}，共 rows*cols 项。
    rows=2, cols=3 → {(0,0):0,(0,1):1,(0,2):2,(1,0):3,...}
    体会 tuple 当 key。
    """
    # TODO
    return None


# ---------- 12. Top-K 高频词 ----------
def top_k(text, k):
    """返回出现频率最高的 k 个单词组成的列表，按频率降序"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    assert word_count("Hello hello world") == {"hello": 2, "world": 1}
    assert word_count("") == {}

    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    assert group_by_length(["ab", "cd", "xyz", "q"]) == {
        2: ["ab", "cd"], 3: ["xyz"], 1: ["q"]
    }

    assert merge_sum({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4}

    assert safe_get({"a": 1}, "a") == 1
    assert safe_get({"a": 1}, "z") == "N/A"
    assert safe_get({}, "z", -1) == -1

    assert filter_dict({"a": 10, "b": 5, "c": 20}, 10) == {"a": 10, "c": 20}

    assert sum_of_squares([1, 2, 3]) == 14

    assert common_elements([1, 2, 2, 3], [2, 3, 4]) == {2, 3}

    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1

    groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    groups = sorted([sorted(g) for g in groups])
    assert groups == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

    assert build_grid(2, 3) == {(0, 0): 0, (0, 1): 1, (0, 2): 2,
                                (1, 0): 3, (1, 1): 4, (1, 2): 5}

    assert top_k("a b a c a b a", 2) == ["a", "b"]

    print("ch05 全部通过 ✓")


# region 参考答案
"""
def word_count(text):
    counts = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return counts

def invert(d):
    return {v: k for k, v in d.items()}

def group_by_length(words):
    groups = {}
    for w in words:
        groups.setdefault(len(w), []).append(w)
    return groups

def merge_sum(d1, d2):
    out = dict(d1)
    for k, v in d2.items():
        out[k] = out.get(k, 0) + v
    return out

def safe_get(d, key, default="N/A"):
    return d.get(key, default)

def filter_dict(d, threshold):
    return {k: v for k, v in d.items() if v >= threshold}

def sum_of_squares(nums):
    return sum(x ** 2 for x in nums)

def common_elements(a, b):
    return set(a) & set(b)

def single_number(nums):
    seen = set()
    for x in nums:
        if x in seen:
            seen.remove(x)
        else:
            seen.add(x)
    return seen.pop()

def group_anagrams(words):
    groups = {}
    for w in words:
        key = tuple(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())

def build_grid(rows, cols):
    return {(r, c): r * cols + c for r in range(rows) for c in range(cols)}

def top_k(text, k):
    counts = word_count(text)
    return [w for w, _ in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:k]]
"""
# endregion
