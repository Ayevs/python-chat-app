# client side for chat app 
# this is just ground work for setting up the connection 

import socket

def main():
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Change this to your server's IP address and port
    
    try:
        client_socket.connect(server_address)
        print("Connected to the server.")
    except Exception as e:
        print("Error connecting to the server:", e)
        return

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    main()
