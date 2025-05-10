import numpy as np
from PIL import Image
import torch
from scipy.ndimage import binary_fill_holes

def pil2mask(pil_image):
    """将单通道 PIL 图转换为 [0,1] 浮点张量"""
    arr = np.array(pil_image.convert("L"))  # uint8 0–255
    tensor = torch.from_numpy(arr.astype(np.float32) / 255.0)
    return tensor

class Fill_Mask:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"masks": ("MASK",)}}

    CATEGORY = "comfyui_app/mask"
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("MASKS",)
    FUNCTION = "fill_region"

    def fill_region(self, masks):
        # 如果是多张 mask
        def _process_one(mask_tensor):
            # 转为 uint8 阈值掩码
            mask_np = np.clip(255. * mask_tensor.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
            # 二值化
            binary = mask_np > 0
            # 填充内部孔洞
            filled = binary_fill_holes(binary)
            # 重建 PIL 图
            pil_img = Image.fromarray((filled * 255).astype(np.uint8), mode="L")
            # 转为 ComfyUI 需要的张量格式
            return pil2mask(pil_img).unsqueeze(0).unsqueeze(1)

        if masks.ndim > 3:
            regions = [_process_one(m) for m in masks]
            regions_tensor = torch.cat(regions, dim=0)
            return (regions_tensor,)
        else:
            region_tensor = _process_one(masks)
            return (region_tensor,)

NODE_CLASS_MAPPINGS = {"comfyui_app:Fill_Mask": Fill_Mask}
NODE_DISPLAY_NAME_MAPPINGS = {"comfyui_app:Fill_Mask": "Fill_Mask"}
