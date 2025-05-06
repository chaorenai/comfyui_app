import importlib
import os

# ComfyUI 要求的两个导出变量
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 可选：序列化函数（调试或导出时防止类型崩溃）
def serialize(obj):
    if isinstance(obj, (str, int, float, bool, list, dict, type(None))):
        return obj
    return str(obj)

# 获取 nodes 子目录路径
current_dir = os.path.dirname(__file__)
nodes_dir = os.path.join(current_dir, "nodes")

# 遍历 nodes/*.py 文件（排除 __init__.py 等）
for file in os.listdir(nodes_dir):
    if file.endswith(".py") and not file.startswith("__"):
        module_name = file[:-3]  # 去掉 .py 后缀
        module_path = f"{__name__}.nodes.{module_name}"

        try:
            mod = importlib.import_module(module_path)
            # 合并该文件中定义的映射
            NODE_CLASS_MAPPINGS.update(mod.NODE_CLASS_MAPPINGS)
            NODE_DISPLAY_NAME_MAPPINGS.update(mod.NODE_DISPLAY_NAME_MAPPINGS)
        except Exception as e:
            print(f"[comfyui_app] Failed to import {module_path}: {e}")

# 可选：若你有 JS 控件前端扩展目录
# WEB_DIRECTORY = os.path.join(current_dir, "web")

# 限制暴露变量
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
