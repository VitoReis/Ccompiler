import os

lastImportant = []
ED = ['EE', 'DIF']
GLE = ['GT', 'LT', 'GE', 'LE', 'OR']
AO = ['ADD', 'SUB', 'MULT', 'DIV']

prints = []         # Guarda os prints declarados e suas posições e valores

declarations = []   # Guarda os ids declarados com suas posições
decID = []          # Guarda os ids declarados
types = []          # Guarda os ids declarados e seus tipos
operations = []
values = []         # Guarda os ids chamados e seus valores
ids = []            # Guarda os ids chamados
idPos = []          # Guarda os ids chamados e suas posições

def myParser():
    file = open('lexOutput.txt', 'r').readlines()
    s = 0
    token = file[s].split('~')
    if token[1] == 'ID':
        ID(file, s + 1)
        print(f'Parser finished with 0 errors')
    elif token[1] == 'INT':
        INT(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'FLOAT':
        FLOAT(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'CHAR':
        CHAR(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'PRINT':
        PRINTF(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'WHILE':
        WHILE(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'IF':
        IF(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == 'BREAK':
        BREAK(file, s + 1)
        print(f'Parser finished with 0 errors')
        return 0
    elif token[1] == '$':
        print(f'Parser finished with 0 errors')
        return 0
    else:
        error(file, s - 1)


############################################ VARIABLES #################################################################
def INT(file, s):
    global lastImportant
    thisToken = file[s-1].split('~')
    next = file[s].split('~')
    if next[1] == 'ID':
        lastImportant.append('INT')
        line = next[3].split('\n')[0]
        declarations.append(f'{next[0]}~{next[2]}~{line}')
        decID.append(next[0])
        types.append(f'{thisToken[1]}~{next[0]}')       # Guarda o tipo de cada ID
        ID(file, s + 1)
    else:
        error(file, s)

def FLOAT(file, s):
    global lastImportant
    thisToken = file[s-1].split('~')
    next = file[s].split('~')
    if next[1] == 'ID':
        lastImportant.append('FLOAT')
        line = next[3].split('\n')[0]
        declarations.append(f'{next[0]}~{next[2]}~{line}')
        decID.append(next[0])
        types.append(f'{thisToken[1]}~{next[0]}')               # Guarda o tipo de cada ID
        ID(file, s + 1)
    else:
        error(file, s)

def CHAR(file, s):
    global lastImportant
    thisToken = file[s-1].split('~')
    next = file[s].split('~')
    if next[1] == 'ID':
        lastImportant.append('CHAR')
        line = next[3].split('\n')[0]
        declarations.append(f'{next[0]}~{next[2]}~{line}')
        decID.append(next[0])
        types.append(f'{thisToken[1]}~{next[0]}')  # Guarda o tipo de cada ID
        ID(file, s + 1)
    else:
        error(file, s)
########################################################################################################################

############################################ RESERVED WORDS ############################################################
def BREAK(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant)-1] == 'WHILE':
            if next[1] == 'SEMICOLON':
                SEMICOLON(file, s + 1)
            else:
                error(file, s - 1)
        else:
            error(file, s - 1)
    else:
        error(file, s)

def WHILE(file, s):
    global lastImportant
    next = file[s].split('~')
    if next[1] == 'OP':
        lastImportant.append('WHILE')
        OP(file, s + 1)
    else:
        error(file, s)

def IF(file, s):
    global lastImportant
    next = file[s].split('~')
    if next[1] == 'OP':
        lastImportant.append('IF')
        OP(file, s + 1)
    else:
        error(file, s)

def ELSE(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant)-1] == 'IF':
            lastImportant.pop()
            if next[1] == 'IF':
                IF(file, s + 1)
            elif next[1] == 'OCB':
                OCB(file, s + 1)
            else:
                error(file, s)
        else:
            error(file, s - 1)
    else:
        error(file, s - 1)

def TRUE(file, s):
    next = file[s].split('~')
    if next[1] == 'CP':
        CP(file, s + 1)
    else:
        error(file, s)

def FALSE(file, s):
    next = file[s].split('~')
    if next[1] == 'CP':
        CP(file, s + 1)
    else:
        error(file, s)

def PRINTF(file, s):
    global lastImportant
    thisToken = file[s-1].split('~')
    next = file[s].split('~')
    value = file[s+1].split('~')
    line = thisToken[3].split("\n")[0]
    if value[1] == 'STRING':
        prints.append(f'{thisToken[1]}~{line}~{thisToken[2]}~{value[0]}')
    else:
        prints.append(f'{thisToken[1]}~{line}~{thisToken[2]}~ ')
    if next[1] == 'OP':
        lastImportant.append('PRINT')
        OP(file, s + 1)
    else:
        error(file, s - 1)
########################################################################################################################

############################################## VALUES ##################################################################
def NUM_INT(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] == 'WHILE' or lastImportant[len(lastImportant) - 1] == 'IF':
            if next[1] == 'EE':
                EE(file, s + 1)
            elif next[1] == 'DIF':
                DIF(file, s + 1)
            elif next[1] == 'GT':
                GT(file, s + 1)
            elif next[1] == 'GE':
                GE(file, s + 1)
            elif next[1] == 'LT':
                LT(file, s + 1)
            elif next[1] == 'LE':
                LE(file, s + 1)
            elif next[1] == 'OR':
                OR(file, s + 1)
            elif next[1] == 'ADD':
                ADD(file, s + 1)
            elif next[1] == 'SUB':
                SUB(file, s + 1)
            elif next[1] == 'MULT':
                MULT(file, s + 1)
            elif next[1] == 'DIV':
                DIV(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant) - 1] != 'FLOAT' and lastImportant[len(lastImportant) - 1] != 'INT':
            errorS(file, s-1)
        elif next[1] == 'EE':
            EE(file, s + 1)
        elif next[1] == 'DIF':
            DIF(file, s + 1)
        elif next[1] == 'GT':
            GT(file, s + 1)
        elif next[1] == 'GE':
            GE(file, s + 1)
        elif next[1] == 'LT':
            LT(file, s + 1)
        elif next[1] == 'LE':
            LE(file, s + 1)
        elif next[1] == 'OR':
            OR(file, s + 1)
        elif next[1] == 'ADD':
            ADD(file, s + 1)
        elif next[1] == 'SUB':
            SUB(file, s + 1)
        elif next[1] == 'MULT':
            MULT(file, s + 1)
        elif next[1] == 'DIV':
            DIV(file, s + 1)
        elif next[1] == 'SEMICOLON':
            SEMICOLON(file, s + 1)
        else:
            error(file, s)
    elif next[1] == 'EE':
        EE(file, s + 1)
    elif next[1] == 'DIF':
        DIF(file, s + 1)
    elif next[1] == 'GT':
        GT(file, s + 1)
    elif next[1] == 'GE':
        GE(file, s + 1)
    elif next[1] == 'LT':
        LT(file, s + 1)
    elif next[1] == 'LE':
        LE(file, s + 1)
    elif next[1] == 'OR':
        OR(file, s + 1)
    elif next[1] == 'ADD':
        ADD(file, s + 1)
    elif next[1] == 'SUB':
        SUB(file, s + 1)
    elif next[1] == 'MULT':
        MULT(file, s + 1)
    elif next[1] == 'DIV':
        DIV(file, s + 1)
    elif next[1] == 'SEMICOLON':
        SEMICOLON(file, s + 1)
    else:
        error(file, s)

def NUM_FLOAT(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] == 'WHILE' or lastImportant[len(lastImportant) - 1] == 'IF':
            if next[1] == 'EE':
                EE(file, s + 1)
            elif next[1] == 'DIF':
                DIF(file, s + 1)
            elif next[1] == 'GT':
                GT(file, s + 1)
            elif next[1] == 'GE':
                GE(file, s + 1)
            elif next[1] == 'LT':
                LT(file, s + 1)
            elif next[1] == 'LE':
                LE(file, s + 1)
            elif next[1] == 'OR':
                OR(file, s + 1)
            elif next[1] == 'ADD':
                ADD(file, s + 1)
            elif next[1] == 'SUB':
                SUB(file, s + 1)
            elif next[1] == 'MULT':
                MULT(file, s + 1)
            elif next[1] == 'DIV':
                DIV(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant) - 1] != 'FLOAT':
            errorS(file, s - 1)
    elif next[1] == 'EE':
        EE(file, s + 1)
    elif next[1] == 'DIF':
        DIF(file, s + 1)
    elif next[1] == 'GT':
        GT(file, s + 1)
    elif next[1] == 'GE':
        GE(file, s + 1)
    elif next[1] == 'LT':
        LT(file, s + 1)
    elif next[1] == 'LE':
        LE(file, s + 1)
    elif next[1] == 'OR':
        OR(file, s + 1)
    elif next[1] == 'ADD':
        ADD(file, s + 1)
    elif next[1] == 'SUB':
        SUB(file, s + 1)
    elif next[1] == 'MULT':
        MULT(file, s + 1)
    elif next[1] == 'DIV':
        DIV(file, s + 1)
    elif next[1] == 'SEMICOLON':
        SEMICOLON(file, s + 1)
    else:
        error(file, s)

def CHAR_VALUE(file, s):
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] != 'CHAR':
            errorS(file, s - 1)
        elif next[1] == 'SEMICOLON':
            SEMICOLON(file, s + 1)
        else:
            error(file, s)
    elif next[1] == 'SEMICOLON':
        SEMICOLON(file, s + 1)
    else:
        error(file, s)

def STRING(file, s):
    next = file[s].split('~')
    if next[1] == 'CP':
        CP(file, s + 1)
    else:
        error(file, s)
########################################################################################################################

def ID(file, s):
    global lastImportant
    thisId = file[s-1].split('~')
    next = file[s].split('~')
    line = thisId[3].split('\n')[0]
    if not thisId[0] in ids:
        ids.append(thisId[0])
        idPos.append(f'{thisId[0]}~{thisId[2]}~{line}')

    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant)-1] == 'PRINT':
            if next[1] == 'CP':
                CP(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant)-1] == 'IF' or lastImportant[len(lastImportant)-1] == 'WHILE':
            if next[1] == 'EE':
                EE(file, s + 1)
            elif next[1] == 'DIF':
                DIF(file, s + 1)
            elif next[1] == 'EQUAL':
                EQUAL(file, s + 1)
            elif next[1] == 'GT':
                GT(file, s + 1)
            elif next[1] == 'GE':
                GE(file, s + 1)
            elif next[1] == 'LT':
                LT(file, s + 1)
            elif next[1] == 'LE':
                LE(file, s + 1)
            elif next[1] == 'OR':
                OR(file, s + 1)
            elif next[1] == 'ADD':
                ADD(file, s + 1)
            elif next[1] == 'SUB':
                SUB(file, s + 1)
            elif next[1] == 'MULT':
                MULT(file, s + 1)
            elif next[1] == 'DIV':
                DIV(file, s + 1)
            elif next[1] == 'CP':
                CP(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant) - 1] == 'INT' or lastImportant[len(lastImportant) - 1] == 'FLOAT' or \
            lastImportant[len(lastImportant)-1] == 'CHAR':
            if next[1] == 'EQUAL':
                EQUAL(file, s + 1)
            elif next[1] == 'COMMA':
                COMMA(file, s + 1)
            elif next[1] == 'SEMICOLON':
                SEMICOLON(file, s + 1)
            else:
                error(file, s)
        else:
            error(file, s)
    elif next[1] == 'EE':
        EE(file, s + 1)
    elif next[1] == 'DIF':
        DIF(file, s + 1)
    elif next[1] == 'GT':
        GT(file, s + 1)
    elif next[1] == 'GE':
        GE(file, s + 1)
    elif next[1] == 'LT':
        LT(file, s + 1)
    elif next[1] == 'LE':
        LE(file, s + 1)
    elif next[1] == 'OR':
        OR(file, s + 1)
    elif next[1] == 'ADD':
        ADD(file, s + 1)
    elif next[1] == 'SUB':
        SUB(file, s + 1)
    elif next[1] == 'MULT':
        MULT(file, s + 1)
    elif next[1] == 'DIV':
        DIV(file, s + 1)
    elif next[1] == 'SEMICOLON':
        SEMICOLON(file, s + 1)
    elif next[1] == 'EQUAL':
        EQUAL(file, s + 1)
    else:
        error(file, s)
########################################################################################################################
def OP(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] == 'IF' or lastImportant[len(lastImportant) - 1] == 'WHILE':
            if next[1] == 'ID':
                ID(file, s + 1)
            elif next[1] == 'TRUE':
                TRUE(file, s + 1)
            elif next[1] == 'FALSE':
                FALSE(file, s + 1)
            elif next[1] == 'NUM - INT':
                NUM_INT(file, s + 1)
            elif next[1] == 'NUM - FLOAT':
                NUM_FLOAT(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant) - 1] == 'PRINT':
            if next[1] == 'STRING':
                STRING(file, s + 1)
            else:
                error(file, s)
        else:
            error(file, s)
    else:
        error(file, s)

def CP(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] == 'IF' or lastImportant[len(lastImportant) - 1] == 'WHILE':
            if next[1] == 'OCB':
                OCB(file, s + 1)
            else:
                error(file, s)
        elif lastImportant[len(lastImportant) - 1] == 'PRINT':
            if next[1] == 'SEMICOLON':
                SEMICOLON(file, s + 1)
            else:
                error(file, s)
    else:
        error(file, s)

def SEMICOLON(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:
        if lastImportant[len(lastImportant) - 1] == 'PRINT' or lastImportant[len(lastImportant) - 1] == 'INT'\
                or lastImportant[len(lastImportant) - 1] == 'FLOAT' or lastImportant[len(lastImportant) - 1] == 'CHAR':
            lastImportant.pop()
            if next[1] == 'ID':
                ID(file, s + 1)
            elif next[1] == 'INT':
                INT(file, s + 1)
            elif next[1] == 'FLOAT':
                FLOAT(file, s + 1)
            elif next[1] == 'CHAR':
                CHAR(file, s + 1)
            elif next[1] == 'PRINT':
                PRINTF(file, s + 1)
            elif next[1] == 'WHILE':
                WHILE(file, s + 1)
            elif next[1] == 'IF':
                IF(file, s + 1)
            elif next[1] == 'BREAK':
                BREAK(file, s + 1)
            elif next[1] == 'CCB':
                CCB(file, s + 1)
            elif next[1] == '$':
                return 0
            else:
                error(file, s)
        else:
            if next[1] == 'ID':
                ID(file, s + 1)
            elif next[1] == 'INT':
                INT(file, s + 1)
            elif next[1] == 'FLOAT':
                FLOAT(file, s + 1)
            elif next[1] == 'CHAR':
                CHAR(file, s + 1)
            elif next[1] == 'PRINT':
                PRINTF(file, s + 1)
            elif next[1] == 'WHILE':
                WHILE(file, s + 1)
            elif next[1] == 'IF':
                IF(file, s + 1)
            elif next[1] == 'BREAK':
                BREAK(file, s + 1)
            elif next[1] == 'CCB':
                CCB(file, s + 1)
            elif next[1] == '$':
                return 0
            else:
                error(file, s - 1)
    elif next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'INT':
        INT(file, s + 1)
    elif next[1] == 'FLOAT':
        FLOAT(file, s + 1)
    elif next[1] == 'CHAR':
        CHAR(file, s + 1)
    elif next[1] == 'PRINT':
        PRINTF(file, s + 1)
    elif next[1] == 'WHILE':
        WHILE(file, s + 1)
    elif next[1] == 'IF':
        IF(file, s + 1)
    elif next[1] == 'BREAK':
        BREAK(file, s + 1)
    elif next[1] == 'CCB':
        CCB(file, s + 1)
    elif next[1] == '$':
        return 0
    else:
        error(file, s - 1)

def OCB(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'INT':
        INT(file, s + 1)
    elif next[1] == 'FLOAT':
        FLOAT(file, s + 1)
    elif next[1] == 'CHAR':
        CHAR(file, s + 1)
    elif next[1] == 'PRINT':
        PRINTF(file, s + 1)
    elif next[1] == 'WHILE':
        WHILE(file, s + 1)
    elif next[1] == 'IF':
        IF(file, s + 1)
    elif next[1] == 'BREAK':
        BREAK(file, s + 1)
    elif next[1] == 'CCB':
        CCB(file, s + 1)
    else:
        error(file, s - 1)

def CCB(file, s):
    global lastImportant
    next = file[s].split('~')
    if len(lastImportant) >= 1:                             # Talvez n precise pois pra ter CCB tem q ter  lastImportant
        if lastImportant[len(lastImportant) - 1] == 'IF':
            if next[1] != 'ELSE':
                lastImportant.pop()
            else:
                ELSE(file, s + 1)
        elif next[1] == 'ID':
            lastImportant.pop()
            ID(file, s + 1)
        elif next[1] == 'INT':
            lastImportant.pop()
            INT(file, s + 1)
        elif next[1] == 'FLOAT':
            lastImportant.pop()
            FLOAT(file, s + 1)
        elif next[1] == 'CHAR':
            lastImportant.pop()
            CHAR(file, s + 1)
        elif next[1] == 'PRINT':
            lastImportant.pop()
            PRINTF(file, s + 1)
        elif next[1] == 'WHILE':
            lastImportant.pop()
            WHILE(file, s + 1)
        elif next[1] == 'IF':
            lastImportant.pop()
            IF(file, s + 1)
        elif next[1] == 'BREAK':
            lastImportant.pop()
            BREAK(file, s + 1)
        elif next[1] == '$':
            return 0
        else:
            error(file, s)
    elif next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'INT':
        INT(file, s + 1)
    elif next[1] == 'FLOAT':
        FLOAT(file, s + 1)
    elif next[1] == 'CHAR':
        CHAR(file, s + 1)
    elif next[1] == 'PRINT':
        PRINTF(file, s + 1)
    elif next[1] == 'WHILE':
        WHILE(file, s + 1)
    elif next[1] == 'IF':
        IF(file, s + 1)
    elif next[1] == 'BREAK':
        BREAK(file, s + 1)
    elif next[1] == '$':
        return 0
    else:
        error(file, s)


def COMMA(file, s):
    global lastImportant
    tokenType = file[s-3].split('~')
    next = file[s].split('~')
    if next[1] == 'ID':
        line = next[3].split('\n')[0]
        declarations.append(f'{next[0]}~{next[2]}~{line}')
        decID.append(next[0])
        types.append(f'{tokenType[1]}~{next[0]}')               # Guarda o tipo de cada ID
        ID(file, s + 1)
    else:
        error(file, s)

######################################### ARITHMETIC OPERATORS #########################################################
def ADD(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)
def SUB(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)
def MULT(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)
def DIV(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)
########################################################################################################################

########################################### LOGICAL OPERATORS ##########################################################
def EE(file, s):
    next = file[s].split('~')
    if next[1] == 'TRUE':
        TRUE(file, s + 1)
    elif next[1] == 'FALSE':
        FALSE(file, s + 1)
    elif next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def DIF(file, s):
    next = file[s].split('~')
    if next[1] == 'TRUE':
        TRUE(file, s + 1)
    elif next[1] == 'FALSE':
        FALSE(file, s + 1)
    elif next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def EQUAL(file, s):
    lastToken = file[s-2].split('~')
    next = file[s].split('~')

    i = 1                               # Guarda os valores de cada ID
    nextValue = file[s+i].split('~')
    i += 1
    value = ''
    if nextValue[1] != 'SEMICOLON':
        value += next[0]
        value += nextValue[0]
    else:
        value += next[0]
    while(nextValue[1] != 'SEMICOLON'):
        nextValue = file[s+i].split('~')
        if nextValue[1] != 'SEMICOLON':
            value += nextValue[0]
        i += 1
    values.append(f'{lastToken[0]}~{value}')

    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'CHAR - VALUE':
        CHAR_VALUE(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def GE(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def GT(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def LE(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def LT(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    else:
        error(file, s)

def OR(file, s):
    next = file[s].split('~')
    if next[1] == 'ID':
        ID(file, s + 1)
    elif next[1] == 'NUM - INT':
        NUM_INT(file, s + 1)
    elif next[1] == 'NUM - FLOAT':
        NUM_FLOAT(file, s + 1)
    elif next[1] == 'TRUE':
        TRUE(file, s + 1)
    elif next[1] == 'FALSE':
        FALSE(file, s + 1)
    else:
        error(file, s)
########################################################################################################################

############################################# ERROR ####################################################################
def error(file, s):
    lastToken = file[s-1].split('~')
    if lastToken[1] == '$':
        token = file[s-1].split('~')
    else:
        token = file[s].split('~')
    line = token[3].split('\n')[0]
    print(f'Syntactic error in line: {line} column: {token[2]}')
    print(f"Error starts in: {token[0]}")
    os._exit(1)

def errorS(file, s):
    lastToken = file[s-1].split('~')
    if lastToken[1] == '$':
        token = file[s-1].split('~')
    else:
        token = file[s].split('~')
    line = token[3].split('\n')[0]
    print(f'Semantic error in line: {line} column: {token[2]}')
    print(f"Error starts in: {token[0]}")
    os._exit(1)
########################################################################################################################