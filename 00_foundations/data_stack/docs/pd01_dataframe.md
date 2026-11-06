#course/CS #course/数据分析 #topic/Python #type/笔记 
# pd01 Series 与 DataFrame：表格数据

> pandas 建立在 numpy 之上：DataFrame 的每一列就是一个 ndarray（外加一个索引）。
> 你学过的 numpy 知识全部有效。

```python
import pandas as pd
import numpy as np
```

## 1.1 两个核心对象

**Series = 一维数组 + 索引**（想象带标签的 ndarray）：

```python
s = pd.Series([95, 88, 76], index=["涛", "李", "王"], name="成绩")
s
# 涛    95
# 李    88
# 王    76
# Name: 成绩, dtype: int64

s["涛"]          # 95    按标签取
s.iloc[0]        # 95    按位置取
s.values         # array([95, 88, 76])   ← 底层就是 ndarray
s.index          # Index(['涛', '李', '王'])
s.mean()         # 86.333  numpy 的方法全能用
```

**DataFrame = 多列共享同一个索引的表格**（想象 dict of Series / Excel 表）：

```python
df = pd.DataFrame({
    "姓名": ["涛", "李", "王", "赵"],
    "数学": [95, 88, 76, 60],
    "英语": [88, 92, 80, 71],
    "组别": ["A", "B", "A", "B"],
})
df
#   姓名  数学  英语 组别
# 0  涛   95   88   A
# 1  李   88   92   B
# 2  王   76   80   A
# 3  赵   60   71   B

df.shape        # (4, 4)
df.columns      # 列名
df.index        # RangeIndex(0..3)
df.dtypes       # 每列类型（一列一个 dtype —— 底层就是 ndarray！）
df.head(2) / df.tail(2)     # 看前/后几行
df.info()       # 总览：行数、列类型、非空数（print 调试第一步）
df.describe()   # 数值列的统计摘要（count/mean/std/min/25%/50%/75%/max）
```

> `DataFrame` ≈ 二维结构里"列优先"的世界：**每一列类型固定**（和 numpy 一致），
> 行可以异构。这一点和"每行一个记录"的直觉刚好相反，记住：**列是基本单位**。

## 1.2 选择数据：loc / iloc —— 90% 的日常操作

```python
df["数学"]              # 取一列 → Series（最常用；df.数学 也行但列名带空格就废）
df[["数学", "英语"]]     # 取多列 → DataFrame（注意双层中括号）

# loc = 按标签（索引名、列名）
df.loc[0, "数学"]          # 第 0 行的数学
df.loc[0:2, ["姓名", "数学"]]   # 切片是【闭区间】！0,1,2 行 —— 和 numpy/python 不同！
df.loc[df["数学"] > 80, "姓名"]  # 行用布尔条件，列选名字

# iloc = 按位置（纯下标，规则和 numpy 完全一样）
df.iloc[0, 1]              # 第 0 行第 1 列
df.iloc[0:2, 0:2]          # 左闭右开（这里又是 Python 规则了！）
df.iloc[-1]                # 最后一行

# 行直接切 df[0:2] 也行（左闭右开），但列不行 —— 别依赖这个，统一用 loc/iloc
```

> ⚠️ 最容易混的点：**`loc` 的切片含端点，`iloc` 的切片不含**。
> ```python
> df.loc[0:2]    # 0,1,2 三行
> df.iloc[0:2]   # 0,1 两行
> ```

## 1.3 布尔过滤 —— 和 numpy 掩码同款

```python
df[df["数学"] > 80]                          # 数学 > 80 的行
df[(df["数学"] > 80) & (df["英语"] > 80)]     # 且（括号必须加！）
df[df["组别"] == "A"]
df[df["姓名"].isin(["涛", "王"])]
df[~(df["组别"] == "B")]                     # 取反

df.query("数学 > 80 and 英语 > 80")           # 字符串表达式版，长条件时更顺眼
```

## 1.4 新增/修改/删除列

```python
df["总分"] = df["数学"] + df["英语"]              # 向量化！整列直接算，无循环
df["平均"] = (df["数学"] + df["英语"]) / 2
df["是否及格"] = df["数学"] >= 60

# 按条件生成新列（np.where 三元）
df["等级"] = np.where(df["平均"] >= 85, "优", "良")

# 多分支：np.select
df["评价"] = np.select(
    [df["平均"] >= 90, df["平均"] >= 80, df["平均"] >= 60],
    ["优秀", "良好", "及格"],
    default="不及格",
)

df = df.drop(columns=["是否及格"])                # 删列（返回新表）
df.rename(columns={"数学": "math"}, inplace=False)   # 改列名
df.drop(index=[3])                               # 删行
```

> 新列的值来自"整列运算"，这就是 numpy 向量化在表格上的直接延伸。
> **看到 `df.iterrows()` 先停一下** —— 十有八九是错的写法（慢 100 倍）。

## 1.5 缺失值 NaN —— 逃不掉的一课

真实数据一定有缺失（Excel 空格、传感器丢帧），pandas 用 `NaN` 表示：

```python
df = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, np.nan]})

df.isna()               # 哪里是缺失（布尔表）
df.isna().sum()         # 每列缺多少 —— 检查数据质量第一步
df.dropna()             # 删掉含缺失的行
df.dropna(subset=["a"]) # 只看 a 列的缺失
df.fillna(0)            # 填 0
df["a"].fillna(df["a"].mean())    # 填均值（数据清洗常见动作）
df.ffill()              # 用上一行填（时间序列常用）
```

> ⚠️ **NaN 参与比较永远是 False**：`nan > 0` 是 False，`nan == nan` 也是 False。
> 判断缺失只能 `isna()`，别用 `== np.nan`。
> numpy 侧对应的是 `np.isnan(a)`（只对 float 有效）。

## 1.6 排序与去重

```python
df.sort_values("数学", ascending=False)                # 按列排序
df.sort_values(["组别", "数学"], ascending=[True, False])   # 多键排序
df.sort_index()                                        # 按索引排
df.nlargest(2, "数学")                                 # 数学最高的 2 行
df.nsmallest(2, "数学")

df.drop_duplicates()                       # 整行去重
df["姓名"].unique()                        # 去重后的值
df["组别"].value_counts()                  # 每个值出现次数 —— 超常用！
df["组别"].value_counts(normalize=True)    # 归一化成比例
```

`value_counts()` 是你将来用得最多的方法之一，一行顶 `Counter`。

## 1.7 Series 的字符串列

```python
names = pd.Series(["涛 Tao", "  Li ", "WANG"])

names.str.strip()               # 每个元素 strip —— 前面说过没有 s.length()，这里是
names.str.lower()
names.str.contains("a", case=False)
names.str.split(" ")
names.str.replace(" ", "_")     # 注意是 .str.replace 不是 .replace（行为不同）
names.str.len()
names.str[0]                    # 每个字符串的第一个字符
```

`.str.xxx` 会把方法广播到每个元素，写起来比列表推导式舒服得多。

---

### 小结

| 想做的事 | 写法 |
|---|---|
| 取一列 | `df["列名"]` → Series |
| 按标签选行列 | `df.loc[行, 列]`（切片**含端点**） |
| 按位置选 | `df.iloc[行, 列]`（切片不含端点） |
| 条件过滤 | `df[(df.a > 1) & (df.b < 2)]` |
| 新列 = 整列运算 | `df["新列"] = df.a + df.b`（向量化） |
| 三元/多分支新列 | `np.where` / `np.select` |
| 缺失值 | `isna().sum()` → `dropna()/fillna()` |
| 计数 | `value_counts()` |

下一章：[pd02 分组、合并与读写](pd02_groupby.md)
