import PySimpleGUI as sg

# sg.Window(title="test window", layout=[[]], margins=(400,200)).read()

# theme for the window
sg.theme('DarkBlue14')  


# layout with some styling
layout = [
    [sg.Text("Enter your username:", font=("Helvetica", 12), text_color="white", key="Status")],
    [sg.InputText(font=("Helvetica", 12), size=(25, 1))],
    [sg.Button("Ok", button_color=("white", "blue"), font=("Helvetica", 12)), sg.Button("Close", button_color=("white", "red"), font=("Helvetica", 12))],
]
window = sg.Window("Chat App", layout, resizable=True, finalize=True)
# window.bind('<Configure>', "Configure")
# status = window['Status']
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Close":
        break
    elif event == "Ok":
        username = values[0]
        print("Your username is:", username)
        break
window.close()

# chat window (will be edited later)
chat_layout = []

#chat window style after getting username
chat_layout = [
    [sg.Text("Global Chat", font=("Helvetica", 14), text_color="white")],
    [sg.Multiline(default_text="", size=(40, 15), key="ChatHistory", autoscroll=True, disabled=True, font=("Helvetica", 12))],
    [sg.InputText(do_not_clear=False, size=(30, 1), font=("Helvetica", 12), key="ChatInput"), sg.Button("Send", bind_return_key=True)]
]

chat_window = sg.Window("Global Chat", chat_layout, resizable=True, finalize=True)
chat_history = ""  #  chat history

# Event loop for the chat window
while True:
    event, values = chat_window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Send":
        message = values["ChatInput"].strip()
        if message:
            # Add the new message to the chat history
            chat_history += f"{username}: {message}\n"
            chat_window["ChatHistory"].update(chat_history)

chat_window.close()