import socket
import threading
import time
import getpass
import json
import msvcrt
import os
import sys
from datetime import datetime as dt
c = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
c.connect((input("address:"),int(input("port:"))))
fuj = ""
while True:
    ## Login
    dat = {}
    da1 = []
    type = input("L-login,R-register:").upper()
    name = input("Username:")
    passw = getpass.getpass()        
    da1.append(type)
    da1.append(name)
    da1.append(passw)
    dat.update({"type":"USER"})
    dat.update({"info":da1})
    c.send(json.dumps(dat).encode())
    err = json.loads(c.recv(4096).decode())["err"]
    print(err)
    if err == "succ":
        while True:
            ## LOAD THREADS
            c.send(json.dumps({"type":"FTHR","info":name}).encode())
            os.system("cls")
            for x in json.loads(c.recv(4096).decode())["thrs"]:
                print(x)
            ## Enter Thread / Create Thread
            mode = input("na četovanie v konverzácií napíšte meno konverzácie (musí byť presne) alebo pre vytvorenie novej konverzácie napíšte 'n'")
            if not mode == "n":
                namethr = mode
                dat = {"type":"FMSGS","info":namethr}
                c.send(json.dumps(dat).encode())
                os.system("cls")
                recv = c.recv(4096).decode()
                print(recv)
                for x in json.loads(recv)["msgs"]:
                    print(x["author"] + ": " + x["text"] + " @ " + str(dt.fromtimestamp(x["timestamp"])))
                while True:
                    ## Sending Messages
                    try:
                        dedo = msvcrt.getch()
                        if dedo != "\r" and ord(dedo.decode()) != 8 and ord(dedo.decode()) != 13:
                            fuj+=dedo.decode()
                        elif ord(dedo.decode()) == 8:
                            fuj = fuj.rstrip(fuj[-1])
                        else:
                            c.send(json.dumps({"type":"nmsg","info":[fuj,namethr,name]}).encode())
                            fuj = ""
                        ## Recieving Messages
                        os.system("cls")
                        c.send(json.dumps({"type":"FMSGS","info":namethr}).encode())
                        for x in json.loads(c.recv(4096).decode())["msgs"]:
                            print(x["author"] + ": " + x["text"] + " @ " + str(dt.fromtimestamp(x["timestamp"])))
                        print(fuj)
                    except Exception as e:
                        print("Exception",e)
            else:
                namethr = input("Napíšte meno novej konverzácie:")
                c.send(json.dumps({"type":"nthr","info":[name,namethr]}).encode())