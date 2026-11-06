"""
仓库自检：练习参考答案 + Markdown 相对链接 + 显式锚点。

用法（在任意目录执行都行，路径由本文件位置推断）：
    python tools/verify_all.py

退出码 0 = 全部通过；1 = 有失败项。

约定见 CONTRIBUTING.md 第 4 节：
- 练习末尾用 `# region 参考答案` / `# endregion` 包住三引号答案，反斜杠只写一份；
- 索引链自定义锚点 `<a id="cNN-MM"></a>`，不用 GitHub 自动 slug；
- `_templates/` 里的 `chNN` 是占位符，整目录跳过。
"""

from __future__ import annotations

import re
import sys
import textwrap
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ANSWER_REGION = re.compile(r"# region 参考答案(.*?)# endregion", re.S)
MAIN_MARKER = 'if __name__ == "__main__":'
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`]*`")
ANCHOR_ID = re.compile(r'<a\s+id="([^"]+)"\s*>\s*</a>', re.I)
CUSTOM_ANCHOR = re.compile(r"^c\d{2}-\d{2}$")


def extract(text: str):
    """拆出 (函数桩前缀, 参考答案, 自测体)。没有答案区返回 (None, None, None)。"""
    m = ANSWER_REGION.search(text)
    if not m:
        return None, None, None
    answers = "\n".join(re.findall(r'"""(.*?)"""', m.group(1), re.S))
    head = text.partition("# region 参考答案")[0]
    if MAIN_MARKER not in head:
        return head, answers, ""
    idx = head.index(MAIN_MARKER)
    return head[:idx], answers, textwrap.dedent(head[idx + len(MAIN_MARKER):])


def strip_code(text: str) -> str:
    """去掉围栏代码块与行内代码，避免 C++ 的 `[](int x)` 被当成 Markdown 链接。"""
    text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE.sub("", text)


def check_exercises() -> tuple[bool, int]:
    files = sorted(p for p in ROOT.rglob("*_ex.py") if ".git" not in p.parts)
    ok, passed = True, 0
    for f in files:
        rel = f.relative_to(ROOT)
        prefix, answers, body = extract(f.read_text(encoding="utf-8"))
        if prefix is None:
            print(f"[SKIP] {rel}  (无答案区)")
            continue
        ns = {"__name__": "__main__", "__file__": str(f)}
        try:
            exec(compile(prefix, str(rel), "exec"), ns)
            exec(compile(answers, str(rel), "exec"), ns)   # 答案覆盖同名 TODO 桩
            if body:
                exec(compile(body, str(rel), "exec"), ns)  # 跑底部 assert
            passed += 1
            print(f"[OK]   {rel}")
        except Exception as e:
            ok = False
            tb = traceback.extract_tb(sys.exc_info()[2])
            print(f"[FAIL] {rel}: {type(e).__name__}: {e} (line {tb[-1].lineno})")
    print(f"\n练习 {passed}/{len(files)} 通过")
    return ok, len(files)


def check_links() -> bool:
    mds = [p.resolve() for p in ROOT.rglob("*.md")
           if ".git" not in p.parts and "_templates" not in p.parts]
    # 每个文件里真实存在的自定义锚点
    ids = {p: set(ANCHOR_ID.findall(p.read_text(encoding="utf-8"))) for p in mds}

    broken_links: list[tuple[str, str]] = []
    broken_anchors: list[tuple[str, str]] = []
    checked_links = checked_anchors = 0

    for md in mds:
        text = strip_code(md.read_text(encoding="utf-8"))
        for m in LINK.finditer(text):
            target = m.group(1).strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "data:")):
                continue

            path_part, _, anchor = target.partition("#")
            if path_part:
                checked_links += 1
                dest = (md.parent / path_part).resolve()
                if not dest.exists():
                    broken_links.append((str(md.relative_to(ROOT)), target))
                    continue
            else:
                dest = md

            # 只校验自定义锚点 cNN-MM；GitHub 自动 slug 无法离线推断，跳过
            if anchor and CUSTOM_ANCHOR.match(anchor):
                checked_anchors += 1
                if anchor not in ids.get(dest, set()):
                    broken_anchors.append((str(md.relative_to(ROOT)), target))

    print(f"相对链接 {checked_links} 条，断链 {len(broken_links)} 条")
    for f, t in broken_links:
        print(f"  [断链] {f} -> {t}")
    print(f"自定义锚点 {checked_anchors} 条，缺失 {len(broken_anchors)} 条")
    for f, t in broken_anchors:
        print(f"  [锚点缺失] {f} -> {t}")
    return not broken_links and not broken_anchors


if __name__ == "__main__":
    ok_ex, _ = check_exercises()
    ok_link = check_links()
    print("\n" + ("ALL PASS" if ok_ex and ok_link else "HAS FAILURES"))
    sys.exit(0 if ok_ex and ok_link else 1)
