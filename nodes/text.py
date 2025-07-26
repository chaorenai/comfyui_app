class Text:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(self):
        return {"required": {
                "text": ("STRING", {"multiline": True}),
            },}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = 'text_box_node'
    CATEGORY = "comfyui_app/tools"

    def text_box_node(self, text):
        return (text,)

NODE_CLASS_MAPPINGS = {
    "comfyui_app:Text": Text
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:Text": "Text"
}