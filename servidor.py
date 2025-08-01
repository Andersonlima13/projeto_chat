import threading
import socket


# Lista para armazenar os clientes conectados
clients = []
usernames = {}

def main():
    # Criação do socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Associa o servidor à porta 7777 e inicia a escuta
        server.bind(('localhost', 7778))
        server.listen()
        print("Servidor iniciado")
        print("\n-------------COMANDOS--------")
        print("\n/remove_all : Remover todos os usuários conectados")
        print("/users : Retorna os usuários e a quantidade de clientes conectados")
    except:
        # Trata a exceção se não for possível iniciar o servidor
        return print('\nNão foi possível iniciar o servidor!\n')

    # Adicionando uma thread para leitura de mensagens do servidor
    thread_server_input = threading.Thread(target=serverInput)
    thread_server_input.start()

    while True:
        client, addr = server.accept()  # Aceita a conexão do cliente
        clients.append(client)
        username = client.recv(2048).decode('utf-8')
        usernames[client] = username

        # Inicia uma thread para tratar as mensagens do cliente
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()
        print(f"{username} Conectado ao servidor")
        broadcast(f"\n{username} Entrou No Chat\n",client)

















def messagesTreatment(client):
    username = usernames.get(client)
    # Função para tratar as mensagens recebidas do cliente
    while True:
        try:
            # Recebe e decodifica a mensagem do cliente
            msg = client.recv(2048).decode('utf-8')

            if "/sair" in msg:
                print(f"{username} Desconectado do servidor")
                client.close()
                deleteClient(client)
                broadcast(f"{username} Saiu do chat",client)
                break


            elif "/listar_usuarios" in msg:
                get_online_users(client)
            elif "/help" in msg:
                HELP = help()
                client.send(HELP.encode('utf-8'))
            else:
                # Transmite a mensagem para todos os clientes conectados
                broadcast(msg, client)
                print(msg)
        except:
            # Se ocorrer um erro, remove o cliente da lista e encerra o loop
            deleteClient(client)
            break


# faz um get de usuarios
def get_online_users(client):
    count_users = len(clients)
    online_users = ", ".join(usernames[c] for c in clients)
    response = f"Total de Usuários: {count_users}\nUsuários Online: {online_users}"
    client.send(response.encode('utf-8'))
    
        
def private(client,username):
    pass


def help():
    return (
        "\n---------------------- AJUDA ----------------------\n"
        "/help               - Lista todos os comandos\n"
        "/private <usuário>  - Envia mensagem privada\n"
        "/left               - Sair do chat\n"
        "/listar_usuarios    - Lista os usuários conectados\n"
        "---------------------------------------------------\n"
    )














def broadcast(msg, client):
    # Função para enviar mensagens para todos os clientes, exceto o remetente
    for clientItem in clients:
        if clientItem != client:
            try:
                # Envia a mensagem codificada em UTF-8
                clientItem.send(msg.encode('utf-8'))
            except:
                # Se ocorrer um erro ao enviar, remove o cliente da lista
                deleteClient(clientItem)




def deleteClient(client):
    # Função para remover um cliente da lista
      clients.remove(client)
      usernames.pop(client,None)
      client.close()





# Função para leitura de mensagens do servidor



def serverInput():
    while True:
        try:
            # Solicitação de comando do servidor a partir da entrada do console
            msg = input()
            if msg == "/remove_all":
                # Remove todos os clientes conectados
                remove_all_clients()
                print("Todos os usuários foram removidos.")
                
            elif "/listar_usuarios" in msg:
                get_online_users(client)             
            else:
                # Transmite a mensagem para todos os clientes conectados
                broadcast(f"Servidor: {msg}", None)
        except KeyboardInterrupt:
            server.close()
            client.close()
            print("Ocorreu um erro inesperado no servidor")
            # Trata a interrupção do teclado (Ctrl+C)
            break






# Escuta as mensagens trocadas pelos clientes
def listen_client():
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
    pass





def remove_all_clients():
    # Função para desconectar e remover todos os clientes da lista
    for client in clients:
        client.close()
    clients.clear()

main()
