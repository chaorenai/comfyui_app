import torch
from PIL import Image
import numpy as np

MAX_RESOLUTION = 8192  # 可根据实际需求调整

class ResizeBySide:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "size": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                "mode": ("BOOLEAN", {"default": True, "label_on": "max", "label_off": "min"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "comfyui_app/image" 
    FUNCTION = "resize_by_side"

    def resize_by_side(self, images, size, mode):
        width = images.shape[2]
        height = images.shape[1]
        if mode:
            scale_by = size / max(width, height)
        else:
            scale_by = size / min(width, height)
        scale_by = min(scale_by, 1.0)
        new_width = int(width * scale_by)
        new_height = int(height * scale_by)
        results = []
        for image in images:
            img = self.tensor2pil(image).convert("RGB")
            img = img.resize((new_width, new_height), Image.LANCZOS)
            results.append(self.pil2tensor(img))
        return (torch.cat(results, dim=0),)

    @staticmethod
    def tensor2pil(image):
        if isinstance(image, torch.Tensor):
            image = image.detach().cpu().numpy()
        image = np.squeeze(image)
        image = np.clip(image * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(image)

    @staticmethod
    def pil2tensor(img):
        arr = np.array(img).astype(np.float32) / 255.0
        return torch.from_numpy(arr).unsqueeze(0)

    
NODE_CLASS_MAPPINGS = {
    "ResizeBySide": ResizeBySide
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResizeBySide": "ResizeBySide"
}
