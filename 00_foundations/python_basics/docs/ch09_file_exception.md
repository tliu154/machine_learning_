---
tags:
  - course/CS
  - type/笔记
  - topic/Python
---
# ch09 文件 IO 与异常

## 9.1 with = RAII 的降级替代品

```cpp
// C++ 靠析构函数自动关闭
std::ifstream f("a.txt");
f << "hi";
// 离开作用域自动 close
```

Python 里靠 **`with` 语句**（上下文管理器）：

```python
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("hi\n")
# 缩进块结束，文件自动关闭 —— 就算中间抛异常也关
```

```python
# ✗ 别这么写，忘了 close 会有资源泄漏 / 数据没 flush
f = open("a.txt")
data = f.read()
f.close()
```

> **一定要写 `encoding="utf-8"`**（Windows 上 Python 默认用 GBK 读中文文件，99% 会乱码）。

## 9.2 打开模式

```python
open(path, "r")     # 读，默认。文件不存在 → FileNotFoundError
open(path, "w")     # 写，**会清空原内容**！不存在则创建
open(path, "a")     # 追加写
open(path, "x")     # 排他创建，文件已存在则报错（防止覆盖）
open(path, "rb")    # 二进制读（图片、视频）
open(path, "r+")    # 读写
```

## 9.3 读文件

```python
with open("a.txt", encoding="utf-8") as f:
    content = f.read()          # 全部读成一个字符串
    # content = f.readlines()   # 全部读成行的列表，每行带 \n
    # content = f.readline()    # 只读一行

with open("a.txt", encoding="utf-8") as f:
    for line in f:              # ✓ 推荐！懒加载，一行一行读，大文件不爆内存
        print(line.strip())     # strip() 去掉末尾换行
```

> 文件对象本身就是迭代器（ch08），所以 `for line in f` 天然可用。

常用简化写法：

```python
lines = open("a.txt", encoding="utf-8").read().splitlines()    # splitlines 不带 \n
```

### pathlib —— 现代路径处理（替代 os.path）

```python
from pathlib import Path

p = Path("data") / "scores.txt"         # / 运算符拼路径！
p.exists()          p.is_file()         p.is_dir()
p.name              # scores.txt
p.stem              # scores
p.suffix            # .txt
p.parent            # data
p.with_suffix(".csv")

p.read_text(encoding="utf-8")           # 一行读全部
p.write_text("hello", encoding="utf-8")
p.read_bytes() / p.write_bytes(b)

Path(".").iterdir()                     # 遍历目录内容
Path(".").glob("**/*.py")               # 递归 glob！
sorted(Path(".").glob("*.txt"))

Path("a/b/c").mkdir(parents=True, exist_ok=True)    # 递归建目录
```

> 写新代码一律用 `pathlib`，别用 `os.path.join` 那种字符串拼接了。

### JSON

```python
import json

data = {"name": "涛", "scores": [95, 88], "pass": True}

json_str = json.dumps(data, ensure_ascii=False, indent=2)   # dict → str
with open("d.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)        # dict → 文件

with open("d.json", encoding="utf-8") as f:
    loaded = json.load(f)                                   # 文件 → dict
loaded = json.loads(json_str)                               # str → dict
```

> `ensure_ascii=False` 是必须的，否则中文会变成 `\u6d9b` 这种转义。

JSON 类型映射：`dict↔object`，`list↔array`，`str↔string`，`int/float↔number`，`True/False↔true/false`，`None↔null`。

## 9.4 异常：EAFP 风格

Python 的哲学和 C++ 不同：

| 风格 | 全称 | 做法 | 谁在用 |
|---|---|---|---|
| LBYL | Look Before You Leap | 先 `if` 检查再做 | C 语言习惯 |
| **EAFP** | **Easier to Ask Forgiveness than Permission** | **直接干，出错再except** | **Python 推荐** |

```python
# LBYL（啰嗦，且有竞态条件）
if os.path.exists(path):
    with open(path) as f:
        ...

# EAFP（推荐）
try:
    with open(path) as f:
        ...
except FileNotFoundError:
    print("文件不存在")
```

## 9.5 try / except / else / finally

```cpp
// C++
try { risky(); }
catch (const std::exception& e) { }
```

```python
try:
    risky_operation()
except ValueError as e:                 # 捕获特定异常，as e 拿到异常对象
    print("值错误:", e)
except (KeyError, IndexError):          # 多个异常用元组
    print("键或下标错误")
except Exception as e:                  # 兜底（慎用，会吞掉 bug）
    print("其他:", e)
else:
    print("没出异常才会执行这里")
finally:
    print("无论如何都会执行 → 清理资源")
```

### 常见内置异常

```python
ValueError          类型对但值不对，int("abc")
TypeError           类型不对，1 + "a"
IndexError          下标越界，lst[100]
KeyError            字典 key 不存在
ZeroDivisionError   除零
FileNotFoundError   文件不存在
AttributeError      访问不存在的属性
ImportError         导入失败
StopIteration       迭代器耗尽（for 循环悄悄吞掉它）
```

完整层级：`BaseException` → `Exception` → 各种具体异常。`KeyboardInterrupt` 和 `SystemExit` 直接继承 BaseException，所以 `except Exception` 抓不到 Ctrl+C。

### raise / 自定义异常

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0:
        raise ValueError(f"年龄不能为负: {age}")
    return age

# 自定义异常
class MyAppError(Exception):
    pass

class ValidationError(MyAppError):
    def __init__(self, msg, field):
        super().__init__(msg)
        self.field = field

raise ValidationError("格式错", "email")
```

### 异常链与忽略

```python
try:
    connect()
except ConnectionError as e:
    raise RuntimeError("服务不可用") from e      # from 保留原始异常上下文

from contextlib import suppress
with suppress(FileNotFoundError):       # 优雅地忽略某个异常
    os.remove("temp.txt")
```

### ⚠️ 别用裸 except

```python
try:
    ...
except:                 # ✗ 连 Ctrl+C、SystemExit 都抓，debug 时想砸电脑
    pass                # ✗✗ 静默吞异常，bug 藏三天

except Exception as e:  # 好一点
    log(e)
    raise               # 重新抛出，让上层处理
```

## 9.6 命令行参数

```python
import sys
print(sys.argv)         # ['script.py', 'arg1', 'arg2']   类似 C++ 的 argv
sys.exit(1)             # 退出并给出状态码

# 正经写法用 argparse
import argparse
parser = argparse.ArgumentParser(description="成绩统计")
parser.add_argument("input", help="输入文件")
parser.add_argument("-o", "--output", default="out.txt")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()
print(args.input, args.output, args.verbose)
```

PyCharm 里可以在 Run → Edit Configurations → Parameters 填参数测试。

---

### 小结

| C++ | Python |
|---|---|
| `ifstream/ofstream` + 析构 | `with open(...)` |
| `std::filesystem::path` | `pathlib.Path`（支持 `/` 拼接） |
| `try/catch` | `try/except`（推荐 EAFP 风格） |
| `throw std::runtime_error(x)` | `raise ValueError(x)` |
| 手动解析 argv | `argparse` |

下一章：[ch10 类与对象](ch10_class.md)
