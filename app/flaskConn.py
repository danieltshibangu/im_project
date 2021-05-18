from flask import Flask, url_for, redirect, render_template, request, flash
import threading
import socket
import base64

HEADER = 16
PORT = 5050
FORMAT = 'ascii'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # connect to server, instead of bind
client.connect(ADDR)

client.setblocking(False)

def getName(username):
    try:
        if username:
            name = username.encode(FORMAT)
            name = base64.b64encode(name)
            return name

    except:
        flash(u'Invalid password provided', 'error')


def send(clientMessage):             # encrypts the message

    while clientMessage:
        
        try:

            if clientMessage:
                message = '{}'.format(clientMessage)            # formats client message
                message = message.encode(FORMAT)                # encodes from <str> to <byte>
                message = base64.b64encode(message)

            msg_length = len(message)
            msg_length = str(msg_length).encode(FORMAT)

            # the length of message is converted to a string and encoded in utf-8 format
            send_length = base64.b64encode(msg_length)

            #pad to make it a length of 8 bytes
            # so subtract 8 bytes by the length of the message to find whitespace length 
            # b' ' is the byte representation of the calculated length ( whitespace)
            send_length += b' ' * (HEADER - len(send_length))

            client.send(send_length)
            client.send(message)

        except:
            client.close()

        clientMessage = ""

def threadClient():
    while True:
        
        conn, addr = client.accept()

        # creates a thread for every new connection that is sent to handle_client()
        thread = threading.Thread(target=get, args=(conn, addr))
        thread.start() 

        # prints how many threads or active connections are running 
        # minus the one start thread that is always running 
        activeConnections = threading.activeCount() - 1 
    

# set up the flask app 
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.static_folder = '../static'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=["GET", "POST"])
def title_screen():
    return render_template('title.html')


@app.route('/dialog', methods=["GET", "POST"])
def my_site():
    if request.method == "POST":
        msg = request.form.get("input-msg")
        send(msg)
    return render_template('index.html')

@app.route('/username.html', methods=["GET", "POST"])
def getusername():
    if request.method == "POST":
        name = request.form.get("#username")
        getName(name)
    return render_template("username.html")

if __name__ == "__main__":
    app.run(debug=True)
    threadClient()