import socket
import os
import PySimpleGUI as sg
from client_interface import ClientInterface, ChatRoomInterface
from client_utils import (
    send_message,
    receive_message,
    set_nickname
)
from threading import Thread, Event
from queue import Queue
import queue
from server import HOST, PORT

PROCESS_ID = os.getpid()

def send(s: socket.socket, message_queue: Queue, stop_event: Event):
     while not stop_event.is_set():
        try:
            message = message_queue.get(timeout=1)
            if message == "EXIT":
                break
            send_message(s, message)
        except queue.Empty:
            continue

def receive(s: socket.socket, chat_room_interface: ChatRoomInterface, stop_event: Event):
    while not stop_event.is_set():
        try:
            message = receive_message(s)
            if message:
                chat_room_interface.window.write_event_value('-RECEIVE-', message)
        except (ConnectionAbortedError, ConnectionResetError, OSError):
            break

def client_interface(s: socket.socket):
    client_interface = ClientInterface()
    if set_nickname(s, client_interface) == None:
        return

    chat_room_interface = ChatRoomInterface()
    message_queue = Queue()
    stop_event = Event()

    send_thread = Thread(target=send, args=(s, message_queue, stop_event))
    receive_thread = Thread(target=receive, args=(s, chat_room_interface, stop_event))

    send_thread.start()
    receive_thread.start()

    while True:
        event, values = chat_room_interface.window.read()
        
        if event == 'Send':
            message = values['-INPUT-']
            chat_room_interface.window['-CHAT-'].update(f'You: {message}\n', append=True)
            chat_room_interface.window['-INPUT-'].update('')
            message_queue.put(message)
        
        if event == sg.WIN_CLOSED:
            message_queue.put("EXIT")
            stop_event.set()
            break
        
        if event == '-RECEIVE-':
            message = values['-RECEIVE-']
            chat_room_interface.window['-CHAT-'].update(f'{message}\n', append=True)


    s.close()
    send_thread.join()
    receive_thread.join()
    chat_room_interface.window.close()


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Process ID: {PROCESS_ID}")

        s.connect((HOST, PORT))
        print("Connected to the server...")

        client_interface(s)

if __name__ == "__main__":
    start_client()
