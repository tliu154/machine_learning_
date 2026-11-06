# 1.1 Python 基础语法（Python Basics）· [待迁移]

之前写过的 ch01~ch12 基础教程（C++ 迁移导向）：

| 章 | 主题 |
|---|---|
| ch01 | 世界观：缩进、变量是便利贴、动态类型 |
| ch02 | 数字与运算 |
| ch03 | 字符串与切片 |
| ch04 | 列表与元组（含深浅拷贝大坑） |
| ch05 | 字典、集合、推导式 |
| ch06 | 控制流 |
| ch07 | 函数（含可变默认参数大坑） |
| ch08 | 迭代器与生成器 |
| ch09 | 文件 IO 与异常 |
| ch10 | 类与对象 |
| ch11 | 模块、包、虚拟环境 |
| ch12 | 递归 |

每章都是 `docs/*.md` + `exercises/*_ex.py`（TODO + assert 自测 + `# region` 折叠答案），
与现在的章节模板基本兼容，只是命名用 `chNN` 而这里也恰好是 `chNN`。

## 为什么还空着

`D:\develop` 被重组过，原 `D:\develop\python\` 已不在原位，
目前只在 `D:\develop\JupyterProject\` 找到 `ch12_ex.py` 一个副本。
**没有擅自搬动或重建任何文件。**

## 迁移步骤

1. 找到那套材料后，把 `docs/` 和 `exercises/` 复制到本目录
2. 跑一遍全部练习的参考答案校验（脚本见 [CONTRIBUTING.md](../../CONTRIBUTING.md)）
3. 在 [SYLLABUS](../../SYLLABUS.md) 把第 1 章 1.1 节状态改成 `[已完成]`
4. 如果章节内容要按新模板拆成「子概念索引 + 独立小节」，单独开一个 commit
