import socket
import threading


def handle_client(client_socket):
    # Send a welcome message to the client
    client_socket.send(b"Welcome to the server. Send your messages.\n")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            # If no data is received, the client has disconnected
            print("Client disconnected.")
            break

        # Print the received message
        print("Received message from client:", data.decode())

    # Close the client socket
    client_socket.close()


def main():
    # Define host and port
    host = "127.0.0.1"  # localhost
    port = 9999

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    try:
        while True:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from:", client_address)

            # Create a new thread to handle the client
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket,)
            )
            client_thread.start()

    except KeyboardInterrupt:
        # Close the server socket on Ctrl+C
        print("Server shutting down.")
        server_socket.close()


if __name__ == "__main__":
    main()
