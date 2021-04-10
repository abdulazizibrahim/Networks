import socket
import time
def make_frame(item):
    return [item[i:i+3] for i in range(0, len(item), 3)]
def sender_Simplest():
    sn = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 5678))
    s.listen(5)
    print("hello worrld")
    while True:
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
                clientsocket.send(bytes(msg[i] + str(sn), "utf-8"))
                copy = msg[i] + str(sn)
                print(copy)
                timer = 0
                while timer <=10:
                    time.sleep(1)
                    txt = clientsocket.recv(1024)
                    txt = txt.decode("utf-8")
                    if(int(txt) == sn + 1):
                        #ack frame recieve
                        if(sn == 9):
                            sn = 0
                        else:
                            sn = sn + 1
                        print(txt)
                        break
                    if(timer == 10):
                        clientsocket.send(bytes(copy, "utf-8"))
                        timer = 0
                    timer = timer + 1

            #s.shutdown(socket.SHUT_RDWR)
            s.close()
        elif inp == 'N':
            break;
        else:
            print("wrong input try again")
            continue
sender_Simplest()
