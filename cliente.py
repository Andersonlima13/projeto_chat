import threading
import socket

def main():
    # Criação do socket do cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexão do cliente ao servidor na porta 7777
        client.connect(('localhost', 7777))
    except:
        # Trata a exceção se a conexão não for bem-sucedida
        return print('\nNão foi possível se conectar ao servidor!\n')

    # Solicitação do nome de usuário ao cliente
    username = input('Digite o Nome Do Usuário> ')
    print('\nConectado')
    print('\nDigite /sair para desconectar')
    print('Digite /listar_usuarios para obter a lista de usuários online')

    # Inicia duas threads: uma para receber mensagens e outra para enviar mensagens
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    # Função para receber mensagens do servidor
    while True:
        try:
            # Recebe e decodifica a mensagem do servidor
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            # Trata a exceção se não for possível permanecer conectado
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break

def sendMessages(client, username):
    # Função para enviar mensagens para o servidor
    while True:
        try:
            # Solicitação da mensagem do usuário
            msg = input('\n')
            if msg == "/sair":
                # Envia mensagem de desconexão ao servidor
                client.send(f'<{username}> {msg}'.encode('utf-8'))
                client.close()
                return print("Você saiu do chat")
            elif msg == "/listar_usuarios":
                # Envia solicitação de listar usuários online ao servidor
                client.send(msg.encode('utf-8'))
            else:
                # Envia a mensagem normalmente ao servidor
                client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            # Trata a exceção se ocorrer um erro durante o envio da mensagem
            return

main()
