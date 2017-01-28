import math
import requests
import urllib
import time
import os
from PIL import Image

bridgeUp = 0
maintenanceCheck = 0
colorblindness = 0

while bridgeUp == 0:

    # Download Image
    jpg = urllib.request.urlretrieve('http://www.seattle.gov/trafficcams/images/Westlake_Dexter.jpg', 'Westlake_Dexter.jpg')[0]

    # Load Image
    im = Image.open(jpg)
    pix = im.load()

    # Check if camera feed is available
    if len(im.crop((0,0,20,20)).getcolors(im.size[0]*im.size[1])) == 1:
        if maintenanceCheck == 0:
            os.system('say "Camera is under maintenance"')
            print("Camera Under Maintenance")
            maintenanceCheck = 1
        time.sleep(60)
        continue
    else:
        if maintenanceCheck == 1:
            os.system('say "I can see again"')
            print("Camera Restored")
            maintenanceCheck = 0

    # Create list of all colors w/counts in image
    redLightColors = im.crop((343,220,355,226)).getcolors(im.size[0]*im.size[1])
    greenLightColors = im.crop((356,220,368,226)).getcolors(im.size[0]*im.size[1])


    # Function to calculate average color
    def avgColor(colors):
        r=g=b=denom=0
        for i,j in colors:
            r += i*j[0]
            g += i*j[1]
            b += i*j[2]
            denom += i
        return (r/denom,g/denom,b/denom)

    # Function for distance between two RGB colors
    def distance(c1, c2):
        (r1,g1,b1) = c1
        (r2,g2,b2) = c2
        return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

    # Define Black/Red/Green RGB values
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)

    # Test image color
    if distance(avgColor(greenLightColors),green) < distance(avgColor(greenLightColors),black) and distance(avgColor(redLightColors),black) < distance(avgColor(redLightColors),red):
        # os.system('say "Bridge is down"')
        colorblindness = 0
        print("Bridge is down")
    elif distance(avgColor(redLightColors),red) < distance(avgColor(redLightColors),black) and distance(avgColor(greenLightColors),black) < distance(avgColor(greenLightColors),green):
        colorblindness = 0
        os.system('say "Bridge is up"')
        print("Bridge is up")
        bridgeUp = 1
    else:
        if colorblindness == 0:
            os.system('say "I am experiencing a temporary episode of colorblindness"')
            print("I am experiencing a temporary episode of colorblindness")

            # Following section of code for debugging
            print("Red Light: " + str(avgColor(redLightColors)))
            print("Dist RL to Red: " + str(distance(avgColor(redLightColors),red)))
            print("Dist RL to Black: " + str(distance(avgColor(redLightColors),black)))
            print("Green Light: " + str(avgColor(greenLightColors)))
            print("Dist GL to Green: " + str(distance(avgColor(greenLightColors),red)))
            print("Dist GL to Black: " + str(distance(avgColor(greenLightColors),black)))

            colorblindness = 1

    time.sleep(60)
