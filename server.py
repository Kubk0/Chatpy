# import socket library
from cmath import e
import socket
import threading
import json
import time
import select
# Choose a port that is free
PORT = 50
def Message(text,author,timestamp):
    dd = {"text":text,"author":author,"timestamp":timestamp}
    return dd
# An IPv4 address is obtained
# for the server.  
SERVER = socket.gethostbyname(socket.gethostname())
 
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
print(ADDRESS)
# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"
 
# Lists that will contains
# all the clients connected to
# the server and their names.
clients,users = [],[]
 
# Create a new socket for
# the server
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
 
# bind the address of the
# server to the socket
server.bind(ADDRESS)
def dedo(nam,js,num=0):
    end = False
    for x in js:
        print(x,nam,num)
        if end == False:
            end = nam == x.split(".")[num]
    return end
def HandleLogin(pd,s,):
    def messages(s,user,thr,):
        while True:
            pd = json.loads(s.recv(4096).decode())
            if "MESS" in pd.keys():
                if pd["MESS"] != "":
                    message = Message(pd["MESS"],user["name"],time.time())
                    with open("messages.json","r") as f:
                        dd = json.load(f)
                        dd[thr].append(message)
                    with open("messages.json","w") as f:
                        json.dump(dd,f)
            elif "ADDU" in pd.keys():
                with open("threads.json","r") as f:
                    dd = json.load(f)
                    dd[pd["ADDU"]].append(thr)
                with open("threads.json","w") as f:
                    json.dump(dd,f)
            with open("messages.json","r") as f:
                ll = json.load(f)
                dat = {"MSGS":ll[thr]}
                s.send(json.dumps(dat).encode())
    def afterLogind(s,user):
        dat = {}
        pd = s.recv(4096).decode()
        pd = json.loads(pd)["mode"]
        if pd.split(".")[0] == "n":
            with open("threads.json","r") as f:
                dd = json.loads(f.read())
                name = user["name"]
                if not pd.split(".")[1] in dd[name]:
                    dd[user["name"]].append(pd.split(".")[1])
                    thr = pd.split(".")[1]
                    de = False
                else:
                    de = True
                    thr = pd.split(".")[1] + " 1"
                    dd[user["name"]].append(pd.split(".")[1] + " 1")
            with open("threads.json","w") as f:
                json.dump(dd,f)
            with open("messages.json","r") as f:
                js = json.load(f)
                if de:
                    thr = pd.split(".")[1] + " 1"
                    js.update({(pd.split(".")[1] + " 1"):[]})
                else:
                    thr = pd.split(".")[1]
                    js.update({(pd.split(".")[1]):[]})
            with open("messages.json","w") as f:
                json.dump(js,f)
            dat = {}
            dat.update({"err":"suc"})
            dat.update({"mess":[]})
        else:
            with open("messages.json","r") as f:
                dat.update({"mess":json.load(f)[pd.split(".")[0]]})
                thr = pd.split(".")[0]
            s.send(json.dumps(dat).encode())
        messages(s,user,thr)
    if "LOGR" in pd.keys():
        with open("./users.json","r") as f:
            js = json.loads(f.read())
            if not js.keys():
                js.update({"logs":[]})
            if not dedo(pd["name"],js["logs"]):
                js["logs"].append(pd["name"]+"."+pd["pass"])
        with open("./users.json","w") as f:
            json.dump(js,f)
        with open("./threads.json","r") as f:
            js = json.loads(f.read())
            js.update({pd["name"]:[]})
        with open("./threads.json","w") as f:
            json.dump(js,f)
        dat = {}
        dat.update({"conn":"suc"})
        with open("./threads.json","r") as f:
            dat.update({"thrs":json.load(f)[pd["name"]]})
        print(dat)
        s.send(json.dumps(dat).encode())
        users.append(pd["name"])
        clients.append(s)
        afterLogind(s,pd)
    elif "LOGL" in pd.keys():
        with open("./users.json","r") as f:
            js = json.loads(f.read())
            if dedo(pd["name"],js["logs"]):
                if dedo(pd["pass"],js["logs"],1):
                    dat = {}
                    dat.update({"conn":"suc"})
                    with open("./threads.json","r") as f:
                        dat.update({"thrs":json.load(f)[pd["name"]]})
                    print(dat)
                    s.send(json.dumps(dat).encode()) 
                    users.append(pd["name"])
                    clients.append(s)
                    afterLogind(s,pd)

while True:
    server.listen()
    s,b = server.accept()
    p = s.recv(4096).decode()
    pd = json.loads(p)
    x = threading.Thread(target=HandleLogin, args=(pd,s,))
    x.start()