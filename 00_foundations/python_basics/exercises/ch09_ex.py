"""
ch09 练习：文件 IO 与异常
──────────────────────────────────────────────────
重点：with 语句、pathlib、json、EAFP 风格
"""

import json
import os
import tempfile
from pathlib import Path


# ---------- 1. 统计文件的行列 ----------
def file_stats(path):
    """
    返回 dict {"lines": 非空行数, "chars": 总字符数(含换行), "words": 单词总数}
    path 是 str 或 Path。必须用 with open(...)，且 encoding="utf-8"
    """
    # TODO
    return None


# ---------- 2. 写入多行 ----------
def write_lines(path, lines):
    """
    把字符串列表按行写入文件（末尾自动加换行），文件不存在要能创建。
    返回写入的行数。
    """
    # TODO
    return None


# ---------- 3. 追加日志 ----------
def append_log(path, message):
    """在文件末尾追加一行 [时间戳] message，时间戳用 time.strftime("%H:%M:%S")"""
    import time

    # TODO
    return None


# ---------- 4. EAFP 风格读取 ----------
def read_or_default(path, default=""):
    """
    尝试读取文件内容；文件不存在或读不了就返回 default。
    不要用 os.path.exists 判断，直接 try/except
    """
    # TODO
    return None


# ---------- 5. JSON 存取 ----------
def save_scores(path, scores):
    """scores 是 dict，存成 JSON 文件。中文要原样保留，不能被转成 Unicode 码位"""
    # TODO
    return None


def load_scores(path):
    """读 JSON 返回 dict；文件不存在返回空 dict"""
    # TODO
    return None


# ---------- 6. 安全的文件删除 ----------
def safe_remove(path):
    """
    删除文件，成功返回 True；
    文件不存在返回 False（不许抛异常）。
    提示：os.remove + FileNotFoundError
    """
    # TODO
    return None


# ---------- 7. 安全的 int 转换 ----------
def try_int(s, default=None):
    """
    "123" → 123；"abc" → default；None → default
    用 try/except ValueError
    """
    # TODO
    return None


# ---------- 8. 自定义异常与校验 ----------
class ValidationError(Exception):
    """数据校验失败"""
    pass


def validate_age(age):
    """
    必须是 int（bool 不算！），且在 [0, 150] 之间。
    不合规抛 ValidationError，通过则返回 True。
    """
    # TODO
    return None


# ---------- 9. CSV 简易解析 ----------
def parse_csv(text):
    """
    text 是多行文本，第一行是表头。
    返回 dict 列表：[{"列1": "值", ...}, ...]
    "name,age↲涛,19↲李,20" → [{"name":"涛","age":"19"},{"name":"李","age":"20"}]
    值保持字符串。
    """
    # TODO
    return None


# ---------- 10. 递归找文件（用 pathlib） ----------
def find_files(root, pattern):
    """
    在 root 目录下递归查找符合 glob pattern 的文件（如 "*.py"），
    返回排序后的 Path 列表。
    """
    # TODO
    return None


# ---------- 11. 词频统计（读文件版） ----------
def word_frequency(path, top_n=10):
    """
    读文本文件，返回出现频率最高的前 top_n 个单词组成的 [(word, count), ...]，
    按 count 降序。单词统一转小写。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # 准备素材
        f = root / "a.txt"
        f.write_text("hello world\n\npython is fun\n", encoding="utf-8")
        st = file_stats(f)
        assert st["lines"] == 2, st
        assert st["words"] == 5, st
        assert st["chars"] == len("hello world\n\npython is fun\n")

        out = root / "out.txt"
        assert write_lines(out, ["第一行", "second", ""]) == 3
        assert file_stats(out)["lines"] == 2

        append_log(root / "app.log", "启动成功")
        assert "启动成功" in (root / "app.log").read_text(encoding="utf-8")

        assert read_or_default(root / "不存在.txt", "兜底") == "兜底"
        assert read_or_default(f).startswith("hello world")

        sd = root / "scores.json"
        save_scores(sd, {"涛": 95, "list": [1, 2]})
        raw = sd.read_text(encoding="utf-8")
        assert "涛" in raw, "JSON 被转义成 Unicode 了，检查 ensure_ascii"
        assert load_scores(sd) == {"涛": 95, "list": [1, 2]}
        assert load_scores(root / "nope.json") == {}

        assert safe_remove(out) is True
        assert safe_remove(root / "ghost.txt") is False

        assert try_int("123") == 123
        assert try_int("abc", -1) == -1
        assert try_int(None, 0) == 0

        assert validate_age(19) is True
        assert validate_age(0) is True
        for bad in [-1, 151, "19", True, 3.5]:
            try:
                validate_age(bad)
                raise AssertionError(f"validate_age({bad!r}) 应该报错")
            except ValidationError:
                pass

        assert parse_csv("name,age\n涛,19\n李,20") == [
            {"name": "涛", "age": "19"}, {"name": "李", "age": "20"}
        ]
        assert parse_csv("a\n") == []   # 只有表头时没有数据行

        (root / "sub").mkdir()
        (root / "sub" / "x.py").write_text("", encoding="utf-8")
        (root / "y.py").write_text("", encoding="utf-8")
        (root / "z.txt").write_text("", encoding="utf-8")
        found = find_files(root, "*.py")
        assert len(found) == 2, found
        assert all(p.suffix == ".py" for p in found)

        big = root / "big.txt"
        big.write_text("apple banana apple cherry banana apple", encoding="utf-8")
        assert word_frequency(big) == [("apple", 3), ("banana", 2), ("cherry", 1)]
        assert word_frequency(big, 2) == [("apple", 3), ("banana", 2)]

    print("ch09 全部通过 ✓")


# region 参考答案
"""
def file_stats(path):
    lines = chars = words = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            chars += len(line)
            if line.strip():
                lines += 1
            words += len(line.split())
    return {"lines": lines, "chars": chars, "words": words}

def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(line + "\n")
    return len(lines)

def append_log(path, message):
    import time
    stamp = time.strftime("%H:%M:%S")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"[{stamp}] {message}\n")

def read_or_default(path, default=""):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return default

def save_scores(path, scores):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(scores, fh, ensure_ascii=False, indent=2)

def load_scores(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}

def safe_remove(path):
    try:
        os.remove(path)
        return True
    except FileNotFoundError:
        return False

def try_int(s, default=None):
    try:
        return int(s)
    except (TypeError, ValueError):
        return default

def validate_age(age):
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValidationError("年龄必须是整数")
    if not 0 <= age <= 150:
        raise ValidationError(f"年龄超出范围: {age}")
    return True

def parse_csv(text):
    rows = text.strip().splitlines()
    if not rows:
        return []
    headers = rows[0].split(",")
    result = []
    for row in rows[1:]:
        values = row.split(",")
        values += [""] * (len(headers) - len(values))
        result.append(dict(zip(headers, values)))
    return result

def find_files(root, pattern):
    return sorted(Path(root).rglob(pattern))

def word_frequency(path, top_n=10):
    counts = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            for w in line.lower().split():
                counts[w] = counts.get(w, 0) + 1
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
"""
# endregion
