import sys
import subprocess
import os
import jsoner
import code_gen
import racket_parse

rack_test_dir = "rack_tests"
ast_file_dir = "ast_gens"
code_file_dir = "cpp_tests"


print("\n\nConverting all racket files to ASTs")
rack_tests = [f"{rack_test_dir}/{file}" for file in os.listdir(rack_test_dir) if file.endswith(".rkt")]
for rkt_file in rack_tests:
    print(f"Processing {rkt_file}")
    racket_parse.run(rkt_file)


print("Converting all ASTs to Compatible Json\n")
test_asts = [f"{ast_file_dir}/{file}" for file in os.listdir(ast_file_dir) if file.endswith(".json")]
for ast in test_asts:
    jsoner.run(ast)


print("Generating code for all ASTs\n") 
cmp_tests = [f"{ast_file_dir}/{file}" for file in os.listdir(ast_file_dir) if file.endswith(".txt")]   
for cmp in cmp_tests:
    print(f"Generating code for {cmp}")
    code_gen.run(cmp)


# print("\n\nCompiling all generated code")
# cpp_files = [f"{code_file_dir}/{file}" for file in os.listdir(code_file_dir) if file.endswith(".cpp")]
# for cpp_file in cpp_files:
#     print(f"Compiling {cpp_file}")
#     subprocess.run(["g++", "-o", f"{cpp_file.removesuffix('.cpp')}.out", cpp_file])

# print("\n\nRunning all compiled code")
# out_files = [f"{code_file_dir}/{file}" for file in os.listdir(code_file_dir) if file.endswith(".out")]
# for out_file in out_files:
#     print(f"Running {out_file}")
#     subprocess.run([out_file])

print("\n\nDone!")

