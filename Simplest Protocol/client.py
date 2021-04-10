import socket

def recv_Simplest():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5678))
    data = ""
    while True:
        msg = s.recv(1024)
        msg = msg.decode("utf-8")
        data = data + msg
        if msg[len(msg)-1] == '$':
            print(data[:len(data)-1])
            break

    s.close()
recv_Simplest()
