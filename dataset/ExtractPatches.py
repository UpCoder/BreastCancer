# -*- coding=utf-8 -*-
from Config import train_png_path, val_png_path, test_png_path, mask_png_path, train_patches_path, test_patches_path, val_patches_path
from utils.Tools import get_boundingbox
import numpy as np
from PIL import Image
import os
from glob import glob


class ExtractPatches:
    def __init__(self):
        print 'ExtractPatches'

    @staticmethod
    def extract_ROI_single(image, mask_image):
        '''
        从一幅图像中提取ROI
        :param image: 图像
        :param mask_image: mask文件
        :return: ROI numpy [ROI_W, ROI_H, channel]
        '''
        mask_image = np.array(mask_image)
        image = np.array(image)
        mask_image[mask_image != 0] = 1
        [x_min, x_max, y_min, y_max] = get_boundingbox(mask_image)
        return image[x_min:x_max, y_min:y_max]

    @staticmethod
    def extract_ROI_multifiles(file_paths, label_dir, save_dir=None):
        '''
        从多个文件中提取多个ROI
        :param file_paths: 文件的路径
        :param label_dir: 对应的mask Image的存储目录
        :return: [N] 长度为Ｎ的数组，代表有Ｎ个ROI
        '''
        ROIs = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path).split('.png')[0]
            paths = glob(os.path.join(label_dir, file_name+'*.png'))
            image = Image.open(file_path)
            for mask_path in paths:
                mask_image = Image.open(mask_path)
                ROI = ExtractPatches.extract_ROI_single(image, mask_image)
                ROIs.append(ROI)
                if save_dir is not None:
                    shape = list(np.shape(ROI))
                    if shape[0] * shape[1] < 50:
                        continue
                    img = Image.fromarray(ROI)
                    img.save(os.path.join(save_dir, os.path.basename(mask_path)))
                    print 'save to ', os.path.join(save_dir, os.path.basename(mask_path))
        return ROIs

    @staticmethod
    def extract_ROI_multidir(file_dirs, label_dir, save_dirs):
        '''
        从多个目录中读取ROI,每个目录下面有许多图像.savedir的长度和filedir的长度必须一直,一一对应
        :param file_dirs: 数组,每个元素代表的是路径
        :param label_dir: 字符串 代表目录的路径
        :param save_dirs: 数组,每个元素代表的是路径
        :return: None
        '''
        for index, file_dir in enumerate(file_dirs):
            names = os.listdir(file_dir)
            paths = [os.path.join(file_dir, name) for name in names]
            print paths
            ExtractPatches.extract_ROI_multifiles(paths, label_dir, save_dirs[index])


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
        mask_image = np.array(mask_image)
        image = np.array(image)
        mask_image[mask_image != 0] = 1
        [x_min, x_max, y_min, y_max] = get_boundingbox(mask_image)
        for i in range(x_min, x_max, step):
            for j in range(y_min, y_max, step):
                if mask_image[i, j] == 0:
                    continue
                cur_patch = image[i-width/2: i+width/2, j-height/2: j+height/2, :]
                cur_patch_mask = mask_image[i-width/2: i+width/2, j-height/2: j+height/2]
                if (1.0 * np.sum(cur_patch_mask) / (1.0 * width * height)) < ratio:
                    continue
                shape = list(np.shape(cur_patch))
                if shape[0] != width or shape[1] != height:
                    continue
                patches.append(cur_patch)
        return np.array(patches)

    @staticmethod
    def extract_patches_multifiles(file_paths, label_dir, save_dir, width, height, step, ratio):
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
            file_name = os.path.basename(file_path).split('.png')[0]
            paths = glob(os.path.join(label_dir, file_name + '*.png'))
            print os.path.join(label_dir, file_name + '*.png')
            print paths
            image = Image.open(file_path)
            for mask_path in paths:
                mask_image = Image.open(mask_path)
                patches = ExtractPatches.extract_patches_single(image, mask_image, width, height, step, ratio)
                patches_dict[os.path.basename(mask_path)] = patches
                if save_dir is not None:
                    save_path = os.path.join(save_dir, os.path.basename(mask_path)).split('.png')[0] + '.npy'
                    np.save(save_path, patches)
                    print 'save to ', save_path, ' the number of patches is ', len(patches)
        if save_dir is None:
            return patches_dict
        else:
            return None

    @staticmethod
    def extract_patches_multidir(file_dirs, label_dir, save_dirs, width, height, step, ratio):
        '''
        从多个目录中读取ROI,每个目录下面有许多图像.savedir的长度和filedir的长度必须一直,一一对应
        :param file_dirs: 数组,每个元素代表的是路径
        :param label_dir: 字符串 代表目录的路径
        :param save_dirs: 数组,每个元素代表的是路径
        :return: None
        '''
        for index, file_dir in enumerate(file_dirs):
            names = os.listdir(file_dir)
            paths = [os.path.join(file_dir, name) for name in names]
            print paths
            ExtractPatches.extract_patches_multifiles(paths, label_dir, save_dirs[index], width, height,
                                                      step, ratio)

    @staticmethod
    def generate_image_paths(file_names, label_dir):
        '''
        根据分割得到的mask文件生成原图的文件
        :param file_names:
        :param label_dir:
        :return:
        '''
        print 'ok'
if __name__ == '__main__':
    extractor = ExtractPatches()
    extractor.extract_patches_multidir(
        ['/home/give/Documents/dataset/BOT_Game/train/positive-png'],
        '/home/give/Documents/dataset/BOT_Game/fill_label_splited',
        ['/home/give/Documents/dataset/BOT_Game/train/positive_patches'],
        width=64,
        height=64,
        step=32,
        ratio=0.2
    )
