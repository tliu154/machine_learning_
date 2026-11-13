# 第 5 篇 深度学习（Deep Learning）

**章号 14~17** ｜ 前置：ch02（梯度与链式法则）、ch07（线性模型）

章节清单与状态看 [SYLLABUS 第 5 篇](../SYLLABUS.md)。

## 顺序：先 numpy 手写，再上 PyTorch

ch14 用 numpy 实现两层网络（含反向传播），ch15/16 才引入框架的训练技巧，
ch17 讲结构。**不把框架当黑箱**是这篇的底线。

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
  `lr=10` 发散 —— 这正是 ch15 初始化与 ch16 优化器要解决的问题

> `python_basics/exercises/` 只到 ch12，**ch14 没有撞名文件**。

## 和 C++ / OpenCV 经验的衔接

- Tensor ≈ 带 autograd 的 ndarray，但形状约定是 `[N, C, H, W]`
  （numpy 图像是 `[H, W, C]`，BGR；这里是 RGB + float32，**下标和通道顺序都反了**）
- 图像预处理（resize、归一化、颜色转换）你已经会，重点讲框架为什么这么规定
- 部署主链路是 Python 服务（见 [第 7 篇实践轨道](../06_engineering/README.md)）；
  C++ / OpenCV 经验仍可用在批量图像预处理与 embedding 抽取的加速上

## 练习设计方向

- [ch14](exercises/ch14_ex.py)（已完成）：numpy 手写 XOR 两层网络，验证损失下降与全参数梯度检验（不用任何框架）
- ch15：观察 Sigmoid 深层的梯度消失；对比不同初始化的激活值分布
- ch16：写可复用的 `train_one_epoch` / `evaluate`
- ch17：数卷积层输出尺寸与参数量；手写 IoU 与 NMS（**视觉组面试常考**）

## 取舍说明

`ch15 激活函数与初始化` 和 `ch16 训练深度网络` 内容重叠度高，
**实际撰写时允许合并成一章，编号保留**（见 SYLLABUS 备注）。
RNN/LSTM 只讲直觉不深挖，Transformer 才是后面 LLM 篇的地基。
