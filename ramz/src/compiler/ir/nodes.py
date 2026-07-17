COMPARE_IR_OPS = {
    "EQUAL": "EQUAL_IR",
    "NOT_EQUAL": "NOT_EQUAL_IR",
    "LESS": "LESS_IR",
    "LESS_EQUAL": "LESS_EQUAL_IR",
    "GREATER": "GREATER_IR",
    "GREATER_EQUAL": "GREATER_EQUAL_IR",
}

class AddIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"AddIR({self.left}, {self.right})"

class SubIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"SubIR({self.left}, {self.right})"

class MulIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"MulIR({self.left}, {self.right})"

class DivIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"DivIR({self.left}, {self.right})"

class NegateIR:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NegateIR({self.value})"
    
class AssignIR:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"AssignIR({self.name}, {self.value})"

class CompareIR:
    def __init__(self, op, left, right):
        parts = op.lower().split("_")
        self.op = "".join(part.capitalize() for part in parts) + "IR"
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.op}({self.left}, {self.right})"
        
class NotIR:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NotIR({self.value})"

class AndIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"AndIR({self.left}, {self.right})"

class OrIR:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"OrIR({self.left}, {self.right})"

class PrintIR:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintIR({self.value})"

class VariableIR:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableIR({self.name})"

class VarDeclIR:
    def __init__(self, name, type_=None, default=None):
        self.name = name
        self.type = type_
        self.value = default

    def __repr__(self):
        return f"VarDeclIR({self.name},{self.type},{self.value})"

class IfIR:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return (
            f"IfIR({self.condition}, "
            f"{self.body}, "
            f"{self.else_body})"
        )

class WhileIR:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileIR({self.condition}, {self.body})"

class FunctionIR:
    def __init__(self, name, params=None, body=None, return_type=None):
        self.name = name
        self.params = params or []
        self.body = body or []
        self.return_type = return_type

    def __repr__(self):
        return (
            f"FunctionIR({self.name}, "
            f"{self.params}, "
            f"{self.body}), "
            f"{self.return_type}) "
        )

class ParameterIR:
    def __init__(self, name, type_=None):
        self.name = name
        self.type = type_

    def __repr__(self):
        return f"ParamIR({self.name}, {self.type})"

class ReturnIR:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnIR({self.value})"


class FunctionCallIR:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def __repr__(self):
        return f"FunctionCallIR({self.name}, {self.args})"

class IntIR:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntIR({self.value})"

class DecimalIR:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"DecimalIR({self.value})"

class StringIR:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringIR({self.value})"

class BoolIR:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BoolIR({self.value})"
