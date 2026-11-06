#course/CS #course/数据分析 #topic/Python #type/笔记 
# 附录：numpy / pandas / matplotlib 速查表

## numpy 创建

```python
np.array(lst, dtype=)
np.zeros((r,c))  np.ones((r,c))  np.full((r,c), v)  np.eye(n)
np.arange(0, 10, 2)      np.linspace(0, 1, 5)
np.zeros_like(x)  np.empty(n)
rng = np.random.default_rng(seed)
rng.integers(0,10,size)  rng.random(size)  rng.normal(mu,sigma,size)
rng.choice(arr, size, p=)  rng.shuffle(a)  rng.permutation(n)
```

## numpy 属性与变形

```python
a.shape  a.ndim  a.size  a.dtype
a.reshape(3,-1)  a.ravel()  a.T  a.astype(np.float32)
np.stack([a,b])   np.vstack   np.hstack   np.concatenate([a,b],axis=)
np.split(a, n, axis=)  a[np.ix_([0,2],[1,3])]
```

## numpy 运算

```python
a + b  a * b(逐元素)  a @ B(矩阵乘)  a ** 2  a // 2  a % 2
np.abs/sqrt/exp/log/sin/cos  np.round(a, 2)
a.sum(axis=)  a.mean(axis=)  a.max(axis=)  a.min(axis=)
a.argmax(axis=)  a.std()  a.var()  a.cumsum(axis=)
np.nansum(a)  # 跳过 NaN 的聚合
np.where(cond, x, y)  a.clip(lo, hi)
np.unique(a, return_counts=True)
np.sort(a)  a.sort()(原地)  np.argsort(a)
np.all(a > 0)  np.any(a > 0)  np.allclose(a, b)
np.linalg.inv/det/solve/eig/svd/norm  np.polyfit(x,y,deg)
np.intersect1d(a,b)  np.union1d(a,b)
```

## numpy 索引

```python
a[i, j]  a[行, :]  a[:, 列]  a[起:止, 起:止]     # 切片=视图
a[[1, 3, 5]]                                        # 花式=拷贝
a[布尔掩码]  a[(a>0) & (a<5)]  a[a<0] = 0           # 掩码
np.where(a == x)  np.nonzero(a)
```

## 图像速查（uint8, (H, W, C)，BGR）

```python
gray = (color @ np.array([0.114, 0.587, 0.299])).astype(np.uint8)
roi = img[y1:y2, x1:x2]
flip_h = img[:, ::-1]  flip_v = img[::-1, :]
binary = np.where(gray > 127, 255, 0).astype(np.uint8)
bright = np.clip(img.astype(np.int16) + 50, 0, 255).astype(np.uint8)
small = img[::2, ::2]
norm  = img.astype(np.float32) / 255.0
r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
```

## pandas 核心

```python
pd.Series(data, index=)  pd.DataFrame(dict)
df.head()  df.tail()  df.info()  df.describe()  df.shape  df.dtypes
df["列"]  df[["列1","列2"]]
df.loc[行标签, 列标签]     # 切片含端点
df.iloc[行号, 列号]        # 切片不含端点
df[df.数学 > 80]  df[(df.a>1) & (df.b<2)]  df.query("a > 1")
df[df.列.isin([...])]  df[~cond]
df["新列"] = df.a + df.b
np.where(cond, x, y) / np.select(conds, choices, default)
df.drop(columns=[])  df.drop(index=[])  df.rename(columns={})
df.dropna()  df.dropna(subset=["a"])  df.fillna(0)  df.ffill()
df.isna().sum()
df.sort_values("列", ascending=False)  df.sort_values(["a","b"], ascending=[True,False])
df.nlargest(n, "列")  df.nsmallest(n, "列")
df["列"].unique()  df["列"].value_counts()  df.drop_duplicates()
s.str.strip/lower/contains/split/replace/len
```

## pandas 分组/合并/IO

```python
df.groupby("组")["列"].mean()
df.groupby("组")["列"].agg(["mean","max","count"])
df.groupby("组").agg(新名=("列","mean"))
df.groupby("组")["列"].transform("mean")     # 等长对齐
df.groupby("组").apply(f)
pd.merge(l, r, on="键", how="inner/left/outer")
pd.concat([a, b], axis=0, ignore_index=True)
df1.join(df2)                                # 按索引连
pd.read_csv(f, encoding=, index_col=, parse_dates=)
df.to_csv(f, index=False, encoding=)
pd.read_excel(f, sheet_name=)  df.to_excel(f, index=False)
pd.to_datetime([...])  s.resample("ME").mean()  s.rolling(n).mean()
s.diff()  s.shift(1)  s.pct_change()
```

## matplotlib

```python
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, y, label=, color=, linestyle=, marker=, alpha=)
ax.scatter(x, y, s=, c=, cmap=)
ax.bar(labels, values, width=)
ax.hist(data, bins=)
ax.set_title/xlabel/ylabel/xlim/ylim(...)
ax.legend()  ax.grid(True)  ax.axhline(y)  ax.axvline(x)
fig, axes = plt.subplots(2, 2)   axes[0,0].plot(...)
fig.tight_layout()  fig.suptitle("总标题")
fig.savefig("f.png", dpi=150, bbox_inches="tight")
df.plot()  df.plot.bar(x=, y=)  df.plot.scatter(x=, y=)  df["列"].plot(kind="hist")
matplotlib.use("Agg")   # 无头
```

## 高频坑清单

1. numpy 切片是**视图**，改了会动原数组 → 要独立就 `.copy()`
2. `A * B` 是逐元素，矩阵乘是 `A @ B`
3. 布尔组合用 `&` `|` `~` 且**必须加括号**（numpy 和 pandas 都是）
4. `uint8` 算术静默回绕 → 先 `astype` 升位再 `clip`
5. `(n,)` `(n,1)` `(1,n)` 不等价，广播行为完全不同
6. 图像下标是 `[y, x]`（行=高在前），和数学坐标相反
7. `df.loc` 切片**含端点**，`df.iloc` 不含 —— 混用必错
8. `NaN` 的一切比较都是 False → 用 `isna()` / `np.isnan`
9. `to_csv(index=False)` 不写就会多出 `Unnamed: 0` 列
10. matplotlib 中文乱码：`font.sans-serif` + `unicode_minus=False`
11. `savefig` 必须在 `show` **之前**（show 会清空画布）
12. `iterrows()` / `apply(axis=1)` 是性能杀手，能用向量化就用
13. 浮点比较一律 `np.allclose`，别 `==`
