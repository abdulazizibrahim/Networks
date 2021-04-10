import socket

def recv_Simplest():
    rn = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5678))
    data = ""
    while True:
        msg = s.recv(1024)
        msg = msg.decode("utf-8")
        sn = int(msg[len(msg) -1])
        print(msg)
        if(sn == rn):
            if(rn == 9):
                rn = 0
            else:
                rn = rn + 1
            print(rn)
            s.send(bytes(str(rn), "utf-8"))
        data = data + msg[:len(msg) -1]
        if msg[len(msg)-2] == '$':
            print(data[:len(data)-1])
            break

    s.close()
recv_Simplest()
