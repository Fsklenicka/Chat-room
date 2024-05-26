import socket
import threading
import logging
import signal

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = 'zpravy.msgs'
lock = threading.Lock()  # Zámek pro přístup k souboru a seznam klientů
clients = []
shutdown_event = threading.Event()  # Událost pro signalizaci ukončení vláken

def handle_client(client_socket, client_address):
    logging.info(f"Nové připojení od {client_address}")
    try:
        with lock:
            with open(path, 'r') as file:
                for line in file:
                    if not line.startswith("GET "):  # Filtrování HTTP GET požadavků
                        client_socket.send(line.encode('utf-8'))

        while not shutdown_event.is_set():
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if not message.startswith("GET "):  # Filtrování HTTP GET požadavků
                    logging.info(f"Přijato od {client_address}: {message}")
                    broadcast(message, client_socket)
                    with lock:
                        with open(path, 'a') as file:
                            file.write(message + '\n')
            except ConnectionResetError:
                break
    except Exception as e:
        logging.error(f"Chyba při zpracování klienta {client_address}: {e}")
    finally:
        client_socket.close()
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
        logging.info(f"Připojení od {client_address} uzavřeno")

def broadcast(message, current_client_socket):
    with lock:
        for client in clients:
            if client != current_client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    logging.error(f"Chyba při vysílání ke klientovi: {e}")
                    clients.remove(client)

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Nastavení SO_REUSEADDR pro povolení opětovného použití adresy
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    logging.info("Server naslouchá na portu 5555")

    def signal_handler(sig, frame):
        logging.info("SIGINT přijat, ukončuji server...")
        shutdown_event.set()  # Signalizace všem vláknům k ukončení
        server_socket.close()  # Uzavření serverového socketu pro zastavení přijímání nových připojení

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while not shutdown_event.is_set():
            try:
                client_socket, client_address = server_socket.accept()
            except OSError:
                break  # Přerušení smyčky, pokud je serverový socket uzavřen
            with lock:
                clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    finally:
        logging.info("Čekání na dokončení všech klientských vláken...")
        for client in clients:
            client.close()  # Uzavření všech klientských socketů
        shutdown_event.set()  # Zajištění nastavení shutdown_event
        logging.info("Server byl ukončen.")

if __name__ == "__main__":
    server_program()
