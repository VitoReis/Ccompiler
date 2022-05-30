lastImportant = ''
subImportant = ''
operatorsList = ['GT', 'LT', 'EE', 'GE', 'LE', 'DIF', 'OR', 'ADD', 'ADDO', 'SUB', 'SUBO', 'MULT', 'DIV', 'EQUAL']

def myParser():
    file = open('lexOutput.txt','r').readlines()
    s = 0
    while s < len(file):
        token = file[s].split('~')
        verify(token, file, s+1)
        s += 1


def verify(token, file, s):
    global lastImportant, subImportant, operatorsList
    if token[1] == 'VOID':
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID':
            lastImportant = token[1]
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'ID':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID' and subImportant == 'INT':
            if nexToken[1] == 'COMMA':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'INT':
            if nexToken[1] == 'COMMA' or nexToken[1] == 'SEMICOLON' or nexToken[1] in operatorsList:
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'SEMICOLON':
            if nexToken[1] in operatorsList or nexToken[1] == 'SEMICOLON':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'VOID':
            if nexToken[1] == 'OP':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'OP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'CP':
                print('OK')
            elif nexToken[1] == 'INT' or nexToken[1] == 'FLOAT':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'CS - V' or nexToken[1] == 'CS - S':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'INT':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'ID':
                subImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'FLOAT':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'ID':
                subImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'CP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'OCB':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'SEMICOLON':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'OCB':
        nexToken = file[s].split('~')
        lastImportant = token[1]
        subImportant = ''
        if nexToken[1] != 'VOID':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'PRINT':
        nexToken = file[s].split('~')
        if lastImportant == 'OCB' or lastImportant == 'SEMICOLON':                 # VERIFICAR POSTERIORMENTE
            if nexToken[1] == 'OP':
                lastImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'CS - S':
        nexToken = file[s].split('~')
        if nexToken[1] == 'CP':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'SEMICOLON':
        lastImportant = token[1]
        print('OK')
    elif token[1] == 'INT':
        nexToken = file[s].split('~')
        if lastImportant == 'OCB' or lastImportant == 'SEMICOLON':                 # VERIFICAR POSTERIORMENTE
            if nexToken[1] == 'ID':
                lastImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
    elif token[1] == 'COMMA':
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')

myParser()