class IntBatchSize:
    @classmethod
    def INPUT_TYPES(s):  # 定义输入类型
        return {
            "required": {  # 必填参数
                "ints": ("INT",),  # 输入的整数集合
            }
        }

    RETURN_TYPES = ("INT",)  # 返回类型：整数（尺寸）
    RETURN_NAMES = ("ints_size",)  # 返回名称：尺寸

    FUNCTION = "execute"  # 执行函数名
    CATEGORY = "comfyui_app/video"  # 节点分类

 
    def execute(self, ints):
        return (len(ints),)

NODE_CLASS_MAPPINGS = {
    "comfyui_app:IntBatchSize": IntBatchSize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:IntBatchSize": "IntBatchSize"
}