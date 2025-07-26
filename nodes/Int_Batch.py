class IntBatch:
    @classmethod
    def INPUT_TYPES(s):  # 定义输入类型
        return {
            "required": {  # 必填参数
                "ints": ("INT",),  # 输入的整数集合
                "int_index": ("INT",),  # 输入的索引
            }
        }

    RETURN_TYPES = ("INT",)  # 返回类型：该索引的整数
    RETURN_NAMES = ("int",)  # 返回名称：该索引的整数

    FUNCTION = "execute"  # 执行函数名
    CATEGORY = "comfyui_app/video"  # 节点分类

    def execute(self, ints, int_index):
        
        # 边界检查
        if int_index >= len(ints):
            val = ints[-1]  # 如果索引超出范围，返回最后一个元素
        else:
            val = ints[int_index]  # 正常返回指定索引的元素

        return (val,)

NODE_CLASS_MAPPINGS = {
    "comfyui_app:IntBatch": IntBatch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:IntBatch": "IntBatch"
}