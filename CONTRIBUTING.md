# 新增章节规范

给自己看的约定。每加一章走这 5 步，保证整个仓库风格统一、随时能跑。

## 1. 命名

```
<模块>/docs/<前缀><两位序号>_<短名>.md
<模块>/exercises/<前缀><两位序号>_ex.py
```

前缀按模块固定：

| 模块 | 前缀 | 例子 |
|---|---|---|
| 00_fundamentals | `py` / `np` / `pd` / `plt` | `np02_broadcast.md` |
| 01_math | `math` | `math01_linear_algebra.md` |
| 02_core | `core` | `core02_evaluation.md` |
| 03_algorithms | `alg` | `alg01_linear_regression.md` |
| 04_deep_learning | `dl` | `dl02_pytorch_basics.md` |
| 05_projects | `proj` | `proj01_tabular.md` |
| 90_appendix | `app` | `app02_glossary.md` |

教学和练习**同名同序号**，一眼能对上。

## 2. 写教学（`_templates/chapter_template.md`）

- 一章一个主题，150~250 行，别贪多
- 开头「前置」一行：需要先会什么
- 正文以「和 C++ / 和已有认知的差异」为切入，不重复讲基础
- 每章末尾「小结」表格 + 上一篇/下一篇链接
- 代码必须能直接复制运行，不依赖仓库外的数据文件

## 3. 写练习（`_templates/exercise_template.py`）

必须满足：

1. 顶部 docstring 写清本章练什么、怎么跑
2. 函数桩留 `# TODO`，返回值先写 `None`
3. 底部 `if __name__ == "__main__":` 里放 `assert`，覆盖：
   - 正常输入
   - 边界（空、单元素、全相等、阈值恰好相等）
   - 不该有副作用的地方（原数组/原表是否被改）
4. 末尾 `# region 参考答案` / `# endregion` 包住答案，答案里的反斜杠**只写一份**
   （写在三引号字符串里，`\\n` 会让用户复制出去拿到错误的字面字符）
5. 随机一律固定种子（`np.random.default_rng(42)`），结果可复现

## 4. 校验（不能跳过）

把答案区抽出来替换函数桩后实际执行自测体。完整流程见本文件末尾的校验脚本说明。
要求：

- 所有 `assert` 通过，打印 `xxNN 全部通过 ✓`
- 无警告（尤其是 matplotlib 的中文/后端、pandas 的 dtype 警告）
- 不产生仓库里的垃圾文件（图片存临时目录，用完 `plt.close("all")`）

## 5. 更新状态

- 模块 `README.md` 里该章状态改成 `[已完成]`
- 根 `README.md` 的总表同步
- 进度数字同步

## 校验脚本（临时用，不入仓库）

```python
import re, textwrap
from pathlib import Path

def extract(text):
    region = re.search(r"# region 参考答案(.*?)# endregion", text, re.S).group(1)
    answers = "\n".join(re.findall(r'"""(.*?)"""', region, re.S))
    head = text.partition("# region 参考答案")[0]
    marker = 'if __name__ == "__main__":'
    idx = head.index(marker)
    return head[:idx], answers, textwrap.dedent(head[idx + len(marker):])

for f in Path(".").rglob("*_ex.py"):
    prefix, answers, body = extract(f.read_text(encoding="utf-8"))
    ns = {"__name__": "__main__", "__file__": str(f)}
    exec(compile(prefix, f.name, "exec"), ns)
    exec(compile(answers, f.name, "exec"), ns)   # 答案覆盖 TODO 桩
    exec(compile(body, f.name, "exec"), ns)      # 跑 assert
```

> 原理：先执行函数桩，再执行答案区（同名函数覆盖），最后执行自测体。

## 提交习惯

- 一章一个 commit，信息写 `add alg01: 线性回归教学与练习`
- 框架调整单独 commit，别和章节内容混在一起
- 不提交数据集、`*.pt`、`*.pkl`、`.venv`（见 `.gitignore`）
