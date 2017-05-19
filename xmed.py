from flask import Flask
from flask_ask import Ask, statement, convert_errors, audio

from SimpleCV import Color,Camera,Display

import RPi.GPIO as GPIO
import logging
import picam_qr
import thread

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

#logging.getLogger("flask_ask").setLevel(logging.DEBUG)
scanner = picam_qr.scanner()

@ask.intent("scanIntent")
def gpio_control(*args):
    #stream_url = '%s' % result
    #thread.start_new_thread(picam_qr.scan, (cam, display))
    scanner.put()
    return statement('Scanning')

if __name__ == '__main__':
    scanner.start()
    
    port = 5000 #the custom port you want
    app.run(host='0.0.0.0', port=port)
    
