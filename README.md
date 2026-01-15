# Java-to-Python Translator

A compiler that translates java source code to Python, built as a project for the Formal Languages and Compilers course. This translator implements the complete compilation pipeline: lexical analysis, syntax analysis, and code generation.

## Overview

This translator converts Java code to functionally equivalent Python code through three main phases:
1. **Lexical Analysis** - tokenizes Java source code using regex patterns
2. **Syntax Analysis** - parses tokens into an Abstract Syntax Tree (AST) using recursive descnet parsing
3. **Code Generation** - emits Python code from the AST

## Architecture
### Lexical Analysis (`lexer.py`)

The lexer uses regular expressions to scan the input and produce tokens. Each token has a kind (identifier, keyword, operator, etc.), value, and position for error reporting.

### Syntax Analysis (`parser.py`)

The parser implements recursive descent parsing to build an Abstract Syntax Tree. It recognizes Java's grammar rules and creates structured representations of classes, methods, control flow, and expressions.

### Code Generation (`emitter.py`)

The emitter traverses the AST and generates equivalent Python code, handling semantic differences like:
- Type declarations (removed in Python)
- Indentation-based blocks (converted from braces)
- `this` vs `self` for instance references
- Boolean literal capitalization
- Print statement type conversions

## Features

**Core Translation Capabilities:**
- Variable declarations (int, String, char, float, double, boolean)
- Print statements (with automatic type conversion for string concatenation)
- If/else statements and if-else-if-else chain statements
- While loops (with simple and complex conditions)
- For loops (converted to Python range() or while)
- Switch statements (with break and fall-through support)
- Functions (with parameters and return values)
- Classes (with constructors, fields, and methods)
- User input (Scanner methods: nextLine, nextInt, nextDouble, nextFloat, next)
- Logical operators (&&, ||) → (and, or)
- Comparison operators (==, !=, <, >, <=, >=)
- Increment/decrement operators (++, --)
- Boolean literals (true/false → True/False)
- Nested control structures


**Additional Features:**
- Object-oriented programming support (classes, constructors, instance methods)
- `this.field` → `self.field` conversion for Python instance variables
- Field increment/decrement (`this.field++` → `self.field += 1`)
- Proper Python indentation (4 spaces, PEP 8 compliant)
- Helpful error messages with token position information
- Command-line interface with multiple output options
- Handles static methods (converted to instance methods in Python)


## Project Structure
- `rules.py`: token patterns and lexer configuration
- `lexer.py`: lexical analyzer (tokenizer)
- `parser.py`: syntax analyzer (AST builder)
- `emitter.py`: code generator (Python emitter)
- `main.py`: command-line interface
- `test_tokens.py`: unit tests for tokenization
- `DemoTest.java`: sample Java input file
- `output.py`: generated Python output
- `README.md`: this file

## How To Run

From the project directory:
```bash
# Translate Java to Python and write to a file
python main.py Input.java output.py

# Translate and just print the result
python main.py Input.java --dry-run

# Translate and print (no output file argument)
python main.py Input.java
```
To test output file:
```bash
python output.py
```

## Requirements
- Python 3.7 or higher
- no external dependencies (uses only Python standard library)

## Limitations
This is a university project, not a full Java compiler. It does not support arrays, objects, imports, exceptions, or complex expressions.

## Authors
Sandu Laura Florentina
Ionescu Ionut


