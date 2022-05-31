lastImportant = ''
subImportant = ''

logicalOperators = ['GT', 'LT', 'EE', 'GE', 'LE', 'DIF', 'OR']
arithmetichOperators = ['ADD', 'SUB', 'MULT', 'DIV']
cbList = []

def myParser():
    file = open('lexOutput.txt','r').readlines()
    s = 0
    while s < len(file):
        token = file[s].split('~')
        verify(token, file, s+1)
        s += 1
    if len(cbList) > 0:
        print(cbList[len(cbList)])


def verify(token, file, s):
    global lastImportant, subImportant, logicalOperators, arithmetichOperators, cbList
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
        elif lastImportant == 'VOID':
            if nexToken[1] == 'OP':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'INT' or lastImportant == 'FLOAT':
            if nexToken[1] == 'COMMA' or nexToken[1] == 'SEMICOLON' or nexToken[1] == 'EQUAL':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'SEMICOLON' or lastImportant == 'OCB':
            if nexToken[1] == 'EQUAL' or nexToken[1] == 'SEMICOLON':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'EQUAL':
            if nexToken[1] in arithmetichOperators or nexToken[1] == 'SEMICOLON':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'CP':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'WHILE':
            if nexToken[1] in logicalOperators or nexToken[1] == 'CP':       # or nexToken[1] == 'CP'
                lastImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'ID':
            if nexToken[1] == 'OP' or nexToken[1] in arithmetichOperators:
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'WHILE':
        nexToken = file[s].split('~')
        if lastImportant == 'SEMICOLON' or lastImportant == 'OCB':
            if nexToken[1] == 'OP':
                lastImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'INT' or token[1] == 'FLOAT':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'ID':
                subImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'OCB' or lastImportant == 'SEMICOLON':                 # VERIFICAR POSTERIORMENTE
            if nexToken[1] == 'ID':
                lastImportant = token[1]
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'ID':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'NUM - INT' or token[1] == 'NUM - FLOAT':
        nexToken = file[s].split('~')
        if lastImportant == 'EQUAL':
            if nexToken[1] in arithmetichOperators or nexToken[1] == 'SEMICOLON':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'WHILE' or lastImportant == 'ID':
            if nexToken[1] == 'CP' or nexToken[1] in arithmetichOperators:
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'OP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'CP' or nexToken[1] == 'INT' or nexToken[1] == 'FLOAT':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'CS - V - INT' or nexToken[1] == 'CS - V - FLOAT' or nexToken[1] == 'CS - V - CHAR' \
                                                                                or nexToken[1] == 'CS - S':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'ID' or nexToken[1] == 'INT' or nexToken[1] == 'FLOAT' \
                                                            or nexToken[1] == 'TRUE' \
                                                            or nexToken[1] == 'FALSE':
                print('OK')
            else:
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'CP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID' or lastImportant == 'WHILE' or lastImportant == 'ID':
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
            cbList.append(f'ERROR: Column {token[2]} - Line {token[3]}')
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'CCB':
        lastImportant = token[1]
        if len(cbList) >= 1:
            cbList.pop()
            print('OK')
        else:
            print(f'ERROR: Column {token[2]} - Line {token[3]}')


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


    elif token[1] == 'CS - V - INT' or token[1] == 'CS - V - FLOAT' or token[1] == 'CS - V - CHAR':
        nexToken = file[s].split('~')
        if nexToken[1] == 'COMMA':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'SEMICOLON':
        lastImportant = token[1]
        print('OK')


    elif token[1] == 'COMMA':
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'EQUAL':
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT':
            lastImportant = token[1]
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] in arithmetichOperators:
        nexToken = file[s].split('~')
        if token[1] == 'DIV':
            if nexToken[0] == '0':
                print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')
        elif nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] == 'TRUE' or token[1] == 'FALSE':
        nexToken = file[s].split('~')
        if nexToken[1] == 'CP':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')

    elif token[1] == 'BREAK':
        nexToken = file[s].split('~')
        if nexToken[1] == 'SEMICOLON':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    elif token[1] in logicalOperators:
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT':
            print('OK')
        else:
            print(f'ERROR: Column {nexToken[2]} - Line {nexToken[3]}')


    else:
        print(f'ERROR: Column {token[2]} - Line {token[3]}')