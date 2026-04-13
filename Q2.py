print ("Q2 starts here")
print ("Q2 starts here")
# --Q2 Part1 Aaron Menezes--
def tokenize(expr):
    tokens = []
    i = 0

    # loop through the entire expression character by character
    while i < len(expr):
        c = expr[i]

        # skip spaces (ignore whitespace)
        if c.isspace():
            i += 1
            continue

        # handle numbers (including decimals like 3.14)
        if c.isdigit() or c == '.':
            num = c
            i += 1
            # keep reading until the number ends
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(("NUM", float(num)))  # store as float
            continue

        # handle operators + - * /
        if c in '+-*/':
            tokens.append(("OP", c))
            i += 1
            continue

        # handle left parenthesis
        if c == '(':
            tokens.append(("LPAREN", c))
            i += 1
            continue

        # handle right parenthesis
        if c == ')':
            tokens.append(("RPAREN", c))
            i += 1
            continue

        # if character is not valid, throw an error
        raise ValueError("Invalid character")

    # add END token to mark end of input
    tokens.append(("END", None))
    return tokens


#   PARSER IMPLEMENTATION

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # keeps track of current position in token list

    # returns the current token without moving forward
    def current(self):
        return self.tokens[self.pos]

    # consumes the current token and moves to next
    def eat(self, expected_type=None):
        token = self.current()
        # if expected type is given, check it matches
        if expected_type and token[0] != expected_type:
            raise ValueError("Unexpected token")
        self.pos += 1
        return token
    
#    EXPRESSION LEVEL(+,-)

    # handles addition and subtraction
    def parse_expression(self):
        node = self.parse_term()  # start with term

        # keep checking for + or - operators
        while self.current()[0] == "OP" and self.current()[1] in "+-":
            op = self.eat("OP")[1]
            right = self.parse_term()

            # build AST node for binary operation
            node = {
                "type": "binop",
                "op": op,
                "left": node,
                "right": right
            }

        return node
    
#  TERM LEVEL(*,/)

    # handles multiplication and division (higher precedence)
    def parse_term(self):
        node = self.parse_factor()

        # keep checking for * or / operators
        while self.current()[0] == "OP" and self.current()[1] in "*/":
            op = self.eat("OP")[1]
            right = self.parse_factor()

            # build AST node
            node = {
                "type": "binop",
                "op": op,
                "left": node,
                "right": right
            }

        return node
    
#  FACTOR

    # handles unary operations and passes control to primary
    def parse_factor(self):
        token = self.current()

        # unary minus (e.g., -5)
        if token[0] == "OP" and token[1] == "-":
            self.eat("OP")
            operand = self.parse_factor()  # recursive call

        # unary plus is not allowed (as per requirement)
        if token[0] == "OP" and token[1] == "+":
            raise ValueError("Unary + not allowed")
            return {
                "type": "neg",
                "value": operand
            }

        # otherwise, parse a normal value
        return self.parse_primary()

# PRIMARY

    # handles numbers and expressions inside parentheses
    def parse_primary(self):
        token = self.current()

        # if it's a number, return it as a node
        if token[0] == "NUM":
            self.eat("NUM")
            return {
                "type": "num",
                "value": token[1]
            }

        # if it's a parenthesized expression
        if token[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expression()  # parse inside brackets
            self.eat("RPAREN")  # expect closing bracket
            return node

        # anything else is invalid syntax
        raise ValueError("Invalid syntax")
    

# wrapper function to start parsing
def parse(tokens):
    parser = Parser(tokens)
    ast = parser.parse_expression()

    # after parsing, we should be at END token
    if parser.current()[0] != "END":
     raise ValueError("Extra input")
    return ast


# TEST 

if __name__ == "__main__":
    expr = "(3 + 5) * 2"

    # tokenize the input expression
    tokens = tokenize(expr)
    print("Tokens:", tokens)

    # parse tokens into AST
    ast = parse(tokens)
    print("AST:", ast)

#Q2 Part1----------------Aaron Menezes------------------------------------
