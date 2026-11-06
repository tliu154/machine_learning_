# 第 5 篇 深度学习（Deep Learning）

**章号 14~17** ｜ 前置：ch02（梯度与链式法则）、ch07（线性模型）

章节清单与状态看 [SYLLABUS 第 5 篇](../SYLLABUS.md)。

## 顺序：先 numpy 手写，再上 PyTorch

ch14 用 numpy 实现两层网络（含反向传播），ch15/16 才引入框架的训练技巧，
ch17 讲结构。**不把框架当黑箱**是这篇的底线。

## 和 C++ / OpenCV 经验的衔接

- Tensor ≈ 带 autograd 的 ndarray，但形状约定是 `[N, C, H, W]`
  （numpy 图像是 `[H, W, C]`，BGR；这里是 RGB + float32，**下标和通道顺序都反了**）
- 图像预处理（resize、归一化、颜色转换）你已经会，重点讲框架为什么这么规定
- 部署阶段回到 C++ / OpenVINO，是已有优势能直接迁移的地方

## 练习设计方向

- ch14：numpy 手写 XOR 两层网络，验证损失下降（不用任何框架）
- ch15：观察 Sigmoid 深层的梯度消失；对比不同初始化的激活值分布
- ch16：写可复用的 `train_one_epoch` / `evaluate`
- ch17：数卷积层输出尺寸与参数量；手写 IoU 与 NMS（**视觉组面试常考**）

## 取舍说明

`ch15 激活函数与初始化` 和 `ch16 训练深度网络` 内容重叠度高，
**实际撰写时允许合并成一章，编号保留**（见 SYLLABUS 备注）。
RNN/LSTM 只讲直觉不深挖，Transformer 才是后面 LLM 篇的地基。
