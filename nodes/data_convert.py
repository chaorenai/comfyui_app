from typing import Any, Mapping
from .vec import VEC2_ZERO, VEC3_ZERO, VEC4_ZERO
from .types import Number, Vec2, Vec3, Vec4


class BoolToInt:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("BOOLEAN", {"default": False})}}

    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: bool) -> tuple[int]:
        return (int(a),)


class IntToBool:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("INT", {"default": 0})}}

    RETURN_TYPES = ("BOOLEAN",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: int) -> tuple[bool]:
        return (a != 0,)


class FloatToInt:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("FLOAT", {"default": 0.0, "round": False})}}

    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: float) -> tuple[int]:
        return (int(a),)


class IntToFloat:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("INT", {"default": 0})}}

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: int) -> tuple[float]:
        return (float(a),)


class IntToNumber:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("INT", {"default": 0})}}

    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: int) -> tuple[Number]:
        return (a,)


class NumberToInt:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("NUMBER", {"default": 0.0})}}

    RETURN_TYPES = ("INT",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: Number) -> tuple[int]:
        return (int(a),)


class FloatToNumber:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("FLOAT", {"default": 0.0, "round": False})}}

    RETURN_TYPES = ("NUMBER",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: float) -> tuple[Number]:
        return (a,)


class NumberToFloat:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("NUMBER", {"default": 0.0})}}

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: Number) -> tuple[float]:
        return (float(a),)


class ComposeVec2:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "x": ("FLOAT", {"default": 0.0, "round": False}),
                "y": ("FLOAT", {"default": 0.0, "round": False}),
            }
        }

    RETURN_TYPES = ("VEC2",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, x: float, y: float) -> tuple[Vec2]:
        return ((x, y),)


class FillVec2:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0, "round": False}),
            }
        }

    RETURN_TYPES = ("VEC2",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: float) -> tuple[Vec2]:
        return ((a, a),)


class BreakoutVec2:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("VEC2", {"default": VEC2_ZERO})}}

    RETURN_TYPES = ("FLOAT", "FLOAT")
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: Vec2) -> tuple[float, float]:
        return (a[0], a[1])


class ComposeVec3:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "x": ("FLOAT", {"default": 0.0}),
                "y": ("FLOAT", {"default": 0.0}),
                "z": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("VEC3",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, x: float, y: float, z: float) -> tuple[Vec3]:
        return ((x, y, z),)


class FillVec3:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("VEC3",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: float) -> tuple[Vec3]:
        return ((a, a, a),)


class BreakoutVec3:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("VEC3", {"default": VEC3_ZERO})}}

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT")
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: Vec3) -> tuple[float, float, float]:
        return (a[0], a[1], a[2])


class ComposeVec4:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "x": ("FLOAT", {"default": 0.0}),
                "y": ("FLOAT", {"default": 0.0}),
                "z": ("FLOAT", {"default": 0.0}),
                "w": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("VEC4",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, x: float, y: float, z: float, w: float) -> tuple[Vec4]:
        return ((x, y, z, w),)


class FillVec4:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = ("VEC4",)
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: float) -> tuple[Vec4]:
        return ((a, a, a, a),)


class BreakoutVec4:
    @classmethod
    def INPUT_TYPES(cls) -> Mapping[str, Any]:
        return {"required": {"a": ("VEC4", {"default": VEC4_ZERO})}}

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "FLOAT")
    FUNCTION = "op"
    CATEGORY = "comfyui_app/match/convert"

    def op(self, a: Vec4) -> tuple[float, float, float, float]:
        return (a[0], a[1], a[2], a[3])


NODE_CLASS_MAPPINGS = {
    "comfyui_app:BoolToInt": BoolToInt,
    "comfyui_app:IntToBool": IntToBool,
    "comfyui_app:FloatToInt": FloatToInt,
    "comfyui_app:IntToFloat": IntToFloat,
    "comfyui_app:IntToNumber": IntToNumber,
    "comfyui_app:NumberToInt": NumberToInt,
    "comfyui_app:FloatToNumber": FloatToNumber,
    "comfyui_app:NumberToFloat": NumberToFloat,
    "comfyui_app:ComposeVec2": ComposeVec2,
    "comfyui_app:ComposeVec3": ComposeVec3,
    "comfyui_app:ComposeVec4": ComposeVec4,
    "comfyui_app:BreakoutVec2": BreakoutVec2,
    "comfyui_app:BreakoutVec3": BreakoutVec3,
    "comfyui_app:BreakoutVec4": BreakoutVec4,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:BoolToInt": "BoolToInt",
    "comfyui_app:IntToBool": "IntToBool",
    "comfyui_app:FloatToInt": "FloatToInt",
    "comfyui_app:IntToFloat": "IntToFloat",
    "comfyui_app:IntToNumber": "IntToNumber",
    "comfyui_app:NumberToInt": "NumberToInt",
    "comfyui_app:FloatToNumber": "FloatToNumber",
    "comfyui_app:NumberToFloat": "NumberToFloat",
    "comfyui_app:ComposeVec2": "ComposeVec2",
    "comfyui_app:ComposeVec3": "ComposeVec3",
    "comfyui_app:ComposeVec4": "ComposeVec4",
    "comfyui_app:BreakoutVec2": "BreakoutVec2",
    "comfyui_app:BreakoutVec3": "BreakoutVec3",
    "comfyui_app:BreakoutVec4": "BreakoutVec4",
}