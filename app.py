from flask import Flask, render_template, request, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from yolo import run_model, run_video_model

# 初始化Flask应用
app = Flask(__name__)
# 定义上传文件夹的路径
UPLOAD_FOLDER = 'static/uploads'
# 支持的文件类型
SUPPORTED_IMAGE_EXTS = {'.jpg', '.jpeg', '.png'}
SUPPORTED_VIDEO_EXTS = {'.mp4'}
SUPPORTED_EXTS = SUPPORTED_IMAGE_EXTS.union(SUPPORTED_VIDEO_EXTS)

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    """渲染主页界面"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """处理上传的文件，并根据文件类型运行相应的模型"""
    file = request.files.get('media')
    if not file or not file.filename:
        return "未接收到文件", 400

    # 提取并安全化文件名
    original_filename = secure_filename(file.filename)
    ext = os.path.splitext(original_filename)[-1].lower()

    if ext not in SUPPORTED_EXTS:
        return "仅支持 JPG / PNG / MP4 文件", 400

    # 生成唯一文件名
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(path)

        # 判断媒体类型并调用对应模型
        if ext in SUPPORTED_IMAGE_EXTS:
            result_path, inference_time = run_model(path)
            media_type = 'image'
        elif ext in SUPPORTED_VIDEO_EXTS:
            result_path, inference_time = run_video_model(path)
            media_type = 'video'

        # 获取处理结果文件名
        result_filename = os.path.basename(result_path)
        result_url = url_for('static', filename=f'uploads/{result_filename}')

        # 渲染结果显示页面
        return render_template('result.html',
                               result_url=result_url,
                               inference_time=inference_time,
                               media_type=media_type)

    except Exception as e:
        app.logger.error(f"处理文件时发生错误: {e}")
        return "服务器内部错误，请稍后再试", 500


if __name__ == '__main__':
    app.run(debug=False)  # 生产环境务必关闭 debug 模式
