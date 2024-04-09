import socket
import threading
import PySimpleGUI as sg

# theme for the window
sg.theme("DarkBlue14")


def receive_messages(sock, chat_window):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            chat_window.write_message(message)
        except ConnectionAbortedError:
            break


def send_message(sock, message):
    try:
        sock.sendall(message.encode("utf-8"))
    except ConnectionAbortedError:
        pass


class ChatWindow:
    def __init__(self, username, server_address):
        self.username = username
        self.server_address = server_address
        self.layout = [
            [sg.Text("Global Chat", font=("Helvetica", 14), text_color="white")],
            [
                sg.Multiline(
                    default_text="",
                    size=(40, 15),
                    key="ChatHistory",
                    autoscroll=True,
                    disabled=True,
                    font=("Helvetica", 12),
                )
            ],
            [
                sg.InputText(
                    do_not_clear=False,
                    size=(30, 1),
                    font=("Helvetica", 12),
                    key="ChatInput",
                ),
                sg.Button("Send", bind_return_key=True),
            ],
        ]
        self.window = sg.Window(
            "Global Chat App", self.layout, resizable=True, finalize=True
        )
        self.chat_history = []

    def write_message(self, message):
        # self.chat_history += message + "\n"
        # self.window["ChatHistory"].update(self.chat_history)
        self.chat_history.append(message)
        self.window["ChatHistory"].update("\n".join(self.chat_history))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            sock.sendall(self.username.encode("utf-8"))

            # recieve chat history from server
            chat_history = sock.recv(1024).decode("utf-8")
            if chat_history:
                self.write_message(chat_history)

            # sock.settimeout(1)  # Adjust the timeout value as needed
            # try:
            #     chat_history = sock.recv(4096).decode("utf-8")
            #     if chat_history:
            #         self.write_message(chat_history)
            # except socket.timeout:
            #     print("No chat history received.")

            # thread to kee recieveing messages
            threading.Thread(target=receive_messages, args=(sock, self)).start()

            # loop for sending messages
            while True:
                event, values = self.window.read()
                if event == sg.WINDOW_CLOSED:
                    break
                elif event == "Send":
                    message = values["ChatInput"].strip()
                    if message:
                        # self.chat_history.append(f"{self.username}: {message}")
                        self.window["ChatHistory"].update("\n".join(self.chat_history))
                        send_message(sock, f"{message}")


if __name__ == "__main__":
    layout = [
        [
            sg.Text(
                "Enter your username:",
                font=("Helvetica", 12),
                text_color="white",
                key="Status",
            )
        ],
        [sg.InputText(font=("Helvetica", 12), size=(25, 1), key="UsernameInput")],
        [
            sg.Button("Ok", button_color=("white", "blue"), font=("Helvetica", 12)),
            sg.Button("Close", button_color=("white", "red"), font=("Helvetica", 12)),
        ],
    ]
    window = sg.Window("Chat App", layout, resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        elif event == "Ok":
            username = values["UsernameInput"]
            server_address = ("127.0.0.1", 9999)  # server address
            chat_window = ChatWindow(username, server_address)
            chat_window.run()
            break
    window.close()
