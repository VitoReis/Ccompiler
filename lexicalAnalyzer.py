import re

def analyse():
    line = 1
    colon = 0
    errors = 0
    file = open('code.c', 'r')
    previousRead = ''
    treatment = False
    logicOperatorsList = ['>', '<', '!', '&', '|', ]
    arithmeticOperatorsList = ['+', '-', '*', '/', '%', '=']
    literalsList = ['(', ')', '[', ']', '{', '}', ',', ';']

    while True:
        tokenCreated = False

        if treatment == False:              #Tratando erro de caracter pulado no read()
            charA = file.read(1)
            if charA == '\n':
                colon = 0
            else:
                colon += 1
        else:
            treatment = False
            charA = previousRead


        if not charA:                                                               #Caso programa tenha terminado
            print(f'Finished with {errors} errors')
            break
        elif charA >= '0' and charA <= '9':                                         #Verifica inteiros e flutuantes
            tokenCreated, previousRead, colon = tokenNumber(charA, file, colon)
            treatment = True
        elif charA >= 'a' and charA <= 'z'or charA >= 'A' and charA <= 'Z':         #Verifica palavras reservadas e identificadores
            tokenCreated, previousRead, colon = tokenReservedOrId(charA, file, colon)
            treatment = True
        elif charA == '"':                                                          #Verifica se é um conjunto de caracteres
            tokenCreated, colon = tokenCharacterSet(charA, file, colon)
        elif charA in logicOperatorsList or charA in arithmeticOperatorsList:       #Verifica se é um operador
            tokenCreated, treatment, previousRead = tokenOperator(charA, file)
            if tokenCreated:
                colon += 1
        elif charA in literalsList:                                                 #Verifica se é um literal
            tokenCreated = tokenLiterals(charA)
        elif charA == ' ' or '\n' or '\t':                                          #Verifica espaçamentos e quebras de linha
            if charA == '\n':
                line += 1
            tokenCreated = True
            continue

        if tokenCreated == False:
            print(f"Lexical error in line: {line} colon: {colon}")        #Mostra a linha do erro
            print(f"Error starts in: {charA}")
            createToken('------MISSING TOKEN------')                  #Imprime o erro no arquivo de saida
            charA = file.readline()                                       #Pula a linha com erro
            line += 1                                                     #Adiciona mais um a linha pois ela foi pulada
            colon = 0                                                     #Zera a coluna
            errors += 1
    file.close()


def tokenReservedOrId(charA, file, colon):
    reservedWordsTuple = {('void'):   'void' + '\t'*4 + 'RESERVED WORD',
                ('main'):   'main' + '\t'*4 + 'RESERVED WORD',         
                ('int'):    'int' + '\t'*4 + 'RESERVED WORD',
                ('float'):  'float' + '\t'*4 + 'RESERVED WORD',
                ('char'):   'char' + '\t'*4 + 'RESERVED WORD',
                ('printf'): 'printf' + '\t'*4 + 'RESERVED WORD',
                ('for'):    'for' + '\t'*4 + 'RESERVED WORD',
                ('while'):  'while' + '\t'*4 + 'RESERVED WORD',
                ('true'):   'true' + '\t'*4 + 'RESERVED WORD',
                ('false'):  'false' + '\t'*4 + 'RESERVED WORD',
                ('break'):  'break' + '\t'*4 + 'RESERVED WORD'}

    charB = file.read(1)
    buff = ''
    buff += charA
    tokenCreated = False
    identifier = re.compile("[a-zA-Z_0-9]")

    while (re.match(identifier, charB)):                                #Le a palavra ate o fim
        buff += charB
        charB = file.read(1)

    colon = colon + len(buff)                                           #Calcula quantas colunas foram lidas

    if buff in reservedWordsTuple:                                                   #Verifica se é uma palavra reservada
        createToken(reservedWordsTuple.get(buff))
        tokenCreated = True
    else:                                                               #Verifica se é um identificador
        identifier = re.compile("^[a-zA-Z][a-zA-Z_0-9]*?$")
        if re.match(identifier, buff):
            createToken(buff + '\t'*4 + 'IDENTIFIER')
            tokenCreated = True
        else:
            colon = colon - len(buff)

    return tokenCreated, charB, colon


def tokenCharacterSet(charA, file, colon):                 #Encontra conjuntos de caracteres usando regex
    tokenCreated = False
    characterSetTuple = {   ('"%i"'):   '"%i"' + '\t' * 2 + 'CHARACTER SET - VARIABLE',
                            ('"%f"'):   '"%f"' + '\t' * 2 + 'CHARACTER SET - VARIABLE',
                            ('"%c"'):   '"%c"' + '\t' * 2 + 'CHARACTER SET - VARIABLE'}
    buff = ''
    buff += charA
    charB = file.read(1)
    buff += charB
    identifier = re.compile("^\".*?\"$")
    if charB == '"':                                        #Se charB for o fim da string ja termina
        colon += 1
        if re.match(identifier, buff):
            createToken(buff + '\t'*2 + 'CHARACTER SET - STRING')
            tokenCreated = True
    else:
        while charB != '"':                                 #Se charB nao for o fim da string adiciona no buff ate acabar
            if not charB:
                break
            charB = file.read(1)
            buff += charB

        colon = colon + len(buff)

        if re.match(identifier, buff):                      #Ao acabar verifica o tipo de conjunto
            if buff in characterSetTuple:
                createToken(characterSetTuple.get(buff))
                tokenCreated = True
            else:
                createToken(buff + '\t'*2 + 'CHARACTER SET - STRING')
                tokenCreated = True
        else:
            colon = colon - len(buff)

    return tokenCreated, colon


def tokenNumber(charA, file, colon):
    charB = file.read(1)
    buff = ''
    buff += charA
    tokenCreated = False
    identifier = re.compile("[0-9\.]")
    identifierDetach = re.compile("[\s\\n\\t;,]")
    identifierInt = re.compile("^[0-9][0-9]*?$")
    identifierFloat = re.compile("^[0-9][0-9]*?\.[0-9]*?[0-9]$")

    while (re.match(identifier, charB)):                            #Verifica se o caracter é um numero ou .
        buff += charB
        charB = file.read(1)

    colon = colon + len(buff)

    if not (re.match(identifierDetach, charB)):                     #Se nao terminar com separador retorna erro
        colon = colon - len(buff)
        return tokenCreated, ' ', colon

    if re.match(identifierInt, buff):                               #Verifica se é um inteiro
        createToken(buff + '\t'*5 + 'INTEGER')
        tokenCreated = True
    elif re.match(identifierFloat, buff):                           #Verifica se é um float
        createToken(buff + '\t'*5 + 'FLOAT')
        tokenCreated = True

    return tokenCreated, charB, colon

def tokenOperator(charA, file):
    tokenCreated = False
    treatment = False
    charB = file.read(1)
    buff = charA + charB
    logicOperatorsTuple = {('>'): '>' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('<'): '<' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('=='): '==' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('>='): '>=' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('<='): '<=' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('!='): '!=' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('!'): '!' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('&'): '&' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('&&'): '&&' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('|'): '|' + '\t' * 5 + 'LOGICAL OPERATOR',
                          ('||'): '||' + '\t' * 5 + 'LOGICAL OPERATOR'}

    arithmeticOperatorsTuple = {('+'): '+' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('++'): '++' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('-'): '-' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('--'): '--' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('*'): '*' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('/'): '/' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('%'): '%' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('+='): '+=' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('-='): '-=' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('*='): '*=' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('/='): '/=' + '\t' * 5 + 'ARITHMETIC OPERATOR',
                               ('='): '=' + '\t' * 5 + 'ARITHMETIC OPERATOR'}
    if buff in logicOperatorsTuple:
        createToken(logicOperatorsTuple.get(buff))
        tokenCreated = True
    elif buff in arithmeticOperatorsTuple:
        createToken(arithmeticOperatorsTuple.get(buff))
        tokenCreated = True
    elif charA in logicOperatorsTuple:
        createToken(logicOperatorsTuple.get(charA))
        tokenCreated = True
        treatment = True
    elif charA in arithmeticOperatorsTuple:
        createToken(arithmeticOperatorsTuple.get(charA))
        tokenCreated = True
        treatment = True

    return tokenCreated, treatment, charB

def tokenLiterals(charA):

    literalsTuple = {   ('('): '(' + '\t' * 5 + 'LITERAL',
                        (')'): ')' + '\t' * 5 + 'LITERAL',
                        ('['): '[' + '\t' * 5 + 'LITERAL',
                        (']'): ']' + '\t' * 5 + 'LITERAL',
                        ('{'): '{' + '\t' * 5 + 'LITERAL',
                        ('}'): '}' + '\t' * 5 + 'LITERAL',
                        (','): ',' + '\t' * 5 + 'SEPARATOR',
                        (';'): ';' + '\t' * 5 + 'SEPARATOR'}

    if charA in literalsTuple:
        createToken(literalsTuple.get(charA))
        tokenCreated = True

    return tokenCreated

def createToken(token):                        #Aqui o token é passado e escrito na saida de acordo com a tabela
    output = open('output2.txt','a')
    output.write(token + '\n')
    output.close()
