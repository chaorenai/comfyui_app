# -*- coding: utf-8 -*-
from comfy.comfy_types import IO, ComfyNodeABC, InputTypeDict # Removed unused imports
from PIL import Image, ImageOps # Removed unused ImageSequence
import node_helpers
import numpy as np
import torch

class FillConditioning(ComfyNodeABC): # Added class definition
    @classmethod
    def INPUT_TYPES(s): # Corrected indentation and class context
        return {"required": {"In_context": ("CONDITIONING",),
                             "negative": ("CONDITIONING",),
                             "vae": ("VAE",),
                             "diptych": ("IMAGE",),
                             "maskDiptych": ("MASK",),
                            #  "maskDiptych": ("BOOLEAN", {"default": True,
                            #                             "tooltip": "Add a noise mask to the latent so sampling will only happen within the mask. Might improve results or completely break things depending on the model."}),
                             }}

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "LATENT")
    RETURN_NAMES = ("In_context", "negative", "latent")
    FUNCTION = "encode"

    CATEGORY = "comfyui_app/tools"

    def encode(self, In_context, negative, diptych, vae, maskDiptych): # Corrected indentation and class context
        x = (diptych.shape[1] // 8) * 8
        y = (diptych.shape[2] // 8) * 8
        print('before')
        maskDiptych = torch.nn.functional.interpolate(maskDiptych.reshape((-1, 1, maskDiptych.shape[-2], maskDiptych.shape[-1])),size=(diptych.shape[1], diptych.shape[2]), mode="bilinear")

        print('after')
        orig_pixels = diptych
        diptych = orig_pixels.clone()
        if diptych.shape[1] != x or diptych.shape[2] != y:
            x_offset = (diptych.shape[1] % 8) // 2
            y_offset = (diptych.shape[2] % 8) // 2
            diptych = diptych[:, x_offset:x + x_offset, y_offset:y + y_offset, :]
            maskDiptych = maskDiptych[:, :, x_offset:x + x_offset, y_offset:y + y_offset]
        # why?
        m = (1.0 - maskDiptych.round()).squeeze(1)
        for i in range(3):
            diptych[:,:,:,i] -= 0.5
            diptych[:,:,:,i] *= m
            diptych[:,:,:,i] += 0.5
            
        concat_latent = vae.encode(diptych)
        orig_latent = vae.encode(orig_pixels)

        out_latent = {}

        out_latent["samples"] = orig_latent
        out_latent["noise_mask"] = maskDiptych


        # c = node_helpers.conditioning_set_values(In_context, {"concat_latent_image": concat_latent,
        #                                                             "concat_mask": maskDiptych})


        out = []
        for conditioning in [In_context, negative]:
            c = node_helpers.conditioning_set_values(conditioning, {"concat_latent_image": concat_latent,
                                                                    "concat_mask": maskDiptych})
            out.append(c)
        return (out[0], out[1], out_latent)#return (c, out_latent)

NODE_CLASS_MAPPINGS = {
    "comfyui_app:FillConditioning": FillConditioning
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:FillConditioning": "FillConditioning"
}