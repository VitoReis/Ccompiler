from myParser import types, declarations, values, ids, idPos, prints, decID, conditions

decOrder = []  # Separa os ids declarados e suas posições
idOrder = []  # Separa os ids chamados e suas posições
valueOrder = []  # Separa os ids declarados e seus valores
printOrder = []  # Separa os prints declarados e seus valores e sua posição
typeOrder = []  # Separa os ids declarados e seus tipos
conditOrder = []    # Separa as condições dos whiles e ifs

def semantic():
    global types, declarations, values, ids, idPos, prints, decID, conditions
    error = 0
############################################ SEPARATORS ################################################################
    for item in declarations:             # Separa os ids e suas posições de declarações dentro de uma lista
        separated = item.split('~')
        decOrder.append(separated)


    for item in idPos:                    # Separa os ids e as posições em que são chamados a primeira vez
        separated = item.split('~')
        idOrder.append(separated)

    for item in conditions:                    # Separa os ids e as posições em que são chamados a primeira vez
        separated = item.split('~')
        conditOrder.append(separated)

    for value in values:                  # Separa os ids declarados e seus valores
        separated = value.split('~')
        valueOrder.append(separated)


    for prt in prints:                    # Separa os prints declarados e seus valores e sua posição
        separated = prt.split('~')
        printOrder.append(separated)


    for id in types:                    # Separa os ids declarados e seus tipos
        separated = id.split('~')
        typeOrder.append(separated)

    for typ in typeOrder:               # Salva o id com sua posição e tipo
        for item in idOrder:
            if item[0] == typ[1]:
                item.append(typ[0])
##################################### VERIFY ###########################################################################
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
########################################################################################################################


    if error == 0:
        write(decOrder, idOrder, printOrder, valueOrder)

    print(f'Semantic finished with {error} errors')
    return error




def write(decOrder, idOrder, printOrder, valueOrder):   # O token é passado e escrito na saida de acordo com a tabela
    output = open('exit.txt','a')
    output.write('Declarations:\n')
    for itens in decOrder:
        output.write(f'Declarated ID: {itens[0]} - Line: {itens[2]} - Column: {itens[1]}\n')

    output.write('\nID Types:\n')

    for itens in idOrder:
        output.write(f'ID: {itens[0]} - Type: {itens[3]} - Line: {itens[2]} - Column: {itens[1]}\n')

    output.write('\nPrints:\n')
    for itens in printOrder:
        output.write(f'Type: {itens[0]} - Content: {itens[3]} - Line: {itens[2]} - Column: {itens[1]}\n')

    output.write('\nID Values:\n')
    for itens in valueOrder:
        output.write(f'ID: {itens[0]} - Value: {itens[3]} - Line: {itens[2]} - Column: {itens[1]}\n')

    output.write('\nConditions:\n')
    for itens in conditOrder:
        output.write(f'ID: {itens[0]} - Condition: {itens[3]} - Line: {itens[2]} - Column: {itens[1]}\n')
    output.close()