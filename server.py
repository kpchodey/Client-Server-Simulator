import socket
import sys
import os
from time import gmtime, strftime
import json

def run_server():
    host = 'localhost'
    port = 8220
    address = (host, port)

    try:
        os.remove('simulatorWallLog.txt')
    except OSError:
        pass

    #Create a socket and start listening for clients
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(address)
    listen_socket.listen(5)

    logToFile("Server initiated and running on port 8220 at localhost")

    while True:
        client_connection, client_address = listen_socket.accept()

        logToFile("Server accepted connection from Client"+str(client_address))

        pid = os.fork()
        if pid == 0:  # child

            while True:
                request = client_connection.recv(2048);
                if request.strip() == "disconnect":
                    client_connection.close()
                    logToFile("Received disconnect message. Client got disconnected.")
                    sys.exit("Bye")
                    client_connection.send("dack")
                elif request:
                    handleRequest(request, client_connection)

            listen_socket.close()  # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:  # parent
            client_connection.close()


# Intelligence in handling the request should go here
def handleRequest(request, conn):
    http_response = b"""Default"""

    line1 = []
    with open("Test_Hooks1.txt") as file1:                     #lookup table to compare the requests and response
        for line in file1.read().splitlines():
            cleanedLine = line.strip()                         #returns a copy of string where all the characters are stripped from beging to ending
            if cleanedLine:
                line1.append(cleanedLine)                      #adding cleaned line to the list

    if request.startswith("${respon}"):                        #Checking for word starting with ${respon}
        idx = line1.index(request)
        http_response = line1[idx+1]                           #incrementing thee response

    logToFile("Request recieved from client  {0}".format(request))

    print 'Sending Response {0}'.format(http_response)
    conn.sendall(http_response)

#opening a logfile where all the results will go
def logToFile(logTxt):
    logFile = open("simulatorWallLog.txt", "a+")
    # logTxt+=getCurrentTimeStamp()

    logFile.write(getCurrentTimeStamp()+" "+logTxt+"\n")
    print logTxt

def getCurrentTimeStamp():
    return strftime("%Y-%m-%d %H:%M:%S")

run_server()
