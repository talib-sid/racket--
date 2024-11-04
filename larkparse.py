# import json
# import sys
from lark import Lark, Transformer
from lark.tree import Tree, Branch, pydot__tree_to_png, pydot__tree_to_dot, pydot__tree_to_graph
# from anytree import Node, RenderTree
# from typing import Any, Dict, List, Union



# Define the Racket grammar with fixed regex patterns
RACKET_GRAMMAR = r"""?start: expr+
?expr: atom
        | list
        | quoted
        | COMMENT
list: "(" expr* ")"
quoted: "'" expr
?atom: NUMBER -> number
        | STRING -> string
        | SYMBOL -> symbol
        | boolean
boolean: "#t" -> true
        | "#f" -> false
SYMBOL: /[a-zA-Z_+\-*\/>=<][a-zA-Z0-9_+\-*\/>=<!?]*/
NUMBER: /[-]?[0-9]+(\.[0-9]+)?/
STRING: /"[^"]*"/
COMMENT: /;[^\n]*/
%import common.WS
%ignore WS
"""

class RacketTransformer(Transformer):
    def list(self, items):
        # Check if this list is a function or variable definition
        if len(items) > 0 and items[0]["type"] == "symbol":
            op = items[0]["value"]
            if op in {"+", "-", "*", "=","/", ">", "<", ">=", "<=", "==", "!=", "and", "or"}:
                return {
                    "type": "BinaryOperation",
                    "operator": op,
                    "left": items[1],
                    "right": items[2]
                }
            elif op in {"not", "abs", "round", "floor", "ceil"}:
                return {
                    "type": "UnaryOperation",
                    "operator": op,
                    "value": items[1]
                }
            elif op in {"if", "else"}:
                return {
                    "type": "IfStatement",
                    "cond": items[1],
                    "then": items[2],
                    "elze": items[3]
                }
            elif op in {"while"}:
                return {
                    "type": "WhileLoop",
                    "cond": items[1],
                    "body": items[2]
                }
            elif op in {"for"}:
                return {
                    "type": "ForLoop",
                    "init": items[1],
                    "cond": items[2],
                    "inc": items[3],
                    "body": items[4]
                }
            elif op in {"break", "continue"}:
                return {
                    "type": "ControlFlow",
                    "operator": op,
                    "cond": items[1]
                }
            elif op in {"define"}:
                return self.handle_define(items)
            elif op in {"lambda"}:
                return self.handle_lambda(items)
            elif op in {"print"}:
                return {
                    "type": "PrintStatement",
                    "value": items[1]
                }
            elif op in {"list"}:
                return self.handle_list(items)
            # else:
            #     return {"type": op, "items": items}
                # raise Exception(f"Unknown operator: {op}")
        # print(items)
        return {
            "type": "list", 
            "items": items
        }
    

    def handle_define(self, items):
        # Check if we're defining a function or a variable
        if isinstance(items[1], dict) and items[1]["type"] == "list":
            # Function definition
            function_name = items[1]["items"][0]["value"]
            params = [param["value"] for param in items[1]["items"][1:]]
            body = items[2] 
            return {
                "type": "FunctionDefinition",
                "name": function_name,
                "params": params,
                "body": body
            }
        else:
            # Variable definition
            var_name = items[1]["value"]
            var_value = items[2]
            return {
                "type": "VariableDeclaration",
                "name": var_name,
                "value": var_value
            }


    def quoted(self, items):
        return {
            "type": "quoted", 
            "value": items[0]
        }
    
    def number(self, tok):
        value = float(tok[0]) if '.' in tok[0] else int(tok[0])
        return {"type": "number", "value": value}
    
    def string(self, tok):
        return {"type": "string", "value": tok[0][1:-1]}  # Remove quotes
    
    def symbol(self, tok):
        return {"type": "symbol", "value": str(tok[0])}
    
    def true(self, _):
        return {"type": "boolean", "value": True}
    
    def false(self, _):
        return {"type": "boolean", "value": False}

class RacketParser:
    def __init__(self):
        self.parser = Lark(RACKET_GRAMMAR, parser='lalr', transformer=RacketTransformer())
    
    def parse_file(self, filename):
        with open(filename, 'r') as f:
            return self.parse(f.read())
    
    def parse(self, code):
        try:
            return self.parser.parse(code)
        except Exception as e:
            raise Exception(f"Parsing error: {str(e)}")

# Example usage
if __name__ == "__main__":
    parser = RacketParser()
    # racket_file = "f1.rkt"
    racket_file = "examp.rkt"

    try:
        ast = parser.parse_file(racket_file)
        # ast = parser.parse(test_code)
        # ast = parser.parse(f1)

        # print("Parsed successfully!")
        print(ast.pretty())

 
    except Exception as e:
        print(f"Error: {e}")