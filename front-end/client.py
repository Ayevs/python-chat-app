# client side for chat app
# this is just ground work for setting up the connection

import socket


def main():
    # Define server host and port
    server_host = "18.221.198.127"  # localhost
    server_port = 9999

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))
        print("Connected to server.")

        while True:
            # Read message from the user
            message = input("Enter message to send (or 'quit' to exit): ").strip()

            if message.lower() == "quit":
                break

            # Send message to the server
            client_socket.sendall(message.encode())

        # Close the socket
        client_socket.close()
        print("Connection closed.")

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except KeyboardInterrupt:
        print("\nClient shutting down.")
        client_socket.close()


if __name__ == "__main__":
    main()
