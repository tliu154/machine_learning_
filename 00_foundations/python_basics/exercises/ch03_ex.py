"""
ch03 练习：字符串
──────────────────────────────────────────────────
目标：切片（重点！）、f-string、常用方法
"""


# ---------- 1. 反转字符串 ----------
def reverse(s):
    """返回反转后的字符串，不许写循环，用切片"""
    # TODO
    return s[::-1]


# ---------- 2. 判断回文 ----------
def is_palindrome(s):
    """
    忽略大小写和空格判断是否是回文。
    例：is_palindrome("Never Odd or Even") → True
    提示：先归一（lower + 去空格），再和反转比较
    """
    # TODO
    t="".join(s.lower().split())
    return t == t[::-1]


# ---------- 3. 取中间部分 ----------
def middle(s):
    """掐头去尾，返回去掉首尾字符后的字符串。长度 < 3 时返回空串"""
    # TODO: 用切片
    if s=="":
        return ""
    else:
        return s[1:-1]


# ---------- 4. 首字母大写 ----------
def title_case(sentence):
    """
    把每个单词首字母大写，其余小写，用空格连接。
    例："hello  world" → "Hello World"（注意多余空格要压缩成一个）
    提示：split() 不传参会自动处理多个空格
    """
    # TODO
    t=" ".join(w.capitalize() for w in sentence.split())
    return t
    return None


# ---------- 5. 统计字符次数 ----------
def char_count(s):
    """
    返回 dict，key 是字符（原样保留大小写），value 是出现次数。
    不用 collections.Counter，手写。
    """
    # TODO
    dict={}
    for c in s:
        if c not in dict:
            dict[c]=1
        elif c in dict:
            dict[c]+=1
    return dict


# ---------- 6. 单词反转 ----------
def reverse_words(sentence):
    """
    反转单词顺序但保留单词内部。
    例："I love Python" → "Python love I"
    提示：split + 反转 + join
    """
    # TODO
    s=" ".join(sentence.split()[::-1])
    return s



# ---------- 7. 隐藏手机号 ----------
def mask_phone(phone):
    """
    保留前 3 位和后 4 位，中间用 **** 替代。
    例："13812345678" → "138****5678"
    """
    # TODO: 用切片 + f-string
    res=phone[:3]+"****"+phone[len(phone)-4:]
    return res


# ---------- 8. 生成成绩报告 ----------
def score_report(name, scores):
    """
    返回形如这样的字符串（一行）：
    涛: [95, 88, 76] 平均 86.3 最高 95 最低 76
    平均分保留 1 位小数。
    """
    # TODO: 用 f-string，平均分用 sum/len
    ave=sum(scores)/len(scores)
    return f"{name}: {scores} 平均 {ave:.1f} 最高 {max(scores)} 最低 {min(scores)}"


# ---------- 9. URL 参数解析 ----------
def parse_query(qs):
    """
    "a=1&b=2&c=3" → {"a": "1", "b": "2", "c": "3"}
    值保持字符串。提示：split("&") 再 split("=", 1)
    """
    # TODO
    res={}
    if not qs:
        return res
    for q in qs.split("&"):
        key, value = q.split("=",1)
        res[key] = value
    return res


# ---------- 10. 检查括号是否配对 ----------
def balanced(s):
    """
    只检查 () 两种括号是否配对。
    例：balanced("(a(b)c)") → True；balanced("(a))") → False
    用一个计数器 int 即可，不需要栈。
    """
    # TODO
    cnt=0
    for ch in s:
        if ch == "(":
            cnt+=1
        elif ch == ")":
            cnt-=1
    return not cnt


# ==================== 自测 ====================
if __name__ == "__main__":
    assert reverse("abcdef") == "fedcba"
    assert reverse("") == ""
    assert reverse("你") == "你"

    assert is_palindrome("abcba") is True
    assert is_palindrome("Never Odd or Even") is True
    assert is_palindrome("python") is False

    assert middle("abcde") == "bcd"
    assert middle("ab") == ""
    assert middle("") == ""

    assert title_case("hello  world") == "Hello World"
    assert title_case("HELLO wOrLD") == "Hello World"

    assert char_count("aAbbA") == {"a": 1, "A": 2, "b": 2}

    assert reverse_words("I love Python") == "Python love I"
    assert reverse_words("  one ") == "one"

    assert mask_phone("13812345678") == "138****5678"
    assert mask_phone("12345678901") == "123****8901"

    assert score_report("涛", [95, 88, 76]) == "涛: [95, 88, 76] 平均 86.3 最高 95 最低 76"
    assert score_report("Li", [60, 60]) == "Li: [60, 60] 平均 60.0 最高 60 最低 60"

    assert parse_query("a=1&b=2") == {"a": "1", "b": "2"}
    assert parse_query("") == {}
    assert parse_query("key=a=b") == {"key": "a=b"}

    assert balanced("(a(b)c)") is True
    assert balanced("(a))") is False
    assert balanced("(()") is False

    print("ch03 全部通过 ✓")


# region 参考答案
"""
def reverse(s):
    return s[::-1]

def is_palindrome(s):
    t = "".join(s.lower().split())
    return t == t[::-1]

def middle(s):
    return s[1:-1] if len(s) >= 3 else ""

def title_case(sentence):
    return " ".join(w.capitalize() for w in sentence.split())

def char_count(s):
    cnt = {}
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
    return cnt

def reverse_words(sentence):
    return " ".join(reversed(sentence.split()))

def mask_phone(phone):
    return f"{phone[:3]}****{phone[-4:]}"

def score_report(name, scores):
    avg = sum(scores) / len(scores)
    return f"{name}: {scores} 平均 {avg:.1f} 最高 {max(scores)} 最低 {min(scores)}"

def parse_query(qs):
    result = {}
    if not qs:
        return result
    for part in qs.split("&"):
        k, v = part.split("=", 1)
        result[k] = v
    return result

def balanced(s):
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0
"""
# endregion
