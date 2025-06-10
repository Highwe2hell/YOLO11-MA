document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-upload");
    const previewImage = document.getElementById("preview-image");
    const previewVideo = document.getElementById("preview-video");
    const loading = document.getElementById("loading");

    // 文件大小限制
    const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

    // 页面初始化时彻底清空视频
    previewVideo.src = "";
    previewVideo.load(); // 强制重新加载，防止残留播放器
    previewVideo.classList.add("hidden");

    // 文件选择事件
    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // 清除之前状态
        previewImage.classList.add("hidden");
        previewVideo.classList.add("hidden");
        previewImage.src = "";
        previewVideo.src = ""; // 确保 src 清空
        previewVideo.load(); // 强制清理播放器缓存
        loading.classList.add("hidden");

        // 检查文件大小
        if (file.size > MAX_FILE_SIZE) {
            alert("文件过大，请上传小于 50MB 的文件");
            e.target.value = "";
            return;
        }

        const fileType = file.type;

        if (fileType.startsWith("image/")) {
            previewImage.src = URL.createObjectURL(file);
            previewImage.classList.remove("hidden");
        } else if (fileType === "video/mp4") {
            previewVideo.src = URL.createObjectURL(file);
            previewVideo.classList.remove("hidden");
            previewVideo.load(); // 加载新视频源
        } else {
            alert("不支持的文件类型，请上传 JPG/PNG 图片或 MP4 视频");
        }
    });

    // 显示 loading 动画
    const form = document.querySelector("form");
    form.addEventListener("submit", (e) => {
        loading.classList.remove("hidden");
    });

    // 返回页面时重置
    window.addEventListener('pageshow', (event) => {
        if (!event.persisted) return;

        loading.classList.add("hidden");
        fileInput.value = '';
        previewImage.classList.add("hidden");
        previewVideo.classList.add("hidden");
        previewImage.src = '';
        previewVideo.src = ''; // 彻底清空
        previewVideo.load();
    });
});
