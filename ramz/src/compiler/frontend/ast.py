# defining the tree structure


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"ADD({self.left}, {self.right})"

class Sub:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"SUB({self.left}, {self.right})"

class Mul:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"MUL({self.left}, {self.right})"

class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"DIV({self.left}, {self.right})"

class Negate:
    def __init__(self, value):
        self.value=value
    def __repr__(self):
        return f"NEGATE({self.value})"

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"ASSIGN({self.name}, {self.value})"

class Compare:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.op}({self.left}, {self.right})"
        
class Not:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NOT({self.value})"

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"AND({self.left}, {self.right})"

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"OR({self.left}, {self.right})"

class Print:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"PRINT({self.value})"

class Variable:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VARIABLE({self.name})"

class VarDecl:
    def __init__(self, name, type_=None, value=None):
        self.name = name
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"VARDECL({self.name},{self.type},{self.value})"

class If:
    def __init__(self, condition, body, elifs=None, else_body=None):
        self.condition = condition
        self.body = body
        self.elifs = elifs or []
        self.else_body = else_body

    def __repr__(self):
        return (
            f"IF({self.condition}, "
            f"{self.body}, "
            f"{self.elifs}, "
            f"{self.else_body})"
        )

class Elif:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"ELIF({self.condition}, {self.body})"

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WHILE({self.condition}, {self.body})"

class Function:
    def __init__(self, name, params=None, body=None, return_type=None):
        self.name = name
        self.params = params or []
        self.body = body or []
        self.return_type = return_type

    def __repr__(self):
        return (
            f"FUNCTION({self.name}, "
            f"{self.params}, "
            f"{self.body}), "
            f"{self.return_type}) "
        )

class Parameter:
    def __init__(self, name, type_=None):
        self.name = name
        self.type = type_

    def __repr__(self):
        return f"PARAM({self.name}, {self.type})"

class Return:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"RETURN({self.value})"


class FunctionCall:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def __repr__(self):
        return f"FUNCTIONCALL({self.name}, {self.args})"

class Int:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"INT({self.value})"

class Decimal:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"DECIMAL({self.value})"

class String:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"STRING({self.value})"

class Bool:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BOOL({self.value})"


