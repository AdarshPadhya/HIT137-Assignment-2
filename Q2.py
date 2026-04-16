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

        if token[0] == "OP" and token[1] == "-":
            self.eat("OP")
            operand = self.parse_factor()
            return {
                "type": "neg",
                "value": operand
            }

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

#Q2 Part1----------------Aaron Menezes------------------------------------




# --Q2 Part2 Aaditya Kulkarni--

def evaluate(expr_node):
    # if it's just a number
    if expr_node["type"] == "num":
        return expr_node["value"]

    # unary negative case
    if expr_node["type"] == "neg":
        inner_value = evaluate(expr_node["value"])
        return -inner_value

    # binary operations
    if expr_node["type"] == "binop":
        left_value = evaluate(expr_node["left"])
        right_value = evaluate(expr_node["right"])

        if expr_node["op"] == "+":
            return left_value + right_value

        elif expr_node["op"] == "-":
            return left_value - right_value

        elif expr_node["op"] == "*":
            return left_value * right_value

        elif expr_node["op"] == "/":
            if right_value == 0:
                raise Exception("division by zero")
            return left_value / right_value

def build_tree(expr_node):
    # number node
    if expr_node["type"] == "num":
        number_value = expr_node["value"]
        return str(int(number_value))

    # unary negation
    if expr_node["type"] == "neg":
        return "(neg " + build_tree(expr_node["value"]) + ")"

    # binary operation
    if expr_node["type"] == "binop":
        left_part = build_tree(expr_node["left"])
        right_part = build_tree(expr_node["right"])
        operator_symbol = expr_node["op"]

        return "(" + operator_symbol + " " + left_part + " " + right_part + ")"


def tokens_to_output(token_list):
    output_line = ""

    for token in token_list:
        token_type = token[0]
        token_val = token[1]

        if token_type == "NUM":
            output_line += "[NUM:" + str(int(token_val)) + "] "

        elif token_type == "OP":
            output_line += "[OP:" + token_val + "] "

        elif token_type == "LPAREN":
            output_line += "[LPAREN:(] "

        elif token_type == "RPAREN":
            output_line += "[RPAREN:)] "

        elif token_type == "END":
            output_line += "[END]"

    return output_line.strip()


def evaluate_file(input_path):
    input_file = open(input_path, "r")
    all_lines = input_file.readlines()
    input_file.close()

    output_file = open("output.txt", "w")

    collected_results = []

    # go through each expression
    for line in all_lines:
        current_expr = line.strip()

        if current_expr == "":
            continue

        # first try: token + parse
        try:
            token_list = tokenize(current_expr)
            parsed_tree = parse(token_list)

            tree_output = build_tree(parsed_tree)
            token_output = tokens_to_output(token_list)

        except:
            tree_output = "ERROR"
            token_output = "ERROR"
            final_value = "ERROR"

            # write and skip to next line
            output_file.write("Input: " + current_expr + "\n")
            output_file.write("Tree: " + tree_output + "\n")
            output_file.write("Tokens: " + token_output + "\n")
            output_file.write("Result: " + str(final_value) + "\n\n")
            continue


        # second try: evaluation ONLY
        try:
            final_value = evaluate(parsed_tree)

            if int(final_value) == final_value:
                final_value = int(final_value)
            else:
                final_value = round(final_value, 4)

        except:
            final_value = "ERROR"

        # writing block
        output_file.write("Input: " + current_expr + "\n")
        output_file.write("Tree: " + tree_output + "\n")
        output_file.write("Tokens: " + token_output + "\n")
        output_file.write("Result: " + str(final_value) + "\n\n")

        collected_results.append({
            "input": current_expr,
            "tree": tree_output,
            "tokens": token_output,
            "result": final_value
        })

    output_file.close()
    return collected_results

#Q2 Part2----------------Aaditya Kulkarni------------------------------------

# TEST 
if __name__ == "__main__":
    evaluate_file("sample_input.txt")