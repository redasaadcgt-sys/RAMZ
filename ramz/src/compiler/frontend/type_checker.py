import compiler.frontend.ast as ast


class TypeChecker:

    def check_binary(self, node, op):
        left_type = self.check(node.left)
        right_type = self.check(node.right)

        if left_type != right_type:
            raise Exception(
                f"Operator '{op}' cannot operate on {left_type} and {right_type}"
            )

        if left_type not in ("INT", "DECIMAL"):
            raise Exception(
                f"Operator '{op}' is not supported for {left_type}"
            )

        return left_type

    def check_comp(self, node, op):
        left_type = self.check(node.left)
        right_type = self.check(node.right)

        if left_type != right_type:
            raise Exception(
                f"Operator '{op}' cannot compare {left_type} and {right_type}"
            )

        return "BOOL"

    def check_logical(self, node, op):
        left_type = self.check(node.left)
        right_type = self.check(node.right)

        if left_type != "BOOL" or right_type != "BOOL":
            raise Exception(
                f"Operator '{op}' requires boolean operands, got {left_type} and {right_type}"
            )

        return "BOOL"

    def check_function_body(self, function):
        self.enter_scope()

        for param in function.params:
                self.declare_variable(
                    param.name,
                    param.type
                )
        return_type = "VOID"

        for statement in function.body:
            
            stmt_type = self.check(statement)
    
            if isinstance(statement, ast.Return):
                return_type = stmt_type
        
        self.exit_scope()

        if return_type != function.return_type:
            raise Exception(
                f"Function '{function.name}' expects return type "
                f"{function.return_type}, got {return_type}"
            )

        return return_type

    def check_value_for_void(self,node):
        if isinstance(node.value, ast.FunctionCall):
            if self.get_function(node.value.name).return_type == "VOID":
                raise Exception(
                    "Cannot assign void value"
                )

    def __init__(self):
        # variable name -> type
        self.scopes = [{
            "variables": {},
            "functions": {}
        }]
        self.checking_functions = set()      # denying recursion 

        self.variables = []
        self.functions = []
    
    def enter_scope(self):
        self.scopes.append({
                "variables": {},
                "functions": {}
            })

    def exit_scope(self):
        self.scopes.pop()

    def declare_variable(self, name, type_):
        variables = self.scopes[-1]["variables"]

        if name in variables:
            raise Exception(
                f"Variable '{name}' already declared in this scope"
            )

        variables[name] = type_

        self.variables.append({
            "name": name,
            "type": type_,
            "depth": len(self.scopes) - 1
        })

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            variables = scope["variables"]

            if name in variables:
                return variables[name]

        raise Exception(
            f"Variable '{name}' not declared"
        )

    def declare_function(self, function):
        functions = self.scopes[-1]["functions"]
  
        if function.name in functions:
            print(function.name)
            raise Exception(
                f"Function '{function.name}' already declared"
            )

        functions[function.name] = function

        self.functions.append({
            "name": function.name,
            "stack_depth": len(self.scopes) - 1
        })

    def get_function(self, name):
        for scope in reversed(self.scopes):
            functions = scope["functions"]

            if name in functions:
                return functions[name]

        raise Exception(
            f"Function '{name}' not declared"
        )

    def check_program(self, nodes):
        for node in nodes:
            node_type = self.check(node)

        return nodes, self.variables ,self.functions

    def check(self, node):

        # literals
        if isinstance(node, ast.Int):
            return "INT"

        if isinstance(node, ast.Decimal):
            return "DECIMAL"

        if isinstance(node, ast.String):
            return "STRING"

        if isinstance(node, ast.Bool):
            return "BOOL"


        # variable usage: x
        if isinstance(node, ast.Variable):
            return self.get_variable(node.name)


        # var x = expr
        if isinstance(node, ast.VarDecl):

            if node.value is None:
                raise Exception(
                    f"Variable '{node.name}' needs a value"
                )
        
            self.check_value_for_void(node)

            value_type = self.check(node.value)

            self.declare_variable(node.name, value_type)

            node.type = value_type

            return value_type


        # x = expr
        if isinstance(node, ast.Assign):
            variable = self.get_variable(node.name)

            self.check_value_for_void(node)
            
            value_type = self.check(node.value)
            old_type = variable

            if value_type != old_type:
                raise Exception(
                    f"Cannot assign {value_type} to {old_type}"
                )

            return old_type


        # operations
        if isinstance(node, ast.Add):
            return self.check_binary(node, "add")

        if isinstance(node, ast.Sub):
            return self.check_binary(node, "subtract")

        if isinstance(node, ast.Mul):
            return self.check_binary(node, "multiply")

        if isinstance(node, ast.Div):
            return self.check_binary(node, "divide")

        # -x
        if isinstance(node, ast.Negate):
            value_type = self.check(node.value)

            if value_type not in ("INT", "DECIMAL"):
                raise Exception(
                    f"Operator '-' cannot negate {value_type}"
                )

            return value_type

        # comparison
        if isinstance(node, ast.Compare):
            return self.check_comp(node, node.op)
        
        # logical not
        if isinstance(node, ast.Not):
            value_type = self.check(node.value)
            if value_type != "BOOL":
                raise Exception(
                    f"Operator 'not' requires boolean operand, got {value_type}"
                )
            return "BOOL"

        # logical and 
        if isinstance(node, ast.And):
            return self.check_logical(node, "and")

        # logical or
        if isinstance(node, ast.Or):
            return self.check_logical(node, "or")

        # if
        if isinstance(node, ast.If):
            condition_type = self.check(node.condition)

            if condition_type != "BOOL":
                raise Exception(
                    f"Condition of 'if' must be BOOL, got {condition_type}"
                )

            self.enter_scope()
            for statement in node.body:
                self.check(statement)
            self.exit_scope()

            for elif_statement in node.elifs:
                self.check(elif_statement)

            if node.else_body:

                self.enter_scope()
                for statement in node.else_body:
                    self.check(statement)
                self.exit_scope()

            return None

        # elif
        if isinstance(node, ast.Elif):
            condition_type = self.check(node.condition)

            if condition_type != "BOOL":
                raise Exception(
                    f"Condition of 'elif' must be BOOL, got {condition_type}"
                )

            self.enter_scope()
            for statement in node.body:
                self.check(statement)
            self.exit_scope()

            return None

        # while
        if isinstance(node, ast.While):
            condition_type = self.check(node.condition)

            if condition_type != "BOOL":
                raise Exception(
                    f"Condition of 'while' must be BOOL, got {condition_type}"
                )
                
            self.enter_scope()
            for statement in node.body:
                self.check(statement)
            self.exit_scope()

            return None

        # function
        if isinstance(node, ast.Function):

            return_count = sum(
                isinstance(stmt, ast.Return) for stmt in node.body)
   
            if return_count > 0 and not isinstance(node.body[-1], ast.Return):
                raise Exception(
                    "Return is expected to be the last statement"
                )
            
            if return_count > 1 :
                raise Exception(
                    "Cant have multiple returns"
                )
            

            self.declare_function(node)

            return None

        # return
        if isinstance(node, ast.Return):
            return self.check(node.value)

        # call
        if isinstance(node, ast.FunctionCall):

            function = self.get_function(node.name)

            if function.name in self.checking_functions:
                raise Exception(
                    f"Recursive call to '{function.name}' is not allowed"
                )

            if len(node.args) != len(function.params):
                raise Exception(
                    f"Function '{function.name}' expects {len(function.params)} arguments"
                )

            for param, arg in zip(function.params, node.args):
                arg_type = self.check(arg)

                if param.type is None:
                    param.type = arg_type

                elif param.type != arg_type:
                    raise Exception(
                        f"Function '{function.name}' parameter '{param.name}' "
                        f"expects {param.type}, got {arg_type}"
                )
            

            self.checking_functions.add(function.name)

            result = self.check_function_body(function)

            self.checking_functions.remove(function.name)
            
            return result

        # print(expr)
        if isinstance(node, ast.Print):
            return self.check(node.value)

        raise Exception(
            f"No type rule for {type(node).__name__}"
        )
    
    