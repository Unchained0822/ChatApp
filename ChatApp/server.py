import tkinter as tk
from tkinter import scrolledtext
from server_connection import ServerConnection
from utils import handle_error

def start_server():
    class ServerApp:
        def __init__(self, master):
            self.master = master
            self.master.title("Server - Chat Application")
            self.connection = ServerConnection(self.update_chat)

            self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
            self.chat_area.pack(pady=10)

            self.message_entry = tk.Entry(master, width=40)
            self.message_entry.pack(side=tk.LEFT, padx=(0, 10))
            self.message_entry.bind("<Return>", self.send_message)

            self.send_button = tk.Button(master, text="Send", command=self.send_message)
            self.send_button.pack(side=tk.LEFT)

            self.connection.start_server()

        def update_chat(self, message):
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, message + "\n")
            self.chat_area.config(state='disabled')

        def send_message(self, event=None):
            message = self.message_entry.get().strip()
            if message:
                self.update_chat(f"You: {message}")
                self.message_entry.delete(0, tk.END)
                self.connection.send_message(message)

    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
