import PySimpleGUI as sg
from threading import Thread
import socket


class ChatRoomInterface:

    def __init__(self):
        self.layout = [
            [sg.Text('Chat Room')],
            [sg.Multiline(size=(80, 30), key='-CHAT-')],
            [sg.Input(size=(50, 1), key='-INPUT-'), sg.Button('Send')],
        ]
        self.window = sg.Window(
            title='Chat Room',
            size=(600, 600),
            layout=self.layout,
            element_justification='center',
        )

class ClientInterface:

    def __init__(self):
        self.layout = [
            [sg.Image(filename='./projeto_de_redes/images/chat.png', size=(200, 200))],
            [sg.Text('Nickname: '), sg.Input(size=(20, 1))],
            [sg.Button(button_text='Entrar no Servidor')],
        ]
        self.window = sg.Window(
            title='Window Title',
            size=(300, 300),
            layout=self.layout,
            element_justification='center',
        )
    
    

