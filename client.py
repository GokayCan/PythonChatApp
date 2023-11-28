import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            input_ready.set()  # Mesaj alındı ve kullanıcıya mesaj göndermeye izni veriyoruz
        except Exception as e:
            print(f"Hata: {e}")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

input_ready = threading.Event()  # Kullanıcının mesaj gönderebilme izni için bir olay tanımladık

while True:
    input_ready.wait()  # Kullanıcının mesaj göndermesini bekliyoruz

    message = input()
    client_socket.sendall(message.encode('utf-8'))

    if message.lower() == 'exit':
        break

client_socket.close()
