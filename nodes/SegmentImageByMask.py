import torch

class SegmentImageByMask:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mask": ("MASK",),
                "method": (["default", "invert"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "comfyui_app/image" 

    def node(self, images, mask, method):
        img_count, img_height, img_width = images[:, :, :, 0].shape
        
        # Handle mask shape flexibly
        if mask.ndim == 4 and mask.shape[1] == 1:
            # If mask is (batch, 1, height, width), squeeze the channel dimension
            mask = mask.squeeze(1)
            # Now mask should be (batch, height, width)

        if mask.ndim == 3:
            mask_count, mask_height, mask_width = mask.shape
        elif mask.ndim == 2:
            mask_count = 1 
            mask_height, mask_width = mask.shape
        else:
            raise ValueError(
                f"[SegmentImageByMask]: Unexpected mask dimension after potential squeeze: {mask.ndim}. Expected 2 or 3 dimensions. Original mask shape: {mask.shape}"
            )

        if mask_width == 64 and mask_height == 64: # This condition might need re-evaluation based on how you handle default/placeholder masks
            mask = torch.zeros((img_count, img_height, img_width))
        else:
            if img_height != mask_height or img_width != mask_width:
                raise ValueError(
                    "[SegmentImageByMask]: Size of images not equals size of mask. " +  # Updated class name here
                    "Images: [" + str(img_width) + ", " + str(img_height) + "] - " +
                    "Mask: [" + str(mask_width) + ", " + str(mask_height) + "]."
                )

        if img_count != mask_count:
            mask = mask.expand((img_count, -1, -1))

        if method == "default":
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    1. - mask[i]
                ), dim=-1) for i in range(len(images))
            ]),)
        else:
            return (torch.stack([
                torch.stack((
                    images[i, :, :, 0],
                    images[i, :, :, 1],
                    images[i, :, :, 2],
                    mask[i]
                ), dim=-1) for i in range(len(images))
            ]),)


class AlphaChanelAsMask:
    def __init__(self):
        pass

NODE_CLASS_MAPPINGS = {
    "comfyui_app:SegmentImageByMask": SegmentImageByMask
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:SegmentImageByMask": "SegmentImageByMask"
}
