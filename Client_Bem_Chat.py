#!/usr/bin/env python3
# chat client
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def askHelp():
    messagebox.showinfo("About", "BEM Chat Client V. 0.01 beta created by BEM at bem dot bem\n 06-05-2018")
def receive():
    # handle incoming messages
    # add a feature to change the text color for each name
    while True:
        try:
            message = clientSocket.recv(bufferSize).decode("utf8")
            messageList.insert(tkinter.END, message)
            messageList.insert(tkinter.END, "\n")
        except OSError:  # Possibly client has left the chat.
            break
def send(event=None):  # event is passed by binders.
    # handle sending a message
    message = myMessage.get()
    myMessage.set("")  # Clears input field.
    clientSocket.send(bytes(message, "utf8"))


def onClose(event=None):
    # end the chat session
    clientSocket.send(bytes("{KillSocket}", "utf8"))
    clientSocket.close()
    root.destroy()


def saveFile():
    global text # contents of the grid text
    fileName=filedialog.asksaveasfile(mode='w',defaultextension=".txt") # get name of file, later add options
    content=messageList.get("1.0",'end-1c') # from first character to last - 1 to avoid newline
    fileName.write(content) # write the content to the file
    fileName.close

# build GUI
root = tkinter.Tk()
root.title("BEM Chat Client V. 0.01 Beta")
chatClientFrame = tkinter.Frame(root)
myMessage = tkinter.StringVar()  # For the messages to be sent.
myMessage.set("")
scrollbar = tkinter.Scrollbar(chatClientFrame)  # To navigate through past messages.
messageList = tkinter.Text(chatClientFrame, height=15, width=45, yscrollcommand=scrollbar.set)
messageList.configure(bg='black',fg='green')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messageList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
#messageList.pack()
chatClientFrame.pack()

# create menubar
menubar = Menu(root)
#menubar.configure(bg="black", fg="green")

# create File pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save Chat to File", command=saveFile)
filemenu.add_command(label="Exit Chat", command=onClose)
menubar.add_cascade(label="File", menu=filemenu)

# create Help pulldown menu, and add it to the menu bar
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=askHelp)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

myMesEnterField = tkinter.Entry(root, textvariable=myMessage)
myMesEnterField.bind("<Return>", send)
myMesEnterField.pack()
send_button = tkinter.Button(root, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", onClose)

host = input('Host IP <localhost>: ')
if not host:
    host = "127.0.0.1" # default to local host
else:
    host = host
port = input('Port <33333>: ')
if not port:
    port = 33333  # Default value.
else:
    port = int(port)
bufferSize = 256
serverAddress = (host, port)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)

getThread = Thread(target=receive)
getThread.start()
tkinter.mainloop()  # Starts GUI execution.
