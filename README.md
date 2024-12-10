# Ra(C)ket(++)

### Transpiler for basic racket source code to equivalent C++ code

# How to use

## Clean the project
```bash
  make clean
```
OR
```
  rm rm "ast_gens/*"
  rm "cpp_tests/*"
```

## Run the tests
```python
  python ./pipeline.py
```

### Pipeline.py

#### pipeline.py will run the following scripts in order:

- **racket_parse.py** on the dir "racket_tests" to generate the ASTs
- **jsoner.py** on the dir "ast_gens" to generate the jsons
- **code_gen.py** on the dir "ast_gens" to generate the C++ code
- **Compile** and **Run** the generated C++ code

### Current functionality:
- We carry out auto type deduction for most type-conversion here  (as racket is dynamically typed unlike C++)
- Successfully converts simple arithemtic and logical expressions to equivalent C++ expressions
  - Binary operations: +, -, *, /, %, <, >, <=, >=, ==, !=
  - Unary operations: not, - (negation)
  - Logical operations: and, or 
- Basic function definitions to C++ function definitions
- Basic function calls to C++ function calls
- Simple variable definitions to C++ variable definitions
- Simple list definitions to C++ vector definitions
- cdr, car, cons to C++ vector functions
