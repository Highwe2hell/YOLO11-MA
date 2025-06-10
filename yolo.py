import time
from ultralytics import YOLO
import os
import cv2
import subprocess
from pathlib import Path

# FFmpeg工具的路径，用于视频格式转换
FFMPEG_PATH = r'C:\Program Files\FFmpeg\bin\ffmpeg.exe'

# 加载预训练的YOLO模型
model = YOLO('static/models/YOLO11-MA_base.pt')


def run_model(image_path):
    """
    使用YOLO模型运行图片检测。

    参数:
    image_path (str): 输入图片的路径。

    返回:
    str: 处理后图片的路径。
    float: 推理时间（毫秒）。
    """
    start_time = time.time()
    image_path = Path(image_path)
    result_path = image_path.with_name(f"{image_path.stem}_result{image_path.suffix}")

    results = model(str(image_path))
    results[0].save(filename=str(result_path))

    inference_time = round((time.time() - start_time) * 1000, 2)
    return str(result_path), inference_time


def convert_to_browser_compatible_mp4(input_path, output_path):
    """
    将视频文件转换为浏览器兼容的MP4格式。

    参数:
    input_path (str): 输入视频文件的路径。
    output_path (str): 输出转换后的视频文件路径。
    """
    cmd = [
        FFMPEG_PATH,
        '-y',
        '-i', input_path,
        '-vcodec', 'libx264',
        '-acodec', 'aac',
        '-strict', '-2',
        '-movflags', '+faststart',
        output_path
    ]
    subprocess.run(cmd, check=True)


def run_video_model(video_path):
    """
    使用YOLO模型运行视频检测。

    参数:
    video_path (str): 输入视频的路径。

    返回:
    str: 处理后视频的路径。
    float: 推理时间（毫秒）。
    """
    start_time = time.time()
    video_path = Path(video_path)
    uploads_folder = Path(os.getcwd()) / 'static' / 'uploads'
    uploads_folder.mkdir(parents=True, exist_ok=True)

    base_name = video_path.stem
    raw_result_path = uploads_folder / f'{base_name}_result_raw.mp4'
    converted_path = uploads_folder / f'{base_name}_result.mp4'

    cap = cv2.VideoCapture(str(video_path))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(raw_result_path), fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()

    convert_to_browser_compatible_mp4(str(raw_result_path), str(converted_path))

    inference_time = round((time.time() - start_time) * 1000, 2)
    return str(converted_path), inference_time
