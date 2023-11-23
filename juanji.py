import subprocess
import numpy as np
import tempfile
import glob
import os
from PIL import Image
import cv2


def apply_filter(input_file, output_file, filter_args):
    command = ['ffmpeg', '-i', input_file] + filter_args + ['-f', 'mp4', output_file]
    print(command)
    subprocess.run(command, check=True)


def read_frames(input_file, output_folder):
    command = ['ffmpeg', '-i', input_file, '-vf', 'select=eq(n\,0)', '-vframes', '1', '-y',
               output_folder + '/out%03d.png']
    subprocess.run(command, check=True)


def apply_sharpening(image_files, output_folder):
    for i in range(len(image_files)):
        image = np.array(Image.open(image_files[i]))
        # 这里可以自定义你的锐化卷积操作，例如使用opencv的filter2D函数。
        # 下面是一个简单的锐化卷积示例，你可以根据需要调整它。
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(image, -1, kernel)
        Image.fromarray(sharpened_image).save(output_folder + '/sharpened_out%03d.png' % i)


def clean_up_images(output_folder):
    # 删除已处理的PNG图像
    for filename in glob.glob(output_folder + '/sharpened_out*.png'):
        os.remove(filename)


def main():
    input_stream = 'http://pull-hs-f5.flive.douyincdn.com/third/stream-402357111639245483_sd/index.m3u8?expire=1701226790&sign=1de5cc9e8519de24d57af60c1e746ae4&volcSecret=1de5cc9e8519de24d57af60c1e746ae4&volcTime=1701226790'  # 输入的HLS流地址
    output_stream = 'output.m3u8'  # 输出的HLS流地址
    temp_folder = "/Users/deejac/tmp/juanji"+ '/ffmpeg_temp/'  # 临时文件夹路径，用于存储读取和处理的帧图像
    print(temp_folder)
    sharpening_kernel = '[-1,-1,-1; -1,9,-1; -1,-1,-1]'  # 锐化卷积核，你可以根据需要修改它。

    # 首先，从HLS流中读取所有帧图像到临时文件夹
    apply_filter(input_stream, temp_folder + 'input.mp4', ['-vf', 'select=eq(n\,0),scale=480:640:-1:flags=lanczos'])
    read_frames(temp_folder + 'input.mp4', temp_folder)  # 这将在temp_folder下生成一系列的png图片，它们是HLS流的帧图像。

    # 对每一帧图像应用锐化卷积，并将处理后的图像保存为新的HLS流。
    apply_sharpening([temp_folder + 'out%03d.png' % i for i in range(len(glob.glob(temp_folder + 'out*.png')))],
                     temp_folder)
    apply_filter('pipe:0', output_stream, ['-vf', 'movie=' + temp_folder + 'sharpened_out*.png[0:0]', '-c:v',
                                           'copy'])  # 使用ffmpeg的movie选项将所有处理过的帧图像作为一个输入流提供给ffmpeg。然后将它们封装为HLS流。

    # 清理已处理的PNG图像
    clean_up_images(temp_folder)


if __name__ == '__main__':
    main()