from myParser import types, declarations, values, ids, idPos, prints, decID

decOrder = []  # Separa os ids declarados e suas posições
idOrder = []  # Separa os ids chamados e suas posições
valueOrder = []  # Separa os ids declarados e seus valores
printOrder = []  # Separa os prints declarados e seus valores e sua posição
typeOrder = []  # Separa os ids declarados e seus tipos

def semantic():
    global decOrder, idOrder, valueOrder, printOrder, typeOrder
    error = 0
    i = 0
    for item in declarations:                   # Separa os ids e suas posições de declarações dentro de uma lista
        separated = declarations[i].split('~')
        decOrder.append(separated)
        i += 1

    i = 0
    for item in idPos:                          # Separa os ids e as posições em que são chamados a primeira vez
        separated = idPos[i].split('~')
        idOrder.append(separated)
        i += 1

    for id in ids:                              # Verifica os ids chamados foram declarados
        if not id in decID:
            print(f'Syntactic error: variable "{id}" was not declared')
            error += 1

    for dec in decOrder:                        # Verifica se a ordem de declaração e chamada de variaveis esta certa
        for id in idOrder:
            if id[0] == dec[0]:
                if id[2] < dec[2]:
                    print(f'Syntactic error in line: {id[2]} column: {id[1]}')
                    print(f"Error starts in: {id[0]}")
                    error += 1

    i = 0
    for value in values:                    # Separa os ids declarados e seus valores
        separated = values[i].split('~')
        valueOrder.append(separated)
        i += 1
    print(valueOrder)

    i = 0
    for prt in prints:                    # Separa os prints declarados e seus valores e sua posição
        separated = prints[i].split('~')
        printOrder.append(separated)
        i += 1

    i = 0
    for id in types:                    # Separa os ids declarados e seus tipos
        separated = types[i].split('~')
        typeOrder.append(separated)
        i += 1
    print(typeOrder)

    for typ in typeOrder:           # Salva o id com sua posição e tipo
        for item in idOrder:
            if item[0] == typ[1]:
                item.append(typ[0])
    print(idOrder)
    print(f'Semantic finished with {error} errors')
    return error