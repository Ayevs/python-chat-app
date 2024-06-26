import socket
import threading
import datetime

# store the client info
clients = {}

# store chat history
chat_history = []


def handle_client(client_socket, client_address):
    try:
        username = client_socket.recv(1024).decode().strip()

        # add client to list
        clients[client_socket] = username

        # Notify all clients except the newly connected one that a new user has connected
        notify_message = f"{username} has connected to the server."
        print(notify_message)
        broadcast(notify_message, exclude_client=client_socket)

        # send the chat history to the newly connected client
        for message in chat_history:
            client_socket.send(message.encode())

        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                # If no data is received, the client has disconnected
                print(f"{username} disconnected.")
                del clients[client_socket]  # removes the client from the list of users
                break

            # broadcast message from the client
            message = f"{username}: {data.decode()}"
            chat_history.append(message)
            broadcast(message)

    except Exception as e:
        print(f"error handling client {username}: {e}")
        del clients[client_socket]
    finally:
        # Close the client socket
        client_socket.close()


def broadcast(message, exclude_client=None):
    # method userd to sending message to all connected clients
    for client_socket in list(clients.keys()):
        if client_socket != exclude_client:
            try:
                client_socket.send(message.encode())
            except ConnectionError:
                # if there's an error sending a message we assume the client disconnected
                username = clients[client_socket]
                print(f"{username} disconnected unexpectedly.")
                del clients[client_socket]


def main():
    # Define host and port
    host = "127.0.0.1"  # localhost
    port = 9999

    # Get the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # appending welcome message to the chat history
    chat_history.append(
        f"welcome to Global chat, this server has been running since: {current_time}"
    )

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
                target=handle_client, args=(client_socket, client_address)
            )
            client_thread.start()

    except KeyboardInterrupt:
        # Close the server socket on Ctrl+C
        print("Server shutting down.")
        server_socket.close()


if __name__ == "__main__":
    main()
