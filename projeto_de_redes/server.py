import os
import socket
from threading import Thread

PROCESS_ID = os.getpid()
HOST = "127.0.0.1" 
PORT = 65432
MAX_CLIENTS = 10

# The clients dictionary will store the client's connection as the key
# and the client's nickname and address as the value in a dictionary.
clients = {}

def broadcast_message(message, sender_conn):
    sender_nickname = clients[sender_conn]['nickname']
    encoded_message = f'{sender_nickname} >> {message}'.encode()
    for conn in clients:
        if conn != sender_conn:
            conn.sendall(encoded_message)



def handle_client(conn, addr):
    with conn:
        print(f"New client connected: {addr}")

        nickname = conn.recv(1024).decode()
        clients[conn] = {'nickname': nickname, 'address': addr}
        print(f'Client: {addr} is now aka: {nickname}')


        while True:
            try:
                message = conn.recv(1024).decode()
                if message:
                    print(f"{nickname} says: {message}")
                    broadcast_message(message, conn)
                else:
                    break
            except:
                break

        print(f"Client {addr} disconnected")
        del clients[conn]
        conn.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Process ID: {PROCESS_ID}")
        
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening...")

        while True:
            conn, addr = s.accept()
            client_thread = Thread(target=handle_client, args=(conn, addr))
            client_thread.start()