'''
Morgan Purcell
04/23
A lexical analyzer system for simple arithmetic expressions
'''


# Global declarations
# Variables
charClass = None # LETTER, DIGIT, or UNKNOWN
lexeme = '' # A number of characters that make up a token
nextChar = '' # The next char that will be read from the input file
lexLen = 0 # The length of the current lexeme 
token = None # The token code of the current lexeme
nextToken = None # The token code of the next lexeme to be read from the input file

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

#Token codes dictionary to map token codes to their names
TOKEN_CODES = {
    'INT_LIT': 10,
    'IDENT': 11,
    'ASSIGN_OP': 20,
    'ADD_OP': 21,
    'SUB_OP': 22,
    'MULT_OP': 23,
    'DIV_OP': 24,
    'LEFT_PAREN': 25,
    'RIGHT_PAREN': 26,
    'EQUALS': 27,
    'SEMICOL': 28
}


# Add a char to the current lexeme
def addChar():
    global lexeme, lexLen

    # 'Max' length of the lexeme is 100
    if (lexLen <= 98):
        # Add the char to the lexeme
        lexeme+= str(nextChar)
        # Increase the lexeme length
        lexLen += 1
    else:
        print('Error - lexeme is too long \n')


# Define the char class for the next char
def getChar():
    global nextChar, charClass
    # Read '1' byte from the input file
    nextChar = in_fp.read(1)
    # Check for the end of the file
    if not nextChar:
        charClass = 'EOF'
    # Check if the next char is a letter
    elif nextChar.isalpha():
        charClass = LETTER
    # Check if the next char is a digit
    elif nextChar.isdigit():
        charClass = DIGIT
    else:
        charClass = UNKNOWN


# Parse through the blank spaces
def getNonBlank():
    while(nextChar.isspace()):
        getChar()


# If the charClass is UNKNOWN look up the char
def lookup(char):
    global nextToken

    if (char == '('):
        addChar()
        nextToken = 'LEFT_PAREN'

    elif (char == ')'):
        addChar()
        nextToken = 'RIGHT_PAREN'

    elif (char == '+'):
        addChar()
        nextToken = 'ADD_OP'

    elif (char == '-'):
        addChar()
        nextToken = 'SUB_OP'

    elif (char == '*'):
        addChar()
        nextToken = 'MULT_OP'

    elif (char == '/'):
        addChar()
        nextToken = 'DIV_OP'

    elif (char == '='):
        addChar()
        nextToken = 'EQUALS'

    elif (char == ';'):
        addChar()
        nextToken = 'SEMICOL'

    else:
        addChar()
        nextToken = 'EOF'


# Lexical analyzer 
def lex():
    global lexLen, nextToken, lexeme
    lexLen = 0
    # Parse over the blank spaces
    getNonBlank()

    # If the char class is LETTER
    if (charClass == LETTER):
        # Add the char to the lexeme
        addChar()
        # Get the next char
        getChar()

        # While the char class is LETTER or DIGIT
        while (charClass == LETTER or charClass == DIGIT):
            # Add the char to the lexeme
            addChar()
            # Get the next char
            getChar()

        nextToken = 'IDENT'
    
    # If the char class is DIGIT
    elif (charClass == DIGIT):
        addChar()
        getChar()

        while (charClass == DIGIT):
            addChar()
            getChar()

        nextToken = 'INT_LIT'

    # If the char class is UNKNOWN
    elif (charClass == UNKNOWN):
        # Lookup the char
        lookup(nextChar)
        # Get the next char
        getChar()

    # If charClass is EOF, the while loop in main will terminate after printing the last token and lexeme
    elif (charClass == 'EOF'):
        nextToken = '-1'
        lexeme = 'EOF'

    # Print the token and lexeme
    if (nextToken == '-1'):
        print("End of file\n")
    else:
        print(f"Next token is: {nextToken}({TOKEN_CODES[nextToken]}), Next lexeme is {lexeme}\n")

    # Reset the lexeme
    lexeme = ''


# main driver
if __name__ == '__main__':
    # Prompt the user for an input file
    filename = input("\nEnter the input file name: ")
    # Handle errors opening the file
    try:
        # Open the input data file and process its contents
        # r = read
        with open(filename, 'r') as in_fp:
            # getChar on the first char in the file
            getChar()
            # Just a new line for readability of output
            print('\n')
            # Perform lexical analysis on the rest of the file
            while nextToken != '-1':
                lex()
    except FileNotFoundError:
        print("Error: file not found")
    except Exception as e:
        print("Error:", e)

