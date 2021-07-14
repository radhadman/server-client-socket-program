# socket app
import socket, sys, ipaddress, time, os


try:
    sys.argv[1]
except:
    print("pass 'client' or 'server' for the respective mode")
    exit()

if sys.argv[1] == "server":

    HOST = "0.0.0.0"
    PORT = 20001
    msgToClient = str.encode("Hello UDP client")

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

        try:
            if isinstance(   int(message.decode()), int   ):
                print("Value from client: '{}'".format(int(message.decode())))
                print("Client: {}".format(address))
            elif isinstance(   float(message.decode()), float   ):
                print("Value from client: '{}'".format(float(message.decode())))
                print("Client: {}".format(address))
        except:
            print("input must be a number")

        # Sending a reply to client
        s.sendto(msgToClient, address)



elif sys.argv[1] == "client":

    try:
        ipaddress.ip_address(sys.argv[2])
        string = str(" ".join(sys.argv[3:]))
        msgToServer = str.encode(string)
        HOST = sys.argv[2]
        PORT = 20001

        # UDP socket at client side
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        s.settimeout(5)

        try:
            s.sendto(msgToServer, (HOST,PORT))
            print("Datagram sent to host server: {}".format(HOST))

        except:
            print("Message could not be sent")

        try:
            msgFromServer = s.recvfrom(512)
            print("Server reply: '{}'".format(msgFromServer[0].decode()))
        except socket.timeout:
            print("No reply from server")

    except:
        print("you must pass a valid ip address and string message")

else:
    print("invalid command")
