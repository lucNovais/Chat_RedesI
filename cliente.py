# Biblioteca utilizada para implementar o cliente/servidor
import socket

from colorama import Fore

HEADER = 64
FORMATO = 'utf-8'
PORTA = 2000
SERVIDOR = socket.gethostbyname(socket.gethostname())
DESCONECTAR = '!sair'
ENDERECO = (SERVIDOR, PORTA)

# Define um cliente como um socket, a familia AF_INET indica que a familia de
# endereco utilizada sera do formato (host, porta), compativel apenas com o IPv4
#
# O tipo de socket utilizado sera o SOCK_STREAM, que e um tipo para propositos gerais
cliente = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM
)

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

    print(cliente.recv(HEADER).decode(FORMATO))
    conectado()

def enviar_mensagem(conteudo):
    """
    Envia uma mensagem para o servidor.

    Parametros
    ----------
        `conteudo`: string contendo a mensagem a ser enviada para o servidor
    """
    mensagem = conteudo.encode(FORMATO)

    tamanho_mensagem = len(mensagem)
    tamanho_enviada = str(tamanho_mensagem).encode(FORMATO)
    tamanho_enviada += b' ' * (HEADER - len(tamanho_enviada))

    cliente.send(tamanho_enviada)
    cliente.send(mensagem)

def conectado():
    """
    Funcao que lida com acoes do cliente enquanto estiver conectado ao servidor
    """
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
