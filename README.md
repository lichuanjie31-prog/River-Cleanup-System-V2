# 🌊 常大河道水面垃圾巡检系统 V2.0

**👉 [点我直接下载 Windows 客户端](https://github.com/lichuanjie31-prog/-/releases/download/v2.0/_V2.0.exe)**

> **项目状态**：已完成 V2.0 精度优化，适配 NVIDIA RTX 5060。

## 🚀 项目亮点
- **精度质变**：针对 V1.0 在强反光、水草遮挡、色彩保护色下的漏检问题进行了深度微调。
- **环境前瞻**：率先适配 Python 3.13 + PyTorch 2.11 + CUDA 12.8 (Blackwell 架构)。
- **工程化**：提供了基于 PyQt6 的可视化操作界面，支持一键打包 `.exe`。

## 🛠️ 技术栈
- **核心算法**: YOLOv8 (Ultralytics)
- **开发语言**: Python 3.13
- **GUI 框架**: PyQt6
- **训练硬件**: NVIDIA GeForce RTX 5060 Laptop (8GB)

## 📁 目录说明
- `/weights`: 存放训练好的 `best.pt` 权重文件。
- `/src`: 存放 UI 界面源代码 `river_app_final.py`。
- `/data`: 示例测试图片（包含反光/遮挡等难样本）。

## 📈 训练复盘 (V2.0 优化点)
1. **反光抑制**: 通过对高亮过曝区域的精准标注，提升了 30% 的识别率。
2. **遮挡补全**: 强化了对被水草切断的破碎特征的学习。
3. **性能**: 在 5060 显卡加持下，单帧推理延迟低于 5ms。

## 🖼️ 运行效果展示 (V2.0 实战)

### 模式 A：实时河道监控 (RTX 5060 加速)
针对 V1.0 的反光与遮挡痛点进行深度微调，实现了毫秒级精准追踪。

<img width="1268" height="1155" alt="demo_live" src="https://github.com/user-attachments/assets/9d4e5f7f-a788-4e0c-bae0-ad45869ce656" />


### 模式 B：文件夹批量分析
支持导入调研照片文件夹，自动输出带检测框的分析结果至 `Results_Output_V2`。

![demo_batch](https://github.com/user-attachments/assets/32279108-fcba-4497-89e9-4eedc35b65ed)


### 实时数据波动图
同步显示当前画面中的垃圾数量变化，方便记录排污峰值。

<img width="933" height="809" alt="demo_chart" src="https://github.com/user-attachments/assets/723f295d-ec60-43af-a696-a0205afc0bf5" />



## 📖 操作指南 (Quick Start)

为了确保 V2.0 系统在不同环境下都能稳定运行，请参考以下操作步骤：

### 1. 组员快捷使用 (双击起飞)
如果你只想运行系统进行测试，无需配置环境：
- 前往右侧 **[Releases]** 下载最新的 `常大河道巡检_V2.0.zip`。
- 解压后，直接双击运行 `常大河道巡检_V2.0.exe`。
- **模式 A** 用于实时演示，**模式 B** 用于处理实验室/实地调研的成批照片。

### 2. 开发者模式 (源码运行)
如果你想修改代码或重新训练，请按以下步骤配置：
```bash
# 克隆项目
git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
cd River-Cleaner-Vision-V2

# 创建并激活 Python 3.13 环境
python -m venv venv
source venv/Scripts/activate

# 安装适配 50 系显卡的依赖 (CUDA 12.8)
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu128](https://download.pytorch.org/whl/cu128)
pip install ultralytics PyQt6 matplotlib opencv-python

# 运行 UI
python river_app_final.py

```

⚠️ 避坑指南 (必读注意事项)
为了保证系统在不同电脑上跑得稳，请务必注意以下几点：

🛑 1. 路径禁忌 (核心报错原因)
严禁中文路径：请确保你的项目文件夹、图片文件夹、以及 .exe 存放的路径里不包含任何中文字符（例如：D:\桌面\项目 是不行的）。YOLO 内核在加载权重时，如果遇到非 ASCII 字符，极大概率会报错崩溃。

❄️ 2. 硬件与性能
显卡驱动：本程序基于 RTX 5060 (Blackwell) 训练。如果组员使用的是旧显卡，请务必更新 NVIDIA 驱动至 2026 年 4 月以后的版本，否则可能无法触发显卡加速，导致 FPS 降低。

虚拟内存：如果批量处理 100 张以上的大图时程序闪退，请检查 Windows 虚拟内存设置，建议手动设为 16GB 以上（班长已亲测，这是解决 WinError 1455 的绝招）。

📂 3. 模型与资源
模型位置：打包版 .exe 已内置 best.pt。但如果是运行源码，请确保 best.pt 存放在 weights/ 文件夹下。

摄像头占用：运行“模式 A”前，请关闭其他占用摄像头的程序（如腾讯会议等），否则会显示“无法启动摄像头”。

📧 4. 报错反馈
运行过程中如果控制台（Console 区域）跳出红色报错，请截图发送给我。

---
**Team**: 常州大学软件252 -李传杰 [组长]
**致谢组员🤝** 沈永权 & 褚恒智 & 蔡宜辰 & 伏丽学 & 梁大娟 & 徐可欣 & 林星言 & 潘彤 & 宋雯萱

**声明**: 感谢常州大学阿里云学院系主任李宁老师的指导。如果对您有帮助，请Star保存使用。

