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
            time.sleep(0.1)
            img = cam.getImage() #gets image from the camera
            #print img.readText()

            barcode = img.findBarcode() #finds barcode data from image
            if self.scan == True and barcode != None:
                #if there is some data processed
                #os.system('aplay accept.wav')
                #os.system('aplay hokkiengreeting.wav')
                barcode = barcode[0]
                result = str(barcode.data)

                print(result)
                if result[:8] == 'https://' and audio.get_state() != vlc.State.Playing:
                    print("HTTP RESULT", result)
                    #audio = vlc.MediaPlayer(result)
                    #audio.play()
                    #vlc isn't playing audio through headphone jack
                    #have to force using omxplayer instead
                    os.system('omxplayer -o local %s' % result)
                    
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
