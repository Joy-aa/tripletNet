import numpy as np
import os
import cv2

# 数据读入
image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


# type(image_types) = tuple

def list_images(basePath, contains=None):
    # 返回有效的图片路径
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        # 循环遍历当前目录中的所有dir
        for filename in filenames:
            # 如果contains为None就不会进入后半部分，避免报错
            if contains is not None and filename.find(contains) == -1:
                continue

            # 确定文件中的拓展名
            ext = filename[filename.rfind("."):].lower()

            # 检查文件是否为图像，若是图像加入生成器中
            if image_types is None or ext.endswith(image_types):
                imagePath = os.path.join(rootDir, filename)
                yield imagePath

def load_data(path):
    # 开始读取数据
    data = []
    labels = []
    imagePaths = list_images("./test_dataset")

    for imagePath in imagePaths:
        # 读取图像数据
        image = cv2.imread(imagePath)
        # 可以降低图像像素点，下采样
        image = cv2.resize(image, (28, 28))
        # 转换成灰度图
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        data.append(image)
        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)
    return data, labels

# 对图像进行完scale操作之后可以看到与原图像保持了一致
data = np.array(data, dtype='float') / 255;
labels = np.array(labels)
