# Biblioteca utilizada para implementar o cliente/servidor
import socket
# Biblioteca utilizada para lidar com os clientes conectados em paralelo
import threading

# Utilizado para mudar a cor das mensagens trocadas no terminal
from colorama import Fore
from constantes import *

servidor = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

clientes_conectados = []

servidor.bind(ENDERECO)

def receptor_cliente(conexao, endereco):
    """
    Lida com os clientes que entrarem no servidor.

    Parametros
    ----------
        :conexao: instancia de um socket capaz de enviar e receber dados na conexao
        :endereco: endereco ligado ao socket no outro fim da conexao
    """
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' Nova conexão, {endereco} se conectou.')

    tamanho_nome_usuario = conexao.recv(HEADER).decode(FORMATO)
    tamanho_nome_usuario = len(tamanho_nome_usuario)

    nome_usuario = conexao.recv(tamanho_nome_usuario).decode(FORMATO)

    conectado = True

    conexao.send((Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f" Olá {nome_usuario}!" + BEMVINDO).encode(FORMATO))
    conexao.send((Fore.YELLOW + MENU2 + Fore.WHITE).encode(FORMATO))

    clientes_conectados.append((conexao, endereco))

    while conectado:
        tamanho_mensagem = conexao.recv(HEADER).decode(FORMATO)

        try:
            tamanho_mensagem = int(tamanho_mensagem)
        except ValueError:
            continue

        mensagem = conexao.recv(tamanho_mensagem).decode(FORMATO)

        for cliente in clientes_conectados:
            cliente[0].send((Fore.CYAN + f'[{nome_usuario}]: ' + Fore.WHITE + mensagem).encode(FORMATO))

        print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE + f' {mensagem}')

        if mensagem == DESCONECTAR:
            conectado = False
            print(Fore.CYAN + f'\t[{nome_usuario}]:'+ Fore.WHITE +' Desconectando...')

    conexao.close()
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' {nome_usuario} desconectou-se.')

def iniciar():
    """
    Inicia um servidor para escutar no endereco definido no socket
    """
    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + ' Iniciando...')
    servidor.listen()

    print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' Rodando no endereço {SERVIDOR}:{PORTA}')

    while True:
        conexao, endereco = servidor.accept()
        
        # Cada conexao de clientes no servidor sera tratada concorrentemente com uma thread
        thread = threading.Thread(
            target=receptor_cliente,
            args=(conexao, endereco)
        )
        thread.start()

        # Imprime o numero de conexoes ativas, subtraindo 1 para desconsiderar a thread principal
        print(Fore.GREEN + '[SERVIDOR]:' + Fore.WHITE + f' {threading.active_count() - 1} conexões ativas.')

iniciar()
