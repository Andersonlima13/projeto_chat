import threading
import socket

clients = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
        print("Servidor iniciado")
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    end = "/sair"
    while True:
        try:
            msg = client.recv(2048)
            accept_msg = msg.decode('utf-8')
            if end in accept_msg:             # servidor faz a Confirmação de desconexão do cliente
                return print("Cliente foi desconectado")
            broadcast(msg, client)
            print(accept_msg)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()