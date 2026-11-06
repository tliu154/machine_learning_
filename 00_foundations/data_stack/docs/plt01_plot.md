#course/CS #course/数据分析 #topic/Python #type/笔记 
# plt01 matplotlib 绘图

```python
import matplotlib.pyplot as plt      # 约定俗成：plt
import numpy as np
```

## 1.1 最小可用例子

```python
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)                # 画线
plt.xlabel("x")               # 轴标签
plt.ylabel("sin(x)")
plt.title("正弦曲线")
plt.legend()                  # 图例（需要先给 label）
plt.savefig("sin.png", dpi=150)   # 保存图片
plt.show()                    # 弹窗显示（脚本最后一行）
```

完整模板（背下来）：

```python
plt.plot(x, y, label="sin")
plt.plot(x, np.cos(x), label="cos", linestyle="--", color="r")
plt.xlabel("x"); plt.ylabel("y")
plt.title("两条曲线")
plt.legend()
plt.grid(True)
plt.savefig("fig.png", dpi=150, bbox_inches="tight")
plt.show()
```

常用参数（不用背，混个脸熟）：

```python
plt.plot(x, y,
    color="r"/"#1f77b4"/"C0",      # 颜色
    linestyle="-"/"--"/":"/"-.",   # 线型
    linewidth=2,                   # 线宽
    marker="o"/"s"/"^",            # 数据点标记
    markersize=5,
    alpha=0.7,                     # 透明度
    label="名称")                   # 配合 legend()
```

## 1.2 中文乱码 —— Windows 上必踩的坑

默认字体不含中文，标签会变成一堆方块。开头三行（Windows）：

```python
plt.rcParams["font.sans-serif"] = ["SimHei"]      # 黑体，Windows 自带
plt.rcParams["axes.unicode_minus"] = False        # 修负号显示（被中文字体搞坏）
```

macOS 用 `"Arial Unicode MS"`，Linux 装 Noto 后用 `["Noto Sans CJK SC"]`。
一次设置，整个脚本生效。

## 1.3 四种最常用的图

```python
# 折线：趋势、时间序列
plt.plot(x, y)

# 散点：两变量关系、点云、目标位置
plt.scatter(x, y, s=20, c=values, cmap="viridis", alpha=0.6)
#   s=点大小  c=每点颜色（可传数组按值着色）  cmap=色图

# 柱状：分类对比（分组柱状：x 偏移）
groups = ["A", "B", "C"]
plt.bar(groups, [3, 5, 2])
plt.bar([i + 0.35 for i in range(3)], [2, 4, 6], width=0.35)   # 并排第二组

# 直方图：分布
plt.hist(data, bins=30, edgecolor="black")     # bins 控制分箱数
```

选择口诀：**趋势用线、关系用散点、对比用柱、分布用直方**。

## 1.4 subplots：一张图里画多张

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))    # 2×2 网格

axes[0, 0].plot(x, np.sin(x))          # 每个小图是一个 Axes 对象
axes[0, 1].plot(x, np.cos(x))
axes[1, 0].scatter(rng.random(100), rng.random(100))
axes[1, 1].hist(rng.normal(0, 1, 1000), bins=30)

axes[0, 0].set_title("sin")            # 注意是 set_title 不是 title！
axes[0, 0].set_xlabel("x")

fig.suptitle("四合一")                 # 总标题
fig.tight_layout()                     # 自动防重叠
fig.savefig("grid.png", dpi=150)
```

## 1.5 两套 API 的区分（看懂老代码用）

```python
# 面向过程（ pyplot 状态机） —— 快速草图
plt.plot(...); plt.title(...)

# 面向对象（ Figure / Axes 对象） —— 正经代码、多图、复用
fig, ax = plt.subplots()
ax.plot(...)
ax.set_title(...)
```

**推荐一律写面向对象版**：

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, label="sin")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("标题")
ax.legend(); ax.grid(True)
fig.savefig("oo.png", dpi=150)
```

| pyplot 版 | 对象版 |
|---|---|
| `plt.title()` | `ax.set_title()` |
| `plt.xlabel()` | `ax.set_xlabel()` |
| `plt.xlim(0, 10)` | `ax.set_xlim(0, 10)` |
| `plt.legend()` | `ax.legend()` |

pyplot 版本质是"操作当前那张图"，一旦多图并发就会乱；
对象版每个 `ax` 自己管自己 —— 和全局变量 vs 局部变量的区别一个道理。

## 1.6 和 pandas 无缝配合

DataFrame/Series 直接画：

```python
df.plot()                        # 折线（数值列全画）
df["数学"].plot(kind="hist")      # kind= line/bar/hist/box/scatter
df.plot.scatter(x="数学", y="英语")
df.plot.bar(x="姓名", y="数学")

result = df.groupby("组别")["数学"].mean()
result.plot.bar(title="各组均分")    # 分析完直接出图 —— 面试/汇报常用套路
```

`df.plot` 返回的就是 matplotlib 的 Axes，后面照样 `ax.set_title(...)`。

## 1.7 脚本/笔记本环境差异

```python
# PyCharm / .py 脚本：最后 plt.show() 弹窗；之前可以 savefig
# plt.savefig 必须写在 show 之前（show 会清空画布！）

# 没有屏幕的环境（自动化、服务器）：
import matplotlib
matplotlib.use("Agg")            # 无头后端，只 savefig 不弹窗
import matplotlib.pyplot as plt
```

练习文件里就用 Agg + savefig —— 不弹窗、可断言（检查文件存在、检查数据正确）。

## 1.8 常用细节

```python
ax.set_xlim(0, 10); ax.set_ylim(-1.5, 1.5)   # 手动轴范围
ax.axhline(0, color="gray", linestyle=":")   # 水平参考线
ax.axvline(5)                                # 垂直参考线
plt.figure(figsize=(10, 6))                  # 画布大小（英寸）
ax.annotate("峰值", xy=(xmax, ymax), xytext=(xmax, ymax+0.2))
plt.style.use("ggplot")                      # 一行换风格（还有 "seaborn-v0_8"）
```

---

### 小结

| 需求 | 一句话 |
|---|---|
| 最小模板 | plot → xlabel/ylabel → legend → savefig → show |
| 中文 | 开头设 `font.sans-serif` + `unicode_minus=False` |
| 图选型 | 趋势线 / 关系散点 / 对比柱 / 分布直方 |
| 多图 | `fig, axes = plt.subplots(行, 列)` |
| 正经写法 | 面向对象：`ax.set_xxx` |
| pandas 直连 | `df.plot(...)` |

教程完 → [附录速查表](appendix_cheatsheet.md) / [练习目录](../exercises/)
