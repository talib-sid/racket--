import json
import sys
import re

def process_ast_file(ast_file):
    with open(ast_file) as file:
        data = file.read()

    clean_data = re.sub(r";.*|#.*", "", data)  
    clean_data = clean_data.replace("'", "\"")  
    clean_data = re.sub(r'\bTrue\b', 'true', clean_data)
    clean_data = re.sub(r'\bFalse\b', 'false', clean_data) 

    data_list = []
    for line in clean_data.splitlines():
        # Ignore first line
        if line == "start":
            continue

        line = line.strip()
        if line:
            try:
                data_list.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line}\n{e}")

    output_file = f"{ast_file}".removesuffix(".json") + ".txt"
    with open(output_file, "w") as file:
        json.dump(data_list, file, indent=2)

    print("JSON data saved")

# Example usage
def run(ast_file):
    process_ast_file(ast_file)

if __name__ == "__main__":
    # ast_file = "ast_gens/ast_1.json"
    ast_file = sys.argv[1]
    process_ast_file(ast_file=ast_file)
