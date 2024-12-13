from flask import Flask, request, jsonify
from flask_cors import CORS

# Create Flask application and enable CORS 
app = Flask(__name__)
CORS(app)

# Function to perform lexical analysis
def lexical_analyzer(input_string):
    tokens = []  # List to store the tokens 
    i = 0  # Initialize the index 

    # Set of predefined keywords
    keywords = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'char', 'void', 'string', 'class', 'public', 'private'}

    # Helper function to check if character is a letter
    def is_letter(char):
        return char.isalpha()

    # Helper function to check if character is a digit
    def is_digit(char):
        return char.isdigit()

    # Helper function to check if identifier is a keyword
    def is_keyword(identifier):
        return identifier in keywords

    # Loop through each character in the input string
    while i < len(input_string):
        char = input_string[i]

        # Skip over space characters
        if char.isspace():
            i += 1
            continue

        # Handle single-line comments (starts with '//')
        if char == '/':
            if i + 1 < len(input_string) and input_string[i + 1] == '/':
                comment = input_string[i:]  # Capture the entire comment
                tokens.append(('COMMENT', comment.strip()))  # Add comment token to the list
                break  # Exit the loop as the rest is a comment
            # Handle multi-line comments (starts with '/*' and ends with '*/')
            elif i + 1 < len(input_string) and input_string[i + 1] == '*':
                comment = char + '*'
                i += 2
                while i < len(input_string) and not (input_string[i] == '*' and i + 1 < len(input_string) and input_string[i + 1] == '/'):
                    comment += input_string[i]
                    i += 1
                comment += '*/' if i < len(input_string) else ''
                tokens.append(('COMMENT', comment))  # Add multi-line comment token
                i += 2  # Skip the closing '*/'
                continue

        # Handle string literals
        if char == '"' or char == "'":
            string_literal = char
            i += 1
            while i < len(input_string) and input_string[i] != char: 
                string_literal += input_string[i]
                i += 1
            string_literal += char if i < len(input_string) else ''
            tokens.append(('STRING_LITERAL', string_literal))  # Add string literal token
            i += 1  # Skip the closing quote
            continue

        # Handle keywords and identifiers 
        if is_letter(char):
            identifier = char
            i += 1
            while i < len(input_string) and (is_letter(input_string[i]) or is_digit(input_string[i])): 
                identifier += input_string[i]
                i += 1
            if is_keyword(identifier):  # Check if the identifier is a keyword
                tokens.append(('KEYWORD', identifier))  # Add keyword token
            else:
                tokens.append(('IDENTIFIER', identifier))  # Add identifier token
            continue

        # Handle numbers
        if is_digit(char):
            number = char
            i += 1
            while i < len(input_string) and (is_digit(input_string[i]) or input_string[i] == '.'): 
                number += input_string[i]
                i += 1
            tokens.append(('NUMBER', number))  # Add number token
            continue

        # Handle  delimiters 
        if char == '(':
            tokens.append(('PARENTHESIS_OPEN', char))
        elif char == ')':
            tokens.append(('PARENTHESIS_CLOSE', char))
        elif char == '{':
            tokens.append(('BRACE_OPEN', char))
        elif char == '}':
            tokens.append(('BRACE_CLOSE', char))
        elif char == '[':
            tokens.append(('BRACKET_OPEN', char))
        elif char == ']':
            tokens.append(('BRACKET_CLOSE', char))
        elif char == ';':
            tokens.append(('SEMICOLON', char))
        elif char == ',':
            tokens.append(('COMMA', char))
        elif char == '.':
            tokens.append(('PERIOD', char))
        elif char == '~':
            tokens.append(('TILDE', char))

        # Handle operators 
        elif char == '+':
            tokens.append(('OPERATOR', char))
        elif char == '-':
            tokens.append(('OPERATOR', char))
        elif char == '*':
            tokens.append(('OPERATOR', char))
        elif char == '/':
            tokens.append(('OPERATOR', char))
        elif char == '=':
            tokens.append(('ASSIGNMENT', char)) 
        elif char == '==' :
            tokens.append(('OPERATOR', '=='))  
            i += 1  
        elif char == '!=':
            tokens.append(('OPERATOR', '!='))  
            i += 1  
        elif char == '<':
            tokens.append(('OPERATOR', char))
        elif char == '>':
            tokens.append(('OPERATOR', char))
        elif char == '<=':
            tokens.append(('OPERATOR', '<=')) 
            i += 1 
        elif char == '>=':
            tokens.append(('OPERATOR', '>=')) 
            i += 1 

        # Handle any unknown characters (invalid or unexpected)
        elif char not in (' ', '\t', '\n', '\r'):
            tokens.append(('UNKNOWN', char))

        i += 1  # Move to the next character

    return tokens  # Return list of tokens


# Define a route for lexical analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({"error": "Invalid request. 'input' field is required."}), 400

        input_string = data['input']  # Get the input string
        if not isinstance(input_string, str):
            return jsonify({"error": "Invalid input. 'input' must be a string."}), 400

        tokens = lexical_analyzer(input_string)  # Perform lexical analysis
        return jsonify({"tokens": tokens})  # Return the list of tokens as a JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error 


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
