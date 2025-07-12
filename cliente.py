import threading
import socket
import re







# array que guarda os comandos que podem ser usados pelo usuario
commands_message = ['/sair','listar_usuarios','/print']


# funções que podem ser usadas pelo cliente

def validate_username(username):
    pattern = r'^[A-Za-z]\w{4,14}$'
    if re.match(pattern, username):
        return True
    else:
        return False    

def set_username():
    try:       
        user_name = input(f"\nDigite seu nome de usuário: ")
        if not validate_username(user_name):
            raise ValueError("Nome de usuário inválido. Deve começar com uma letra, ter entre 5 e 15 caracteres e conter apenas letras, números e sublinhados.")
        print(f"\nBem-vindo ao chat, {user_name}!\n")
        return user_name
    except Exception as e:
        print(f"\nErro ao definir o nome de usuário: {e}\n")
        return set_username()





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





# funçao que verifica qual comando foi usado pelo usuario  
def message(client, msg):
    if msg == '/sair':
        client.send(msg.encode('utf-8'))
        client.close()
        print("Você saiu do chat.")
        exit()
    elif msg == '/listar_usuarios':
        client.send(msg.encode('utf-8'))
    elif msg == '/help':
        client.send(msg.encode('utf-8'))
   
     
      
def sendMessages(client, username):
    while True:
        try:
            msg = input(f'{username}: ').strip()
            if msg in commands_message:
                message(client, msg)  # Executa a função para lidar com o comando
            else:
                client.send(f'<{username}> {msg}'.encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando cliente...")
            client.close()
            break
        except Exception as e:
            print(f"[Erro]: {e}")
            client.close()
            break
 
        
        
        
        
        
        
def main():
    # Criação do socket do cliente
    username = set_username()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexão do cliente ao servidor na porta 7777
        client.connect(('localhost', 7778))
    except:
        # Trata a exceção se a conexão não for bem-sucedida
        return print('\nNão foi possível se conectar ao servidor!\n')

    # Solicitação do nome de usuário ao cliente
    print('\nDigite /sair para desconectar')
    print('Digite /listar_usuarios para obter a lista de usuários online')





    thread1 = threading.Thread(target=receiveMessages, args=[client]) # Thread para escutar mensagens 
    thread2 = threading.Thread(target=sendMessages, args=[client, username]) # Thread para enviar mensagens
    thread1.start()
    thread2.start()
main()
