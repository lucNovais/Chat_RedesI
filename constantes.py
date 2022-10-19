import socket

PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
ENDERECO = (SERVIDOR, PORTA)
HEADER = 128
FORMATO = 'utf-8'
DESCONECTAR = '!sair'
BEMVINDO = ' Bem vindo ao chat geral do servidor!'
MENU1 = '\n\tDigite !geral para voltar para o chat geral.'
MENU2 = '\n\tDigite !privado para escolher um chat privado.'
GERAL = '!geral'
PRIVADO = '!privado'
