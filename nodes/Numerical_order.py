class NumericalOrder:
    """
    数值排序节点
    输入一组整数，按照从小到大的顺序排列后输出
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "numbers": ("INT", {"forceInput": True, "array": True}),
            }
        }

 

    RETURN_TYPES = ("INT",)
    RETURN_IS_LIST = (True,)
    RETURN_NAMES = ("sorted_numbers",)
    FUNCTION = "sort_numbers"
    CATEGORY = "comfyui_app/tools"

    def sort_numbers(self, numbers):
        # 过滤非整数元素
        filtered_numbers = [num for num in numbers if isinstance(num, int)]
        
        # 排序
        sorted_numbers = sorted(filtered_numbers)
        
        return (sorted_numbers,)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "comfyui_app:NumericalOrder": NumericalOrder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:NumericalOrder": "Numerical Order"
}

