from myParser import types, declarations, values, ids, prints

def semantic():
    error = 0
    idTypes = []        # Separa os ids e seus tipos
    idValues = []       # Separa os ids e seus valores
    separatedID = []    # Separa os ids de suas linhas e colunas


    for id in ids:                              # Separa os ids de suas linhas e colunas
        separatedID.append(id.split('~'))

    for id in separatedID:                      # Verifica se as variaveis foram declaradas
        if not id[0] in declarations:
            line = id[2].split('\n')[0]
            print(f'Semantic error in line: {line} column: {id[1]}')
            print(f'"{id[0]}" was not declared')
            error += 1

    for type in types:                      # Separa os ids e seus tipos
        idTypes.append(type.split('~'))
    for value in values:                    # Separa os ids e seus valores
        idValues.append(value.split('~'))

    for id in idTypes:                       # Separa os ids e seus valores
        for item in value:
            continue

    print(f'Semantic finished with {error} errors')
    return error