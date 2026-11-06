#course/CS #course/数据分析 #topic/Python #type/笔记 
# pd02 分组、合并与读写

## 2.1 groupby：拆-算-合

SQL 的 `GROUP BY`、Excel 的数据透视表，pandas 一行搞定：

```python
df = pd.DataFrame({
    "组别": ["A", "B", "A", "B", "A"],
    "姓名": ["涛", "李", "王", "赵", "孙"],
    "数学": [95, 88, 76, 60, 82],
    "英语": [88, 92, 80, 71, 90],
})

df.groupby("组别")["数学"].mean()
# 组别
# A    84.333333
# B    74.000000

df.groupby("组别")["数学"].agg(["mean", "max", "min", "count"])
#        mean  max  min  count
# 组别
# A   84.333   95   76      3
# B   74.000   88   60      2

df.groupby("组别").agg(
    数学均分=("数学", "mean"),
    英语最高=("英语", "max"),
    人数=("姓名", "count"),          # 命名聚合：列名可读性拉满
)

# 多列分组 → 多级索引（结果长这样）
df.groupby(["组别"])["数学"].mean()
df.groupby(["组别", "是否"]).mean()   # 演示用
```

心法：**groupby 永远是"分组键 + 聚合函数"成对出现**。
`groupby(x)` 单独出现只是个惰性对象，必须跟 `mean()/agg()/apply()` 才会计算 ——
和生成器一个脾气（ch08）。

```python
# 每组的 Top1：sort + groupby 的经典组合
df.sort_values("数学", ascending=False).groupby("组别").head(1)

# transform：结果和原表等长（不是每组一行！）
df["组均分"] = df.groupby("组别")["数学"].transform("mean")
df["偏离组均"] = df["数学"] - df["组均分"]
# 加班费/偏差/标准化一类的"每行算相对所在组的值"都靠 transform
```

`agg` vs `transform` 一图流：

```
agg：       N 组 → N 行       （压扁）
transform： N 行 → N 行       （对齐回去广播）
```

## 2.2 merge：表的连接

```python
scores = pd.DataFrame({"姓名": ["涛", "李", "王"], "数学": [95, 88, 76]})
info   = pd.DataFrame({"姓名": ["涛", "李", "赵"], "组别": ["A", "B", "C"]})

pd.merge(scores, info, on="姓名")                # 内连接：两边都有的
pd.merge(scores, info, on="姓名", how="left")    # 保左表
pd.merge(scores, info, on="姓名", how="outer")   # 全保留
pd.merge(scores, info, on="姓名", how="inner")   # 默认
```

| how | 效果 |
|---|---|
| `inner` | 交集（默认） |
| `left` | 保左表全部行 |
| `outer` | 并集，缺的填 NaN |

> `on` 的列名不同时：`left_on="姓名", right_on="name"`。
> 这就是 SQL 的 JOIN，一模一样。

拼接（不按键，纯堆叠）：

```python
pd.concat([df1, df2], axis=0, ignore_index=True)    # 上下摞（加行）
pd.concat([df1, df2], axis=1)                       # 左右拼（加列）
```

## 2.3 读写文件

```python
df = pd.read_csv("scores.csv", encoding="utf-8")
df = pd.read_csv("scores.csv", encoding="utf-8",
                 index_col=0,           # 第 0 列当索引
                 parse_dates=["日期"])   # 指定日期列
df.to_csv("out.csv", index=False, encoding="utf-8")   # index=False 别把行号写进文件

# 读的时候常见坑：
# Windows 下中文 CSV 如果乱码，试 encoding="gbk" 或 "utf-8-sig"
pd.read_excel("data.xlsx", sheet_name="Sheet1")      # 需要 openpyxl
df.to_excel("out.xlsx", index=False)

# 别忘了你还有纯 Python 的 json（ch09）：
pd.read_json("data.json")
```

> **`to_csv(index=False)` 必写**，否则每次读写都多出一列 `Unnamed: 0`。

## 2.4 apply：最后手段

```python
# 对整列逐元素用函数
df["数学"].apply(lambda x: x * 2)

# 对每行用函数（axis=1）—— 慢！能向量化就别用
def grade(row):
    return "优" if row["数学"] + row["英语"] >= 180 else "良"
df["评价"] = df.apply(grade, axis=1)

# 更快的逐元素版：map
df["数学"].map(lambda x: x * 2)     # Series 专用
df["等级"] = df["数学"].map({95: "A", 88: "B"})   # 还能做字典映射（重编码）
```

**优先级**：向量化（整列运算/np.where）> `np.select` > `map` > `apply`。
`apply` 是给"实在没有向量化写法"的复杂逻辑兜底的，**每写一次 apply 都应该问问自己能不能不写**。

## 2.5 日期处理（时序数据必背）

```python
dates = pd.to_datetime(["2026-10-01", "2026-10-02"])
s = pd.Series([10, 20], index=dates)

s.index.year / s.index.month / s.index.day / s.index.dayofweek   # 0=周一
s.resample("ME").mean()          # 按月重采样聚合（老版本是 "M"）
s.rolling(2).mean()              # 滑动窗口均值（MA 均线的本质）
s.diff()                         # 一阶差分
s.shift(1)                       # 整体后移一格（做"对比昨天"类特征）
s.pct_change()                   # 变化率
```

## 2.6 30 秒真实工作流

```python
df = pd.read_csv("scores.csv")                   # 1. 读
df.info(); df.isna().sum()                       # 2. 体检
df = df.dropna(subset=["数学"])                   # 3. 清洗
df["总分"] = df["数学"] + df["英语"]               # 4. 派生列
result = df.groupby("组别")["总分"].agg(["mean", "max"])   # 5. 分析
result.to_csv("组别统计.csv")                      # 6. 落盘
```

读 → 体检 → 清洗 → 派生 → 分组聚合 → 写。所有 pandas 工作都是这六步的变体。

---

### 小结

| 想做的事 | 写法 |
|---|---|
| 分组聚合 | `df.groupby("组")["列"].mean()` / `.agg([...])` |
| 每行对齐所在组 | `groupby(...)["列"].transform("mean")` |
| 连接两表 | `pd.merge(left, right, on=..., how=...)` |
| 上下摞行 | `pd.concat([...], ignore_index=True)` |
| 读/写 CSV | `read_csv` / `to_csv(index=False)` |
| 逐行函数 | `apply(f, axis=1)` —— 最好别用 |
| 日期 | `to_datetime` → `resample` / `rolling` |

下一章：[plt01 matplotlib 绘图](plt01_plot.md)
