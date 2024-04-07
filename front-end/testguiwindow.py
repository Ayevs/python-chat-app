import PySimpleGUI as sg

# sg.Window(title="test window", layout=[[]], margins=(400,200)).read()

layout = [
    [sg.Text("Enter your username", size=(30, 1), key="Status")],
    [sg.InputText()],
    [sg.Button("Ok"), sg.Button("Close")],
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
        print("Youre username is: ", username)
        break
window.close()
