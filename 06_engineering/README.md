# 第 7 篇 工程实践与部署（Engineering and Deployment）

**章号 20~21** ｜ 前置：任意一个能跑通的模型

章节清单与状态看 [SYLLABUS 第 7 篇](../SYLLABUS.md)。原框架的「实战项目」升级成
「项目流程 + 部署监控」两章，具体项目降为**贯穿各篇的实践轨道**，不占章号。

## 实践轨道（`projects/`）

| 项目 | 用得到的章 | 目录 |
|---|---|---|
| 表格数据端到端 | ch03~ch10 | `projects/tabular/` |
| 图像分类（迁移学习） | ch14~ch17 | `projects/image_classification/` |
| **RoboMaster 装甲板识别** | ch17 / ch21 + OpenCV | `projects/armor_detection/` |
| 模型服务化 Demo | ch21 | `projects/serving_demo/` |

终点目标仍是装甲板识别，把已有 C++/OpenCV 经验和 ML 串起来：

```
采集/标注 → 数据集划分 → YOLO 训练 → mAP/速度评估
   → 导出 ONNX → C++ / OpenVINO 推理 → 上机测试
```

框架阶段只建目录，做的时候再决定数据集规模、标注工具、部署平台。

## 每个项目的固定交付物

1. `README.md`：目标、数据来源、复现步骤、结果指标
2. 能从头跑通的脚本（`src/` 或单个 `.py`）
3. `notes.md`：踩过的坑 + 为什么这么选（比代码更值钱）

> `.gitignore` 已排除数据集与权重（`.pt` / `.onnx` / `.csv`），
> **不要往仓库里放大文件**。项目不强制配 `exercises/`，但脚本要能 smoke test。

## 取舍说明

ch20 的「实验记录 / 可复现性」和 ch21 的「监控 / 漂移」看起来像运维话题，
但对单人项目同样重要：三个月后看不懂自己当时为什么调这个参数，就是没做记录。
