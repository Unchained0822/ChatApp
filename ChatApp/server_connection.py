import socket
import threading
from utils import log_connection_attempt, log_connection_error, log_message, log_error

class ServerConnection:
    def __init__(self, update_chat_callback):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.update_chat_callback = update_chat_callback

    def start_server(self, host="0.0.0.0", port=54321):
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.update_chat_callback("Server started. Waiting for a connection...")
        threading.Thread(target=self.accept_client, daemon=True).start()

    def accept_client(self):
        try:
            self.connection, addr = self.socket.accept() 
            log_connection_attempt(addr[0], "connected")  
            self.update_chat_callback(f"Client connected from {addr}")       
            self.send_message("Welcome to the chat server!")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            log_connection_error("Unknown", str(e))
            self.update_chat_callback(f"Error accepting client connection: {e}")

    def send_message(self, message):
        if self.connection:
            try:
                self.connection.send(message.encode('utf-8'))
                log_message("Server", message)  # Log the sent message
            except Exception as e:
                log_error(f"Error sending message: {e}")  
                self.update_chat_callback(f"Error sending message: {e}")
        else:
            self.update_chat_callback("Error: No client connection established.")

    def receive_messages(self):
        while True:
            try:
                message = self.connection.recv(1024).decode('utf-8')
                if message:
                    self.update_chat_callback(f"Client: {message}")
                else:
                    self.update_chat_callback("Client disconnected.")
                    log_error("Client disconnected or connection lost.")
                    break  
            except Exception as e:
                self.update_chat_callback(f"Connection error: {e}")
                log_error(f"Error receiving message: {e}")
                break 
