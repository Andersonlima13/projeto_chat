import threading
import socket


def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
        print("rodando na porta 7777")
        print("\n Digite /Sair para sair do chat")
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = input('Digite seu Nome de Usuário> ')
    print(f'\n {username} Entrou no chat')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break


def sendMessages(client, username): 
    while True:
        try:
            msg = input('\n')
            if msg == "/fim":
                client.close()
                return print(f" Conexão encerrada, vc saiu do chat")
            client.send(f'<{username}> {msg}'.encode('utf-8'))
            
            
        except:
            return

main()