# 新增章节规范

给自己看的约定。加一章走 5 步，保证整个仓库风格统一、链接不烂、随时能跑。

**状态只改 [SYLLABUS.md](SYLLABUS.md)**，篇 README 和根 README 不重复维护章节清单。
符号与术语见 [NOTATION.md](NOTATION.md)。

## 1. 命名：全局章号

```
<篇目录>/docs/chNN_<短名>.md
<篇目录>/exercises/chNN_ex.py
```

- `NN` 是 [SYLLABUS.md](SYLLABUS.md) 里分配的**两位章号**，全仓库唯一
- 章号不随篇移动而变；跨篇搬文件时不用改名
- 教学和练习**同号**，一眼对上
- 旧内容（np01~np03 / pd01~pd02 / plt01）保留原命名，作为第 1 篇的历史资产，不强行改号

| 篇目录 | 章号范围 |
|---|---|
| `00_foundations/` | 00~02 |
| `01_ml_framework/` | 03~06 |
| `02_supervised/` | 07~10 |
| `03_unsupervised/` | 11~13 |
| `04_deep_learning/` | 14~17 |
| `05_llm/` | 18~19 |
| `06_engineering/` | 20~21 |
| `07_topics/` | 22~23 |
| `90_appendix/` | `app[A-F]_*.md` |

## 2. 写章节（`_templates/chapter_template.md`）

> 模板里的 `chNN_ex.py` / `chNN-1_xxx.md` 是**占位链接**，复制后必须逐个替换；
> 用链接检查脚本时应排除 `_templates/`，否则会报预期内的假警报。

必须有的三样：

1. **本章子概念索引置顶** —— 每个概念链到对应小节的显式锚点
2. **一个概念一个三级标题** —— `### 7.1 中文（English）`，标题前单独一行 `<a id="c07-01"></a>`
3. **每节五段模板** —— 见下

### 锚点规则（重要）

中文 + 括号 + 英文的标题，GitHub 自动生成的 slug 会被吞括号、中英混排易变，
**禁止在索引里链自动锚点**。统一：

```markdown
<a id="c07-01"></a>
### 7.1 线性回归（Linear Regression）
```

索引里写 `[线性回归（Linear Regression）](#c07-01)`。
ID 格式 `c<章号>-<节号>`，分配后不改；删节保留占位并标「已合并」。

### 单节五段（`_templates/concept_section.md`）

```
概念定义 → 数学形式（可选）→ 最小代码 → 常见误区 → 对应练习链接
（可选：和 C++ / 已有认知的差异）
```

取舍说明：

- **数学形式可选** —— Git、Jupyter、项目流程这类概念没有公式，整段删掉，别硬凑
- **练习不在每节重复** —— 每章一份 `chNN_ex.py`，节内只放 `[第 N 题](...)` 链接。
  一个概念一份练习文件会碎成 150 个文件，且共享数据难复用
- 代码必须能直接跑：数据现场造、`default_rng(42)`、不依赖仓库外文件

## 3. 写练习（`_templates/exercise_template.py`）

1. 顶部 docstring 写清练什么、怎么跑、对应章节
2. 函数桩留 `# TODO`，返回 `None`；注释标出对应锚点
3. 底部 `if __name__ == "__main__":` 里 `assert` 覆盖：正常输入、边界（空/单元素/全相等/阈值相等）、副作用检查
4. 末尾 `# region 参考答案` / `# endregion` 包答案，答案里的**反斜杠只写一份**
   （写在三引号字符串里，`\\n` 会让用户复制出去拿到错误的字面字符）
5. 随机固定种子；`matplotlib` 用 Agg 后端 + 临时目录存图，跑完 `plt.close("all")`

## 4. 校验（不能跳过）

把答案区抽出来替换函数桩后**实际执行**自测体：

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

要求：所有 assert 通过、无警告、不在仓库里留下图片/CSV 垃圾。

另外人工检查一次：

- [ ] 子概念索引里每个链接都能跳到对应 `<a id>`
- [ ] 章号、文件名、练习文件三者一致
- [ ] 标题中英双语格式统一
- [ ] 没有重复定义同一个概念（先在 SYLLABUS 里搜一遍）

## 5. 更新状态

- [SYLLABUS.md](SYLLABUS.md)：该章状态改 `[已完成]`，填实际文件列
- 根 README：只更新「进度」里的汇总数字
- 附录 E：加一条练习索引（只放链接，不复制答案）

## 提交习惯

- 一章一个 commit：`add ch07: 线性模型教学与练习`
- 框架调整单独 commit，别和章节内容混
- 不提交数据集、`*.pt`、`*.pkl`、`.venv`（见 `.gitignore`）
- 推送前 `git status` 确认工作区干净
