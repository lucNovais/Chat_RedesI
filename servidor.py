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
clientes_privado = []

servidor.bind(ENDERECO)

def receptor_cliente_geral(conexao, endereco):
    """
    Lida com os clientes que entrarem no servidor.

    Parametros
    ----------
        `conexao`: instancia de um socket capaz de enviar e receber dados na conexao
        `endereco`: endereco ligado ao socket no outro fim da conexao
    """
    print(MSG_SERVIDOR + f' Nova conexão, {endereco} se conectou.')

    tamanho_nome_usuario = conexao.recv(HEADER).decode(FORMATO)
    tamanho_nome_usuario = len(tamanho_nome_usuario)

    nome_usuario = conexao.recv(tamanho_nome_usuario).decode(FORMATO)

    conectado = True

    conexao.send((MSG_SERVIDOR + f" Olá {nome_usuario}!" + BEMVINDO).encode(FORMATO))
    conexao.send((Fore.YELLOW + MENU2 + Fore.WHITE).encode(FORMATO))

    usuario = (conexao, endereco, nome_usuario)
    clientes_geral.append(usuario)

    while conectado:
        mensagem = conexao.recv(HEADER).decode(FORMATO)

        if mensagem == DESCONECTAR:
            conectado = False

            print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE +' Desconectando...')

            for cliente in clientes_geral:
                cliente[0].send((Fore.CYAN + f'[{nome_usuario}]:' + Fore.WHITE + ' Desconectando...').encode(FORMATO))

        if mensagem == PRIVADO:
            clientes_geral.remove(usuario)
            clientes_privado.append(usuario)
            receptor_cliente_privado(usuario)

        if MOVIDO in mensagem:
            # Se chegar aqui, significa que esse cliente precisa ser movido para um chat privado
            endereco_origem = mensagem.replace(MOVIDO + ' ', '') # Captura o endereco do usuario que solicitou o chat privado
            clientes_geral.remove(usuario)

            receptor_cliente_privado(
                usuario=usuario,
                flag_movido=True,
                endereco_origem=endereco_origem
            )

        for cliente in clientes_geral:
            cliente[0].send((Fore.CYAN + f'[{nome_usuario}]: ' + Fore.WHITE + mensagem).encode(FORMATO))

        print(Fore.CYAN + f'\t[{nome_usuario}]:' + Fore.WHITE + f' {mensagem}')

    conexao.close()
    print(MSG_SERVIDOR + f' {nome_usuario} desconectou-se.')

def receptor_cliente_privado(usuario, flag_movido=False, endereco_origem=None):
    """
    Lida com os direcionamentos de mensagens quando uma conexao privada de
    cliente para cliente e solicitada.

    Parametros
    ----------
        `usuario`: tupla (conexao, endereco, nome_usuario) que representa o usuario da thread
        `flag_movido`: flag que indica se essa funcao esta lidando com o cliente que foi solicitado
                       em uma conexao privada, se nao estiver setada, significa que a funcao esta
                       lidando com o cliente que quer estabelecer uma conexao privada
        `endereco_origem`: caso essa funcao esteja rodando em uma thread de um cliente que foi solicitado
                       de partiripar em um chat privado, entao esse parametro representa o nome
                       do cliente que fez a solicitacao
    """
    if not flag_movido:
        usuario[0].send(('\n' + MSG_SERVIDOR + ' Voce entrou no chat' + Style.BRIGHT + ' privado' + Style.NORMAL + ', usuarios conectados:\n').encode(FORMATO))

        conexao_aceita = False

        if clientes_geral:
            for i, cliente in enumerate(clientes_geral):
                usuario[0].send((Fore.GREEN + f'\n\t{i + 1}.' + Fore.WHITE + f' {cliente[2]}').encode(FORMATO))
        else:
            usuario[0].send(('\n' + MSG_SERVIDOR + ' Nenhum cliente conectado! Voltando ao chat' + Style.BRIGHT + ' geral' + Style.NORMAL + '...').encode(FORMATO))
            clientes_geral.append(usuario)

        usuario[0].send(('\n\n' + Fore.YELLOW + MENU3 + Fore.WHITE).encode(FORMATO))
        usuario[0].send((Fore.YELLOW + MENU1 + Fore.WHITE).encode(FORMATO))
    else:
        # Percorre todos os usuarios conectados a um chat privado e pega aquele
        # que realizou a solicitacao de conexao para este usuario, pelo nome

        usuario_origem = [c for c in clientes_privado if f"('{c[1][0]}', {c[1][1]})" == endereco_origem]
        usuario_origem = usuario_origem[0][0]

        # Se entrar nessa condicional, significa que a conexao privada foi aceita pela parte
        # solicitada, e o direcionamento de mensagens pode ser feito entre o par
        conexao_aceita = True

    while True:
        mensagem = usuario[0].recv(HEADER).decode(FORMATO)

        usuario[0].send((Fore.MAGENTA + f'[{usuario[2]}]: ' + Fore.WHITE + mensagem).encode(FORMATO))

        if conexao_aceita and not flag_movido:
            # Se entrar aqui, significa que essa thread remete ao usuario que solicitou a conexao privada
            # logo, a mensagem recebida deve ser enviada para o cliente que se conectou
            cliente_privado[0].send((Fore.MAGENTA + f'[{usuario[2]}]: ' + Fore.WHITE + mensagem).encode(FORMATO))
        elif conexao_aceita and flag_movido:
            usuario_origem.send((Fore.MAGENTA + f'[{usuario[2]}]: ' + Fore.WHITE + mensagem).encode(FORMATO))
        elif ESCOLHA in mensagem:
            # Se o programa entrar aqui, entao uma conexao privada ainda nao foi estabelecida, e o laco esta esperando o
            # cliente que solicitou fazer uma conexao privada escolher um usuario na lista de disponiveis
            resposta = int(mensagem.replace('!esc=', ''))
            cliente_privado = clientes_geral[resposta - 1]

            cliente_privado[0].send((Fore.MAGENTA + f'\n[{usuario[2]}]: ' + Fore.WHITE + 'Olá, estou te solicitando um chat privado...\n').encode(FORMATO))
            cliente_privado[0].send(('\n' + MSG_SERVIDOR + '[!resp=S para ACEITAR / !resp=N para NEGAR]').encode(FORMATO))
            cliente_privado[0].send(('\n' + MSG_SERVIDOR + 'Aguardando resposta...').encode(FORMATO))

            while True and not conexao_aceita:
                mensagem = cliente_privado[0].recv(HEADER).decode(FORMATO)

                if RESPOSTA in mensagem:
                    resposta = mensagem.replace('!resp=', '')
                    if resposta == 'S':
                        conexao_aceita = True
                        cliente_privado[0].send((PUXAR + f' {usuario[1]}').encode(FORMATO))
                    elif resposta == 'N':
                        conexao_aceita = False
                else:
                    cliente_privado[0].send(('\n' + MSG_SERVIDOR + '[!resp=S para ACEITAR / !resp=N para NEGAR]').encode(FORMATO))
                    cliente_privado[0].send((MSG_SERVIDOR + 'Aguardando resposta...').encode(FORMATO))
        elif ESCOLHA not in mensagem and not conexao_aceita and not flag_movido:
            # Garante que o usuario ira escolher corretamente
            usuario[0].send(('\n' + MSG_SERVIDOR + 'Aguardando resposta válida...').encode(FORMATO))

def iniciar():
    """
    Inicia um servidor para escutar no endereco definido no socket
    """
    print(MSG_SERVIDOR + ' Iniciando...')
    servidor.listen()

    print(MSG_SERVIDOR + f' Escutando no endereço {SERVIDOR}:{PORTA}')

    while True:
        conexao, endereco = servidor.accept()
        
        # Cada conexao de clientes no servidor sera tratada concorrentemente com uma thread
        thread = threading.Thread(
            target=receptor_cliente_geral,
            args=(conexao, endereco)
        )
        thread.start()

        # Imprime o numero de conexoes ativas, subtraindo 1 para desconsiderar a thread principal
        print(MSG_SERVIDOR + f' {threading.active_count() - 1} conexões ativas.')

iniciar()
