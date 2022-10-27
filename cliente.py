# Biblioteca utilizada para implementar o cliente/servidor
import socket
import threading
import os

from colorama import Fore
from constantes import *

# Define um cliente como um socket, a familia AF_INET indica que a familia de
# endereco utilizada sera do formato (host, porta), compativel apenas com o IPv4
# O tipo de socket utilizado sera o SOCK_STREAM, que e um tipo para propositos gerais
cliente = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

mensagens = []
disp = False
connect = False

def receber_mensagem():
    """
    Funcao que roda concorrentemente esperando receber uma mensagem do servidor,
    e caso isso aconteca, insere essa mensagem na lista de mensagens e chama
    a funcao de impressao das mensagens na tela do usuario.
    """
    global mensagens
    global disp
    global connect

    while True:
        mensagem = cliente.recv(HEADER).decode(FORMATO)

        if mensagem:
            # Se receber essa mensagem, significa que uma conexao no chat privado foi estabelecida
            if PUXAR in mensagem:
                mover = mensagem.replace(PUXAR, '')
                mover = MOVIDO + mover
                enviar_mensagem(mover)

            mensagens.append(mensagem)
            imprime_mensagens()

def imprime_mensagens():
    """
    Funcao que limpa a tela e imprime todas as mensagens armazenadas no buffer
    de mensagens recebidas do servidor.
    """
    os.system('clear')

    for mensagem in mensagens:
        print(mensagem)
    print("\nDigite uma mensagem: ")

def conectar():
    """
    Funcao que faz a conexao do cliente com o servidor
    """
    nome_usuario = str(input(Fore.CYAN + '[CLIENTE]:' + Fore.WHITE + ' Informe o seu nome de usuário: '))

    cliente.connect(ENDERECO)

    nome_usuario = nome_usuario.encode(FORMATO)

    tamanho_nome_enviado = str(len(nome_usuario)).encode(FORMATO)
    tamanho_nome_enviado += b' ' * (HEADER - len(tamanho_nome_enviado))

    cliente.send(tamanho_nome_enviado)
    cliente.send(nome_usuario)

    mensagens.append(cliente.recv(HEADER).decode(FORMATO))
    mensagens.append(cliente.recv(HEADER).decode(FORMATO))

    imprime_mensagens()

    conectado()

def enviar_mensagem(conteudo):
    """
    Envia uma mensagem para o servidor.

    Parametros
    ----------
        `conteudo`: string contendo a mensagem a ser enviada para o servidor
    """
    mensagem = conteudo.encode(FORMATO)
    cliente.send(mensagem)

def conectado():
    """
    Funcao que lida com acoes do cliente enquanto estiver conectado ao servidor.
    """
    global mensagens
    global disp
    global connect

    sair = False

    thread = threading.Thread(
        target=receber_mensagem
    )

    thread.start()

    while not sair:
        mensagem = str(input(''))

        if mensagem == SAIR:
            print('Saindo...')
            sair = True
        else:
            enviar_mensagem(mensagem)

    enviar_mensagem(DESCONECTAR)
    return

conectar()
