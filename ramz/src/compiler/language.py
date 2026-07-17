TOKEN_TYPES = {
    "INT",
    "DECIMAL",
    "STRING",
    "BOOL",
    "VOID",
    
    "MINUS",
    "PLUS",
    "MULTIPLY",
    "DIVIDE",
    
    "EQUAL",
    "NOT_EQUAL",
    "LESS",
    "LESS_EQUAL",
    "GREATER",
    "GREATER_EQUAL",
    "NOT",

    "AND",
    "OR",

    "ASSIGN",
    "IDENT",
    "VAR",

    "PRINT",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",

    "IF",
    "ELIF",
    "ELSE",
    "WHILE",
    "FUNC",
    "RETURN",

    "INT_TYPE",
    "DEC_TYPE",
    "BOOL_TYPE",
    "STR_TYPE",
    "VOID_TYPE",

    "INT_MAX",
    "INT_MIN",
    "DEC_MAX",
    "DEC_MIN",
    "HELLO_WORLD",

    "COMMA",
    "SEMICOLON",
    "NEWLINE"
}


OPEN_GROUPS = {
    "(": ")",
}
CLOSE_GROUPS = {v: k for k, v in OPEN_GROUPS.items()}


WHITE_SPACE = " \t\r" # exclude new line

SINGLE_LINE_COMMENTS = (
    "//",
    "#",
)

MULTI_LINE_COMMENTS = (
    ("/*", "*/"),
)

QUOTE_CHARS = {
    '"',
    "'"
}

ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    "\"": "\"",
    "'": "'",
    "0": "\0"
}

SYMBOLS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
    ",": "COMMA"
}

OPERATORS = {
    "=": "ASSIGN",
    "==": "EQUAL",
    "<": "LESS",
    "<=": "LESS_EQUAL",
    ">": "GREATER",
    ">=": "GREATER_EQUAL",
    "!": "NOT",
    "!=": "NOT_EQUAL",
}
OPERATOR_STARTERS = set(op[0] for op in OPERATORS)

KEYWORDS = {
    "var": "VAR",
    "print": "PRINT",
    "True": "BOOL",
    "False": "BOOL",
    "and": "AND",
    "or": "OR",
    "if": "IF",
    "elif": "ELIF",
    "else": "ELSE",
    "while": "WHILE",
    "function": "FUNC",
    "return": "RETURN",
    "int": "INT",
    "dec": "DECIMAL",
    "bool": "BOOL",
    "str": "STRING",
    "void": "VOID",

    "INT_MAX":"INT_MAX",
    "INT_MIN":"INT_MIN",
    "DEC_MAX":"INT_MAX",
    "DEC_MIN":"INT_MIN",
    "HELLO_WORLD":"HELLO_WORLD"
}

VALID_AFTER_NUMBER = {
    "+",
    "-",
    "*",
    "/",
    ")",
    "}",
    ";",
    " ",
    "\n",
    ",",
    *OPERATORS.keys()
}