import sys
from client import start_client
from server import start_server

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["client", "server"]:
        print("Usage: python main.py [client|server]")
        return

    if sys.argv[1] == "server":
        start_server()
    elif sys.argv[1] == "client":
        start_client()

if __name__ == "__main__":
    main()
