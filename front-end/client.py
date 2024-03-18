# client side for chat app 
# this is just ground work
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred while receiving messages.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def main():
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)  # Change this to your server's IP address and port
    client_socket.connect(server_address)

    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send and receive messages continuously
    while True:
        send_messages(client_socket)

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    main()
