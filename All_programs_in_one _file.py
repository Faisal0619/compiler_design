"""
Code Analysis Toolkit - All-in-One Solution
Author: Your Name
Date: Current Date
"""

import re
import keyword
from typing import List, Tuple

# ==================== LINE COUNTING FUNCTIONS ====================

def count_all_lines(filename: str) -> int:
    """Count all lines in a file including blank lines.
    
    Args:
        filename: Path to the file to analyze
        
    Returns:
        Total number of lines in the file
    """
    try:
        with open(filename, 'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return -1

def count_non_empty_lines(filename: str) -> int:
    """Count only non-empty lines in a file.
    
    Args:
        filename: Path to the file to analyze
        
    Returns:
        Number of non-empty lines in the file
    """
    try:
        with open(filename, 'r') as file:
            return sum(1 for line in file if line.strip())
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return -1

def count_c_comments(filename: str) -> int:
    """Count comment lines in a C program file.
    
    Args:
        filename: Path to the C source file
        
    Returns:
        Number of comment lines (both single-line and multi-line)
    """
    try:
        in_multi_line_comment = False
        comment_count = 0
        
        with open(filename, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                
                if in_multi_line_comment:
                    comment_count += 1
                    if '*/' in stripped_line:
                        in_multi_line_comment = False
                elif stripped_line.startswith('//'):
                    comment_count += 1
                elif '/*' in stripped_line:
                    comment_count += 1
                    if '*/' not in stripped_line:
                        in_multi_line_comment = True
        
        return comment_count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return -1

# ==================== TOKENIZATION FUNCTIONS ====================

def tokenize_by_space(input_string: str) -> List[str]:
    """Tokenize a string using spaces as delimiters.
    
    Args:
        input_string: The string to tokenize
        
    Returns:
        List of tokens
    """
    return input_string.split()

def categorize_tokens(filename: str) -> List[Tuple[str, str]]:
    """Tokenize a program file and categorize tokens.
    
    Args:
        filename: Path to the file to analyze
        
    Returns:
        List of tuples (token, category)
    """
    try:
        # Extended set of keywords for C-like languages
        keywords = {
            'if', 'else', 'while', 'for', 'return', 'break', 'continue',
            'int', 'float', 'double', 'char', 'void', 'bool', 'true', 'false',
            'struct', 'typedef', 'enum', 'union', 'const', 'static', 'extern',
            'switch', 'case', 'default', 'do', 'goto', 'sizeof', 'volatile'
        }
        
        tokens = []
        
        with open(filename, 'r') as file:
            content = file.read()
            # Enhanced pattern to handle more cases
            pattern = r'''
                [a-zA-Z_]\w*       | # Identifiers
                \d+\.?\d*          | # Numbers (int and float)
                0x[0-9a-fA-F]+     | # Hex numbers
                \".*?\"            | # Double quoted strings
                \'.*?\'            | # Single quoted chars
                \/\/.*             | # Single line comments
                \/\*.*?\*\/        | # Multi-line comments
                \+\+ | --          | # Increment/decrement
                == | != | <= | >= | # Comparison operators
                && | \|\|          | # Logical operators
                << | >>            | # Bit shift
                [+\-*/%=<>!&|^~]   | # Other operators
                [\[\](){},.;:]     | # Punctuation
                \S                   # Any other non-space
            '''
            for match in re.finditer(pattern, content, re.VERBOSE):
                token = match.group()
                
                # Skip whitespace and comments
                if token.isspace() or token.startswith(('//', '/*')):
                    continue
                
                # Determine category
                if token in keywords:
                    category = 'keyword'
                elif token.isdigit() or (token.replace('.', '', 1).isdigit() and '.' in token):
                    category = 'constant'
                elif token.startswith(('"', "'")):
                    category = 'string'
                elif re.match(r'^0x[0-9a-fA-F]+$', token):
                    category = 'hex_constant'
                elif re.match(r'^[a-zA-Z_]\w*$', token):
                    category = 'identifier'
                else:
                    category = 'operator/punctuation'
                
                tokens.append((token, category))
        
        return tokens
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def tokenize_code(code: str) -> List[Tuple[str, str]]:
    """Tokenize code snippet into keywords, identifiers, and operators.
    
    Args:
        code: The code string to tokenize
        
    Returns:
        List of tuples (category, token)
    """
    # Extended set of keywords
    keywords = {
        'if', 'else', 'while', 'for', 'return', 'break', 'continue',
        'int', 'float', 'double', 'char', 'void', 'bool', 'true', 'false',
        'struct', 'typedef', 'enum', 'union', 'const', 'static', 'extern',
        'switch', 'case', 'default', 'do', 'goto', 'sizeof', 'volatile'
    }
    
    tokens = []
    
    # Enhanced pattern
    pattern = r'''
        [a-zA-Z_]\w*       | # Identifiers
        \d+\.?\d*          | # Numbers (int and float)
        0x[0-9a-fA-F]+     | # Hex numbers
        \".*?\"            | # Double quoted strings
        \'.*?\'            | # Single quoted chars
        \+\+ | --          | # Increment/decrement
        == | != | <= | >=  | # Comparison operators
        && | \|\|          | # Logical operators
        << | >>            | # Bit shift
        [+\-*/%=<>!&|^~]   | # Other operators
        [\[\](){},.;:]     | # Punctuation
        \S                   # Any other non-space
    '''
    
    for match in re.finditer(pattern, code, re.VERBOSE):
        token = match.group()
        
        if token in keywords:
            tokens.append(('keyword', token))
        elif token.isdigit() or (token.replace('.', '', 1).isdigit() and '.' in token):
            tokens.append(('constant', token))
        elif token.startswith(('"', "'")):
            tokens.append(('string', token))
        elif re.match(r'^0x[0-9a-fA-F]+$', token):
            tokens.append(('hex_constant', token))
        elif re.match(r'^[a-zA-Z_]\w*$', token):
            tokens.append(('identifier', token))
        else:
            tokens.append(('operator/punctuation', token))
    
    return tokens

# ==================== IDENTIFIER VALIDATION FUNCTIONS ====================

def is_valid_c_identifier(name: str) -> bool:
    """Check if a string is a valid C identifier.
    
    Args:
        name: The identifier to check
        
    Returns:
        True if valid, False otherwise
    """
    c_keywords = {
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
        'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
        'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
        'volatile', 'while'
    }
    return (bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name)) and 
            name not in c_keywords)

def is_valid_python_variable(name: str) -> bool:
    """Check if a string is a valid Python variable name.
    
    Args:
        name: The variable name to check
        
    Returns:
        True if valid, False otherwise
    """
    return (bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name)) and not keyword.iskeyword(name))

def is_valid_java_identifier(name: str) -> bool:
    """Check if a string is a valid Java identifier.
    
    Args:
        name: The identifier to check
        
    Returns:
        True if valid, False otherwise
    """
    java_keywords = {
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
        'char', 'class', 'const', 'continue', 'default', 'do', 'double',
        'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
        'goto', 'if', 'implements', 'import', 'instanceof', 'int',
        'interface', 'long', 'native', 'new', 'package', 'private',
        'protected', 'public', 'return', 'short', 'static', 'strictfp',
        'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
        'transient', 'try', 'void', 'volatile', 'while'
    }
    return (bool(re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', name))) and name not in java_keywords

# ==================== MAIN MENU ====================

def display_menu():
    """Display the program menu."""
    print("\n" + "="*50)
    print("CODE ANALYSIS TOOLKIT".center(50))
    print("="*50)
    print("1. Count all lines in a file")
    print("2. Count non-empty lines in a file")
    print("3. Count comment lines in a C program")
    print("4. Tokenize and categorize program file")
    print("5. Tokenize string using spaces")
    print("6. Tokenize code snippet")
    print("7. Check valid C identifier")
    print("8. Check valid Python variable name")
    print("9. Check valid Java identifier")
    print("0. Exit")
    print("="*50)

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (0-9): ")
        
        if choice == '0':
            print("Exiting program. Goodbye!")
            break
            
        elif choice == '1':
            filename = input("Enter file path: ")
            count = count_all_lines(filename)
            if count >= 0:
                print(f"\nTotal lines in '{filename}': {count}")
                
        elif choice == '2':
            filename = input("Enter file path: ")
            count = count_non_empty_lines(filename)
            if count >= 0:
                print(f"\nNon-empty lines in '{filename}': {count}")
                
        elif choice == '3':
            filename = input("Enter C file path: ")
            count = count_c_comments(filename)
            if count >= 0:
                print(f"\nComment lines in '{filename}': {count}")
                
        elif choice == '4':
            filename = input("Enter file path: ")
            tokens = categorize_tokens(filename)
            if tokens:
                print("\nToken Categories:")
                print("-"*40)
                print(f"{'Token':<20} {'Category':<20}")
                print("-"*40)
                for token, category in tokens:
                    print(f"{token:<20} {category:<20}")
                
        elif choice == '5':
            text = input("Enter string to tokenize: ")
            tokens = tokenize_by_space(text)
            print("\nTokens:")
            for i, token in enumerate(tokens, 1):
                print(f"{i}. {token}")
                
        elif choice == '6':
            code = input("Enter code snippet:\n")
            tokens = tokenize_code(code)
            print("\nCode Tokens:")
            print("-"*40)
            print(f"{'Category':<20} {'Token':<20}")
            print("-"*40)
            for category, token in tokens:
                print(f"{category:<20} {token:<20}")
                
        elif choice == '7':
            identifier = input("Enter identifier to check: ")
            if is_valid_c_identifier(identifier):
                print(f"\n'{identifier}' is a VALID C identifier")
            else:
                print(f"\n'{identifier}' is NOT a valid C identifier")
                
        elif choice == '8':
            variable = input("Enter variable name to check: ")
            if is_valid_python_variable(variable):
                print(f"\n'{variable}' is a VALID Python variable name")
            else:
                print(f"\n'{variable}' is NOT a valid Python variable name")
                
        elif choice == '9':
            identifier = input("Enter identifier to check: ")
            if is_valid_java_identifier(identifier):
                print(f"\n'{identifier}' is a VALID Java identifier")
            else:
                print(f"\n'{identifier}' is NOT a valid Java identifier")
                
        else:
            print("\nInvalid choice. Please enter a number between 0-9.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()