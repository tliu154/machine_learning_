# 第 5 篇 深度学习（Deep Learning）

**章号 14~17** ｜ 前置：ch02（梯度与链式法则）、ch07（线性模型）

章节清单与状态看 [SYLLABUS 第 5 篇](../SYLLABUS.md)。

## 顺序：先 numpy 手写，再上 PyTorch

ch14 / ch15 全用 numpy 手写（反向传播、逐层梯度机制、激活与初始化），
**ch16 起才引入 PyTorch**（要装 CPU 版并实跑对照代码），ch17 讲结构。
**不把框架当黑箱**是这篇的底线：先看透里面的矩阵和梯度，再让 autograd 代劳。

## 已完成：第 14 章 神经网络基础（docs/ + exercises/）

[ch14 教学](docs/ch14_nn_basics.md) + [ch14 练习](exercises/ch14_ex.py)，12 题，参考答案通过自测。
5 节：神经元与层、多层叠加（线性退化）、前向传播与缓存、反向传播、NumPy 两层网络。
**全部只用 numpy，不引入任何框架**；教学里的 `LogisticRegression` 对照需 `pip install scikit-learn`。

- 严格守 [ch02 2.8 的够用边界](../00_foundations/docs/ch02_math_foundations.md#c02-08)：
  反向传播只讲「逐段连乘 + 中心差分验证」，不写 Jacobian、不写矩阵微分推导
- 全参数数值梯度检验最大差 `8.3e-11`（[ch04](../01_ml_framework/docs/ch04_training_steps.md) 定的警戒线是 `1e-5`）
- 在 [ch08 同一份 XOR](../02_supervised/docs/ch08_classical_classifiers.md) 上：
  逻辑回归 val `0.675` → 手写两层网络 val **`1.0000`**，loss `0.690430 → 0.023061`
- 隐藏层宽度 / 学习率扫描如实给非单调结果：`h=3` 反而比 `h=2` 差（局部最优），
  `lr=10` 发散 —— 悬念在 [ch15](docs/ch15_activation_init.md#c15-04) 了结，系统解法留给 ch16

> `python_basics/exercises/` 只到 ch12，**ch14 及以后没有撞名文件**。

## 已完成：第 15 章 激活函数与初始化（docs/ + exercises/）

[ch15 教学](docs/ch15_activation_init.md) + [ch15 练习](exercises/ch15_ex.py)，12 题，参考答案通过自测。
4 节：激活函数族、梯度消失与爆炸、权重初始化、实操清单（了结 ch14 的 `h=3` 悬念）。
**继续全部只用 numpy，不引入 PyTorch** —— 逐层梯度机制要自己乘一遍才看得清。

- 只用到 [ch02 2.8](../00_foundations/docs/ch02_math_foundations.md#c02-08) 那句「一串导数相乘」，
  不写 Jacobian、不推方差公式；符号配人话，每节标「够用边界」
- 8 层网络（`d=32, n=64, seed=0`）实测：ReLU + He 首/末层梯度范数 `2.558 → 1.068`（仅差 2.4 倍）；
  naive `std=0.1` 衰减 **596 倍**、`std=1.0` 放大约 **4 万倍**、`std=2.0` 前向激活 std 到 `1.89e+07`
- Sigmoid 导数上界 `0.25`，8 层即 `1.53e-05`；偏置被一次大更新推到 `-0.5`，后两层 ReLU 全死、末层梯度归零
- **如实写了负面结果**：ch14 `h=3` 的 XOR 换 5 种初始化，20 种子成功率仍只有 `0.40~0.60`，
  加到 `h=4` 反而有 `0.90` —— 浅网络的瓶颈是容量 / 局部最优，不是梯度消失。
  别把初始化当万能旋钮，系统解法（优化器 / 归一化）在 ch16

## 已完成：第 16 章 训练深度网络（docs/ + exercises/）

[ch16 教学](docs/ch16_training_dnn.md) + [ch16 练习](exercises/ch16_ex.py)，12 题，参考答案通过自测。
6 节：优化器、学习率调度、归一化、Dropout 与残差、深度的代价、从 numpy 到 PyTorch。
**练习题仍只用 numpy**；16.6 的 PyTorch 代码在 CPU 版 `torch 2.9.1` 上实跑过。

- 病态二次型（条件数 100）实测：SGD `362` 步、Momentum `299` 步、Adam `82` 步达标；
  SGD `lr=0.02` 踩到稳定上限 `2/λmax` 直接不收敛
- 调度的作用是压**噪声地板**：带噪声梯度的末段 loss constant `0.02705` → cosine `0.00012`；
  去掉噪声后结论反转（constant `5.0e-06` 最好）—— 如实写了两面
- `std=1.0` 的 8 层网：无 BN 激活 std `3.29 → 2.03e+04`（每层约 ×4.3），有 BN `0.586 → 0.635`
- **负面结果一条不藏**：深度同装置上没有收益（2 层 test `0.00199` vs 32 层 `0.00336`）；
  无缩放残差 32 层激活 std 涨 `415` 倍、梯度涨 `122` 倍；2 层加 BN 是负收益；`h=3` 换 Adam 仍 `0/20`
- autograd 与手写反向最大绝对差 `8.674e-18` —— 框架没做你不知道的事

## 和 C++ / OpenCV 经验的衔接

- Tensor ≈ 带 autograd 的 ndarray，但形状约定是 `[N, C, H, W]`
  （numpy 图像是 `[H, W, C]`，BGR；这里是 RGB + float32，**下标和通道顺序都反了**）
- 图像预处理（resize、归一化、颜色转换）你已经会，重点讲框架为什么这么规定
- 部署主链路是 Python 服务（见 [第 7 篇实践轨道](../06_engineering/README.md)）；
  C++ / OpenCV 经验仍可用在批量图像预处理与 embedding 抽取的加速上

## 练习设计方向

- [ch14](exercises/ch14_ex.py)（已完成）：numpy 手写 XOR 两层网络，验证损失下降与全参数梯度检验（不用任何框架）
- [ch15](exercises/ch15_ex.py)（已完成）：8 层前向激活 std 与逐层梯度范数、死 ReLU 统计、Xavier / He，
  最后亲手复现 `seed=0` 那个卡住的 `h=3`（不用任何框架）
- ch16（已完成）：[ch16](exercises/ch16_ex.py) 手写 SGD / Momentum / Adam、调度、BN / LN、Dropout、残差，
  用几何平均判断「数值是否在逐层放大」（不用任何框架）
- ch17：数卷积层输出尺寸与参数量；手写 IoU 与 NMS（**视觉组面试常考**）

## 取舍说明

原备注说「`ch15 激活函数与初始化` 和 `ch16 训练深度网络` 允许合并成一章」，
**实际撰写时决定不合并**：ch15 的梯度消失 / 初始化实测本身就够 4 节，
合成一章要塞 8+ 节，会破掉「按节控长度」的规范；ch16 的优化器 / 学习率调度 /
归一化 / Dropout / 残差是独立主题。**章号仍保留以便对照**（见 SYLLABUS 结构备注）。
RNN/LSTM 只讲直觉不深挖，Transformer 才是后面 LLM 篇的地基。
