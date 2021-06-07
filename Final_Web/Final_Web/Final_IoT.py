from flask import Flask, render_template, Response, request, redirect, url_for
import threading
import socket
import json
import re
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

app = Flask(__name__)
valueA = 2
valueB = 2

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

signal = True

def control_gate():
    global signal
    signal = not signal
    print(signal)

def mqttcallback(client, userdata, message):
    global currentRing,conn,addr,Lock,valueA,valueB
    try:
        # [TODO] write callback to deal with MQTT message from Lambda(done)
        print("Message received: " + str(message.payload))
        string = message.payload.decode("utf-8");
        if "desired" in string:
            substringA = string[29:30]
            substringB = string[39:40]
            s1 = substringA.encode("utf-8")
            s2 = substringB.encode("utf-8")
            print(s1)
            print(s2)
            valueA = int(s1)
            valueB = int(s2)
            
            #conn.send(s)
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
            distance = re.findall(r"[-+]?\d*\.\d+|\d+",string)
            #currentRing = lightness[1]
            print("received: "+distance[0])
            topic = "$aws/things/106000266/shadow/update"
            payload = '{"state":{"reported":{"distanceA1":'+ distance[0] +'}}}'
            
            myAWSIoTMQTTClient.publish(topic, payload, 0)
            pass
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

@app.route("/forward/", methods=['POST'])
def open_gate():
    control_gate()
    return render_template('control_gate.html')

def main():
    global conn, addr
    try:
        app.run(debug = True, host = '0.0.0.0', port = 16628)
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        t = threading.Thread(target=on_new_client,args=(conn,addr))
        t.daemon = True
        tSocket.append(t)
        tSocket[-1].start()
    except Exception as e:
        print(e)
        s.close()
        print("socket close")

if __name__ == '__main__':
    main()
