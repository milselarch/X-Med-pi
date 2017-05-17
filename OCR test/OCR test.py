from PIL import Image
from pytesser import *

from SimpleCV import Color,Camera,Display
import vlc
 
image_file = '2017-03-27.png'
im = Image.open(image_file)
text = image_to_string(im)
text = image_file_to_string(image_file)
text = image_file_to_string(image_file, graceful_errors=True)
print "=====output=======\n"
print text


import sys, os
import Queue
import threading
import time

from SimpleCV import Color,Camera,Display
import vlc

class scanner(threading.Thread):
    def __init__(self):
        self.display = Display()
        self.camera = Camera()
        self.queue = Queue.Queue()
        self.scan = False
        
        threading.Thread.__init__(self)

    def put(self):
        self.queue.put(True)
        
    def run(self):
        display = self.display
        cam = self.camera
        #prevBarcode = None
        audio = vlc.MediaPlayer('')
        
        while display.isNotDone():
            img = cam.getImage() #gets image from the camera
            print img.readText()


            barcode = img.findBarcode() #finds barcode data from image
            if self.scan == True and barcode != None:
                #if there is some data processed
                os.system('aplay accept.wav')
                os.system('aplay hokkiengreeting.wav')
                barcode = barcode[0]
                result = str(barcode.data)

                if result[:8] == 'https://' and audio.get_state() != vlc.State.Playing:
                    audio = vlc.MediaPlayer(result)
                    audio.play()
                else:
                    gold = os.system('aplay %s' % result)
                    gold = 1
                    
                barcode = [] #reset barcode data to empty set
                self.scan = False
                #cam.close()

            else:
                try:
                    self.queue.get(block=False)
                    self.scan = True
                except Queue.Empty:
                    pass

            img.save(display) #shows the image on the screen

        #prevBarcode = barcode
    
if __name__ == '__main__':
    scanner().start()
