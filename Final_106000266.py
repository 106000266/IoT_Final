import threading
import socket
import json
import re
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

class Main_System:
    def __init__(self,data):
        self.parking_A = None
        self.parking_B = None
        self.data = data


HOST = '192.168.56.1' 
# [TODO] 166XX, XX is your tool box number(done)
PORT = 16628

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
tSocket=[]

# [HINT] currentRing stores the ring state
currentRing = None
# [HINT] Lock maintain the indentity of resource
Lock = threading.Lock()
# [HINT] variable for socket
conn, addr = None,None


def mqttcallback(client, userdata, message):
    global currentRing,conn,addr,Lock
    try:
        # [TODO] write callback to deal with MQTT message from Lambda(done)
        print("Message received: " + str(message.payload))
        string = message.payload.decode("utf-8");
        if "desired" in string:
            substring = string[23:33]
            s = substring.encode("utf-8")
            print(s)
            
            conn.send(s)
        #index = open("index.html").read().format(p1='', p2='')
    except Exception as e:
        print(e)


# [TODO] Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT(done)
ENDPOINT = "a2n8nzfjjzpdhv-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "b0e1f939f3a24ac9bfd952dc7c93ae4a"
PATH_TO_CERT = "./af56662380-certificate.pem.crt"
PATH_TO_KEY = "./af56662380-private.pem.key"
PATH_TO_ROOT = "./root_CA_1.txt"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
# [TODO] subscribe AWS topic(s)(done)
myAWSIoTMQTTClient.subscribe("$aws/things/106000266/shadow/update",1,mqttcallback)

def on_new_client(clientsocket,addr):
    global currentRing
    while True:
        # [TODO] decode message from Arduino and send to AWS(done)
        data = clientsocket.recv(6)
        string = data.decode("utf-8")
        if (string != ""):
            print(string)
            lightness = re.findall(r"[-+]?\d*\.\d+|\d+",string)
            #currentRing = lightness[1]
            print("received: "+lightness[0])
            topic = "$aws/things/106000266/shadow/update"
            payload = '{"state":{"reported":{"lightness":'+lightness[0]+'}}}'
            
            myAWSIoTMQTTClient.publish(topic, payload, 0)
            pass
    clientsocket.close()

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

def main():
    global conn, addr
    try:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        t = threading.Thread(target=on_new_client,args=(conn,addr))
        tSocket.append(t)
        tSocket[-1].start()
    except Exception as e:
        print(e)
        s.close()
        print("socket close")

if __name__ == '__main__':
    main()
