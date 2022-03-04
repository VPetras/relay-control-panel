#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
# rpi relay
# Title: idk
# Author: Vojtěch Petrásek 
# Generated: 18/1/2022 13:31:01
##################################################

###
# imports
###

from flask import Flask
from flask import render_template
from flask import request
import RPi.GPIO as GPIO
import sys
import time
import socket

###
# defines & settings
###

relays = {"1":[0,3],"2":[0,5],"3":[0,7],"4":[0,11],"5":[0,13],"6":[0,15],"test":[0,None]}

GPIO.setmode(GPIO.BOARD)

for relay in relays:
    if relay != "test":
        GPIO.setup(relays[relay][1], GPIO.OUT)

app = Flask(__name__)

###
# main
###

def main():
    while(True):
        GPIO.output(relay_1, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(relay_1, GPIO.LOW)
        time.sleep(1)

###
# routes
###


@app.route('/')
def home():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(ip, type(ip))
    return render_template('index.html', server_ip=ip)

@app.route('/relay_states', methods=['GET'])
def relay_states():
    global relays
    print(relays)
    return relays

@app.route('/relay_state/<id>', methods=['GET'])
def relay_state(id):
    global relays
    print(relays)
    return {"relay_id":id,"state":relays[id][0]}

@app.route('/relay_post/<id>', methods=['POST'])
def relay_post(id):
    global relays
    request_data = request.get_json()
    relays[id][0] = request_data["state"]
    print(id,relays[id])
    delay = 0.02
    if id != "test":
        if relays[id][0]:
            GPIO.output(relays[id][1], GPIO.HIGH)
        else:
            GPIO.output(relays[id][1], GPIO.LOW)
    else:
        while(relays[id][0]):
            for idr in range(len(relays)-1):
                print(idr)
                GPIO.output(relays[str(idr+1)][1], GPIO.HIGH)
                time.sleep(delay)
            for idr in range(len(relays)-1,0,-1):
                print(idr)
                GPIO.output(relays[str(idr)][1], GPIO.LOW)
                time.sleep(delay)

    print(relays)
    return {"relay_id":id,"state":relays[id][0]}

if __name__ == '__main__':
    try:
        app.run(host= '0.0.0.0',debug=True,port=8000) 
        #GPIO.cleanup()
    except Exception as e:
        GPIO.cleanup()
        print('Exited with error: {}'.format(e))
        #sys.exit(1)
    except KeyboardInterrupt:

        #GPIO.cleanup()
        sys.exit(1)