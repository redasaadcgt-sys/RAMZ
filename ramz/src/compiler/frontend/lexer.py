import compiler.language as lang


def skip_ignored(text, i):
    while i < len(text):
        
        # whitespace
        if text[i] in lang.WHITE_SPACE:
            i += 1
            continue

        # single line comments
        if text.startswith(lang.SINGLE_LINE_COMMENTS, i):
            while i < len(text) and text[i] != "\n":
                i += 1
            continue

        # multi line comments
        found_comment = False

        for start, end in lang.MULTI_LINE_COMMENTS:
            if text.startswith(start, i):
                found_comment = True
                i += len(start)

                while i < len(text) and not text.startswith(end, i):
                    i += 1

                if i >= len(text):
                    raise Exception("Unterminated comment")

                i += len(end)
                break

        if found_comment:
            continue

        # nothing to skip
        break

    return i


class Token:
    def __init__(self, type_, value=None):
        if type_ not in lang.TOKEN_TYPES:
            raise Exception(f"Unknown token type: {type_}")
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

def lexer(text):
    tokens = []
    i = 0
    stack = [] #checking levels

    while i < len(text):
        i = skip_ignored(text, i)
        if i >= len(text):
            break

        char = text[i]

        if char in lang.OPEN_GROUPS:
            stack.append(char)

        elif char in lang.CLOSE_GROUPS:
            if not stack:
                raise Exception(f"Unexpected '{char}'")

            expected_open = lang.CLOSE_GROUPS[char]

            if stack[-1] != expected_open:
                raise Exception(
                    f"Expected '{lang.OPEN_GROUPS[stack[-1]]}', got '{char}'"
                )

            stack.pop()

        if char == "\n":
            if not stack:
                tokens.append(Token("NEWLINE"))
            i += 1
            continue
            
        # number 
        if char.isdigit():
            num = ""

            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1

            if i < len(text) and text[i] == ".":
                num += "."
                i += 1

                if i >= len(text) or not text[i].isdigit():
                    raise Exception("Decimal needs digits after '.'")

                while i < len(text) and text[i].isdigit():
                    num += text[i]
                    i += 1

                token_type = "DECIMAL"

            else:
                token_type = "INT"

            
            if i < len(text) and text[i] not in lang.VALID_AFTER_NUMBER:
                raise Exception(
                    f"Invalid token : {num}{text[i]}"
                )

            tokens.append(Token(token_type, num))
            continue

        # string
        if char in lang.QUOTE_CHARS:
            quote = char
            string = ""
            i += 1

            while i < len(text) and text[i] != quote:

                if text[i] == "\\":
                    i += 1

                    if i >= len(text):
                        raise Exception("Invalid escape")

                    escape = text[i]

                    if escape not in lang.ESCAPES:
                        raise Exception(f"Unknown escape \\{escape}")

                    string += lang.ESCAPES[escape]

                else:
                    string += text[i]

                i += 1

            if i >= len(text):
                raise Exception("Unterminated string")

            i += 1

            tokens.append(Token("STRING", string))
            continue

        # identifier (x, print, abc)
        if char.isalpha() or char == "_":
            ident = ""
            while i < len(text) and (text[i].isalnum() or text[i] == "_"):
                ident += text[i]
                i += 1
            if ident in lang.KEYWORDS:
                value=ident
                if ident in ("True","False"):
                    value=ident=="True"
                tokens.append(Token(lang.KEYWORDS[ident] , value))
            else:
                tokens.append(Token("IDENT", ident))
            continue
        
        # symbols
        if char in lang.SYMBOLS:
            tokens.append(Token(lang.SYMBOLS[char]))
            i += 1
            continue

        # operations
        if text[i] in lang.OPERATOR_STARTERS:
            op = text[i]

            if i + 1 < len(text):
                possible = op + text[i + 1]

                if possible in lang.OPERATORS:
                    op = possible
                    i += 1

            tokens.append(Token(lang.OPERATORS[op]))
            i += 1
            continue

        raise Exception(f"Unknown character: {char}")

    return tokens