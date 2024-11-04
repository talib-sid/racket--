import parso
import lark
import json

# Classes for types
class Variable:
    def __init__(self,name):
        self.type = "Variable"
        self.name = name

class Function:
    def __init__(self,name,params,body):
        self.type = "Function"
        self.name = name

        # we will use the first param as the return 
        # type (for our cpp functor)
        self.params = params

        # function content
        self.body

class BinaryExp:
    def __init__(self,operator,left,right):
        self.type = "BinaryExpression"
        
        # + - += -= == != and or
        self.operator = operator

        self.left = left
        self.right = right

class UnaryExp:
    def __init__(self,operator,operand):
        self.type = "UnaryExpression"

        # ++ -- !
        self.operator = operator
        self.operand = operand

class Assignment:
    def __init__(self,operator,left,right):
        self.type = "Assignment"

        # = += -= *= /=
        self.operator = operator
        self.left = left
        self.right = right

class IfStatement:
    def __init__(self,cond,then,elze):
        self.type = "IfStatement"
        self.cond = cond
        self.then = then
        self.elze = elze

class WhileLoop:
    def __init__(self,cond,body):
        self.type = "WhileLoop"
        self.cond = cond
        self.body = body

class ForLoop:
    def __init__(self,init,cond,inc,body):
        self.type = "ForLoop"
        self.init = init
        self.cond = cond
        self.inc = inc
        self.body = body

class ControlFlow:
    def __init__(self,operator,cond):
        self.type = "ControlFlow"
        self.operator = operator
        # condition
        self.cond = cond


# def parse_expression(exp):
#     if isinstance(exp,sexpdata.Symbol):
#         return Variable(exp.value())
#     elif isinstance(exp,sexpdata.List):
#         if exp[0].value() == "if":
#             return parse_if_statement(exp)
#         elif exp[0].value() == "while":
#             return parse_while_loop(exp)
#         elif exp[0].value() == "for":
#             return parse_for_loop(exp)
#         elif exp[0].value() == "control":
#             return parse_control_flow(exp)
#         else:
#             return parse_binary_expression(exp)
#     else:
#         return None


# Load the racket file to parse
def parse_racket_file(file_path):
    try:
        # print('here')
        with open(file_path,mode="r") as f:
            data = f.read()
            # print(data)
            data = sexpdata.loads(data)
            print(data)
    except Exception as e:
        print(e)
        return None
    

parse_racket_file("f1.rkt")
# print(5)
