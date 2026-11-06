"""
plt01 练习：matplotlib 绘图
──────────────────────────────────────────────────
用 Agg 无头后端：只保存文件不弹窗，assert 检查图的数据和文件本身。
PyCharm 里跑完去输出目录看 PNG。
"""

import matplotlib

matplotlib.use("Agg")           # 必须在 import pyplot 之前！

import matplotlib.pyplot as plt
import numpy as np

# 中文支持（Windows：黑体）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


# ---------- 1. 折线图 ----------
def plot_line(x, y, title="", xlabel="", ylabel=""):
    """
    画 x/y 折线，设置标题和轴标签，返回 ax（Axes 对象）。
    要求：label="数据"，并开启图例和网格。
    """
    fig, ax = plt.subplots()
    # TODO
    return ax


# ---------- 2. 双曲线 ----------
def plot_two(x, y1, y2):
    """
    同一张图里画两条曲线，label 分别为 "A"（实线）和 "B"（虚线）。
    返回 ax。要求 ax 上有 2 条线且带图例。
    """
    fig, ax = plt.subplots()
    # TODO
    return ax


# ---------- 3. 散点图 ----------
def plot_scatter(xs, ys, values):
    """
    画散点：xs/ys 定位，values 决定每点颜色（c=values）。
    返回 ax。
    """
    fig, ax = plt.subplots()
    # TODO
    return ax


# ---------- 4. 柱状图 ----------
def plot_bar(labels, values, title=""):
    """画柱状图 + 标题。返回 ax。"""
    fig, ax = plt.subplots()
    # TODO
    return ax


# ---------- 5. 直方图 ----------
def plot_hist(data, bins=30):
    """画直方图。返回 ax。"""
    fig, ax = plt.subplots()
    # TODO
    return ax


# ---------- 6. 子图网格 ----------
def plot_grid(x):
    """
    2×2 子图：左上 plot(x)，右上 plot(x**2)，
    左下 scatter(x, x)，右下 hist(x, bins=10)。
    每个子图 set_title 分别为 "原始"、"平方"、"散点"、"分布"。
    返回 axes（2×2 数组）。
    """
    fig, axes = plt.subplots(2, 2)
    # TODO
    return axes


# ---------- 7. 保存 ----------
def save_figure(fig, path, dpi=150):
    """把 fig 存成 PNG。返回 path。"""
    # TODO
    return None


# ---------- 8. pandas 联动 ----------
def plot_df_column(df, column, title=""):
    """
    用 matplotlib（面向对象 API）画 df[column] 的折线：x 用 df.index。
    返回 ax。
    """
    fig, ax = plt.subplots()
    # TODO
    return ax


# ==================== 自测 ====================
if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    ax = plot_line(x, y, title="正弦", xlabel="x", ylabel="sin(x)")
    assert ax.get_title() == "正弦"
    assert ax.get_xlabel() == "x" and ax.get_ylabel() == "sin(x)"
    assert len(ax.lines) == 1
    assert np.allclose(ax.lines[0].get_xdata(), x)
    assert np.allclose(ax.lines[0].get_ydata(), y)
    assert ax.get_legend() is not None, "忘了 legend()"

    ax2 = plot_two(x, np.sin(x), np.cos(x))
    assert len(ax2.lines) == 2
    assert ax2.lines[0].get_label() == "A"
    assert ax2.lines[1].get_linestyle() == "--", "B 线应为虚线"

    xs, ys = np.random.default_rng(1).random(50), np.random.default_rng(2).random(50)
    vals = xs + ys
    ax3 = plot_scatter(xs, ys, vals)
    coll = ax3.collections[0]
    assert np.allclose(coll.get_offsets().ravel()[::2], xs), "散点位置不对"

    ax4 = plot_bar(["A", "B", "C"], [3, 5, 2], title="对比")
    assert ax4.get_title() == "对比"
    heights = [p.get_height() for p in ax4.patches]
    assert heights == [3, 5, 2]

    data = np.random.default_rng(3).normal(0, 1, 500)
    ax5 = plot_hist(data, bins=20)
    counts = [p.get_height() for p in ax5.patches]
    assert sum(counts) == 500

    axes = plot_grid(x)
    assert axes.shape == (2, 2)
    assert axes[0, 0].get_title() == "原始"
    assert axes[0, 1].get_title() == "平方"
    assert axes[1, 1].get_title() == "分布"
    assert len(axes[0, 1].lines[0].get_ydata()) == 50
    assert np.allclose(axes[0, 1].lines[0].get_ydata(), x ** 2)

    with tempfile.TemporaryDirectory() as tmp:
        p = str(Path(tmp) / "fig.png")
        fig = ax.figure
        result = save_figure(fig, p)
        assert result == p
        assert Path(p).exists() and Path(p).stat().st_size > 0, "图没存上"

    import pandas as pd

    df = pd.DataFrame({"温度": [20, 22, 25, 23, 21]}, index=pd.date_range("2026-10-01", periods=5))
    ax6 = plot_df_column(df, "温度", title="温度曲线")
    assert ax6.get_title() == "温度曲线"
    assert np.allclose(ax6.lines[0].get_ydata(), [20, 22, 25, 23, 21])
    assert len(ax6.lines[0].get_xdata()) == 5

    # 防止上百个图对象堆积
    plt.close("all")

    print("plt01 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看 ↓↓↓
"""
def plot_line(x, y, title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots()
    ax.plot(x, y, label="数据")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    return ax

def plot_two(x, y1, y2):
    fig, ax = plt.subplots()
    ax.plot(x, y1, label="A")
    ax.plot(x, y2, "--", label="B")
    ax.legend()
    return ax

def plot_scatter(xs, ys, values):
    fig, ax = plt.subplots()
    ax.scatter(xs, ys, c=values)
    return ax

def plot_bar(labels, values, title=""):
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title(title)
    return ax

def plot_hist(data, bins=30):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    return ax

def plot_grid(x):
    fig, axes = plt.subplots(2, 2)
    axes[0, 0].plot(x)
    axes[0, 0].set_title("原始")
    axes[0, 1].plot(x ** 2)
    axes[0, 1].set_title("平方")
    axes[1, 0].scatter(x, x)
    axes[1, 0].set_title("散点")
    axes[1, 1].hist(x, bins=10)
    axes[1, 1].set_title("分布")
    return axes

def save_figure(fig, path, dpi=150):
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path

def plot_df_column(df, column, title=""):
    fig, ax = plt.subplots()
    ax.plot(df.index, df[column])
    ax.set_title(title)
    return ax
"""
# endregion
