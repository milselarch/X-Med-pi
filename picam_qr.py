import os
from SimpleCV import Color,Camera,Display

def scan():
    cam = Camera()  #starts the camera
    display = Display()

    while display.isNotDone():
        img = cam.getImage() #gets image from the camera

        barcode = img.findBarcode() #finds barcode data from image
        if (barcode is not None): #if there is some data processed
            os.system('aplay accept.wav')
            os.system('aplay hokkiengreeting.wav')
            barcode = barcode[0]
            result = str(barcode.data)
            gold = os.system('aplay %s' % result)
            gold = 1 
            barcode = [] #reset barcode data to empty set

        img.save(display) #shows the image on the screen
