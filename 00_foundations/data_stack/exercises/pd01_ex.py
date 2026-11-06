"""
pd01 练习：Series 与 DataFrame
──────────────────────────────────────────────────
重点：loc/iloc 的端点差异、布尔过滤、向量化新列、缺失值
"""

import numpy as np
import pandas as pd


def make_df():
    """构造并返回标准测试表（练习全程复用）"""
    return pd.DataFrame({
        "姓名": ["涛", "李", "王", "赵", "孙"],
        "组别": ["A", "B", "A", "B", "A"],
        "数学": [95, 88, 76, 60, 82],
        "英语": [88, 92, 80, 71, 90],
    })


# ---------- 1. 基础选择 ----------
def get_math(df):
    """返回数学列（Series）"""
    # TODO
    return None


def pass_students(df, threshold=80):
    """返回数学 >= threshold 的所有行（DataFrame）"""
    # TODO
    return None


def a_group_math(df):
    """返回 A 组学生的数学列（用布尔过滤选行 + 选列）"""
    # TODO
    return None


# ---------- 2. loc / iloc（注意端点差异！） ----------
def loc_slice(df, lo, hi):
    """df.loc[lo:hi] 的结果（切片【含】端点）"""
    # TODO
    return None


def iloc_slice(df, lo, hi):
    """df.iloc[lo:hi] 的结果（切片【不】含端点）"""
    # TODO
    return None


# ---------- 3. 向量化新列 ----------
def with_total(df):
    """返回新 DataFrame，新增"总分" = 数学 + 英语（不许用 apply/循环）"""
    # TODO
    return None


def with_grade(df):
    """
    返回新 DataFrame，新增"等级"列：
      总分 >= 180 → "优"；>= 150 → "良"；>= 120 → "及格"；否则 "不及格"
    提示：np.select
    """
    # TODO
    return None


# ---------- 4. 排序 ----------
def top_students(df, n):
    """返回总分最高的 n 行（先加总分再排），姓名顺序无关，按总分降序核对"""
    # TODO
    return None


# ---------- 5. 缺失值 ----------
def na_report(df):
    """返回每列缺失值个数（Series，index 是列名）"""
    # TODO
    return None


def fill_with_mean(s):
    """返回新 Series：NaN 用该列均值填。非 NaN 的值保持不变"""
    # TODO
    return None


# ---------- 6. 计数与去重 ----------
def group_counts(df):
    """返回每个组别人数的 Series（index 是组别，按数量降序）"""
    # TODO
    return None


# ---------- 7. 字符串列 ----------
def clean_names(names):
    """
    names 是带脏数据的 Series（多余空格、大小写混乱）。
    返回清理后的 Series：strip + 首字母大写其余小写。
    提示：.str.strip().str.title()
    """
    # TODO
    return None


# ---------- 8. 重编码 ----------
def encode_group(df):
    """返回新 DataFrame，新增 "组编号" 列：A→1, B→2（用 map + 字典）"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    df = make_df()

    assert get_math(df).tolist() == [95, 88, 76, 60, 82]

    assert len(pass_students(df)) == 3
    assert pass_students(df, 60)["姓名"].tolist() == ["涛", "李", "王", "赵", "孙"], \
        "注意 >= 是含边界的，赵的数学恰好 60"

    assert a_group_math(df).tolist() == [95, 76, 82]

    # loc 含端点 / iloc 不含端点 —— 两行结果必须差一行
    assert len(loc_slice(df, 0, 2)) == 3
    assert len(iloc_slice(df, 0, 2)) == 2
    assert loc_slice(df, 1, 3).index.tolist() == [1, 2, 3]

    wdf = with_total(df)
    assert "总分" in wdf.columns
    assert wdf["总分"].tolist() == [183, 180, 156, 131, 172]
    assert "总分" not in df.columns, "不应该修改原表"

    gdf = with_grade(make_df())
    assert gdf["等级"].tolist() == ["优", "优", "良", "及格", "良"]

    top = top_students(make_df(), 2)
    assert top["总分"].tolist() == [183, 180]
    assert set(top["姓名"]) == {"涛", "李"}

    assert na_report(make_df()).sum() == 0
    s = pd.Series([1.0, np.nan, 3.0])
    filled = fill_with_mean(s)
    assert filled.isna().sum() == 0
    assert abs(filled[1] - 2.0) < 1e-9
    assert filled[0] == 1.0 and filled[2] == 3.0

    gc = group_counts(make_df())
    assert gc.index.tolist()[0] == "A" and gc.iloc[0] == 3

    dirty = pd.Series(["  tao LI ", "wang", "  ZHao "])
    assert clean_names(dirty).tolist() == ["Tao Li", "Wang", "Zhao"]

    edf = encode_group(make_df())
    assert edf["组编号"].tolist() == [1, 2, 1, 2, 1]

    print("pd01 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def get_math(df):
    return df["数学"]

def pass_students(df, threshold=80):
    return df[df["数学"] >= threshold]

def a_group_math(df):
    return df.loc[df["组别"] == "A", "数学"]

def loc_slice(df, lo, hi):
    return df.loc[lo:hi]

def iloc_slice(df, lo, hi):
    return df.iloc[lo:hi]

def with_total(df):
    out = df.copy()
    out["总分"] = out["数学"] + out["英语"]
    return out

def with_grade(df):
    out = df.copy()
    total = out["数学"] + out["英语"]
    out["等级"] = np.select(
        [total >= 180, total >= 150, total >= 120],
        ["优", "良", "及格"],
        default="不及格",
    )
    return out

def top_students(df, n):
    out = df.copy()
    out["总分"] = out["数学"] + out["英语"]
    return out.nlargest(n, "总分")

def na_report(df):
    return df.isna().sum()

def fill_with_mean(s):
    return s.fillna(s.mean())

def group_counts(df):
    return df["组别"].value_counts()      # value_counts 默认降序

def clean_names(names):
    return names.str.strip().str.title()

def encode_group(df):
    out = df.copy()
    out["组编号"] = out["组别"].map({"A": 1, "B": 2})
    return out
"""
# endregion
