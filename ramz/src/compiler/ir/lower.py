import compiler.ir.nodes as nodes
import compiler.frontend.ast as ast


def generate_ir(node):
    if isinstance(node, ast.Add):
        return nodes.AddIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.Sub):
        return nodes.SubIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.Mul):
        return nodes.MulIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.Div):
        return nodes.DivIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.Negate):
        return nodes.NegateIR(
            generate_ir(node.value)
        )

    if isinstance(node, ast.Assign):
        return nodes.AssignIR(
            node.name,
            generate_ir(node.value)
        )

    if isinstance(node, ast.Compare):
        return nodes.CompareIR(
            node.op,
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.Not):
        return nodes.NotIR(
            generate_ir(node.value)
        )

    if isinstance(node, ast.And):
        return nodes.AndIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )
    
    if isinstance(node, ast.Or):
        return nodes.OrIR(
            generate_ir(node.left),
            generate_ir(node.right)
        )

    if isinstance(node, ast.If):                                    # turning it into (if/else) branshes
        if_body = [ generate_ir(stmt) for stmt in node.body ]

        # start with else
        else_body = None

        if node.else_body:
            else_body = [ generate_ir(stmt) for stmt in node.else_body ]

        # build elif chain backwards
        for elif_node in reversed(node.elifs):
            else_body = [
                nodes.IfIR(
                    generate_ir(elif_node.condition),
                    [ generate_ir(stmt) for stmt in elif_node.body ],
                    else_body
                )
            ]

        return nodes.IfIR(
            generate_ir(node.condition),
            if_body,
            else_body
        )
            
    if isinstance(node, ast.While):
        while_body = [ generate_ir(stmt) for stmt in node.body ]

        return nodes.WhileIR(
            generate_ir(node.condition),
            while_body
        )
    
    if isinstance(node, ast.Function):
        function_body = [ generate_ir(stmt) for stmt in node.body ]
        function_param = [ generate_ir(stmt) for stmt in node.params ]


        return nodes.FunctionIR(
            node.name,
            function_param,
            function_body,
            node.return_type
        )

    if isinstance(node, ast.Parameter):
        return nodes.ParameterIR(node.name, node.type)

    if isinstance(node, ast.Return):
        return nodes.ReturnIR(generate_ir(node.value))

    if isinstance(node, ast.FunctionCall):
        args = [ generate_ir(stmt) for stmt in node.args ]

        return nodes.FunctionCallIR(
            node.name,
            args
        )

    if isinstance(node, ast.Print):
        return nodes.PrintIR(
            generate_ir(node.value)
        )

    if isinstance(node, ast.Variable):
        return nodes.VariableIR(
            node.name
        )

    if isinstance(node, ast.VarDecl):
        return nodes.VarDeclIR(
            node.name,
            node.type,
            generate_ir(node.value)
        )

    if isinstance(node, ast.Int):
        return nodes.IntIR(node.value)

    if isinstance(node, ast.Decimal):
        return nodes.DecimalIR(node.value)

    if isinstance(node, ast.String):
        return nodes.StringIR(node.value)

    if isinstance(node, ast.Bool):
        return nodes.BoolIR(node.value)

    raise TypeError(f"Unknown node type: {type(node)}")



def generate_lower(ast_nodes):
    return [generate_ir(node) for node in ast_nodes]