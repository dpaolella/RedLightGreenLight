import math
from PIL import Image

# Load Image
im = Image.open("trafficCam.jpg") #Can be many different formats.
pix = im.load()

# Create list of all colors w/counts in image
# Choose a subset of pixels around light location with which to determine dominant color
colors = im.crop((185,230,215,260)).getcolors(im.size[0]*im.size[1])

# Calculate average color
r=g=b=denom=0
for i,j in colors:
    r += i*j[0]
    g += i*j[1]
    b += i*j[2]
    denom += i
c = (r/denom,g/denom,b/denom)

# Function for distance between two RGB colors
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

# Define Red/Green RGB values
red = (255,0,0)
green = (0,255,0)

# Test image color
if distance(c,red) > distance(c,green):
    print("Bridge is down")
elif distance(c,red) < distance(c,green):
    print("Bridge is up")
else:
    print("I am experiencing a temporary episode of colorblindness")
