class CPlusPlusCodeGenerator:
    def __init__(self, ast): # ast is a list of dictionaries
        self.ast = ast
        self.code = ""

    def generate_code(self):
        for node in self.ast:
            # print(node)
            self.code += self.handle_node(node) + "\n"
            # self.handle_node(node)
        return self.code

    def handle_node(self, node):
        # print(node['type'])
        # if node['type'] == 'list' and node['items'][0]['value'] == 'define':
        return self.generate_define(node)
        # elif node['type'] == 'symbol':
            # return node['value']
        # Handle other node types as needed
        # return ""

    def generate_define(self, node):
        # Detect if it's a function or variable based on structure
        # define_type = 'function' if isinstance(node['items'][1], dict) and node['items'][1]['type'] == 'list' else 'variable'

        # Defined a variable
        # type == VariableDeclaration
        if node['type'] == 'VariableDeclaration':
            var_name = node['name']
            var_value = node['value']['value']
            return f"\tauto {var_name} = {var_value};"
        if node['type'] == 'FunctionDefinition':
            func_name = node['name']
            params = [f"auto {param}" for param in node['params']]
            body = self.handle_node(node['body'])
            return f"\tauto {func_name}({', '.join(params)}) {{ return {body}; }}"
        
        return f"// comment"
        # print(node)

        # if define_type == 'function':
        #     func_name = node['items'][1]['items'][0]['value']
        #     params = [f"int {param['value']}" for param in node['items'][1]['items'][1:]]
        #     body = self.handle_node(node['items'][2])
        #     return f"int {func_name}({', '.join(params)}) {{ return {body}; }}"

        # elif define_type == 'variable':
        #     var_name = node['items'][1]['value']
        #     var_value = self.handle_node(node['items'][2])
        #     return f"int {var_name} = {var_value};"

    def handle_operations(self, node):
        # print(node)
        # print(node['operator'])
        if(node['type'] == 'BinaryOperation'):
            left = self.handle_node(node['left'])
            right = self.handle_node(node['right'])
            return f"{left} {node['operator']} {right}"
        if(node['type'] == 'UnaryOperation'):
            operand = self.handle_node(node['operand'])
            return f"{node['operator']} {operand}"


# Usage
# json_file = "ast_gens/ast_1.json"
# with open(json_file) as file:

if __name__ == "__main__":
    # Read the JSON data
    # with open("ast_gens/ast_1.json") as file:
    #     data = json.load(file)
    data = [
        {         
            "type": "VariableDeclaration",
            "name": "a",
            "value": {"type": "number", "value": 10}
        },
        {
            "type": "VariableDeclaration",
            "name": "b",
            "value": {"type": "number", "value": 5}
        },
        {    
            "type": "FunctionDefinition",
            "name": "sum",
            "params": [
                "x",
                "y"
            ],
            "body": {
                "type": "BinaryOperation",
                "operator": "+",
                "left": {"type": "symbol","value": "x"},
                "right": {"type": "symbol","value": "y"}
            }
        }
    ]

    # Generate C++ code
    generator = CPlusPlusCodeGenerator(data)
    code = generator.generate_code()

    # Write the code to a file
    with open("output.cpp", "w") as file:
        file.write("#include <iostream>\n\n")
        file.write("using namespace std;\n\n")
        file.write("int main() {\n")
        file.write(code)
        file.write("\n\n\treturn 0;\n}")


    print("C++ code generated and saved to 'output.cpp'")