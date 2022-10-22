# Biblioteca utilizada para implementar o cliente/servidor
import socket
# Biblioteca utilizada para lidar com os clientes conectados em paralelo
import threading

# Utilizado para mudar a cor das mensagens trocadas no terminal
from colorama import Fore
from colorama import Style
from constantes import *

servidor = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

clientes_geral = []

servidor.bind(ENDERECO)

def receptor_cliente(conexao, endereco):
    """
    Lida com os clientes que entrarem no servidor.

    Parametros
    ----------
        :conexao: instancia de um socket capaz de enviar e receber dados na conexao
        :endereco: endereco ligado ao socket no outro fim da conexao
    """
    print(MSG_SERVIDOR + f' Nova conexão, {endereco} se conectou.')

    tamanho_nome_usuario = conexao.recv(HEADER).decode(FORMATO)
    tamanho_nome_usuario = len(tamanho_nome_usuario)

    nome_usuario = conexao.recv(tamanho_nome_usuario).decode(FORMATO)

    conectado = True
    conexao_privada = False

    conexao.send((MSG_SERVIDOR + f" Olá {nome_usuario}!" + BEMVINDO).encode(FORMATO))
    conexao.send((Fore.YELLOW + MENU2 + Fore.WHITE).encode(FORMATO))

    clientes_geral.append((conexao, endereco, nome_usuario))

    while conectado:
        tamanho_mensagem = conexao.recv(HEADER).decode(FORMATO)

        try:
            tamanho_mensagem = int(tamanho_mensagem)
        except ValueError:
            continue

        mensagem = conexao.recv(tamanho_mensagem).decode(FORMATO)

        if not conexao_privada:
            for cliente in clientes_geral:
                cliente[0].send((Fore.CYAN + f'[{nome_usuario}]: ' + Fore.WHITE + mensagem).encode(FORMATO))
        else:
            conexao.send((Fore.CYAN + f'[{nome_usuario}]: ' + Fore.WHITE + mensagem).encode(FORMATO))

        print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE + f' {mensagem}')

        if mensagem == DESCONECTAR:
            conectado = False
            print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE +' Desconectando...')

        if mensagem == PRIVADO and not conexao_privada:
            conexao_privada = True
            clientes_geral.remove((conexao, endereco, nome_usuario))

            conexao.send(('!disp=' + str(len(clientes_geral))).encode(FORMATO))
            conexao.send(('\n' + MSG_SERVIDOR + ' Voce entrou no chat' + Style.BRIGHT + ' privado' + Style.NORMAL + ', usuarios conectados:\n').encode(FORMATO))

            for cliente in clientes_geral:
                conexao.send((Fore.GREEN + '\n\t1.' + Fore.WHITE + f' {cliente[2]}').encode(FORMATO))

            conexao.send(('\n\n' + Fore.YELLOW + MENU3 + Fore.WHITE).encode(FORMATO))
            conexao.send((Fore.YELLOW + MENU1 + Fore.WHITE).encode(FORMATO))

    conexao.close()
    print(MSG_SERVIDOR + f' {nome_usuario} desconectou-se.')

def iniciar():
    """
    Inicia um servidor para escutar no endereco definido no socket
    """
    print(MSG_SERVIDOR + ' Iniciando...')
    servidor.listen()

    print(MSG_SERVIDOR + f' Rodando no endereço {SERVIDOR}:{PORTA}')

    while True:
        conexao, endereco = servidor.accept()
        
        # Cada conexao de clientes no servidor sera tratada concorrentemente com uma thread
        thread = threading.Thread(
            target=receptor_cliente,
            args=(conexao, endereco)
        )
        thread.start()

        # Imprime o numero de conexoes ativas, subtraindo 1 para desconsiderar a thread principal
        print(MSG_SERVIDOR + f' {threading.active_count() - 1} conexões ativas.')

iniciar()
