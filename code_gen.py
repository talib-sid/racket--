import subprocess
import sys
import json
import os

class CPlusPlusCodeGenerator:
    def __init__(self, ast): # ast is a list of dictionaries
        self.ast = ast
        self.code = ""

    def generate_code(self):
        for node in self.ast:
            self.code += self.handle_node(node) + "\n"
        return self.code

    def handle_node(self, node):
        # print(node['type'])
        # if node['type'] == 'list' and node['items'][0]['value'] == 'define':
        if(node['type'] == 'BinaryOperation' or node['type'] == 'UnaryOperation'):
            return self.handle_operations(node)
        elif(node['type'] == 'symbol'):
            return node['value']
        elif(node['type'] == 'number'):
            return str(node['value'])
        elif(node['type'] == 'VariableDeclaration'):
            return self.generate_variable_declaration(node)
        elif(node['type'] == 'FunctionDefinition'):
            return self.generate_function_definition(node)
        else:
            return f"Error"
        

    def generate_variable_declaration(self, node):
        var_name = node['name']
        var_value = self.handle_node(node['value'])
        return f"\tauto {var_name} = {var_value};"
    
    def generate_function_definition(self, node):
        # func_name = node['name'].
        func_name = self.sanitize_identifier(node['name'])
        params = [f"auto {param}" for param in node['params']]
        body = self.handle_node(node['body'])
        return f"\tauto {func_name}({', '.join(params)}) {{ return {body}; }}"



    def handle_operations(self, node):
        
        operator = node['operator']
        if(node['type'] == 'BinaryOperation'):
            left = self.handle_node(node['left'])
            right = self.handle_node(node['right'])
            
            if operator == "=":
                operator = "=="


            return f"{left} {operator} {right}"
    
        elif(node['type'] == 'UnaryOperation'):
            operand = self.handle_node(node['operand'])
            return f"{operator} {operand}"

        else:
            return f"Error"
        
    def sanitize_identifier(self, identifier):
        # Replace invalid characters in identifiers
        return identifier.replace("?", "_")


def run(file_name):
    # file_name = sys.argv[1]
    # file_name = "ast_gens/ast_1.txt"
    data = []
    with open(file_name) as file:
        data = json.load(file)

    generator = CPlusPlusCodeGenerator(data)
    code = generator.generate_code()

    file_name = os.path.basename(file_name).split('.')[0];
    file_name = file_name.split('_')[1]
    output_file = f"cpp_tests/{file_name}.cpp"
    
    with open(output_file, "w") as file:
        file.write("#include <iostream>\n\n")
        file.write("using namespace std;\n\n")

        # file.write("int main() {\n")
        file.write(code)
        # file.write("\n\n\treturn 0;\n}")

    # Using Clang-format to add proper indentation
    subprocess.run(["clang-format", "-i", output_file])
    print(f"C++ code generated and saved to {output_file}")


if __name__ == "__main__":
    # file_name = sys.argv[1]
    file_name = "ast_gens/ast_code1.txt"
    
    data = []
    with open(file_name) as file:
        data = json.load(file)
    
    generator = CPlusPlusCodeGenerator(data)
    code = generator.generate_code()

    file_name = os.path.basename(file_name).split('.')[0];
    file_name = file_name.split('_')[1]
    output_file = f"cpp_tests/{file_name}.cpp"
    
    with open(output_file, "w") as file:
        file.write("#include <iostream>\n\n")
        file.write("using namespace std;\n\n")

        # file.write("int main() {\n")
        file.write(code)
        # file.write("\n\n\treturn 0;\n}")

    subprocess.run(["clang-format", "-i", output_file])
    print(f"C++ code generated and saved to {output_file}")