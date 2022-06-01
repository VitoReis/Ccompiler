# Ccompiler

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Este é um compilador desenvolvido em python para leitura de códigos simples escritos para a linguagem C.
___
## Compiler:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O arquivo [compiler](https://github.com/VitoReis/Ccompiler/blob/main/compiler.py) é utilizado apenas para importação e chamada de outros arquivos do compilador, sua função é facilitar o entendimento e a ordem de execução de cada parte do compilador, começando pelo [lexicalAnalyzer](https://github.com/VitoReis/Ccompiler/blob/main/lexicalAnalyzer.py), seguido do [parser]() (Em desenvolvimento) e por fim o [semanticAnalyzer]() (Ainda em desenvolvimento).
___

## Lexical Analyzer:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O analisador léxico está dividido em 7 funções, cada uma delas sera explicada de forma detalhada nós tópicos a seguir.

#### &nbsp;&nbsp;&nbsp;Analyse:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa é a principal função do analisador léxico, ela é responsável por fazer os caracteres do *arquivo.c* serem lidos em ordem, dependendo do caracter lido é verificado o que este caracter pode ser e uma função apropriada é chamada para lidar com ele.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa função também é responsável por armazenar algumas variáveis especificas, listas para verificação, e por fim, tratamento de erros quando as funções chamadas não retornam um valor verdadeiro sobre o token criado.

#### &nbsp;&nbsp;&nbsp;Reserved or Id:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa função é chamada quando um caracter do tipo char é lido na função *analyse*, este caracter pode ser o início de um identificador ou de uma palavra reservada, para fazer a verificação disso é necessário a criação de um buffer que ira armazenar todos os próximos caracteres lidos até que a palavra seja formada.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Após a palavra ser lida por completo verificamos se ela está ou não na tupla de palavras reservadas, se estiver iremos passar o valor da tupla para a função *createToken*, caso ela não esteja na lista verificamos se ela se encaixa como um identificador, se sim, um *token* é gerado, caso contrário nós temos um erro.

#### &nbsp;&nbsp;&nbsp;Character Set:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ao ler aspas duplas**"** , essa função adiciona os caracteres lidos em um buffer e só para quando encontrar outro caracter do mesmo tipo, ao encontra-lo o buffer é verificado, se seu conteúdo for igual ao da tupla então ele serve para impressão de variáveis, logo, seu token será '**CHARACTER SET - VARIABLE**', caso o conteúdo não seja para impressão, o token gerado é '**CHARACTER SET - STRING**'.

#### &nbsp;&nbsp;&nbsp;Number:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sabendo-se que números não são usados para iniciar palavras reservadas ou identificadores, quando um números são lidos resta apenas verificar se estes são do tipo inteiro ou flutuante.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A função *Number* se encarrega de realizar está verificação adicionando os números em um buffer, caso o numero não possua frações ele é classificado como **INTEGER**, caso possua então ele é classificado como **FLOAT**.

#### &nbsp;&nbsp;&nbsp;Operator:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Os operadores lógicos e aritméticos, por sua vez, possuem de 1 a 2 caracteres, e por serem muitos não é possível criar uma expressão regular para identifica-los, deste modo o melhor a se fazer é separa-los em uma pequena lista com apenas os operadores de 1 caracter para serem verificados na função principal, já dentro da função *operator* colocamos todos os possiveis operadores em tuplas, assim sua verificação pode ser feita de modo mais otimizado.

#### &nbsp;&nbsp;&nbsp;Literals:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Assim como os operadores os literais não podem ser classificados em expressões regulares, felizmente eles possuem apenas um caracter, logo se torna menos trabalhoso verificar um por um na função *Literals*.

#### &nbsp;&nbsp;&nbsp;Create Token:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Esta simples função é a responsável pela criação de todos os tokens, ela recebe uma string como token e a escreve em um arquivo de saída.

Para criação do *Parser* é aconselhável a criação de uma tabela de IDs para cada token ao inves de gerar string, assim o *Parser* pode identificar cada token de modo mais rápido e eficiente do que pela leitura de strings.
### &nbsp;OBS:
#### &nbsp;&nbsp;&nbsp;Verificação de erros:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A principal função do analisador léxico é verificar se existem erros na escrita do código, como por exemplo, o uso de números no início de identificadores.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ao identificar um erro temos que para evitar que o analisador pare de funcionar, então a linha que possui erros é pulada, é escrito **------MISSING TOKEN------** no arquivo de saída, e por fim, o terminal imprime as posições do erro, o caracter onde o erro se inicia e o total de erros que foram encontrados durante a análise.

___
## Parser
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O Parser foi dividido em apenas duas funções, uma responsavel por fazer a leitura da saida do analisador lexico e outra pro verificar se a ordem dos token esta correta

#### &nbsp;&nbsp;&nbsp;MyParser:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Esta função fica encarregada de fazer as leituras do arquivo **lexOutput**, sendo este o segundo arquivo gerado pelo lexicalAnalyzer para facilitar a leitura do compilador, MyParser lê os tokens linha por linha e os envia para a função verify que por sua vez retorna um True caso encontre um erro e não retorna nada caso esteja tudo certo, em caso de erro a função myParser procura a quebra de linha ou inicio de bloco mais proximo para continuar a leitura sem maiores problemas.

#### &nbsp;&nbsp;&nbsp;Verify:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Esta função recebe como parametros o token, com seu conteudo, linha e coluna, o arquivo e um index para leitura da proxima linha do arquivo, ela então verifica o Token atual e verifica se o proximo Token depois deste esta correto, caso ele esteja nada acontece, caso não esteja retorna um valor verdadeiro para **error** na função MyParser.
___
## Semantic Analyzer
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Em desenvolvimento**_

___
### OBS:
* O analisador possui limitações, ele reconhece apenas códigos simples da linguagem C e não possui totas as palavras reservadas e operadores da linguagem original.
