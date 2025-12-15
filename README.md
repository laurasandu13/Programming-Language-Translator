# Java-to-Python Translator

A compiler that translates java source code to Python, built as a project for the Python 101.1 course. This translator implements the complete compilation pipeline: lexical analysis, syntax analysis, and code generation.

## Overview

This translator converts Java code to functionally equivalent Python code through three main phases:
1. **Lexical Analysis** - tokenizes Java source code using regex patterns
2. **Syntax Analysis** - parses tokens into an Abstract Syntax Tree (AST) using recursive descnet parsing
3. **Code Generation** - emits Python code from the AST

## Features

**Core Translation Capabilities:**
- variable declarations (int, String, char, float, double, boolean)
- print statements
- if/else statements and if-else-if-else chain statements
- while loops
- for loops (converted to pyhton range() or while)
- logical operators (&&, ||)
- comparison operators (==, !=, <, >, <=, >=)
- increment/decrement operators (++, --)
- boolean literals 
- nested control structures

**Additional Featuires:**
- proper Python indentation (4 spaces, PEP 8 compliant)
- helpful error messages with line/column information
- command-line interfaces with multiple output options

## Project Structure
- `rules.py`: token patterns and lexer configuration
- `lexer.py`: lexical analyzer (tokenizer)
- `parser.py`: syntax analyzer (AST builder)
- `emitter.py`: code generator (Python emitter)
- `main.py`: command-line interface
- `test_tokens.py`: unit tests for tokenization
- `Input.java`: sample Java input file
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
This is a university project, not a full Java compiler. It does not support things like methods beyond ```main```, classes beyond the top-level wrapper, arrays, objects, imports, exceptions, or complex expressions.

