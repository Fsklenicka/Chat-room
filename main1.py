import socket
import threading
import logging
import signal
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = 'zpravy.msgs'
lock = threading.Lock()  # Lock for file access and clients list
clients = []
shutdown_event = threading.Event()  # Event to signal threads to shut down

def handle_client(client_socket, client_address):
    logging.info(f"New connection from {client_address}")
    try:
        with lock:
            with open(path, 'r') as file:
                for line in file:
                    if not line.startswith("GET "):  # Filtering out HTTP GET requests
                        client_socket.send(line.encode('utf-8'))

        while not shutdown_event.is_set():
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if not message.startswith("GET "):  # Filtering out HTTP GET requests
                    logging.info(f"Received from {client_address}: {message}")
                    broadcast(message, client_socket)
                    with lock:
                        with open(path, 'a') as file:
                            file.write(message + '\n')
            except ConnectionResetError:
                break
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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR to allow reuse of the address
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    logging.info("Server is listening on port 5555")

    def signal_handler(sig, frame):
        logging.info("SIGINT received, shutting down server...")
        shutdown_event.set()  # Signal all threads to shut down
        server_socket.close()  # Close the server socket to stop accepting new connections

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while not shutdown_event.is_set():
            try:
                client_socket, client_address = server_socket.accept()
            except OSError:
                break  # Break out of loop if server socket is closed
            with lock:
                clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    finally:
        logging.info("Waiting for all client threads to finish...")
        for client in clients:
            client.close()  # Close all client sockets
        shutdown_event.set()  # Ensure shutdown_event is set
        logging.info("Server has shut down.")

if __name__ == "__main__":
    server_program()
