import math
import ast
import operator as op
import re

class SimpleMath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "a": ("INT,FLOAT", { "default": 0.0, "step": 0.1 }),
                "b": ("INT,FLOAT", { "default": 0.0, "step": 0.1 }),
                "c": ("INT,FLOAT", { "default": 0.0, "step": 0.1 }),
            },
            "required": {
                "value": ("STRING", { "multiline": False, "default": "" }),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", )
    FUNCTION = "execute"
    CATEGORY = "comfyui_app/match"

    def preprocess_expression(self, value):
        # Replace implicit multiplication (e.g., "2a" -> "2 * a", "3b" -> "3 * b")
        value = re.sub(r'(\d+)([abc])', r'\1 * \2', value)
        # Handle cases like "2(a)" -> "2 * (a)"
        value = re.sub(r'(\d+)\(', r'\1 * (', value)
        # Handle cases like ")a" -> ") * a"
        value = re.sub(r'\)([abc])', r') * \1', value)
        return value

    def execute(self, value, a=0.0, b=0.0, c=0.0):
        # Preprocess the input string to handle implicit multiplication
        value = self.preprocess_expression(value)

        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.FloorDiv: op.floordiv,
            ast.Pow: op.pow,
            ast.BitXor: op.xor,
            ast.USub: op.neg,
            ast.Mod: op.mod,
        }

        op_functions = {
            'min': min,
            'max': max,
            'round': round,
            'sum': sum,
            'len': len,
        }

        def eval_(node):
            if isinstance(node, ast.Num):  # number
                return node.n
            elif isinstance(node, ast.Name):  # variable
                if node.id == "a":
                    return a
                if node.id == "b":
                    return b
                if node.id == "c":
                    return c
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return operators[type(node.op)](eval_(node.operand))
            elif isinstance(node, ast.Call):  # custom function
                if node.func.id in op_functions:
                    args = [eval_(arg) for arg in node.args]
                    return op_functions[node.func.id](*args)
            elif isinstance(node, ast.Subscript):  # indexing or slicing
                value = eval_(node.value)
                if isinstance(node.slice, ast.Constant):
                    return value[node.slice.value]
                else:
                    return 0
            else:
                return 0

        try:
            result = eval_(ast.parse(value, mode='eval').body)
        except SyntaxError as e:
            raise SyntaxError(f"Invalid expression: {value}. Ensure the expression is valid Python syntax (e.g., use '2 * a' instead of '2a'). Original error: {str(e)}")

        if math.isnan(result):
            result = 0.0
        
        return (round(result), result, )

NODE_CLASS_MAPPINGS = {
    "comfyui_app:SimpleMath": SimpleMath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_app:SimpleMath": "SimpleMath"
}