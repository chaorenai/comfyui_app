import torch
from PIL import Image
import numpy as np

class GetImageSize:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "image": ("IMAGE", ),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("INT", "INT", "BOX")
    RETURN_NAMES = ("width", "height",  "original_size")
    FUNCTION = 'get_image_size'
    CATEGORY = "comfyui_app/image"

    def tensor2pil(self, t_image: torch.Tensor) -> Image.Image:
        # 假设输入为 [B, H, W, C] 或 [1, H, W, C]
        np_img = t_image.cpu().numpy().squeeze()
        if np_img.shape[-1] == 1:
            np_img = np_img[..., 0]
        np_img = np.clip(255.0 * np_img, 0, 255).astype(np.uint8)
        return Image.fromarray(np_img)

    def get_image_size(self, image):
        if image.shape[0] > 0:
            image = torch.unsqueeze(image[0], 0)
        _image = self.tensor2pil(image)
        return (_image.width, _image.height, [_image.width, _image.height],)

NODE_CLASS_MAPPINGS = {
    "GetImageSize": GetImageSize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetImageSize": "GetImageSize"
}