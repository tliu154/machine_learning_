"""
pd02 练习：分组、合并与读写
──────────────────────────────────────────────────
重点：groupby/agg/transform、merge、CSV 往返
"""

import numpy as np
import pandas as pd


def make_df():
    return pd.DataFrame({
        "姓名": ["涛", "李", "王", "赵", "孙"],
        "组别": ["A", "B", "A", "B", "A"],
        "数学": [95, 88, 76, 60, 82],
        "英语": [88, 92, 80, 71, 90],
    })


# ---------- 1. 分组均值 ----------
def group_mean_math(df):
    """返回每个组别的数学均分（Series，index 是组别）"""
    # TODO
    return None


# ---------- 2. 多统计量 ----------
def group_stats(df):
    """
    返回 DataFrame：index 是组别，列为 "均分"、"最高"、"人数"（都针对数学列）
    """
    # TODO
    return None


# ---------- 3. transform（每行对齐所在组） ----------
def with_group_offset(df):
    """
    返回新 DataFrame，新增 "组均分" 和 "偏距" 两列：
      组均分 = 该生所在组的数学均分（每行都有，长度不变！）
      偏距   = 该生数学 - 组均分
    提示：groupby + transform("mean")
    """
    # TODO
    return None


# ---------- 4. 每组第一名 ----------
def group_top(df):
    """
    返回 DataFrame：每组数学最高的那一行（应共 2 行，A 组 1 行 + B 组 1 行）
    提示：sort_values + groupby().head(1)
    """
    # TODO
    return None


# ---------- 5. merge ----------
def merge_tables(left, right):
    """
    left 有 "姓名","数学"；right 有 "姓名","组别"。
    返回按姓名内连接（how="inner"）的结果，列顺序为 姓名/数学/组别
    """
    # TODO
    return None


# ---------- 6. concat ----------
def stack_tables(dfs):
    """把多个同列名的 DataFrame 上下拼接成一个，行号重新连续。不许改输入"""
    # TODO
    return None


# ---------- 7. CSV 往返 ----------
def save_and_load(df, path):
    """
    把 df 存到 path（CSV，不写行号），再读回来，返回读回的 DataFrame。
    要求：round-trip 之后和 df 完全相等（pd.testing.assert_frame_equal 级别）
    """
    # TODO
    return None


# ---------- 8. 分析小综合 ----------
def best_group(df):
    """
    返回总分（数学+英语）均分最高的组别名字符串。
    要求全程向量化（groupby 聚合），不许 apply。
    """
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    df = make_df()

    m = group_mean_math(df)
    assert isinstance(m, pd.Series)
    assert abs(m["A"] - (95 + 76 + 82) / 3) < 1e-9
    assert abs(m["B"] - (88 + 60) / 2) < 1e-9

    gs = group_stats(df)
    assert list(gs.columns) == ["均分", "最高", "人数"]
    assert gs.loc["A", "最高"] == 95
    assert gs.loc["B", "人数"] == 2
    assert gs.loc["A", "人数"] == 3

    wdf = with_group_offset(df)
    assert len(wdf) == len(df), "transform 必须保持行数！"
    assert abs(wdf.loc[0, "组均分"] - (95 + 76 + 82) / 3) < 1e-9
    assert wdf.loc[3, "偏距"] == 60 - 74.0
    assert wdf.loc[4, "偏距"] == 82 - 84.33333333333333

    top = group_top(df)
    assert len(top) == 2
    assert set(top["姓名"]) == {"涛", "李"}

    left = pd.DataFrame({"姓名": ["涛", "李", "王"], "数学": [95, 88, 76]})
    right = pd.DataFrame({"姓名": ["涛", "李", "赵"], "组别": ["A", "B", "C"]})
    merged = merge_tables(left, right)
    assert len(merged) == 2
    assert list(merged.columns) == ["姓名", "数学", "组别"]
    assert merged["姓名"].tolist() == ["涛", "李"]

    a = pd.DataFrame({"x": [1, 2]})
    b = pd.DataFrame({"x": [3, 4]})
    st = stack_tables([a, b])
    assert st["x"].tolist() == [1, 2, 3, 4]
    assert st.index.tolist() == [0, 1, 2, 3]

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "rt.csv"
        back = save_and_load(df, str(p))
        pd.testing.assert_frame_equal(back, df)
        raw = p.read_text(encoding="utf-8")
        assert "Unnamed" not in raw, "忘了 to_csv(index=False)？"
        assert raw.splitlines()[0].startswith("姓名")

    assert best_group(df) == "A"     # A 组总分均分 (183+156+172)/3≈170.3 > B 组 (180+131)/2=155.5

    print("pd02 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def group_mean_math(df):
    return df.groupby("组别")["数学"].mean()

def group_stats(df):
    return df.groupby("组别")["数学"].agg(均分="mean", 最高="max", 人数="count")

def with_group_offset(df):
    out = df.copy()
    out["组均分"] = out.groupby("组别")["数学"].transform("mean")
    out["偏距"] = out["数学"] - out["组均分"]
    return out

def group_top(df):
    return df.sort_values("数学", ascending=False).groupby("组别").head(1)

def merge_tables(left, right):
    merged = pd.merge(left, right, on="姓名", how="inner")
    return merged[["姓名", "数学", "组别"]]

def stack_tables(dfs):
    return pd.concat(dfs, axis=0, ignore_index=True)

def save_and_load(df, path):
    df.to_csv(path, index=False, encoding="utf-8")
    return pd.read_csv(path, encoding="utf-8")

def best_group(df):
    out = df.copy()
    out["总分"] = out["数学"] + out["英语"]
    means = out.groupby("组别")["总分"].mean()
    return means.idxmax()
"""
# endregion
