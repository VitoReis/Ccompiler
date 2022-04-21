# Ccompiler

Este é um compilador desenvolvido em python para leitura de códigos simples
escritos para a linguagem C.
___
##Compliler:
O arquivo [compiler]() é utilizado apenas para importação e chamada de outros 
arquivos do compilador, sua função é facilitar o entendimento e a ordem de 
execução de cada parte do compilador, começando pelo [lexicalAnalyzer](),
seguido do [parser]() (Em desenvolvimento) e por fim o
[semanticAnalyzer]() (Ainda em desenvolvimento).
___

##Lexical Analyzer:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O analisador léxico está dividido em 7 funções,
cada uma delas sera explicada de forma detalhada nós tópicos a seguir.

####&nbsp;&nbsp;&nbsp;Analyse:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa é a principal função do analisador léxico,
ela é responsável por fazer os caracteres do *arquivo.c* serem lidos em ordem, 
dependendo do caracter lido é verificado o que este caracter pode ser e uma função
apropriada é chamada para lidar com ele.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa função também é responsável por armazenar
algumas variaveis especificas, listas para verificação, e por fim, tratamento de erros 
quando as funções chamadas não retornam um valor verdadeiro sobre o token criado.

####&nbsp;&nbsp;&nbsp;Reserved or Id:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Essa função é chamada quando um caracter do tipo
char é lido na função *analyse*, este caracter pode ser o inicio de um identificador 
ou de uma palavra reservada, para fazer a verificação disso é necessario a criação de
um buffer que ira armazenar todos os próximos caracteres lidos até que a palavra seja
formada.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Após a palavra ser lida por completo verificamos 
se ela está ou não na lista de palavras reservadas, se estiver iremos achar qual das
palavras da lista ela é e geramos um *token*, caso ela não esteja na lista verificamos
se ela se encaixa como um identificador, se sim, um *token* é gerado, caso contrário
nós temos um erro.
####&nbsp;&nbsp;&nbsp;Character Set:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

####&nbsp;&nbsp;&nbsp;Number:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

####&nbsp;&nbsp;&nbsp;Operator:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

####&nbsp;&nbsp;&nbsp;Literals:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
####&nbsp;&nbsp;&nbsp;Create Token:

###&nbsp;OBS:
####&nbsp;&nbsp;&nbsp;Verificação de erros:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

___
##Parser
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Em desenvolvimento**_

___
##Lexical Analyzer
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Em desenvolvimento**_

___
###OBS:
* Ao escrever um código em C para teste é obrigatório soltar um espaço a direita
dos números quando estes forem seguidos de um caracter que não seja ',' ou ';'.
* O analisador possui limitações, ele reconhece apenas códigos simples da linguagem C
