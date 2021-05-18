import socket 
import threading 
import base64

HEADER = 16

# format used in possible decryption
FORMAT = 'ascii'

#want a port that isnt being used
# other common ports are 8080 or 80 used for HTTP or the web
PORT = 5050

# this is the local address for my device, and I want to set the server up here
# this can be changed too 
SERVER = "10.0.0.222"

# get the IP address of this computer by name, and it takes the name of the computer 
# as a paramter 

#-----------------------------------------------------------------------

SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
# binding a socket to an address must be in a tuple with server and port
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bound socket to ADDR address ( server and port)
server.bind(ADDR)


#-------------------------------------------
# Now we have a small server set up, and now to set it up for listening and other 
# functions


# handles new connections and sends them where they need to go
def start():
    server.listen(5)
    print( "[LISTENING] Server is listening on {}".format(SERVER) )


# this will be running concurrentluy for each client 
def handle_client(conn, addr):
    print("[NEW CONNECTION] {} connected.".format(addr))

    try:
        while True:

            msg_length = conn.recv(HEADER)          #get length of message

            if not len(msg_length):
                conn.close()
            else:
                message = conn.recv(HEADER)
                server.send(message)            
        
    except: 
        # close the connection if an error happens
        conn.close()

def recieve():
    # server will continue to listen until error or manual end
    #when a new connection is found, it is accepted. The IP and port it 
    # came from is given to addr, then is stored in socket obj conn 
    # allowing it to communicate back 
    while True:

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
