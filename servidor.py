# Biblioteca utilizada para implementar o cliente/servidor
import socket
# Biblioteca utilizada para lidar com os clientes conectados em paralelo
import threading

# Utilizado para mudar a cor das mensagens trocadas no terminal
from colorama import Fore

# Constantes utilizadas
PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
ENDERECO = (SERVIDOR, PORTA)
HEADER = 64
FORMATO = 'utf-8'
DESCONECTAR = '!sair'
BEMVINDO = ' Bem vindo ao nosso servidor :)'
# ---------------------------------------------------- #

servidor = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

servidor.bind(ENDERECO)

def receptor_cliente(conexao, endereco):
    """
    Lida com os clientes que entrarem no servidor.

    Parametros
    ----------
        :conexao: 
        :endereco: 
    """
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' Nova conexão, {endereco} se conectou.')

    tamanho_nome_usuario = conexao.recv(HEADER).decode(FORMATO)
    tamanho_nome_usuario = len(tamanho_nome_usuario)

    nome_usuario = conexao.recv(tamanho_nome_usuario).decode(FORMATO)

    conectado = True
    conexao.send((Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f" Olá {nome_usuario}!" + BEMVINDO).encode(FORMATO))

    while conectado:
        tamanho_mensagem = conexao.recv(HEADER).decode(FORMATO)

        try:
            tamanho_mensagem = int(tamanho_mensagem)
        except ValueError:
            continue

        mensagem = conexao.recv(tamanho_mensagem).decode(FORMATO)
        conexao.send((f'[{nome_usuario}]:' + mensagem).encode(FORMATO))

        print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE + f' {mensagem}')

        if mensagem == DESCONECTAR:
            conectado = False
            print(Fore.CYAN + f'\t[{nome_usuario}]:'+ Fore.WHITE +' Desconectando...')

    conexao.close()
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' {nome_usuario} desconectou-se.')

def iniciar():
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + ' Iniciando...')
    servidor.listen()

    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' Rodando no endereço {SERVIDOR}:{PORTA}')

    while True:
        conexao, endereco = servidor.accept()
        thread = threading.Thread(
            target=receptor_cliente,
            args=(conexao, endereco)
        )
        thread.start()

        print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' {threading.active_count() - 1} conexões ativas.')

iniciar()