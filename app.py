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

###
# defines & settings
###

relay_1 = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_1, GPIO.OUT)

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


relays = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/relay_states', methods=['GET'])
def relay_states():
    global relays
    print(relays)
    return relays

@app.route('/relay_state/<id>', methods=['GET'])
def relay_state(id):
    global relays
    print(relays)
    return {"relay_id":id,"state":relays[id]}

@app.route('/relay_post/<id>', methods=['POST'])
def relay_post(id):
    global relays
    request_data = request.get_json()
    relays[id] = request_data["state"]
    print(id,relays[id])
    if relays[id]:
        GPIO.output(relay_1, GPIO.HIGH)
    else:
        GPIO.output(relay_1, GPIO.LOW)
    print(relays)
    return {"relay_id":id,"state":relays[id]}

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