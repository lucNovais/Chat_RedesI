# Trabalho Prático - Redes de Computadores I

## Chat com Sockets em Python

Neste trabalho, foi desenvolvido um chat multiusuário a partir de sockets, implementado na linguagem Python.
Este repositório contém os módulos desenvolvidos e necessários para realizar a conexão.

## Integrantes

- Daniel Henrique Batista de Magalhães (18.1.8042)
- Lucas Novais da Silva (18.1.8046)
- Luiz Henrique Marcos Ferreira (18.1.8020)

## Requisitos

- [Python==3.10](https://www.python.org/downloads/)
- [colorama==0.4.4](https://pypi.org/project/colorama/)

## Como funciona?

O projeto consiste de dois módulos principais: `servidor.py` e `cliente.py`. Além disso, 
algumas constantes úteis foram definidas no módulo `constantes.py`.

Para executar o projeto, não necessariamente é preciso que cliente e servidor estejam em uma mesma pasta,
no entanto, é necessário que o arquivo de constantes esteja na mesma pasta que ambos. 
Para iniciar o servidor, utiliza-se o comando:

```bash
python3 servidor.py
```

**Obs:** no Windows, pode ser preciso trocar a expressão `python3` por `python`.

Com o servidor escutando no endereço localhost:PORTA de sua máquina local, basta executar o comando abaixo
em um outro terminal para executar o cliente:

```bash
python3 cliente.py
```

Este procedimento pode ser feito em vários terminais para conectar diversos clientes ao
servidor.

## Funcionalidades disponíveis:

Aqui apresentamos algumas funcionalidades implementadas no chat.

### Chat geral:

- No início, todo usuário é conectado a um chat geral, em que pode interagir com todos os outros
usuários presentes nesse chat. Nenhum comando específico é necessário para realizar essa
conexão, ao rodar o módulo `cliente.py` o cliente já é automaticamente incluído nesse chat.

### Chat privado:

- Caso um usuário queira, é possível escolher um cliente da lista de clientes conectados
 no chat geral para começar uma conversa em privado (ou seja, as mensagens trocadas
 entre eles serão direcionadas apenas para seus respectivos endereços).

    - Para fazer isso, é necessário enviar a mensagem de controle `!privado`, e logo após
    seguir as instruções que o servidor passar.
    
**Obs:** É importante que algumas respostas para o servidor sejam feitas utilizando um conjunto as palavras de controle solicitadas, como `!esc=` e `!resp=`. 
