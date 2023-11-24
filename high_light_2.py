import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/deejac/Pictures/WX20231124-085746@2x.png', 0)

# 计算图像的直方图
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

# 计算累积分布函数 (CDF)
cdf = hist.cumsum()

# 归一化CDF到最大值255
cdf_normalized = cdf * hist.max() / cdf.max()

# 创建查找表 (LUT)
lut = np.zeros(256, dtype=np.uint8)
# 对于暗部像素（低于中位数），映射到更高的值，对于亮部像素（高于中位数），映射到更低的值
lut[cdf_normalized <= 128] = 255 - np.abs(cdf_normalized[cdf_normalized <= 128] - 128) * 2
lut[cdf_normalized > 128] = cdf_normalized[cdf_normalized > 128] - 128

# 应用LUT到图像
img_stretch = cv2.LUT(img, lut)

# 显示原图和处理后的图像
cv2.imshow('Original', img)
cv2.imshow('Stretched', img_stretch)
cv2.waitKey(0)