from tkinter import messagebox
import logging

def handle_error(message):
    messagebox.showerror("Error", message)

import logging

# Configure logging to write to a file with debug level
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_connection_attempt(client_ip, status):
    logging.info(f"Connection from {client_ip}: {status}")

def log_error(message):
    logging.error(f"Error: {message}")

def log_message(direction, message):
    logging.info(f"{direction} message: {message}")
    
def log_connection_error(client_ip, error_message):
    logging.error(f"Connection attempt from {client_ip} failed: {error_message}")

def log_timeout_error(message):
    logging.error(f"Timeout error: {message}")
