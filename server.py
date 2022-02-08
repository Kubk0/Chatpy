import socket
import threading
import time
import json
from datetime import datetime as dt
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()),50))
def main(s):
    while True:
        data = json.loads(s.recv(4096).decode())
        type = data["type"]
        info = data["info"]
        if type == "USER":
            fail = "succ"
            ## LOGIN
            if info[0] == "L":
                with open("./user.json","r") as f:
                    dat = json.load(f)
                    if not info[1] in dat["logs"].keys():
                        fail = "fail"
                        print(info[1],dat["logs"].keys())
                    else:
                        if not info[2] == dat["logs"][info[1]]:
                            fail = "fail"
                            print(info[2],dat["logs"][info[1]])
            ## REGISTER
            elif info[0] == "R":
                ## json getting
                with open("./user.json","r") as f:
                    dat = json.load(f)
                    if not info[1] in dat["logs"].keys():
                        dat["logs"].update({info[1]:info[2]})
                    else:
                        fail = "fail"
                with open("./user.json","w") as f:
                    json.dump(dat,f)
                ## adding thread list
                with open("./threads.json","r") as f:
                    dat = json.load(f)
                    dat.update({info[1]:[]})
                with open("./threads.json","w") as f:
                    json.dump(dat,f)
            s.send(json.dumps({"err":fail}).encode())
        elif type == "FTHR":
            with open("./threads.json") as f:
                s.send(json.dumps({"thrs":json.load(f)[info]}).encode())
        elif type == "FMSGS":
            with open("./messages.json") as f:
                data = json.load(f)
            s.send(json.dumps({"msgs":data[info]}).encode())
            print("sending")
        elif type == "nmsg":
            if not info[0].startswith("!"):
                with open("./messages.json") as f:
                    data = json.load(f)
                with open("./messages.json","w") as f:
                    data[info[1]].append({"text":info[0],"timestamp":int(time.time()),"author":info[2]})
                    json.dump(data,f)
            elif info[0].startswith("!adduser"):
                name = info[0][9:]
                with open("./threads.json") as f:
                    data = json.load(f)
                with open("./threads.json","w") as f:
                    data[name].append(info[1])
                    json.dump(data,f)
            elif info[0].startswith("!listusers"):
                lol = []
                with open("./threads.json") as f:
                    data = json.load(f)
                for x in data:
                    if info[1] in data[x]:
                        lol.append(x)
                    else:
                        print(info[1],x,data[x])
                with open("./messages.json") as f:
                    data = json.load(f)
                with open("./messages.json","w") as f:
                    data[info[1]].append({"text":str(lol),"timestamp":int(time.time()),"author":"SYSTEM"})
                    json.dump(data,f)
        elif type == "nthr":
            with open("./threads.json") as f:
                data = json.load(f)
            with open("./threads.json","w") as f:
                data[info[0]].append(info[1])
                json.dump(data,f)
            with open("./messages.json") as f:
                data = json.load(f)
            with open("./messages.json","w") as f:
                data.update({info[1]:[]})
                json.dump(data,f)
while True:
    server.listen()
    s,b = server.accept()
    x = threading.Thread(target=main, args=(s,))
    x.start()