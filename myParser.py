#Apenas testando

contP = 0
contB = 0
contCB = 0

def myParser():
    file = open('lexOutput.txt','r')
    while True:
        token = file.readline()
        if not token:
            break
        token = token.split('~')
        if token[1] == 'RW':
            reservedWord(token, file)
        elif token[1] == 'ID':
            identifier(token, file)
        elif token[1] == 'LIT':
            literals(token, file)
    if contP > 0 or contP < 0:          #Se algum bloco não for fechado ou aberto retorna erro
        print('ERROR')

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
            print(f'Error RW {token[2]} {token[3]}')

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
        print(f'Error ID {token[2]} {token[3]}')

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
        print(f'Error AO {token[2]} {token[3]}')

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
        print(f'Erro int {token[2]} {token[3]}')

def floater(token, file):
    print('Float')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'AO':
        ArithmeticOperator(token, file)
    else:
        print(f'Erro float {token[2]} {token[3]}')

def charSetV(token, file):
    print('CSV')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    else:
        print(f'Erro CSV {token[2]} {token[3]}')

def charSetS(token, file):
    print('CSS')
    token = file.readline().split('~')
    if token[1] == 'SEP':
        separator(token, file)
    elif token[1] == 'LIT':
        literals(token, file)
    else:
        print(f'Erro CSS {token[2]} {token[3]}')

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
        print(f'Erro LO {token[2]} {token[3]}')

        if token[1] == 'OP' or token[1] == 'OB' or token[1] == 'OCB':
            OP(token, file)
        elif token[1] == 'CP' or token[1] == 'CB' or token[1] == 'CCB':
            CP(token, file)



def OP(token, file):
    print('OP')
    global contP
    global contB
    global contCB
    if token[1] == 'OP':
        contP += 1
    elif token[1] == 'OB':
        contB += 1
    elif token[1] == 'OCB':
        contCB += 1


def CP(token, file):
    print('CP')
    global contP
    global contB
    global contCB
    if token[1] == 'CP':
        contP -= 1
    elif token[1] == 'CB':
        contB -= 1
    elif token[1] == 'CCB':
        contCB -= 1