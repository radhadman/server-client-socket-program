# socket app
import socket, sys, ipaddress, time, os

# initial check for 'client' or 'server' argument
try:
    sys.argv[1]
except:
    print("pass 'client' or 'server' for the respective mode")
    exit()


# run in server mode
if sys.argv[1] == "server":

    HOST = "0.0.0.0" # to accept all incoming connections
    PORT = 20001

    # Create a datagram socket at server side
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for Errno 98: Address already in use

    # Bind socket to 0.0.0.0 and specified port no.
    s.bind((HOST, PORT))
    print("UDP server started")


    # Listen for incoming datagrams
    while(True):
        msgFromClient = s.recvfrom(512)
        message = msgFromClient[0]
        address = msgFromClient[1]
        msgToClient = ""
        decoded = message.decode()

        # check for valid float, then reply with two times that value
        try:
            isinstance(float(decoded), float)
            if isinstance(float(decoded), float):
                print("Value from client: '{}'".format(float(decoded)))
                print("Client: {}".format(address))
                msgToClient = str(2*float(decoded))

                # Sending value reply
                s.sendto(str.encode(msgToClient), address)

        except:
            print("input was not a number")
            print("Message from client: '{}'".format(decoded))
            print("Client: {}".format(address))

            # send string reply
            s.sendto(str.encode(decoded), address)

# run in client mode
elif sys.argv[1] == "client":

    try:
        ipaddress.ip_address(sys.argv[2]) # check for valid ip address input
        string = str(" ".join(sys.argv[3:])) # all remaining command arugments are string to send (ie. [3:])
        msgToServer = str.encode(string)
        HOST = sys.argv[2] # argument 2 is host server ip
        PORT = 20001

        # UDP socket at client side
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        s.settimeout(5) # time out in 5 seconds if there is no reply datagram

        try:
            s.sendto(msgToServer, (HOST,PORT))
            print("Datagram sent to host server: {}".format(HOST))

        # if a datagram fails to send (this exception never seems to trigger)
        except:
            print("Message could not be sent")

        # wait 5 seconds for a reply from server
        try:
            msgFromServer = s.recvfrom(512)
            print("Server reply: '{}'".format(msgFromServer[0].decode()))

        except socket.timeout:
            print("No reply from server") # timeout on socket error

    # valid ip error catch
    except:
        print("you must pass a valid ip address and string message")

# all invalid commands
else:
    print("invalid command")
