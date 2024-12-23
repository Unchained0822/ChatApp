import tkinter as tk
from tkinter import scrolledtext
from client_connection import ClientConnection
from utils import handle_error

def start_client():
    def connect_to_server():
        server_ip = ip_entry.get().strip()
        if not server_ip:
            handle_error("Please enter a valid IP address.")
            return
        app.connection.connect(server_ip)
        ip_window.destroy()

    class ClientApp:
        def __init__(self, master):
            self.master = master
            self.master.title("Client - Chat Application")
            self.connection = ClientConnection(self.update_chat)

            self.chat_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
            self.chat_area.pack(pady=10)

            self.message_entry = tk.Entry(master, width=40)
            self.message_entry.pack(side=tk.LEFT, padx=(0, 10))
            self.message_entry.bind("<Return>", self.send_message)

            self.send_button = tk.Button(master, text="Send", command=self.send_message)
            self.send_button.pack(side=tk.LEFT)

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
    app = ClientApp(root)
    ip_window = tk.Toplevel(root)
    tk.Label(ip_window, text="Server IP Address:").pack(pady=5)
    ip_entry = tk.Entry(ip_window, width=30)
    ip_entry.pack(pady=5)
    tk.Button(ip_window, text="Connect", command=connect_to_server).pack(pady=10)
    root.mainloop()
