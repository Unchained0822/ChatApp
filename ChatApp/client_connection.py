import socket
import threading
from utils import log_connection_attempt, log_connection_error, log_message, log_error, log_timeout_error

class ClientConnection:
    def __init__(self, update_chat_callback):
        self.socket = None
        self.update_chat_callback = update_chat_callback
        self.is_connected = False  # Initialize connection status

    def connect(self, server_ip, port=54321):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_ip, port))
            self.is_connected = True  # Set connected status to True
            self.update_chat_callback("Connected to server!")
            log_connection_attempt(server_ip, "connected")

            # Start a new thread to listen for incoming messages
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.update_chat_callback(f"Connection error: {e}")
            log_connection_error(server_ip, str(e))

    def send_message(self, message):
        try:
            if self.is_connected and self.socket:
                self.socket.send(message.encode('utf-8'))
                log_message("Client", message)
            else:
                self.update_chat_callback("Error: Not connected to the server.")
        except Exception as e:
            self.update_chat_callback(f"Error sending message: {e}")
            log_error(f"Error sending message: {e}")

    def receive_messages(self):
        try:
            while self.is_connected:  
                self.socket.settimeout(5)  
                try:
                    message = self.socket.recv(1024).decode('utf-8')                 
                    if message:
                        self.update_chat_callback(f"Server: {message}")
                    else:
                        self.update_chat_callback("Server disconnected.")
                        log_error("Server disconnected or connection lost.")
                        self.is_connected = False  
                        break  
                except socket.timeout:
                    continue 
        except Exception as e:
            self.update_chat_callback(f"Connection error: {e}")
            log_error(f"Error receiving message: {e}")
            self.is_connected = False  