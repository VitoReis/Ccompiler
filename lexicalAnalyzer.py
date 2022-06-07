import re

def lexical():
    line = 1
    column = 0
    errors = 0
    jump = True
    treatment = False
    identifierNumber = ("[0-9]")
    identifierWord = ("[a-zA-Z]")
    identifierSpaces = ("[\s\\n\\t]")
    previousRead = ''
    logicOperatorsList = ['>', '<', '|']
    arithmeticOperatorsList = ['+', '-', '*', '/', '=']
    literalsList = ['(', ')', '{', '}', ',', ';']

    file = open('code.c', 'r')

    while True:
        tokenCreated = False

        if treatment == False:              #Tratando erro de caracter pulado no read()
            charA = file.read(1)
            if charA == '\n':
                column = 0
            else:
                column += 1
        else:
            treatment = False
            charA = previousRead


        if not charA:                                                               # Caso programa tenha terminado
            print(f'Lexical analyzer finished with {errors} errors')
            break
        elif (re.match(identifierNumber, charA)):                                   # Verifica inteiros e flutuantes
            tokenCreated, previousRead, column = tokenNumber(charA, file, column, line)
            treatment = True
        elif (re.match(identifierWord, charA)):                                     # Verifica palavras reservadas e identificadores
            tokenCreated, previousRead, column = tokenReservedOrId(charA, file, column, line)
            treatment = True
        elif charA == '"' or charA == '\'':                                         # Verifica se é um conjunto de caracteres
            tokenCreated, column, jump = tokenCharacterSet(charA, file, column, line)
        elif charA in logicOperatorsList or charA in arithmeticOperatorsList:       # Verifica se é um operador
            tokenCreated, treatment, previousRead = tokenOperator(charA, file, column, line)
            if tokenCreated:
                column += 1
        elif charA in literalsList:                                                 # Verifica se é um literal
            tokenCreated = tokenLiterals(charA, column, line)
        elif re.match(identifierSpaces, charA):                              # Verifica espaçamentos e quebras de linha
            if charA == '\n':
                line += 1
            tokenCreated = True
            continue
        else:
            tokenCreated = False

        if tokenCreated == False:
            print(f"Lexical error in line: {line} column: {column}")          #Mostra a linha do erro
            print(f"Error starts in: {charA}")
            createToken('------MISSING TOKEN------','ERROR',column,line)     #Imprime o erro no arquivo de saida
            if jump:
                charA = file.readline()                                     #Pula a linha com erro
            else:
                jump = True
            line += 1                                                       #Adiciona mais um a linha pois ela foi pulada
            column = 0                                                       #Zera a coluna
            errors += 1
    file.close()


def tokenReservedOrId(charA, file, column, line):
    reservedWordsDict = {'int'  :   ['int', 'INT'],
                        'float' :   ['float', 'FLOAT'],
                        'char'  :   ['char', 'CHAR'],
                        'printf':   ['printf', 'PRINT'],
                        'while' :   ['while', 'WHILE'],
                        'true'  :   ['true', 'TRUE'],
                        'false' :   ['false', 'FALSE'],
                        'break' :   ['break', 'BREAK']}

    identifier = re.compile("[a-zA-Z_0-9]")
    charB = file.read(1)
    buff = ''
    buff += charA
    tokenCreated = False

    while (re.match(identifier, charB)):
        buff += charB
        charB = file.read(1)

    tokenColumn = column

    column = column + len(buff)                                           #Calcula quantas colunas foram lidas

    if buff in reservedWordsDict:                                      #Verifica se é uma palavra reservada
        createToken(reservedWordsDict.get(buff)[0],reservedWordsDict.get(buff)[1], tokenColumn, line)
        tokenCreated = True
    else:                                                               #Verifica se é um identificador
        identifier = re.compile("^[a-zA-Z][a-zA-Z_0-9]*?$")
        if re.match(identifier, buff):
            createToken(buff, 'ID', tokenColumn, line)
            tokenCreated = True
        else:
            column = column - len(buff)

    return tokenCreated, charB, column


def tokenCharacterSet(charA, file, column, line):                 #Encontra conjuntos de caracteres usando regex
    tokenCreated = False
    jump = True
    characterSetDict = {'"%i"':   ['"%i"', 'CS - V - INT'],
                        '"%f"':   ['"%f"', 'CS - V - FLOAT'],
                        '"%c"':   ['"%c"', 'CS - V - CHAR']}
    buff = ''
    buff += charA
    charB = file.read(1)
    buff += charB
    tokenColumn = column
    identifier = re.compile('^\".*?\"$')
    identifierCharCaracter = re.compile('^\'.?\'$')
    if charB == '"':                                        #Se charB for o fim da string ja termina
        column += 1
        if re.match(identifier, buff):
            createToken(buff, 'CS - S', tokenColumn, line)
            tokenCreated = True
    elif charB == '\'':
        column += 1
        if re.match(identifierCharCaracter, buff):
            createToken(buff, 'CHAR - VALUE', tokenColumn, line)
            tokenCreated = True
    else:
        while charB != '"' and charB != '\'' and charB != '\n':                                 #Se charB nao for o fim da string adiciona no buff ate acabar
            if not charB:
                break
            charB = file.read(1)
            buff += charB

        column = column + len(buff)
        if charB == '\n':
            jump = False
        elif re.match(identifier, buff):                      #Ao acabar verifica o tipo de conjunto
            if buff in characterSetDict:
                createToken(characterSetDict.get(buff)[0], characterSetDict.get(buff)[1], tokenColumn, line)
                tokenCreated = True
            else:
                createToken(buff, 'CS - S', tokenColumn, line)
                tokenCreated = True
        elif re.match(identifierCharCaracter, buff):
            createToken(buff, 'CHAR - VALUE', tokenColumn, line)
            tokenCreated = True
        else:
            column = column - len(buff)

    return tokenCreated, column, jump


def tokenNumber(charA, file, column, line):
    charB = file.read(1)
    buff = ''
    buff += charA
    tokenCreated = False
    identifier = re.compile("[0-9\.]")
    identifierDetach = re.compile("[\s\n\t;,)\]+\-*/><=!|]")
    identifierInt = re.compile("^[0-9][0-9]*?$")
    identifierFloat = re.compile("^[0-9][0-9]*?\.[0-9]*?[0-9]$")

    while (re.match(identifier, charB)):                            #Verifica se o caracter é um numero ou .
        buff += charB
        charB = file.read(1)
    tokenColumn = column
    column = column + len(buff)

    if not (re.match(identifierDetach, charB)):                     #Se nao terminar com separador retorna erro
        column = column - len(buff)
        return tokenCreated, ' ', column

    if re.match(identifierInt, buff):                               #Verifica se é um inteiro
        createToken(buff, 'NUM - INT', tokenColumn, line)
        tokenCreated = True
    elif re.match(identifierFloat, buff):                           #Verifica se é um float
        createToken(buff, 'NUM - FLOAT', tokenColumn, line)
        tokenCreated = True

    return tokenCreated, charB, column

def tokenOperator(charA, file, column, line):
    tokenColumn = column
    tokenCreated = False
    treatment = False
    charB = file.read(1)
    buff = charA + charB
    logicOperatorsDict = {'>': ['>', 'GT'],
                          '<': ['<', 'LT'],
                          '==': ['==', 'EE'],
                          '>=': ['>=', 'GE'],
                          '<=': ['<=', 'LE'],
                          '!=': ['!=', 'DIF'],
                          '||': ['||', 'OR']}

    arithmeticOperatorsDict = {'+': ['+', 'ADD'],
                               '-': ['-', 'SUB'],
                               '*': ['*', 'MULT'],
                               '/': ['/', 'DIV'],
                               '=': ['=', 'EQUAL']}

    if buff in logicOperatorsDict:
        createToken(logicOperatorsDict.get(buff)[0], logicOperatorsDict.get(buff)[1], tokenColumn, line)
        tokenCreated = True
    elif buff in arithmeticOperatorsDict:
        createToken(arithmeticOperatorsDict.get(buff)[0], arithmeticOperatorsDict.get(buff)[1], tokenColumn, line)
        tokenCreated = True
    elif charA in logicOperatorsDict:
        createToken(logicOperatorsDict.get(charA)[0], logicOperatorsDict.get(charA)[1], tokenColumn, line)
        tokenCreated = True
        treatment = True
    elif charA in arithmeticOperatorsDict:
        createToken(arithmeticOperatorsDict.get(charA)[0], arithmeticOperatorsDict.get(charA)[1], tokenColumn, line)
        tokenCreated = True
        treatment = True

    return tokenCreated, treatment, charB

def tokenLiterals(charA, column, line):
    tokenColumn = column
    literalsDict = {    '(': ['(', 'OP'],
                        ')': [')', 'CP'],
                        '{': ['{', 'OCB'],
                        '}': ['}', 'CCB'],
                        ',': [',', 'COMMA'],
                        ';': [';', 'SEMICOLON']}

    if charA in literalsDict:
        createToken(literalsDict.get(charA)[0], literalsDict.get(charA)[1], tokenColumn, line)
        tokenCreated = True
    return tokenCreated

def createToken(content, token, tokenColumn, tokenLine):                        #Aqui o token é passado e escrito na saida de acordo com a tabela
    output = open('lexOutput.txt','a')
    userOutput = open('lexUserOutput.txt','a')
    output.write(f'{content}~{token}~{tokenColumn}~{tokenLine}\n')
    userOutput.write(f'CONTENT: {content} - TOKEN: {token} - COLUMN: {tokenColumn} - LINE: {tokenLine}\n')
    output.close()
    userOutput.close()