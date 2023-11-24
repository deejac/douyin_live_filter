import cv2
import ffmpeg
import numpy as np
def adjust_brightness(image, threshold, slope):
    # 将图片转换为Lab颜色空间
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # 分离L、a、b通道
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # 对L通道进行亮度调整
    scar = (l_channel - np.min(l_channel)) / (np.max(l_channel) - np.min(l_channel))
    actor = 1/(scar+0.2)
    l_channel = np.where(l_channel  , l_channel*actor, l_channel)

   # l_channel = (l_channel - np.min(l_channel)) / (np.max(l_channel) - np.min(l_channel))
    #l_channel = np.where((l_channel>90)&(l_channel<100), l_channel * 1.5, l_channel)
    #l_channel = np.where(l_channel < threshold, l_channel * slope, l_channel)
    scale = 0.03
    #l_channel = np.log1p(l_channel*10)
    l_channel = np.clip(l_channel, 0, 255)
    l_channel = l_channel.astype(np.uint8)

    # 合并调整后的通道
    lab_adjusted = cv2.merge((l_channel, a_channel, b_channel))

    # 将图片转换回BGR颜色空间
    adjusted_image = cv2.cvtColor(lab_adjusted, cv2.COLOR_LAB2BGR)

    return adjusted_image

# HLS协议视频源地址
hls_url = "http://pull-hs-f5.flive.douyincdn.com/stage/stream-7304891437177522956_ld/index.m3u8?expire=1701418949&sign=128619be920c10cb7d5b97c0706cfbd9&volcSecret=128619be920c10cb7d5b97c0706cfbd9&volcTime=1701418949"

# 使用OpenCV读取HLS协议数据
cap = cv2.VideoCapture(hls_url)

# 获取输入源的分辨率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#width = 150
#height = 150

# 创建FFmpeg写入器
output_filename = "output.m3u8"
output = ffmpeg.output(
    ffmpeg.input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(width, height)),
    output_filename,
    vcodec='libx264',
    preset='ultrafast',
    tune='zerolatency',
    f='hls',
    hls_time=1,
    hls_list_size=10,
    hls_flags='delete_segments'
)
output = output.overwrite_output()

# 打开FFmpeg进程
process = ffmpeg.run_async(output, pipe_stdin=True)
# 裁剪区域 (x, y, width, height)
crop_area = (300, 300, width, height)
# 读取并处理每一帧数据
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 在这里进行卷积处理，这里只是一个示例，你可以根据你的需求修改
    #processed_frame = cv2.filter2D(frame, -1, kernel)
    # 选择放大区域的圆心位置（x，y）
    center_x = 240
    center_y = 550

    # 设置放大倍数和半径
    scale_factor = 3
    radius = 45

    # 在原始图像上绘制放大区域的圆圈
    # cv2.circle(image, (center_x, center_y), radius, (0, 255, 0), 2)

    # 计算放大区域的位置和尺寸
    x = int(center_x - radius)
    y = int(center_y - radius)
    width = int(radius * 2)
    width =width*2
    height = int(radius * 2)

    # 提取放大区域
    zoomed_region = frame[y:y + height, x:x + width]

    # 放大区域
    zoomed_region = cv2.resize(zoomed_region, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    zoomed_region = adjust_brightness(zoomed_region, 90, 2)
    # 将放大区域叠加到原始图像上
    zoomed_region = cv2.resize(zoomed_region, (int(width * scale_factor), int(height * scale_factor)),
                               interpolation=cv2.INTER_LINEAR)
    width = zoomed_region.shape[0]
    height = zoomed_region.shape[1]
    position_x =10
    position_y =10
    if(position_x+width>frame.shape[0]):
        frame_end_x = frame.shape[0]
        zoomed_region_end_x = frame.shape[0]-position_x
    else:
        frame_end_x = position_x+width
        zoomed_region_end_x = width
    if(position_y+height>frame.shape[1]):
        frame_end_y = frame.shape[1]
        zoomed_region_end_y = frame.shape[1]-position_y
    else:
        frame_end_y = position_y+height
        zoomed_region_end_y = height
    frame[position_x:frame_end_x, position_y:frame_end_y] = zoomed_region[0:zoomed_region_end_x, 0:zoomed_region_end_y]
    # 将处理后的帧数据写入FFmpeg进程的输入管道
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    #process.stdin.write(frame.tobytes())

# 关闭FFmpeg进程和OpenCV视频流
process.stdin.close()
process.wait()
cap.release()