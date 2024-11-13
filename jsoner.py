import json
import re

# Original raw string with data (as multiline string for example)
# data = """
#   {'type': 'FunctionDefinition', 'name': 'greater?', 'params': ['x', 'y'], 'body': {'type': 'BinaryOperation', 'operator': '>=', 'left': {'type': 'symbol', 'value': 'x'}, 'right': {'type': 'symbol', 'value': 'y'}}}
#   {'type': 'FunctionDefinition', 'name': 'less?', 'params': ['x', 'y'], 'body': {'type': 'BinaryOperation', 'operator': '<=', 'left': {'type': 'symbol', 'value': 'x'}, 'right': {'type': 'symbol', 'value': 'y'}}}
#   # ... more data as shown in your message
# """

# read data from file
ast_file = "ast_gens/ast_1.json"

with open(ast_file) as file:
    data = file.read()

clean_data = re.sub(r";.*|#.*", "", data)  
clean_data = clean_data.replace("'", "\"")  
clean_data = re.sub(r'\bTrue\b', 'true', clean_data)
clean_data = re.sub(r'\bFalse\b', 'false', clean_data) 

data_list = []
for line in clean_data.splitlines():
    #ignore first line
    if line == "start":
        continue

    line = line.strip()
    if line:
        try:
            data_list.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"Error decoding line: {line}\n{e}")

with open(f"{ast_file}".removesuffix(".json")+".txt", "w") as file:
    json.dump(data_list, file, indent=2)

print("JSON data saved")

