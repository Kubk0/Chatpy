# import all the required  modules
import socket
import json
import getpass
import sys
import datetime
import os
from datetime import datetime as dt
from inputimeout import inputimeout,TimeoutOccurred
# import all functions /
#  everything from chat.py file
dat = input("ip:")
if ":" in dat:
    SERVER,PORT = dat.split(":")
    PORT = int(PORT)
else:
    PORT = 50
    SERVER = dat
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
client.connect(ADDRESS)
reg = input("l-login;r-register:")
pjs = {}
if reg == "r":
    pjs.update({"LOGR":"TYPEVAR"})
elif reg == "l":
    pjs.update({"LOGL":"TYPEVAR"})

pjs.update({"name":input("name:")})
pjs.update({"pass":getpass.getpass()})
client.send(json.dumps(pjs).encode())
pd = client.recv(4096).decode()
pd = json.loads(pd)
if pd["conn"] == "suc":
    for x in pd["thrs"]:
        print(x)
while True:
    mode = input('Type the name of a thread to enter or type "n" to create a new thread:')
    if mode == "n":
        name = input("name of thread: ")
        mode+=("."+name)
    else:
        mode+="."
    dat = {}
    dat.update({"mode":mode})
    client.send(json.dumps(dat).encode())
    pd = client.recv(4096).decode()
    ## MESSAGES
    for x in json.loads(pd)["mess"]:
        print(x["author"] + ": " + x["text"] + " " + str(dt.fromtimestamp(x["timestamp"])))
    print("""You can type "!adduser <name of user> to add a user to this thread,
press "q" to close this program
or just type your message.
""")
    while True:
        dat = {}
        try:
            mode = inputimeout(prompt='', timeout=10)
        except TimeoutOccurred:
            os.system("cls")
            mode = ''
        if mode == "q":
            sys.exit()
        elif not mode.startswith("!adduser "):
            dat.update({"MESS":mode})
        else:
            dat.update({"ADDU":mode[9:]})
            print("adding " + mode[9:] + "to this thread")
        client.send(json.dumps(dat).encode())
        for x in json.loads(client.recv(4096))["MSGS"]:
            print(x["author"] + ": " + x["text"] + "  @ " + str(dt.fromtimestamp(x["timestamp"])))