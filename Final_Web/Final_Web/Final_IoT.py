# from Data_Bridge import get_signal, give_value
from Data_Bridge import get_value
import threading
import socket
import json
import re
import os
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import sys

app = Flask(__name__)
@app.route('/_stuff', methods = ['GET'])
def stuff():
    global valueA
    return jsonify(result = valueA)

@app.route('/')
def index():
    return render_template('index.html', p2 = valueB)

@app.route("/forward/", methods=['POST'])
def open_gate():
    global signal
    signal = True
    # print("signal: %b", signal, file=sys.stderr)
    # print("Button pressed, diable LED")
    return render_template('index.html', p2 = valueB)

valueA = 1
valueB = 0
signal = False
car_is_in = False

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

            # conn.send(valueA)
            
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
    global currentRing, signal, car_is_in
    while True:
        print("signal: %b", signal, file=sys.stderr)
        if clientsocket is not None:
            if signal is False:
                print("inside enable")
                msg = 'enable' # parking space is ready to park, disable LED
            else:
                print("inside disable")
                msg = 'disable' # parking space can not be park now, enable LED

            clientsocket.send(msg.encode('utf-8'))#send signal back to arduino
        # [TODO] decode message from Arduino and send to AWS(done)
        data = clientsocket.recv(6)
        string = data.decode("utf-8")
        if (string != ""):
            print(string)
            distance = re.findall(r"[-+]?\d*\.\d+|\d+",string)
            if int(distance[0]) > 10 and car_is_in is True:
                signal = False
                car_is_in = False
            if int(distance[0]) < 10 and signal is True:
                car_is_in = True

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
conn, addr = s.accept()
print('connected by ' + str(addr))

def main():
    global conn, addr
    try:
        t = threading.Thread(target=on_new_client,args=(conn,addr))
        tSocket.append(t)
        tSocket[-1].start()
        print("running")
        app.run(debug = False, host = '0.0.0.0', port = 16628)
        
    except Exception as e:
        print(e)
        s.close()
        print("socket close")

if __name__ == '__main__':
    main()
