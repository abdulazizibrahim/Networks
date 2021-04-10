#  Import so/cket module 
import socket      
import time, sys   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     

port = 20155  

dest = (socket.gethostname(), port)   # ip and port
try:      
    s.connect((socket.gethostname(), port))
except socket.error:
    print("\n\n*** Conection Refused! Check server or port ***\n") 
    exit(0)


frameSize = 5
fulldata = ''
ack = 0      # Rn
def receiver():
    s.settimeout(0.05)
    data = ""
    try:
        global ack,fulldata
        time.sleep(1)
        data = s.recv(frameSize).decode('utf-8')
        
        n = len(data)-1
        while(n>0):
            if (data[n] == '|'):break
            n-=1
        
        print("Recieved frame :{}".format(data[n+1:]))
        time.sleep(1)
        if '}^{' in data:
            send_ack = "end"+str(ack) 
            s.send(bytes(send_ack,'utf-8'))
            print("\tend ack :{}".format(str(ack)))
            return False
        if (int(data[n+1:]) == ack):
            send_ack = "posACK"+ str(ack)
            s.send(bytes(send_ack,'utf-8'))
            print("\tsent ack :{}".format(str(ack)))
            ack+=1
        else:
            send_ack = "negACK"+ str(ack)
            s.send(bytes(send_ack,'utf-8'))
            print("\tsent neg ack :{}".format(str(ack)))
            
    except socket.timeout:
        send_ack = "Timeout"
        s.send(bytes(send_ack,'utf-8'))
    except Exception as e:
        print(str(e))
        s.close()
        exit(0)
    except KeyboardInterrupt as e:
        print("connection closed")
        s.close()
        exit(0)
    print('\t'+data+'],\n')
    fulldata += data[:n]
    return True

if __name__ == "__main__":
    
    print("\n\nFRAMES: ",end='')
    while True:
        print('[',end='')
        if not (receiver()):break
        print('\t',end='')
    s.close()
    print(']')
    print("\nComplete data: '"+fulldata+"'\n")