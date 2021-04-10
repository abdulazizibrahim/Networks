import socket
def make_frame(item):
    return [item[i:i+3] for i in range(0, len(item), 3)]
def sender_StopandWait():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 5678))
    s.listen(5)
    print("hello worrld")
    while True:
        canSend = True
        inp = input("do you want to send message Y/N")
        if inp == 'Y':
            clientsocket, address = s.accept();
            print(f" Connection from {address} has been established")
            #get data
            msg = input("enter message that you want send")
            msg = msg + "$"
            # make frame
            msg = make_frame(msg)
            #send frame
            for i in range(0, len(msg)):
                if(canSend == True):
                    clientsocket.send(bytes(msg[i], "utf-8"))
                    canSend = False
                    while True:
                        txt = clientsocket.recv(1024)
                        txt = txt.decode("utf-8")
                        if(len(txt) > 0):
                            #ack frame recieved
                            canSend = True
                            print(txt)
                            break
            #s.shutdown(socket.SHUT_RDWR)
            s.close()
        elif inp == 'N':
            break;
        else:
            print("wrong input try again")
            continue
sender_StopandWait()
