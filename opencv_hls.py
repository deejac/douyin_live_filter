import cv2
import ffmpeg

# HLS协议视频源地址
hls_url = "http://pull-hls-l6.douyincdn.com/third/stream-114132150640181287_md/index.m3u8?k=0d1e1c6dc0faf82f&t=1701307592"

# 使用OpenCV读取HLS协议数据
cap = cv2.VideoCapture(hls_url)

# 获取输入源的分辨率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 创建FFmpeg写入器
output_filename = "output.m3u8"
output = ffmpeg.output(
    ffmpeg.input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(width, height)),
    output_filename,
    vcodec='libx264',
    preset='ultrafast',
    tune='zerolatency',
    f='hls',
    hls_time=2,
    hls_list_size=10,
    hls_flags='delete_segments'
)
output = output.overwrite_output()

# 打开FFmpeg进程
process = ffmpeg.run_async(output, pipe_stdin=True)

# 读取并处理每一帧数据
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 在这里进行卷积处理，这里只是一个示例，你可以根据你的需求修改
    #processed_frame = cv2.filter2D(frame, -1, kernel)

    # 将处理后的帧数据写入FFmpeg进程的输入管道
    process.stdin.write(frame.tobytes())

# 关闭FFmpeg进程和OpenCV视频流
process.stdin.close()
process.wait()
cap.release()