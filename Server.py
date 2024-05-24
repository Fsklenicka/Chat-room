import socket
import threading

path='zpravy.msgs'

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    with open(path, 'r+') as file:
        for line in  file:
            broadcast(line, client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received from {client_address}: {message}")
                broadcast(message, client_socket)
                with open(path, 'r+') as file:
                    file.write(message+'\n')
            else:
                break
        except :
            print(e)
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection from {client_address} closed")

def broadcast(message, current_client_socket):
    for client in clients:
        if client != current_client_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                client.close()
                clients.remove(client)

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('89.203.249.186', 5555))
    server_socket.listen(5)
    print("Server is listening on port 5555")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

clients = []
if __name__ == "__main__":
    server_program()
