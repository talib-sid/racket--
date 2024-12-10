import subprocess
import sys
import json
import os

class CPlusPlusCodeGenerator:
    def __init__(self, ast): # ast is a list of dictionaries
        self.ast = ast
        # keep a set of all the variables declared
        self.variables = set()
        self.functions = set()
        self.main_calls = []
        self.main_code = "int main() {\n"
        self.code = ""
        self.cons_defined = False;
       

    def generate_code(self):
        for node in self.ast:
            self.code += self.handle_node(node) + "\n"
        
        # MAIN FUNCTION HANDLING
        self.generate_main_function()
        
        self.main_code += "\n\treturn 0;\n}"

        self.code += "\n"
        self.code += self.main_code


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
        elif(node['type'] == 'list'):
            if(node['items'][0]['value'] in self.functions):
                self.generate_function_call(node)
                return ""
            elif(node['items'][0]['value'] == 'print'):
                return self.generate_print_statement(node)
        elif(node['type'] == 'FunctionDefinition'):
            return self.generate_function_definition(node)
        elif node['type'] == 'ListDeclaration':
            return self.generate_list_declaration(node)
        elif node['type'] == 'ListOperation':
            return self.generate_list_operation(node)
        elif node['type'] == 'IfStatement':
            return self.generate_if_statement(node)
        else:
            return f"Errorr {node['type']}"
        
    def generate_if_statement(self, node):
        condition = self.handle_node(node['cond'])
        then_branch = self.handle_node(node['then'])
        else_branch = self.handle_node(node['elze'])

        cpp_code = f"if ({condition}) {{\n  return {then_branch};\n}} else {{\n  return {else_branch};\n}}"
        return cpp_code

    
    def generate_function_call(self, node, addToMain=True):
        # print(node)
        func_name = self.sanitize_identifier(node['items'][0]['value'])
        args = [self.handle_node(arg) for arg in node['items'][1:]]
        call = f"{func_name}({', '.join(args)})"


        if(addToMain):self.main_calls.append(call) 
        return call

    def generate_print_statement(self, node):
        value = self.handle_node(node['value'])
        return f"cout << {value} << endl;"
    
    def generate_main_function(self,node=None,isVarAssign=False, 
                               var_name=None):
        # case 1 : when the main function is calling a function

        # for the assignment of a variable in the main function
        # (only when it is calling a function)
        if(isVarAssign): 
            self.main_code += "\n"
            self.main_code += f"auto {var_name} = "
            self.main_code += self.generate_function_call(node['value'],addToMain=False)
            self.main_code += ";\n"

            return ""
        
        
        for call in self.main_calls:
            self.main_code += f"\t{call};\n"
        
        
        return ""
    
        
    def generate_variable_declaration(self, node):
        var_name = self.sanitize_identifier(node["name"])

        # var_value = self.handle_node(node['value'])
        
        self.variables.add(var_name)
        type = node['value']['type']
    
        if type == "ListOperation":
            value_code = self.handle_node(node["value"])
            if node["value"]["operator"] in {"car"}:
                return f"int {var_name} = {value_code};"
            elif node["value"]["operator"] in {"cdr", "cons"}:
                return f"std::vector<int> {var_name} = {value_code};"

        if(type == 'number'): 
            val = self.handle_node(node['value'])
            return f"int {var_name} = {val};"

        if(type == 'symbol'):
            val = self.handle_node(node['value'])
            return f"int {var_name} = {val};"

        # variable declared as a function call
        if(type == 'list'):
            self.generate_main_function(node,True, var_name)
            return ""
           
        
        return ""
    
    def generate_function_definition(self, node):
        func_name = self.sanitize_identifier(node['name'])
        params = [f"auto {param}" for param in node['params']]
        body = self.handle_node(node['body'])
        self.functions.add(func_name)
        return f"\tauto {func_name}({', '.join(params)}) {{ return {body}; }}"

    def generate_list_declaration(self, node):
        list_name = self.sanitize_identifier(node['name'])
        items = [item['value'] for item in node['items']]
        items_str = ", ".join(map(str, items))  # Convert the items to a comma-separated string
        # return f"\tauto {list_name} = {{ {items_str} }};"
        return f"\tstd::vector<int> {list_name} = {{ {items_str} }};"


    def generate_list_operation(self, node):
        operator = node["operator"]
        args = [self.handle_node(arg) for arg in node["args"]]

        if operator == "car":
            # Access the first element of the vector
            return f"{args[0]}.front()"
        elif operator == "cdr":
            # Create a subvector excluding the first element
            return f"std::vector<int>({args[0]}.begin() + 1, {args[0]}.end())"
        elif operator == "cons":
            # Add a new element at the front of the vector
            # created a function to handle the cons operation
            
            # call the function in main
            call = f"cons({args[1]} ,{args[0]})"
            self.main_calls.append(call)

            if(self.cons_defined == False):
                self.cons_defined = True
                return "\n\ntemplate <typename T>\n\nvoid cons(vector<T>& mylist, T elem){\n\tmylist.insert(mylist.begin(), elem);\n}"
            else:
                return ""
            # self.cons_defined = True
            # return f"([]{{ std::vector<int> temp = {{ {args[0]} }}; temp.insert(temp.end(), {args[1]}.begin(), {args[1]}.end()); return temp; }}())"
        else:
            raise ValueError(f"Unsupported list operation: {operator}")

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
        file.write("#include <iostream>\n")
        file.write("#include <vector>\n\n")
        file.write("using namespace std;\n\n")

        # file.write("int main() {\n")
        file.write(code)
        # file.write("int main() {\n")
        # file.write("\n\n\treturn 0;\n}")

    # Using Clang-format to add proper indentation
    subprocess.run(["clang-format", "-i", output_file])

    print(f"C++ code generated and saved to {output_file}\n")


if __name__ == "__main__":
    file_name = sys.argv[1]
    # file_name = "ast_gens/ast_code1.txt"
    
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

        file.write(code)
        # file.write("\nint main() {\n")
        # file.write("\n\n\treturn 0;\n}")

    subprocess.run(["clang-format", "-i", output_file])
    print(f"C++ code generated and saved to {output_file}")