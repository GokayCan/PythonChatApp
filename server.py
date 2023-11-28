import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

clients = {}

def handle_client_messages(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{client_address}: {message}")
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
        except Exception as e:
            print(f"Hata: {e}")
            remove_client(client_socket)
            break

def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address[0]}:{client_address[1]} bağlandı.")
        client_socket.send("Bağlandınız! Sohbet edebilirsiniz.".encode('utf-8'))
        clients[client_socket] = client_address
        client_thread = threading.Thread(target=handle_client_messages, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()

def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                # Diğer istemcilere mesajları iletmek için gönderen istemci dışındaki tüm istemcilere gönderiyoruz.
                client_socket.send(f"{str(sender_socket.getpeername())}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Hata: {e}")
                remove_client(client_socket)

def remove_client(client_socket):
    if client_socket in clients:
        print(f"{clients[client_socket][0]}:{clients[client_socket][1]} ayrıldı.")
        del clients[client_socket]
        client_socket.close()

if __name__ == "__main__":
    print("Sunucu başlatılıyor...")
    print(f"Dinlenen port: {SERVER_PORT}")

    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.daemon = True
    accept_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
