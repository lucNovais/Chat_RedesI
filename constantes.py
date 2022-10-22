import socket

from colorama import Fore
from colorama import Style

PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
ENDERECO = (SERVIDOR, PORTA)

HEADER = 1024
FORMATO = 'utf-8'

DESCONECTAR = '!sair'
BEMVINDO = ' Bem vindo ao chat' + Style.BRIGHT + ' geral ' + Style.NORMAL + 'do servidor!'
MENU1 = '\n\t- Digite !geral para voltar para o chat geral.\n'
MENU2 = '\n\t- Digite !privado para escolher um chat privado.'
MENU3 = '\t- Digite um número correspondente a um usuário.\n'
GERAL = '!geral'
PRIVADO = '!privado'

MSG_SERVIDOR = Fore.GREEN + '[SERVIDOR]: ' + Fore.WHITE
