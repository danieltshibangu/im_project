import socket 
import threading 
import base64
'''
What is threading?
This allows pieces of code to run simultaneously as others run 
rather than having to wait for each code to run sequentially
'''

'''
first message recieved from client is a header of 8 bytes
since we don't know how big a message is going to be the server will 
get two messages: the aqmount of bytes from the header and the actual msg
'''
HEADER = 16

# format used in possible decryption
FORMAT = 'utf-8'

#want a port that isnt being used
# other common ports are 8080 or 80 used for HTTP or the web
PORT = 5050

# this is the local address for my device, and I want to set the server up here
# this can be changed too 
SERVER = "10.0.0.222"

# get the IP address of this computer by name, and it takes the name of the computer 
# as a paramter 
'''
Why would we want to just hardcode the direct address?
if we want to access this one on a different device, we woud have to change the name 
each time
'''
SERVER = socket.gethostbyname(socket.gethostname())

# binding a socket to an address must be in a tuple with server and port
ADDR = (SERVER, PORT)

OK_FEEDBACK = 'text recieved'

# when recieved, we disconnect client from server
DISCONNECT_MESSAGE = "bye"

# list of all the clients and usernames

#-----------------------------------------------------------------------

#We have the port(5050) and the server, next we pick the socket 
# and bind socket to address

# Here we create a socket, in this case to make a TCP connection 
# AF_INET tells the socket to communicate with IP addresses

'''
# SOCK_STREAM tells how to package the data for sending 
specifically that it is being sent in sequential order, not randomly
Also
when sending something on a socket, it is a packet or frame that holds more
than just the data itself. 
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bound socket to ADDR address ( server and port) so, 
# anything that connects to this address also connects to this server socket
server.bind(ADDR)

#-------------------------------------------
# Now we have a small server set up, and now to set it up for listening and other 
# functions


# handles new connections and sends them where they need to go
def start():
    # allow server to listen for connections
    server.listen()

    print( f"[LISTENING] Server is listening on {SERVER}" )



# this will be running concurrentluy for each client 
def handle_client(conn, addr):
    # who connected?
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected: 
        '''
        VERY IMPORTANT! 
        conn.recv() is a blocking line of code that doesn't allow anything to happen
        until we get a response from the client. This is why it's important to have
        these in threads so other clients aren't kept in waiting for one client to
        respond
        '''

        # we recieve messages through the socket conn
        # the recv() method needs a number for bytes to recieved
        # aka need a protocol to determine number of bytes for messages that
        # can be recieved

        # when msgs are sent they are encoded into byte format so they
        # must be decoded into utf-8 format
        msg_length = conn.recv(HEADER)
        msg_length = msg_length.decode(FORMAT)
        msg_length = base64.b64decode(msg_length).decode(FORMAT)


          # HOW LONG IS  MSG
        if msg_length:
            msg_length = int(msg_length)                 # TURN MSG LENGTH TO INT
            msg = conn.recv(HEADER)
            msg = msg.decode(FORMAT)
            msg = base64.b64decode(msg).decode(FORMAT)

            #---- disconnecting -------
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'{msg}')
            
    conn.close()

def recieve():
    # server will continue to listen until error or manual end
    while True:
        #when a new connection is found, it is accepted. The IP and port it 
        # came from is given to addr, then is stored in socket obj conn 
        # allowing it to communicate back 
        conn, addr = server.accept()
        
        print("Connected with {}".format(str(addr))) 
        
        # creates a thread for every new connection that is sent to handle_client()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() 

        # prints how many threads or active connections are running 
        # minus the one start thread that is always running 
        activeConnections = threading.activeCount() - 1  
    
# output code to indicate server is listening. The IP and port it came from 
# is given to addr, then is stored in obj conn allowing it to communicate back
print( "[STARTING] server is starting...")
start()
recieve()