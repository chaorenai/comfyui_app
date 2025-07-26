import sys

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_typ = AnyType("*")

class IntList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any_list": (any_typ,),  # 使用通配类型防止自动广播
                "index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": sys.maxsize,
                        "step": 1,
                        "tooltip": "从列表中提取第 N 项",
                    },
                ),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    FUNCTION = "doit"
    CATEGORY = "comfyui_app/video"
    INPUT_IS_LIST = True  # ⚠️ 必须加这一行！

    def doit(self, any_list, index):
        # index 会被包装为 [index]，所以取第一个
        i = index[0]


        # 边界判断
        if i >= len(any_list):
            val = any_list[-1]
        else:
            val = any_list[i]

        # 强制转换为 int
        try:
            val = int(val)
        except Exception as e:
            raise TypeError(f"提取出的值无法转为整数：{val}，错误：{e}")

        return (val,)

NODE_CLASS_MAPPINGS = {
    "comfyui_app:Int_List": IntList
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:Int_List": "IntList"
}
