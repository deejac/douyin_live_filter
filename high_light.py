import math

import cv2
import numpy as np

image = cv2.imread('/Users/deejac/Pictures/WX20231124-085746@2x.png')
# 检查图像的通道数
num_channels = image.shape[2]
print("图像通道数：", num_channels)

# 检查每个通道的维度
channel_dims = [image[:, :, i].shape for i in range(num_channels)]
print("通道维度：", channel_dims)
def exponential_scaling(arr, scale):
    return np.exp(arr * scale)

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
# 设置亮度阈值和线性拉升的斜率
brightness_threshold = 90
brightness_slope = 2

# 调整图片亮度
adjusted_image = adjust_brightness(image, brightness_threshold, brightness_slope)

# 显示原始图片和处理后的图片
cv2.imshow('Original Image', image)
cv2.imshow('Adjusted Image', adjusted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
