import socket
import time
import sys

def sendFrames(frames):
    print("welcome to Selective ARQ Server Side");
    print("Frames: ",frames)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 20155

    dest = (socket.gethostname(), port)   # ip and port
    try:
        s.bind((socket.gethostname(), port))
       # print ("socket binded to %s" %(port))
    except(socket.error ):
        print("\n\n**** Please! Change the port number and run again. *****\n\n")
        exit()
    s.listen(5)

    try:
        c,addr = s.accept()
        print("client conneted at ip",addr[0]+" port: "+str(addr[1])+"\n\n")
    except Exception as e:
        print(str(e))
        s.close()
        sys.exit(0)
     # print( 'Connected to: ', addr )


    f = 0
    totalFrames = len(frames)
    s.settimeout(0.05)
    global window
    Sw = 3
    Sn = 0
    Sf = 0
    ackNo = 0
    window[1][:] = frames[0:Sw]
    next1 = Sw
    while True:

        try:
            c.send(bytes(window[1][0]+'|'+str(ackNo),"utf-8"))
            window[0].append(window[1].pop(0))
            print("\nSent frame :{} but no ack ----> ".format(str(ackNo)),window)
            Sn += 1
            time.sleep(.3)

            startTime = time.time()
            stopTime = 0
            ack = c.recv(20).decode('utf-8')
            ackNo = int(ack[-1])      #  this is the golden line
            if 'Timeout' in ack:
                print("timeout")
                continue
            if 'end' in ack:
                window[0].pop(0)
                print("Received posACK :"+str(ackNo)," ---> ",ack)

                break
            if "negACK" in ack:       # if ack is not received
                print("\n\n *** negative ack ***\n\n")
                time.sleep(5)
            if(ackNo>=Sf and ackNo<=Sn):
                if  "posACK" in ack:
                    print("Received posACK :"+str(ackNo)," ---> ",ack)
                    while(Sf<=ackNo):
                        window[0].pop(0)
                        if (next1 < totalFrames):
                            window[1].append(frames[next1])
                            next1+=1
                        Sf += 1
                    ackNo+=1
            stopTime = time.time()
            timeout = stopTime - startTime
            # print("Timeout: ",timeout)

        except socket.timeout:
            c.send(bytes(window[1][0]+'|'+str(ackNo),"utf-8"))
        except Exception as e:
            print(str(e))
            s.close()
            exit(0)
        except KeyboardInterrupt as e:

            print("\n\t*** Server Closed ***\n\n")
            exit(0)
        except ConnectionResetError as e:
            print("\n\t*** Connection closed by the server. ***\n")
            s.close()
            exit(0)

frameSize = 1
window = [[],[]]     ## 1st [] for sent and ack, 2nd for sent but not ack

def getData():
    return str(input("Enter your data: "))


def makeFrames(data):
    frames = []
    if len(data) > frameSize:
        for i in range(0,len(data),frameSize):
            frame = data[i:i+frameSize]
            frames.append(frame)
    else:
        frames.append(data)
    frames.append('}^{')
    return frames

def selective():

    flag = True
    event = False    ## do not send
    new = ''
    while(flag):
        request = str(input("\n\nDo you want to send {}data(y/n): ".format(new)))



        if(request == 'y'):
            data = getData()
            frames = makeFrames(data)
            sendFrames(frames)
            new = "new "




        elif (request == 'n'):
            flag = False
        else:
            print("Don't be software tester, just type 'y' or 'n'")

    print("connection closed!")

# sendFrames(["hello","world",''])
if __name__ == "__main__":
    selective()
