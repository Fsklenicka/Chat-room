import socket
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = 'zpravy.msgs'
lock = threading.Lock()  # Lock for file access and clients list
clients = []


def handle_client(client_socket, client_address):
    logging.info(f"New connection from {client_address}")
    try:
        with lock:
            with open(path, 'r') as file:
                for line in file:
                    client_socket.send(line.encode('utf-8'))

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            logging.info(f"Received from {client_address}: {message}")
            broadcast(message, client_socket)
            with lock:
                with open(path, 'a') as file:
                    file.write(message + '\n')
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
        logging.info(f"Connection from {client_address} closed")


def broadcast(message, current_client_socket):
    with lock:
        for client in clients:
            if client != current_client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    logging.error(f"Error broadcasting to a client: {e}")
                    clients.remove(client)


def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('89.203.249.186', 5555))
    server_socket.listen(5)
    logging.info("Server is listening on port 5555")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            with lock:
                clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        logging.info("Server is shutting down")
    finally:
        server_socket.close()


if __name__ == "__main__":
    server_program()
