# Ra(C)ket(++)

## Transpiler for basic racket source code to equivalent C++ code


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
