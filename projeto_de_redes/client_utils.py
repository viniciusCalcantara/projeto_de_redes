import PySimpleGUI as sg
import socket
from client_interface import ClientInterface

def send_message(s: socket.socket, message: str) -> None:
    s.sendall(message.encode())

def receive_message(s: socket.socket) -> str:
    data = s.recv(1024)
    return data.decode()

def set_nickname(s: socket.socket, client_interface: ClientInterface) -> None:

    while True:
        event, values = client_interface.window.read()

        if event == 'Entrar no Servidor':
            nickname = values[1]
            send_message(s, nickname)
            break

        if event == sg.WIN_CLOSED:
            client_interface.window.close()
            return None
        
    client_interface.window.close()    