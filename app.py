# socket app
import socket, random, sys, ipaddress, time, os

if sys.argv[1] == "server":

    HOST = "0.0.0.0"
    PORT = 20001
    msgToClient = str.encode("Hello UDP Client")

    # Create a datagram socket at server side
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for Errno 98: Address already in use

    # Bind socket to localhost and port
    s.bind((HOST, PORT))
    print("UDP server started")



    # Listen for incoming datagrams
    while(True):
        msgFromClient = s.recvfrom(512)

        message = msgFromClient[0]
        address = msgFromClient[1]

        print("Message from Client: '{}'".format(message.decode()))
        print("Client: {}".format(address))

        # Sending a reply to client
        s.sendto(msgToClient, address)



elif sys.argv[1] == "client":

    try:
        ipaddress.ip_address(sys.argv[2])
        msgToServer = str.encode("Hello UDP Server")
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
        print("you must pass a valid ip address")


else:
    print("invalid command")
