# YOLO11-MA — 军用飞机识别网站示例

![YOLO11-MA](https://img.shields.io/badge/YOLO11--MA-Aircraft%20Recognition-blue)

---

## 项目简介

**YOLO11-MA** 是一个基于 Flask 的网页应用示例，演示如何将训练好的 YOLO 模型无缝集成到网站中，实现图像和视频的上传、识别与结果展示。 
本项目以**军用飞机识别**为示例场景，用户可上传 JPG/PNG 图片或 MP4 视频，系统自动检测并标注飞机类型，展示标注后的识别结果。

此网站设计灵活，支持用户替换自己的 YOLO 模型，方便快速改造为任意目标检测识别系统，满足多样化的实际需求。

---

## 主要功能

- 支持图像（JPG/PNG）和视频（MP4）文件上传
- 自动调用 YOLO 模型进行目标检测与标注
- 视频处理后自动转码为浏览器兼容格式
- 识别结果直观展示，含标注图/视频与推理耗时
- 结构清晰，易于替换模型和二次开发

---

## 目录结构
```

YOLO11-MA/
 ├── app.py                 # Flask主程序，负责文件上传与请求处理
 ├── yolo.py                # YOLO模型推理及视频处理核心代码
 ├── static/                # 静态资源目录（CSS/JS/模型/上传文件）
 │   ├── css/
 │   ├── js/
 │   ├── models/            # 预训练模型文件
 │   └── uploads/           # 上传与结果文件存储目录
 ├── templates/             # HTML页面模板
 ├── README.md              # 项目说明文档
 ├── LICENSE                # GPL-3.0 许可证文件
 └── requirements.txt       # Python依赖列表

```
---

## 环境要求

- Python 3.10+
- Flask
- OpenCV (`cv2`)
- Ultralytics YOLO (`ultralytics` Python包)
- FFmpeg（需安装并配置环境变量或在 `yolo.py` 中指定路径）

---

## 快速开始

1. 克隆仓库

```bash
git clone https://github.com/Highwe2hell/YOLO11-MA.git
cd YOLO11-MA
```

2. 创建并激活虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 安装并配置 FFmpeg
    请根据系统从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载并安装，确保 `ffmpeg` 命令可用，或修改 `yolo.py` 中的 `FFMPEG_PATH` 变量指向正确路径。
5. 启动应用

```bash
python app.py
```

6. 打开浏览器访问：

```
http://127.0.0.1:5000
```

上传图片或视频，即可进行军用飞机识别。

------

## 如何替换为自己的模型

1. 将训练好的 YOLO 模型权重文件放入 `static/models/` 目录。
2. 修改 `yolo.py` 中 `model = YOLO('static/models/YOLO11-MA_base.pt')`，替换为你的模型路径。
3. 根据需要调整标签或后处理逻辑。
4. 重新启动应用，即可使用你的自定义模型。

------

## 许可证

本项目采用 **GNU GPL v3.0** 许可证，详细内容请参见 LICENSE 文件。

------

## 联系与反馈

欢迎提交 Issues 或 Pull Requests，交流改进建议。
 项目地址：https://github.com/Highwe2hell/YOLO11-MA/

------

> YOLO11-MA 助力快速构建可定制的目标检测识别网站，期待您的使用和贡献！