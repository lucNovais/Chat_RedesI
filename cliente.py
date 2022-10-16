# Biblioteca utilizada para implementar o cliente/servidor
import socket

from colorama import Fore

HEADER = 64
FORMATO = 'utf-8'
PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
DESCONECTAR = '!sair'
ENDERECO = (SERVIDOR, PORTA)

cliente = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

def conectar():
    nome_usuario = str(input(Fore.CYAN + '[CLIENTE]:' + Fore.WHITE + ' Informe o seu nome de usuário: '))

    cliente.connect(ENDERECO)

    nome_usuario = nome_usuario.encode(FORMATO)

    tamanho_nome_enviado = str(len(nome_usuario)).encode(FORMATO)
    tamanho_nome_enviado += b' ' * (HEADER - len(tamanho_nome_enviado))

    cliente.send(tamanho_nome_enviado)
    cliente.send(nome_usuario)

    print(cliente.recv(HEADER).decode(FORMATO))
    conectado()

def enviar_mensagem(conteudo):
    mensagem = conteudo.encode(FORMATO)

    tamanho_mensagem = len(mensagem)
    tamanho_enviada = str(tamanho_mensagem).encode(FORMATO)
    tamanho_enviada += b' ' * (HEADER - len(tamanho_enviada))

    cliente.send(tamanho_enviada)
    cliente.send(mensagem)

def conectado():
    sair = False

    while not sair:
        mensagem = str(input("\nDigite uma mensagem: "))

        if mensagem == '!sair':
            print('Saindo...')
            sair = True
        else:
            enviar_mensagem(mensagem)

    enviar_mensagem(DESCONECTAR)

conectar()
