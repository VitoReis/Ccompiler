lastImportant = ''
subImportant = ''

logicalOperators = ['GT', 'LT', 'EE', 'GE', 'LE', 'DIF', 'OR']
arithmetichOperators = ['ADD', 'SUB', 'MULT', 'DIV']
cbList = []

declarationList = []

def myParser():
    global lastImportant
    file = open('lexOutput.txt','r').readlines()
    s = 0
    token = file[s].split('~')
    if token[1] != 'VOID':
        line = token[3].split('\n')[0]
        print(f'Syntactic error on line: {line} column: {token[2]}')
        errorCount = 1
    else:
        error = False
        errorCount = 0

        while s < len(file):
            token = file[s].split('~')
            error = verify(token, file, s+1)
            if error:
                while s < len(file):
                    token = file[s].split('~')
                    if token[1] == 'SEMICOLON' or token[1] == 'OCB':
                        break
                    else:
                        s += 1
                if token[1] == 'OCB':
                    lastImportant = token[1]
                    line = token[3].split('\n')[0]
                    cbList.append(f'Syntactic error on line: {line} column: {token[2]}')
                    errorCount += 1
                elif token[1] == 'SEMICOLON':
                    lastImportant = 'SEMICOLON'
                    errorCount += 1
            s += 1

    if len(cbList) > 0:
        print(cbList[len(cbList)-1])
        errorCount += 1
    print(f'Parser finished with {errorCount} errors')


def verify(token, file, s):
    global lastImportant, logicalOperators, arithmetichOperators, cbList,subImportant

    if token[1] == 'VOID':
        nexToken = file[s].split('~')
        if nexToken[1] == 'ID':
            lastImportant = token[1]
            return False
        else:
            line = nexToken[3].split('\n')[0]
            print(f'Semantic error in line: {line} column: {nexToken[2]}')
            return True

    elif token[1] == 'ID':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID' and subImportant == 'INT' or lastImportant == 'VOID' and subImportant == 'FLOAT' or \
                                                                    lastImportant == 'VOID' and subImportant == 'CHAR':
            if nexToken[1] == 'COMMA' or nexToken[1] == 'CP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Semantic error in line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'VOID':
            if nexToken[1] == 'OP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Semantic error in line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'INT' or lastImportant == 'FLOAT' or lastImportant == 'CHAR':
            if nexToken[1] == 'COMMA' or nexToken[1] == 'SEMICOLON' or nexToken[1] == 'EQUAL':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'SEMICOLON' or lastImportant == 'OCB':
            if nexToken[1] == 'EQUAL' or nexToken[1] == 'SEMICOLON':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'EQUAL' or lastImportant in arithmetichOperators:
            if nexToken[1] in arithmetichOperators or nexToken[1] == 'SEMICOLON':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'CP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'WHILE':
            if nexToken[1] in logicalOperators or nexToken[1] == 'CP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True

    elif token[1] == 'WHILE':
        nexToken = file[s].split('~')
        if lastImportant == 'SEMICOLON' or lastImportant == 'OCB':
            if nexToken[1] == 'OP':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'INT' or token[1] == 'FLOAT' or token[1] == 'CHAR':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'ID':
                subImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Semantic error in line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'OCB' or lastImportant == 'SEMICOLON':
            if nexToken[1] == 'ID':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'ID':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True

    elif token[1] == 'CHAR - VALUE':
        nexToken = file[s].split('~')
        if lastImportant == 'EQUAL':
            if nexToken[1] == 'SEMICOLON':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'CP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'NUM - INT' or token[1] == 'NUM - FLOAT':
        nexToken = file[s].split('~')
        if lastImportant == 'EQUAL' or lastImportant in arithmetichOperators:
            if nexToken[1] in arithmetichOperators or nexToken[1] == 'SEMICOLON':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'CP' or nexToken[1] in logicalOperators:
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'OP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'CP' or nexToken[1] == 'INT' or nexToken[1] == 'FLOAT':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Semantic error in line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'CS - V - INT' or nexToken[1] == 'CS - V - FLOAT' or nexToken[1] == 'CS - V - CHAR' \
                                                                                or nexToken[1] == 'CS - S':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'WHILE':
            if nexToken[1] == 'ID' or nexToken[1] == 'TRUE' or nexToken[1] == 'FALSE' or nexToken[1] == 'NUM - INT'\
                                                                                        or nexToken[1] == 'NUM - FLOAT':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True


    elif token[1] == 'CP':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID' or lastImportant == 'WHILE':
            if nexToken[1] == 'OCB':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif lastImportant == 'PRINT':
            if nexToken[1] == 'SEMICOLON':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True

    elif token[1] == 'OCB':
        nexToken = file[s].split('~')
        if nexToken[1] != 'VOID':
            lastImportant = token[1]
            line = token[3].split('\n')[0]
            cbList.append(f'Syntactic error on line: {line} column: {token[2]}')  # Frase retornada caso esta chave não possua fechamento
            return False
        else:
            line = nexToken[3].split('\n')[0]
            print(f'Semantic error in line: {line} column: {nexToken[2]}')
            return True



    elif token[1] == 'CCB':
        lastImportant = token[1]
        if len(cbList) >= 1:
            cbList.pop()
            return False
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'PRINT':
        nexToken = file[s].split('~')
        if lastImportant == 'OCB' or lastImportant == 'SEMICOLON':
            if nexToken[1] == 'OP':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True

    elif token[1] == 'CS - S':
        nexToken = file[s].split('~')
        if lastImportant == 'OP':
            if nexToken[1] == 'CP':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'CS - V - INT' or token[1] == 'CS - V - FLOAT' or token[1] == 'CS - V - CHAR':
        nexToken = file[s].split('~')
        if lastImportant == 'OP':
            if nexToken[1] == 'COMMA':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'SEMICOLON':
        lastImportant = token[1]
        return False

    elif token[1] == 'COMMA':
        nexToken = file[s].split('~')
        if lastImportant == 'VOID':
            if nexToken[1] == 'INT' or nexToken[1] == 'FLOAT' or nexToken[1] == 'CHAR':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        elif nexToken[1] == 'ID':
            return False
        else:
            line = nexToken[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {nexToken[2]}')
            return True

    elif token[1] == 'EQUAL':
        nexToken = file[s].split('~')
        if lastImportant == 'ID' or lastImportant == 'NUM - INT' or lastImportant == 'NUM - FLOAT' or lastImportant == 'CHAR - VALUE':
            if nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT' or nexToken[1] == 'CHAR - VALUE':
                lastImportant = token[1]
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] in arithmetichOperators:
        nexToken = file[s].split('~')
        if lastImportant == 'ID' or lastImportant == 'NUM - INT' or lastImportant == 'NUM - FLOAT':
            if nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT':
                lastImportant = token[1]
                if token[1] == 'DIV':
                    if nexToken[0] == '0':
                        line = nexToken[3].split('\n')[0]
                        print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                else:
                    return False
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] in logicalOperators:
        nexToken = file[s].split('~')
        if lastImportant == 'ID' or lastImportant == 'NUM - INT' or lastImportant == 'NUM - FLOAT' or lastImportant == 'CHAR - VALUE':
            if nexToken[1] == 'ID' or nexToken[1] == 'NUM - INT' or nexToken[1] == 'NUM - FLOAT' or nexToken[1] == 'CHAR - VALUE':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True
        else:
            line = token[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {token[2]}')
            return True

    elif token[1] == 'TRUE' or token[1] == 'FALSE':
        nexToken = file[s].split('~')
        if nexToken[1] == 'CP':
            return False
        else:
            line = nexToken[3].split('\n')[0]
            print(f'Syntactic error on line: {line} column: {nexToken[2]}')
            return True

    elif token[1] == 'BREAK':
        nexToken = file[s].split('~')
        if lastImportant == 'SEMICOLON' or lastImportant == 'OCB':
            if nexToken[1] == 'SEMICOLON':
                return False
            else:
                line = nexToken[3].split('\n')[0]
                print(f'Syntactic error on line: {line} column: {nexToken[2]}')
                return True

    else:
        line = token[3].split('\n')[0]
        print(f'Syntactic error on line: {line} column: {token[2]}')
        return True