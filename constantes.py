import socket

from colorama import Fore
from colorama import Style

# Constantes que dizem respeito a conexao cliente-servidor
PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
ENDERECO = (SERVIDOR, PORTA)

# Constantes que dizem respeito as mensagens trocadas
HEADER = 1024
FORMATO = 'utf-8'

# Constantes que armazenam mensgaens que realizam operacoes
SAIR = '!sair'
GERAL = '!geral'
PRIVADO = '!privado'
ESCOLHA = '!esc='
RESPOSTA = '!resp='
PUXAR = '!puxar'
MOVIDO = '!movido'
DESCONECTAR = '!sair'

# Constantes que armazenam mensagens gerais do servidor
BEMVINDO = ' Bem vindo ao chat' + Style.BRIGHT + ' geral ' + Style.NORMAL + 'do servidor!'
MENU1 = '\n\t- Digite !geral para voltar para o chat geral.\n'
MENU2 = '\n\t- Digite !privado para escolher um chat privado.\n'
MENU3 = f'\t- Digite {ESCOLHA}<numero>, em que numero corresponde a um usuário da lista.\n'

MSG_SERVIDOR = Fore.GREEN + '[SERVIDOR]: ' + Fore.WHITE
