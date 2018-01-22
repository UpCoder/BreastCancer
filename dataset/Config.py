# -*- coding=utf-8 -*-

# About 原始数据
# 训练数据的存储路径 key-value: key代表的是目录的路径，value代表的是label
train_png_path = {
    '/home/give/Documents/dataset/BOT_Game/train/positive-png': 1,
    '/home/give/Documents/dataset/BOT_Game/train/negative-png': 0
}
# 所有的mask文件的目录
mask_png_path = [
    '/home/give/Documents/dataset/BOT_Game/fill_label_splited'
]
# 验证集数据的存储路径，格式参照训练数据
val_png_path = {
    '/home/give/Documents/dataset/BOT_Game/val/negative-png': 0,
    '/home/give/Documents/dataset/BOT_Game/val/positive-png': 1
}
# 测试数据的存储路径
test_png_path = [
    '/home/give/Documents/dataset/BOT_Game/test/test_jpg'
]


# About patch
# 训练集patch的存储路径，每种类别的存储路径不同， key代表的是类别， value代表的是存储的路径
train_patches_path = {
    0: '/home/give/Documents/dataset/BOT_Game/train/negative_patches',
    1: '/home/give/Documents/dataset/BOT_Game/train/positive_patches'
}
# 验证集patch的存储路径，格式参照训练集合
val_patches_path = {
    0: '/home/give/Documents/dataset/BOT_Game/val/negative_patches',
    1: '/home/give/Documents/dataset/BOT_Game/val/positive_patches'
}
# 测试集patch的存储路径
test_patches_path = '/home/give/Documents/dataset/BOT_Game/test/test_patches'

