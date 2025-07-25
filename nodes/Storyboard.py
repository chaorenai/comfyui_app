from inspect import cleandoc
import torch
import cv2
import numpy as np


class Storyboard:  # 定义提取关键帧的类
    @classmethod
    def INPUT_TYPES(s):  # 定义输入类型
        return {
            "required": {  # 必填参数
                "image": ("IMAGE",),  # 输入的图片序列
                "threshold": ("FLOAT", { "default": 0.1, "min": -1.0, "max": 1.00, "step": 0.01, }),
                "mergeInterFrames": ("INT", { "default": 10, "min": 0, "max": 999, "step": 1, }),  # 合并间隔帧数
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "INT")  # 返回类型：图片和字符串
    RETURN_NAMES = ("keyframes", "indexes_string", "indexes_int")  # 返回名称：关键帧和索引

    FUNCTION = "execute"  # 执行函数名
    CATEGORY = "comfyui_app/video"  # 节点分类

    def ssim(self, img1, img2, C1=0.01**2, C2=0.03**2):
        # 如果是彩色图像，先转为灰度
        if img1.shape[-1] == 3:
            img1 = 0.299 * img1[..., 0] + 0.587 * img1[..., 1] + 0.114 * img1[..., 2]
            img2 = 0.299 * img2[..., 0] + 0.587 * img2[..., 1] + 0.114 * img2[..., 2]
        # 计算均值
        mu1 = img1.mean()
        mu2 = img2.mean()
        # 计算方差
        sigma1 = ((img1 - mu1) ** 2).mean()
        sigma2 = ((img2 - mu2) ** 2).mean()
        # 计算协方差
        sigma12 = ((img1 - mu1) * (img2 - mu2)).mean()
        # 计算SSIM
        ssim = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1 + sigma2 + C2))
        # 保证结果在0~1之间
        return max(0.0, min(1.0, ssim.item()))

    def mse(self, img1, img2):
        """
        计算两张图片的均方误差（MSE）
        参数:
            img1, img2: 输入的两张图片，shape相同
        返回:
            mse: 均方误差，值越小越相似
        """
        # 如果是Tensor，先转为numpy
        if hasattr(img1, 'cpu') and hasattr(img1, 'numpy'):
            img1 = img1.cpu().numpy()
        if hasattr(img2, 'cpu') and hasattr(img2, 'numpy'):
            img2 = img2.cpu().numpy()
        # 如果是彩色图像，先转为灰度
        if img1.ndim == 3 and img1.shape[-1] == 3:
            img1 = 0.299 * img1[..., 0] + 0.587 * img1[..., 1] + 0.114 * img1[..., 2]
            img2 = 0.299 * img2[..., 0] + 0.587 * img2[..., 1] + 0.114 * img2[..., 2]
        # 保证类型为float32
        img1 = img1.astype(np.float32)
        img2 = img2.astype(np.float32)
        # 计算MSE
        mse_val = np.mean((img1 - img2) ** 2)
        return mse_val

    def execute(self, image,threshold, mergeInterFrames):
        # image: [B, H, W, C]
        B = image.shape[0]
        ssim_list = []
        for i in range(B-1):
            ssim_val = self.ssim(image[i], image[i+1]) # 计算相似度
            ssim_list.append(ssim_val)
        if not ssim_list:
            keyframes = [0]
            return (image[keyframes], ','.join(map(str, keyframes)),)
        print("ssim_list:", ssim_list)
        ssim_max = max(ssim_list)
        ssim_mean = sum(ssim_list) / len(ssim_list)
        ssim_limit = ssim_max - (ssim_max - ssim_mean) * 2 - threshold
        print("极限值：", ssim_limit)
        keyframes = [0]
        for i, ssim_val in enumerate(ssim_list):
            if ssim_val < ssim_limit:
                keyframes.append(i+1)
        print("keyframes:", keyframes)
        # 从前往后筛选，密集关键帧只保留最后一个
        filtered_keyframes = [keyframes[0]]
        for kf in keyframes[1:]:
            if kf - filtered_keyframes[-1] > mergeInterFrames:
                filtered_keyframes.append(kf)
            else:
                filtered_keyframes[-1] = kf  # 替换为更大的索引
        return (image[filtered_keyframes], ','.join(map(str, filtered_keyframes)), filtered_keyframes)

    def phash(self, img, hash_size=8):
        """
        计算图像的感知哈希（pHash）
        参数:
            img: 输入的图像，shape为(H, W, C)或(H, W)
            hash_size: 哈希大小，默认8
        返回:
            hash: 长度为hash_size*hash_size的01向量
        """
        # 如果是Tensor，先转为numpy
        if hasattr(img, 'cpu') and hasattr(img, 'numpy'):
            img = img.cpu().numpy()
        # 转为灰度
        if img.ndim == 3 and img.shape[-1] == 3:
            img = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]
        img = img.astype(np.float32)
        # 缩放到32x32
        img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
        # 进行DCT变换
        dct = cv2.dct(img)
        # 取左上角hash_size*hash_size的DCT系数
        dct_low_freq = dct[:hash_size, :hash_size]
        # 计算中值
        med = np.median(dct_low_freq)
        # 生成hash
        hash = (dct_low_freq > med).astype(np.uint8)
        return hash.flatten()

    def phash_similarity(self, img1, img2, hash_size=8):
        """
        计算两张图片的pHash相似度（归一化为0~1，1为完全相同）
        """
        hash1 = self.phash(img1, hash_size)
        hash2 = self.phash(img2, hash_size)
        # 汉明距离
        dist = np.count_nonzero(hash1 != hash2)
        similarity = 1 - dist / (hash_size * hash_size)
        return similarity

    def mse_similarity(self, img1, img2):
        """
        计算两张图片的MSE相似度，返回值归一化到0~1，1表示完全相同，0表示差异最大。
        """
        mse_val = self.mse(img1, img2)
        # 归一化，假设像素值范围为0~1
        # mse=0时相似度为1，mse=1时相似度为0
        similarity = 1.0 - min(1.0, mse_val)
        return similarity



NODE_CLASS_MAPPINGS = {
    "comfyui_app:Storyboard": Storyboard
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:Storyboard": "Storyboard"
}