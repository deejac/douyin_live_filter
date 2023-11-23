import cv2
import subprocess

# 设置输入视频流的URL
input_url = "http://pull-hls-f6.douyincdn.com/media/stream-690588919695934124_md/index.m3u8"
#input_url = "/Users/deejac/input.mp4"
# 设置FFmpeg命令行参数
ffmpeg_cmd = [
    "ffmpeg",
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",# 设置输入帧的像素格式
    "-s", "640x360",  # 设置输入帧的尺寸
    "-i", "-",  # 从标准输入读取帧数据
    "-c:v", "libx264",
    "-f", "hls",
    "-hls_time", "2",  # 设置每个片段的时长（单位：秒）
    "-hls_list_size", "5",  # 设置播放列表中的片段数
    "output.m3u8"  # 输出的HLS文件名
]

# 创建FFmpeg进程
ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

# 创建OpenCV视频捕获对象
cap = cv2.VideoCapture(input_url)

while True:
    # 读取一帧视频数据
    ret, frame = cap.read()
    if not ret:
        break

    # 在这里对每帧数据进行卷积处理
    # ...

    # 将处理后的帧数据写入FFmpeg的标准输入
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    ffmpeg_process.stdin.write(frame.tostring())
    #ffmpeg_process.stdin.write(frame.tobytes())

# 关闭视频捕获对象和FFmpeg进程
cap.release()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()
