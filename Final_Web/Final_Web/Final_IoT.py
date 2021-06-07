from flask import Flask, render_template, Response, request, redirect, url_for
from Data_Bridge import get_signal
import threading
import socket
import json
import re
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

app = Flask(__name__)
valueA = 1
valueB = 0

HOST = '192.168.137.1' 
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
    global currentRing,conn,addr,Lock,valueA,valueB
    try:
        # [TODO] write callback to deal with MQTT message from Lambda(done)
        print("Message received: " + str(message.payload))
        string = message.payload.decode("utf-8")
        if "desired" in string:
            substringA = string[35]
            substringB = string[50]
            s1 = substringA.encode("utf-8")
            s2 = substringB.encode("utf-8")
            print(s1)
            print(s2)
            valueA = int(s1)
            valueB = int(s2)
            
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
        # signal = get_signal()
        # print(signal)
        # if signal and clientsocket is not None:
        #     clientsocket.send()#send signal back to arduino
            # print("message sent to arduino")
        # [TODO] decode message from Arduino and send to AWS(done)
        data = clientsocket.recv(6)
        string = data.decode("utf-8")
        if (string != ""):
            print(string)
            distance = re.findall(r"[-+]?\d*\.\d+|\d+",string)
            #currentRing = lightness[1]
            print("received from arduino: "+distance[0])
            topic = "$aws/things/106000266/shadow/update"
            payload = '{"state":{"reported":{"distanceA1":'+ distance[0] +', "distanceB1": 2 }}}'
            myAWSIoTMQTTClient.publish(topic, payload, 0)
            pass

        # msg = "Open Gate"
        # clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

@app.route('/')
def index():
    if valueA == 0:
        return render_template('index.html', p1 = 'FULL', p2 = valueB)
    elif valueB == 0:
        return render_template('index.html', p1 = valueA, p2 = 'FULL')
    else:
        return render_template('index.html', p1 = valueA, p2 = valueB)

def main():
    global conn, addr
    try:
        # app.run(debug = True, host = '0.0.0.0', port = 16628)
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
