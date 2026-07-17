from llvmlite import ir
import compiler.ir.nodes as nodes

def declare_runtime_function(module, name, return_type, args):
    return ir.Function(
        module,
        ir.FunctionType(return_type, args),
        name=name
    )
def get_llvm_type(type_):

    if type_ == "INT":
        return ir.IntType(32)

    if type_ == "DECIMAL":
        return ir.DoubleType()

    if type_ == "STRING":
        return ir.PointerType(ir.IntType(8))

    if type_ == "BOOL":
        return ir.IntType(1)

    if type_ == "VOID":
        return ir.VoidType()
    
    raise Exception(f"Unknown type {type_}")
    
class LLVMGen:
    
    def emit_unary(self, op, value):
        if value.type == get_llvm_type("INT"):
            type_ = "INT"

        elif value.type == get_llvm_type("DECIMAL"):
            type_ = "DECIMAL"

        else:
            raise Exception(
                f"Unsupported unary operation on {value.type}"
            )

        return self.unary_ops[op][type_](self.builder, value)

    def emit_int_neg(builder, value):
        zero = ir.Constant(get_llvm_type("INT"), 0)
        return builder.sub(zero, value)
    
    def emit_binary(self, op, left, right):
        if left.type == get_llvm_type("INT"):
            type_ = "INT"

        elif  left.type == get_llvm_type("DECIMAL"):
            type_ = "DECIMAL"

        else:
            raise Exception(f"Unsupported type {left.type}")

        return self.binary_ops[op][type_](self.builder, left, right)

    def emit_compare(self, op, left, right):
        if left.type == get_llvm_type("INT"):
            type_ = "INT"

        elif left.type == get_llvm_type("DECIMAL"):
            type_ = "DECIMAL"

        elif left.type == get_llvm_type("BOOL"):
            type_ = "BOOL"

        else:
            raise Exception(f"Cannot compare {left.type}")

        return self.compare_ops[type_](
            self.builder,
            self.compare_predicates[op],
            left,
            right
        )

    def emit_not(builder, value):
        if value.type != get_llvm_type("BOOL"):
            raise Exception(
                f"Cannot NOT type {value.type}"
            )

        return self.builder.xor(
            value,
            ir.Constant(get_llvm_type("BOOL"), 1)
        )

    def emit_logical(self, op, left, right):
        bool_type = get_llvm_type("BOOL")
        if left.type != bool_type or right.type != bool_type:
            raise Exception(
                f"Operator '{op}' requires boolean operands, got {left.type} and {right.type}"
            )

        return self.logical_ops[op](self.builder, left, right)

    def emit_if(self, node):

        condition = self.visit(node.condition)

        if condition.type != get_llvm_type("BOOL"):
            raise Exception("If condition must be BOOL")

        then_block = self.func.append_basic_block("if_then")

        else_block = None
        if node.else_body:
            else_block = self.func.append_basic_block("if_else")

        end_block = self.func.append_basic_block("if_end")


        if else_block:
            self.builder.cbranch(
                condition,
                then_block,
                else_block
            )

            # THEN
            self.builder.position_at_end(then_block)

            self.enter_scope()
            for stmt in node.body:
                self.visit(stmt)
            self.exit_scope()

            if not self.builder.block.is_terminated:
                self.builder.branch(end_block)


            # ELSE
            self.builder.position_at_end(else_block)

            self.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.exit_scope()

            if not self.builder.block.is_terminated:
                self.builder.branch(end_block)


        else:
            self.builder.cbranch(
                condition,
                then_block,
                end_block
            )

            self.builder.position_at_end(then_block)

            self.enter_scope()
            for stmt in node.body:
                self.visit(stmt)
            self.exit_scope()

            if not self.builder.block.is_terminated:
                self.builder.branch(end_block)


        self.builder.position_at_end(end_block)

    def emit_while(self, node):

        cond_block = self.func.append_basic_block("while.cond")
        body_block = self.func.append_basic_block("while.body")
        end_block = self.func.append_basic_block("while.end")


        self.builder.branch(cond_block) # start at condition

        self.builder.position_at_end(cond_block)

        condition = self.visit(node.condition)

        self.builder.cbranch(
            condition,
            body_block,
            end_block
        )

        self.builder.position_at_end(body_block)

        self.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.exit_scope()

        # Loop back to the condition
        self.builder.branch(cond_block)

        self.builder.position_at_end(end_block)

    def emit_function(self, node):

        self.function_path.append(node.name)
        llvm_name = ".".join(self.function_path)
        
        function_type = ir.FunctionType(
            get_llvm_type(node.return_type),
            [
                get_llvm_type(param.type if param.type is not None else "INT")
                for param in node.params
            ]
        )

        function = ir.Function(
            self.module,
            function_type,
            name=llvm_name
        )

        # save current context
        old_builder = self.builder
        old_func = self.func

        entry = function.append_basic_block("entry")

        self.func = function
        self.builder = ir.IRBuilder(entry)

        self.declare_function(node.name,function)

        self.enter_scope()

        for param, llvm_arg in zip(node.params, function.args):

            ptr = self.builder.alloca(llvm_arg.type, name=param.name)
            self.builder.store(llvm_arg, ptr)

            self.declare_variable(param.name, ptr)

        for statement in node.body:
            self.visit(statement)

        # making sure LLVM block ends correctly
        if not self.builder.block.is_terminated:
            if node.return_type == "VOID":
                self.builder.ret_void()
            else:
                raise Exception(
                    f"Function '{node.name}' has no return"
                )

        self.exit_scope()

        # restore previous context
        self.builder = old_builder
        self.func = old_func

        self.function_path.pop()

        return function

    def emit_call(self, node):
        function = self.get_function(node.name)
        args = []

        for arg in node.args:
            args.append(
                self.visit(arg)
            )

        return self.builder.call(
            function,
            args
        )

    def create_string(self, text):
        data = bytearray(text.encode("utf8")) + b"\0"   # convert to bytes + null terminator

        const = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(data)),     # create array of one byte
            data
        )

        name = f".str{len(self.module.globals)}"

        global_str = ir.GlobalVariable(                 # create a global constant
            self.module,
            const.type,
            name=name
        )

        global_str.global_constant = True
        global_str.initializer = const

        return global_str

    def enter_scope(self):
        self.scopes.append({
            "variables": {},
            "functions": {}
        })

    def exit_scope(self):
        self.scopes.pop()

    def declare_variable(self, name, ptr):
        scope = self.scopes[-1]["variables"]

        if name in scope:
            raise Exception(f"Variable {name} already exists")

        scope[name] = ptr

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope["variables"]:
                return scope["variables"][name]

        raise Exception(f"Undefined variable {name}")

    def declare_function(self, name, function):
        scope = self.scopes[-1]["functions"]

        if name in scope:
            raise Exception(f"Function {name} already exists")

        scope[name] = function

    def get_function(self, name):
        for scope in reversed(self.scopes):
            if name in scope["functions"]:
                return scope["functions"][name]

        raise Exception(f"Undefined function {name}")

    def __init__(self):
        self.module = ir.Module(name="ramz")   
        self.module.triple = "x86_64-pc-windows-msvc19.50.35730" 
        self.func = None                        
        self.builder = None                     
        self.scopes = [{
            "variables": {},
            "functions": {}
        }]
        self.function_path = []

        self.runtime = {
            "print_int": declare_runtime_function(
                self.module,
                "print_int",
                ir.VoidType(),
                [get_llvm_type("INT")]
            ),

            "print_decimal": declare_runtime_function(
                self.module,
                "print_decimal",
                ir.VoidType(),
                [get_llvm_type("DECIMAL")]
            ),

            "print_string": declare_runtime_function(
                self.module,
                "print_string",
                ir.VoidType(),
                [get_llvm_type("STRING")]
            ),

            "print_boolean": declare_runtime_function(
                self.module,
                "print_boolean",
                ir.VoidType(),
                [get_llvm_type("BOOL")]
            )
        }


    def create_main(self):
        func_type = ir.FunctionType(get_llvm_type("INT"), [])
        self.func = ir.Function(self.module, func_type, name="main")

        block = self.func.append_basic_block("entry")
        self.builder = ir.IRBuilder(block)
        self.binary_ops = {
            "ADD": {
                "INT": ir.IRBuilder.add,
                "DECIMAL": ir.IRBuilder.fadd,
            },

            "SUB": {
                "INT": ir.IRBuilder.sub,
                "DECIMAL": ir.IRBuilder.fsub,
            },

            "MUL": {
                "INT": ir.IRBuilder.mul,
                "DECIMAL": ir.IRBuilder.fmul,
            },

            "DIV": {
                "INT": ir.IRBuilder.sdiv,
                "DECIMAL": ir.IRBuilder.fdiv,
            }
        }
        self.compare_ops = {
            "INT": ir.IRBuilder.icmp_signed,
            "BOOL": ir.IRBuilder.icmp_unsigned,
            "DECIMAL": ir.IRBuilder.fcmp_ordered,
        }
        self.compare_predicates = {
            "EqualIR": "==",
            "NotEqualIR": "!=",
            "LessIR": "<",
            "LessEqualIR": "<=",
            "GreaterIR": ">",
            "GreaterEqualIR": ">="
        }
        self.logical_ops = {
            "AND": ir.IRBuilder.and_,
            "OR": ir.IRBuilder.or_
        }
        self.unary_ops = {
            "NEGATE": {
                "INT": LLVMGen.emit_int_neg,
                "DECIMAL": ir.IRBuilder.fneg,
            },
            "NOT": {
                "BOOL": LLVMGen.emit_not
            }
        }


    def compile_ir(self, node):
        self.create_main()

        for stmt in node:
            self.visit(stmt)

        self.builder.ret(ir.Constant(get_llvm_type("INT"), 0)) #return
        return self.module


    def visit(self, node):

        # NUMBER
        if isinstance(node, nodes.IntIR):
            return ir.Constant(get_llvm_type("INT"), node.value)
        if isinstance(node, nodes.DecimalIR):
            return ir.Constant(get_llvm_type("DECIMAL"), node.value)

        #STRING
        if isinstance(node, nodes.StringIR):
            global_str = self.create_string(node.value)

            return self.builder.bitcast(
            global_str,
            get_llvm_type("STRING")
            )

        #BOOLEAN
        if isinstance(node, nodes.BoolIR):
            return ir.Constant(get_llvm_type("BOOL"), node.value)

        # ADD
        if isinstance(node, nodes.AddIR):
            return self.emit_binary(
                "ADD",
                self.visit(node.left),
                self.visit(node.right)
            )

        # SUB
        if isinstance(node, nodes.SubIR):
            return self.emit_binary(
                "SUB",
                self.visit(node.left),
                self.visit(node.right)
            )

        # MUL
        if isinstance(node, nodes.MulIR):
            return self.emit_binary(
                "MUL",
                self.visit(node.left),
                self.visit(node.right)
            )

        # DIV
        if isinstance(node, nodes.DivIR):
            return self.emit_binary(
                "DIV",
                self.visit(node.left),
                self.visit(node.right)
            )
        
        # NEGATE
        if isinstance(node, nodes.NegateIR):
            return self.emit_unary(
                "NEGATE",
                self.visit(node.value)
            )

        # COMPARE
        if isinstance(node, nodes.CompareIR):
            return self.emit_compare(
                node.op,
                self.visit(node.left),
                self.visit(node.right)
            )

        # NOT
        if isinstance(node, nodes.NotIR):
            return self.emit_not(
                self.visit(node.value)
            )

        # LOGICAL AND
        if isinstance(node, nodes.AndIR):
            return self.emit_logical(
                "AND",
                self.visit(node.left),
                self.visit(node.right)
            )

        # LOGICAL OR
        if isinstance(node, nodes.OrIR):
            return self.emit_logical(
                "OR",
                self.visit(node.left),
                self.visit(node.right)
            )
        
        # DECLARE (var x = expr)
        if isinstance(node, nodes.VarDeclIR):
            
            value = self.visit(node.value)
            
            ptr = self.builder.alloca(get_llvm_type(type_=node.type), name=node.name) # create storage
            self.builder.store(value, ptr)                                            # store the value

            self.declare_variable(node.name, ptr)
            return value

        # ASSIGN (x = expr)
        if isinstance(node, nodes.AssignIR):
            value = self.visit(node.value)
            
            ptr = self.get_variable(node.name)
            self.builder.store(value, ptr)
            return value

        # VARIABLE READ (x)
        if isinstance(node, nodes.VariableIR):
            ptr = self.get_variable(node.name)
            return self.builder.load(ptr)

        # if statement
        if isinstance(node, nodes.IfIR):
            return self.emit_if(node)

        # while loop
        if isinstance(node, nodes.WhileIR):
            return self.emit_while(node)

        # function declaration
        if isinstance(node, nodes.FunctionIR):
            return self.emit_function(node)

        # return
        if isinstance(node, nodes.ReturnIR):
            if node.value is None:
                self.builder.ret_void()
                return None

            value = self.visit(node.value)

            self.builder.ret(value)
            return value

        # function call
        if isinstance(node, nodes.FunctionCallIR):
            return self.emit_call(node)

        # PRINT
        if isinstance(node, nodes.PrintIR):
            value = self.visit(node.value)

            if value.type == get_llvm_type("INT"):
                func = self.runtime["print_int"]

            elif value.type == get_llvm_type("DECIMAL"):
                func = self.runtime["print_decimal"]

            elif value.type == get_llvm_type("BOOL"):
                func = self.runtime["print_boolean"]

            elif value.type == get_llvm_type("STRING"):
                func = self.runtime["print_string"]

            else:
                raise Exception(f"Cannot print type {value.type}")

            self.builder.call(func, [value])
            return value

        raise TypeError(f"Unknown IR node: {type(node)}")

        