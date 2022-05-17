#Apenas testando
def myParser():
    file = open('lexOutput.txt','r')
    while True:
        token = file.readline()
        if not token:
            quit()
        token = token.split('~')
        reservedWord(token, file)

def reservedWord(token, file):
    if token[1] == 'RESERVED WORD':
        token = file.readline()
        if token[1] == 'RESERVED WORD':
            reservedWord(token, file)
        identifier(token, file)

def identifier(token, file):
    if token[1] == 'IDENTIFIER':
        print('identifier')