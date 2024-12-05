import subprocess
import sys
import json


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
        # type == VariableDeclaration

        # Check if it's an operation call
        if node['type'] == 'BinaryOperation' or node['type'] == 'UnaryOperation':
            return self.handle_operations(node)
    
        # Defined a variable
        if node['type'] == 'VariableDeclaration':
            var_name = node['name']
            var_value = node['value']['value']
            return f"\tauto {var_name} = {var_value};"
        if node['type'] == 'FunctionDefinition':
            func_name = node['name']
            params = [f"auto {param}" for param in node['params']]
            # print(node['body'])
            body = self.handle_node(node['body'])
            
            return f"\tauto {func_name}({', '.join(params)}) {{ return {body}; }}"
        # return f""

    def handle_operations(self, node):
        # print(node)
        # print(node['operator'])

        if(node['type'] == 'BinaryOperation'):
            # left = self.handle_node(node['left'])
            # right = self.handle_node(node['right'])
            left = node['left']['value']
            right = node['right']['value']
            return f"{left} {node['operator']} {right}"
    
        if(node['type'] == 'UnaryOperation'):
            operand = self.handle_node(node['operand'])
            return f"{node['operator']} {operand}"
    


# Usage
# json_file = "ast_gens/ast_1.json"
# with open(json_file) as file:

if __name__ == "__main__":
    # file_name = sys.argv[1]
    file_name = "ast_gens/ast_1.txt"
    data = []
    with open(file_name) as file:
        data = json.load(file)

    # Generate C++ code
    generator = CPlusPlusCodeGenerator(data)
    code = generator.generate_code()

    # Write the code to a file
    with open("output.cpp", "w") as file:
        file.write("#include <iostream>\n\n")
        file.write("using namespace std;\n\n")

        # file.write("int main() {\n")
        file.write(code)
        # file.write("\n\n\treturn 0;\n}")

    
    # Using Clang-format to add proper indentation
    subprocess.run(["clang-format", "-i", "output.cpp"])
    # Shift to astyle later

    print("C++ code generated and saved to 'output.cpp'")