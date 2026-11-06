"""
chNN 练习：<章节标题（English）>
──────────────────────────────────────────────────
重点：<一两条本章核心考点>
把每个 TODO 补完，右键 Run；底部 assert 全过就过关。
对应章节：docs/chNN_<短名>.md
"""

# import numpy as np


# ---------- 第 1 题：<对应概念 / 锚点 cNN-01> ----------
def task_one(x):
    """<一句话需求，包含边界行为的约定>"""
    # TODO
    return None


# ---------- 第 2 题：<对应概念 / 锚点 cNN-02> ----------
def task_two(a):
    """<一句话需求>"""
    # TODO
    return None


# ==================== 自测 ====================
if __name__ == "__main__":
    # 正常输入
    assert task_one(1) == 1
    # 边界（空 / 单元素 / 全相等 / 阈值恰好相等）
    assert task_one(0) == 0
    # 无副作用
    src = [1, 2]
    task_two(src)
    assert src == [1, 2], "不应该修改输入"

    print("chNN 全部通过 ✓")


# region 参考答案
# ↓↓↓ 展开前先自己做完，别偷看（PyCharm 里点左侧折叠箭头） ↓↓↓
"""
def task_one(x):
    return x

def task_two(a):
    return list(a)
"""
# endregion
