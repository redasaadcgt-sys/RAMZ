import compiler.frontend.ast as ast

BUILTIN_CONSTANTS = {
    "INT_MAX": ast.Int(2147483647),
    "INT_MIN": ast.Int(-2147483648),

    "DEC_MAX": ast.Decimal(1.7976931348623157e308),
    "DEC_MIN": ast.Decimal(-1.7976931348623157e308),
    "HELLO_WORLD": ast.String("Hello from Ramz! This is a long test sentence designed to verify that string literals, spaces, punctuation marks, numbers like 12345, and special characters such as !@#$% are handled correctly by the compiler runtime.")
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0


    def current(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def eat(self, token_type):
        if self.current() and self.current().type == token_type:
            self.i += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current().type if self.current() else None}")

    def skip_newlines(self):
        while self.current() and self.current().type == "NEWLINE":
            self.eat("NEWLINE")

    def peek_non_newline(self):
        j = self.i
        while j < len(self.tokens) and self.tokens[j].type == "NEWLINE":
            j += 1
        return self.tokens[j] if j < len(self.tokens) else None

    def expect_statement_end(self):
        if not self.current() :
            return

        if self.current().type in ("SEMICOLON", "NEWLINE"):
            self.eat(self.current().type)
            self.skip_newlines()
            
        else:
            raise Exception(
                f"Expected ';' or NEWLINE after statement, got {self.current().type}"
            )

    def parse_condition_block(self, keyword):
        self.eat(keyword)

        if self.current() and self.current().type == "LPAREN":
            self.eat("LPAREN")
        else:
            raise Exception(
                f"Expected '(' after '{keyword}', got {self.current().type}"
            )

        condition = self.expr()

        if self.current() and self.current().type == "RPAREN":
            self.eat("RPAREN")
            self.skip_newlines()
        else:
            raise Exception(
                f"Expected ')' after condition, got {self.current().type}"
            )

        if self.current() and self.current().type == "LBRACE":
            self.eat("LBRACE")
        else:
            raise Exception(
                f"Expected '{{' after condition, got {self.current().type}"
            )

        body = self.block()

        if self.current() and self.current().type == "RBRACE":
            self.eat("RBRACE")
        else:
            raise Exception(
                f"Expected '}}' after block, got {self.current().type}"
            )

        return condition, body

    def parse_function_block(self):
        self.eat("FUNC")

        return_type ="None"
        if self.current() and self.current().type in (
            "INT",
            "DECIMAL",
            "BOOL",
            "STRING",
            "VOID"
        ):
            return_type = self.current().type
            self.eat(return_type)
        else:
           return_type = "VOID"

        name = "None" 
        if self.current() and self.current().type == "IDENT":
            name = self.current().value
            self.eat("IDENT")
        else:
            raise Exception(
                f"Expected 'name' after 'return type', got {self.current().type}"
            )

        params = self.parse_params()

        if self.current() and self.current().type == "LBRACE":
            self.eat("LBRACE")
        else:
            raise Exception(
                f"Expected '{{' after condition, got {self.current().type}"
            )

        body = self.block()

        if self.current() and self.current().type == "RBRACE":
            self.eat("RBRACE")
        else:
            raise Exception(
                f"Expected '}}' after block, got {self.current().type}"
            )

        return name, params, body, return_type

    def parse_params(self):

        if self.current() and self.current().type == "LPAREN":
            self.eat("LPAREN")
        else:
            raise Exception(
                f"Expected '(' after 'FUNCTION', got {self.current().type}"
            )
        params = []
        while self.current() and self.current().type == "IDENT":
            params.append(ast.Parameter(self.current().value))
            self.eat("IDENT")
            if self.current() and self.current().type != "RPAREN":
                if self.current() and self.current().type == "COMMA":
                    self.eat("COMMA")
                else:
                    raise Exception(
                        f"Expected ',' after parameter, got {self.current().type}"
                    )
        
        if self.current() and self.current().type == "RPAREN":
            self.eat("RPAREN")
            self.skip_newlines()
        else:
            raise Exception(
                f"Expected ')' after condition, got {self.current().type}"
            )

        return params

    def parse_args(self):
        if self.current() and self.current().type == "LPAREN":
            self.eat("LPAREN")
        else:
            raise Exception(
                f"Expected '(' after 'FUNCTION', got {self.current().type}"
            )
        args = []
        while self.current() and self.current().type != "RPAREN":
            args.append(self.expr())
            
            if self.current() and self.current().type != "RPAREN":
                if self.current() and self.current().type == "COMMA":
                    self.eat("COMMA")
                else:
                    raise Exception(
                        f"Expected ',' after argument, got {self.current().type}"
                    )
        
        if self.current() and self.current().type == "RPAREN":
            self.eat("RPAREN")
        else:
            raise Exception(
                f"Expected ')' after condition, got {self.current().type}"
            )
        return args

    def block(self):
        statements = []

        self.skip_newlines()

        while self.current() and self.current().type != "RBRACE":
            
            statements.append(self.statement())

            if self.current() and self.current().type != "RBRACE":
                self.expect_statement_end()

        return statements

    # entry point

    def parse(self):
        statements = []

        while self.current() :
            
            self.skip_newlines()
            
            statements.append(self.statement())
            
            self.expect_statement_end()

        return statements


    # statements

    def statement(self):
            
        tok = self.current()
        if not tok:
            return

        # var x
        if tok.type == "VAR" :
            self.eat("VAR")
            if self.current() and self.current().type == "IDENT":
                name = self.current().value
                self.eat("IDENT")
                if self.current() and self.current().type == "ASSIGN":
                    self.eat("ASSIGN")
                    expr = self.expr()
                    return ast.VarDecl(name=name,value=expr)
                else :
                    return ast.VarDecl(name=name)
            raise Exception(
                    f"Expected variable name after 'var', got {self.current().type if self.current() else 'EOF'}"
                )
        
        # assignment or variable / function call
        if tok.type == "IDENT":

            if (
                self.i + 1 < len(self.tokens)
                and self.tokens[self.i + 1].type == "ASSIGN"
            ):
                name = tok.value
                self.eat("IDENT")
                self.eat("ASSIGN")

                return ast.Assign(name, self.expr())
            return self.factor()

        # print(expr)
        if tok.type == "PRINT":
            self.eat("PRINT")
            if self.current() and self.current().type == "LPAREN":
                self.eat("LPAREN")
            else:
                raise Exception(
                    f"Expected '(' after 'print', got {self.current().type}"
                )
            expr = self.expr()
            if self.current() and self.current().type == "RPAREN":
                self.eat("RPAREN")
            else:
                raise Exception(
                    f"Expected ')' after 'print', got {self.current().type}"
                )
            return ast.Print(expr)
        
        # if statement
        if tok.type == "IF":

            if_condition, if_body = self.parse_condition_block("IF")

            elifs = []

            tok = self.peek_non_newline()
            if tok and (tok.type == "ELIF" or tok.type == "ELSE"):
                self.skip_newlines()
            
            while self.current() and self.current().type == "ELIF":
                condition, body = self.parse_condition_block("ELIF")
                elifs.append(ast.Elif(condition, body))

                tok = self.peek_non_newline()
                if tok and (tok.type == "ELIF" or tok.type == "ELSE"):
                    self.skip_newlines()

            else_body = None

            if self.current() and self.current().type == "ELSE":
                self.eat("ELSE")

                if self.current().type != "LBRACE":
                    raise Exception(
                        f"Expected '{{' after else, got {self.current().type}"
                    )

                self.eat("LBRACE")

                else_body = self.block()

                if self.current().type != "RBRACE":
                    raise Exception(
                        f"Expected '}}' after else, got {self.current().type}"
                    )

                self.eat("RBRACE")

            return ast.If(
                if_condition,
                if_body,
                elifs,
                else_body
            )

        # while loop
        if tok.type == "WHILE":
            while_condition, while_body = self.parse_condition_block("WHILE")
            return ast.While(while_condition, while_body)

        # function
        if tok.type == "FUNC":
            name, params, function_body, return_type = self.parse_function_block()
            return ast.Function(name, params, function_body, return_type)

        if tok.type == "RETURN":
            self.eat("RETURN")
            return ast.Return(self.expr())


        raise Exception(f"Invalid statement : {self.current().type} ")


    def expr(self):
        return self.logical_or()

    # -----------------------
    # expressions (logical op)
    # -----------------------
    def logical_or(self): 
        node = self.logical_and()
        while self.current() and self.current().type == "OR":
            self.eat("OR")

            right = self.logical_and()
            node = ast.Or(node, right)
        return node

    def logical_and(self): #compute before (or)
        node = self.comparison()
        while self.current() and self.current().type == "AND":
            self.eat("AND")

            right = self.comparison()
            node = ast.And(node, right)
        return node

    # -----------------------
    # comparison (>,>=,<,<=,==)
    # -----------------------
    def comparison(self):
        node = self.addition()

        while self.current() and self.current().type in (
            "EQUAL",
            "LESS",
            "LESS_EQUAL",
            "GREATER",
            "GREATER_EQUAL",
            "NOT_EQUAL"
        ):
            op = self.current().type
            self.eat(op)

            right = self.addition()

            node = ast.Compare(op, node, right)

        return node

    # -----------------------
    # additions (add / sub)
    # -----------------------
    def addition(self):
        node = self.term()

        while self.current() and self.current().type in (
            "PLUS",
            "MINUS"
        ):
            op = self.current().type
            self.eat(op)

            right = self.term()

            if op == "PLUS":
                node = ast.Add(node, right)
            else:
                node = ast.Sub(node, right)

        return node

    # -----------------------
    # terms (mul / div)
    # -----------------------
    def term(self):
        node = self.factor()
        while self.current() and self.current().type in ("MULTIPLY", "DIVIDE"):
            op = self.current().type
            self.eat(op)

            right = self.factor()

            if op == "MULTIPLY":
                node = ast.Mul(node, right)
            else:
                node = ast.Div(node, right)

        return node


        raise Exception("Invalid term")


    # -----------------------
    # factors (signs/values/not/()/constants)
    # -----------------------
    def factor(self):
        tok = self.current()
        if tok.type == "PLUS":
            self.eat("PLUS")
            return self.factor()

        if tok.type == "MINUS":
            self.eat("MINUS")
            return ast.Negate(self.factor())
            
        #values
        if tok.type == "INT":
            self.eat("INT")
            return ast.Int(tok.value)

        if tok.type == "DECIMAL":
            self.eat("DECIMAL")
            return ast.Decimal(tok.value)
        
        if tok.type == "STRING":
            self.eat("STRING")
            return ast.String(tok.value)
        
        if tok.type == "BOOL":
            self.eat("BOOL")
            return ast.Bool(tok.value)

        # variable
        if tok.type == "IDENT":
            name = tok.value
            self.eat("IDENT")

            if self.current() and self.current().type == "LPAREN":
                args = self.parse_args()
                return ast.FunctionCall(name, args)

            return ast.Variable(name)

        # constants
        if tok.type in BUILTIN_CONSTANTS:
            self.eat(tok.type)
            return BUILTIN_CONSTANTS[tok.value]

        # parentheses
        if tok.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node
        
        # not
        if tok.type == "NOT":
            self.eat("NOT")
            return ast.Not(self.factor())

        raise Exception("Invalid factor")