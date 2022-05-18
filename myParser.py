#Apenas testando
def myParser():
    file = open('lexOutput.txt','r')
    while True:
        token = file.readline()
        if not token:
            quit()
        token = token.split('~')
        if token[1] == 'RW':
            reservedWord(token, file)
        elif token[1] == 'ID':
            identifier(token, file)
        elif token[1] == 'LIT':
            literals(token, file)

def reservedWord(token, file):
        print('RW')
        token = file.readline()
        if not token:
            quit()
        token = token.split('~')
        if token[1] == 'ID':
            identifier(token, file)
        elif token[1] == 'LIT':
            literals(token, file)
        elif token[1] == 'SEP':
            separator(token, file)
        else:
            print('Error RW')

def identifier(token, file):
    print('ID')
    token = file.readline()
    if not token:
        quit()
    token = token.split('~')
    if token[1] == 'ID':
        identifier(token, file)
    elif token[1] == 'AO':
        ArithmeticOperator(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    elif token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'LO':
        logicalOperator(token, file)
    else:
        print('Error ID')

def ArithmeticOperator(token, file):
    print('AO')
    token = file.readline().split('~')
    if token[1] == 'ID':
        identifier(token, file)
    elif token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'INT':
        integer(token, file)
    elif token[1] == 'FLOAT':
        floater(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    else:
        print('Error AO')

def literals(token, file):
    print('Lit')
    token = file.readline()
    if not token:
        quit()
    token = token.split('~')
    if token[1] == 'LIT':
        literals(token, file)
    elif token[1] == 'CS - V':
        charSetV(token, file)
    elif token[1] == 'CS - S':
        charSetS(token, file)
    elif token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'RW':
        reservedWord(token, file)
    elif token[1] == 'ID':
        identifier(token, file)
    else:
        print(f'Erro literals {token[2]} {token[3]}')

def separator(token, file):
    print('SEP')

def integer(token, file):
    print('INT')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'AO':
        ArithmeticOperator(token, file)
    else:
        print('Erro int')

def floater(token, file):
    print('Float')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'AO':
        ArithmeticOperator(token, file)
    else:
        print('Erro float')

def charSetV(token, file):
    print('CSV')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    else:
        print('Erro CSV')

def charSetS(token, file):
    print('CSS')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    else:
        print('Erro CSS')

def logicalOperator(token, file):
    print('LO')
    token = file.readline().split('~')
    if token[1] == 'ID':
        identifier(token, file)
    elif token[1] == 'INT':
        integer(token, file)
    elif token[1] == 'FLOAT':
        floater(token, file)
    else:
        print('Erro LO')