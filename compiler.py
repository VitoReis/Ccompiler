from lexicalAnalyzer import *
from myParser import *
from mySemantic import *
import os

list = os.listdir()
for file in list:
    if file == 'lexOutput.txt' or file == 'lexUserOutput.txt' or file == 'exit.txt':
        os.remove(file)

errors = lexical()
if errors == 0:
    errors = myParser()
if errors == 0:
    errors = semantic()
if errors == 0:
    print('Codigo compilado com sucesso')
else:
    print('Seu codigo não pode ser compilado')