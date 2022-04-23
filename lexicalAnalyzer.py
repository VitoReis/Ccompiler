import re

def analyse():
    line = 1
    colon = 0
    errors = 0
    file = open('code.c', 'r')
    previousRead = ''
    treatment = False
    logicOperatorsList = ['>', '<', '==', '>=', '<=', '!=', '!', '&', '&&', '|', '||']
    arithmeticOperatorsList = ['+', '++', '-', '--', '*', '/', '%', '+=', '-=', '*=', '/=', '=']
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
            tokenCreated, treatment, previousRead = tokenOperator(charA, file, logicOperatorsList, arithmeticOperatorsList)
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
    list = ['#include', 'main', 'void',
            'int', 'float', 'char',
            'printf', 'for', 'while',
            'true', 'false', 'break']

    charB = file.read(1)
    buff = ''
    buff += charA
    tokenCreated = False
    identifier = re.compile("[a-zA-Z_0-9]")

    while (re.match(identifier, charB)):                                #Le a palavra ate o fim
        buff += charB
        charB = file.read(1)

    colon = colon + len(buff)                                           #Calcula quantas colunas foram lidas

    if buff in list:                                                    #Verifica se é uma palavra reservada
        index = 0
        while index < len(list):                                        #Acha qual palavra reservada deu match
            if buff == list[index]:
                createToken(list[index] + '\t'*4 + 'RESERVED WORD')
                tokenCreated = True
                break
            index += 1
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
    list = ['"%i"','"%f"','"%c"']                          #Conjuntos para impressão de aritmeticos em C
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
            if buff in list:
                createToken(buff + '\t' * 2 + 'CHARACTER SET - VARIABLE')
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


def tokenOperator(charA, file, logicOperatorsList, arithmeticOperatorsList):
    tokenCreated = False
    treatment = False
    charB = file.read(1)
    op = charA + charB

    #Se o charB nao esta na lista ele nao nos interessa e o tratamento é necessario, caso contrario um caracter sera ignorado
    if not charB in logicOperatorsList and not charB in arithmeticOperatorsList:
        treatment = True

    #Verifica todas as possibilidades, nao encontrei um modo mais facil de fazer essa operação
    if charA == '>':
        if treatment:
            createToken(charA + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '<':
        if treatment:
            createToken(charA + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '=':
        if treatment:
            createToken(charA + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '&':
        if treatment:
            createToken(charA + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
        elif treatment and charB != '&':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '|':
        if treatment:
            createToken(charA + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
        elif treatment and charB != '|':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '!':
        if treatment:
            createToken(charA + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'LOGICAL OPERATOR')
            tokenCreated = True
    elif charA == '+':
        if treatment:
            createToken(charA + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
        elif treatment and charB != '+':
            tokenCreated = False
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
    elif charA == '-':
        if treatment:
            createToken(charA + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
        elif treatment and charB != '-':
            tokenCreated = False
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
    elif charA == '/':
        if treatment:
            createToken(charA + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
    elif charA == '%':
        createToken('% '+ '\t'*5 + 'ARITHMETIC OPERATOR')
        tokenCreated = True
    elif charA == '*':
        if treatment:
            createToken(charA + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
        elif treatment and charB != '=':
            tokenCreated = False
        else:
            createToken(op + '\t'*5 + 'ARITHMETIC OPERATOR')
            tokenCreated = True
    return tokenCreated, treatment, charB


def tokenLiterals(charA):
    #Verifica os literais um por um
    if charA == '(':
        createToken('(' + '\t' * 5 + 'LITERAL')
        tokenCreated = True
    elif charA == ')':
        createToken(')' + '\t' * 5 + 'LITERAL')
        tokenCreated = True
    elif charA == '{':
        createToken('{' + '\t' * 5 + 'LITERAL')
        tokenCreated = True
    elif charA == '}':
        createToken('}' + '\t' * 5 + 'LITERAl')
        tokenCreated = True
    elif charA == ';':
        createToken(';' + '\t' * 5 + 'SEPARATOR')
        tokenCreated = True
    elif charA == ',':
        createToken(',' + '\t' * 5 + 'SEPARATOR')
        tokenCreated = True
    return tokenCreated


def createToken(token):                        #Aqui o token é passado e escrito na saida de acordo com a tabela
    output = open('output.txt','a')
    output.write(token + '\n')
    output.close()