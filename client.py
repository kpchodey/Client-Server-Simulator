import socket
import sys
import os
import time
from time import gmtime, strftime
import json

def initialSetup():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8220))

    try:
        os.remove('testSuitelLog.txt')
    except OSError:
        pass
    logToFile("initial Setup complete. Connected with Server")

    line2 = []
    with open("Test_hooks.txt", "r") as inp:            #Send a test suite to the server
        for line in inp.read().splitlines():
            cleanedLine = line.strip()                  #returns a copy of string where all the characters are stripped from beging to ending
            if cleanedLine:
                line2.append(cleanedLine)               #adding cleaned line to the list

    for r in line2:
        client_socket.send(r)
        logToFile("request made:" + str(r))             #log the request made to server
        response = client_socket.recv(1024)
        logToFile(str(response))                        #log the response received

    # send disconnect message
    dmsg = "disconnect"
    print "Disconnecting"
    client_socket.send(dmsg)

    client_socket.close()
    logToFile("Closed connection with Server. Exiting...")


def logToFile(logTxt):
    logFile = open("testSuitelLog.txt", "a+")
    # logTxt+=getCurrentTimeStamp()

    logFile.write(getCurrentTimeStamp()+" "+logTxt+"\n")
    print logTxt

def getCurrentTimeStamp():
    return strftime("%Y-%m-%d %H:%M:%S")

initialSetup()
