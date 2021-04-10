import socket
def make_frame(item):
    return [item[i:i+3] for i in range(0, len(item), 3)]
def sender_Simplest():
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
                clientsocket.send(bytes(msg[i], "utf-8"))
            #s.shutdown(socket.SHUT_RDWR)
            s.close()
        elif inp == 'N':
            break;
        else:
            print("wrong input try again")
            continue
sender_Simplest()
