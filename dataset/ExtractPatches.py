# -*- coding=utf-8 -*-
from Config import train_png_path, val_png_path, test_png_path, mask_png_path, train_patches_path, test_patches_path, val_patches_path
from utils.Tools import get_boundingbox
import numpy as np
from PIL import Image
import os


class ExtractPatches:
    def __init__(self):
        print 'ExtractPatches'

    @staticmethod
    def extract_patches_single(image, mask_image, width, height, step, ratio):
        '''
        根据mask文件从image中mask不为0的部分提取patch
        :param image: 将要提取patch的图片
        :param mask_image: 标记出ROI的图像
        :param width: patch的宽
        :param height: patch的高
        :param step: patch的step
        :param ratio: ROI占比的最少比率
        :return:[N, width, height, image_channel] 返回的是该类型的numpy数组，其中N代表的是可以提取出来N个patch
        '''
        patches = []
        mask_image[mask_image != 0] = 1
        [x_min, x_max, y_min, y_max] = get_boundingbox(mask_image)
        for i in range(x_min, x_max, step):
            for j in range(y_min, y_max, step):
                if mask_image[i, j] == 0:
                    continue
                cur_patch = image[i-width/2: i+width/2, j-height/2: j+height/2]
                cur_patch_mask = mask_image[i-width/2: i+width/2, j-height/2: j+height/2]
                if (1.0 * np.sum(cur_patch_mask) / (1.0 * width * height)) < ratio:
                    continue
                patches.append(cur_patch)
        return np.array(patches)

    @staticmethod
    def extract_patches_multifiles(file_paths, label_dir, width, height, step, ratio):
        '''
        从多个文件中提取patch
        :param file_paths: 文件的路径
        :param label_dir: 所有mask文件的路径
        :param width: patches 的宽
        :param height: patches 的高
        :param step: 提取patches的步长
        :param ratio: ROI占比的最少比率
        :return: dict{KEY:VALUE}，其中key代表的是文件名，value是extract_patches_single返回的numpy数组
        '''
        patches_dict = {}
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            mask_path = os.path.join(label_dir, file_name)
            image = Image.open(file_path)
            mask_image = Image.open(mask_path)
            patches = ExtractPatches.extract_patches_single(image, mask_image, width, height, step, ratio)
            patches_dict[file_name] = patches
        return patches_dict

    @staticmethod
    def generate_image_paths(file_names, label_dir):
        '''
        根据分割得到的mask文件生成原图的文件
        :param file_names:
        :param label_dir:
        :return:
        '''
if __name__ == '__main__':
    image = np.array(Image.open(
        '/home/give/Documents/dataset/BOT_Game/train/positive-png/2017-06-09_18.08.16.ndpi.16.14788_15256.2048x2048.png'))
    print np.shape(image)
    mask_image = np.array(Image.open(
        '/home/give/Documents/dataset/BOT_Game/fill_label_splited/2017-06-09_18.08.16.ndpi.16.14788_15256.2048x2048_1.png'))
    print np.shape(mask_image)
    extractor = ExtractPatches()
    patches = extractor.extract_patches_single(image, mask_image, 256, 256, 64, 0.3)
    print patches.shape