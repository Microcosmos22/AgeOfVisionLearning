import sys
#sys.path.insert(0,"C:\\Users\\Andres\\Downloads\\pythonnet-master\\src\\runtime\\resources")
from PIL import ImageGrab, Image
from ctypes import windll
import time
import numpy as np
import mss
import numpy
import cv2, math
from PIL import Image, ImageDraw, ImageColor
from findlines import getminimapscreen

"""
Minimap Coordinates:

"""

#opencv (template matching, segmentierung), numpy array sind schnell weil C.
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss.mss()

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def getRgbmatrix(x0, y0, xn, yn, foto, space):
    matrix = np.array([[[0 for rgb in range(3)] for x in range(x0, xn)] for y in range(y0, yn)])
    
    #bmp = windll.gdi32.Bitmap
    
    for i in range(0,yn, space):
        for j in range(0,xn, space):
            matrix[i][j] = windll.gdi32.GetPixel(windll.user32.GetDC(0), j, i)
            #matrix[i][j] = foto[j,i]
            #print(matrix[i][j])
    return matrix
    
def showRgbmatrix(matrix):
    img = Image.fromarray(matrix.astype('uint8'))
    img.show()
    
def savepicturefromarray(pic):
    output = "monitor-{}.png"
    pic.save(output)
    
def getscreenasarray(monitor):
    # Get part of the screen defined in "monitor" and return as numpy array.
    im = numpy.asarray(sct.grab(monitor))
    return im

def getscreenaspic(monitor):
    # Get part of the screen defined in "monitor" and return as numpy array.
    im = sct.grab(monitor)
    return im
    
def paint_minimap_background(img):
    # Paints the background of the minimap to simplify Shape detection
    draw = ImageDraw.Draw(img, mode = "RGB")
    color = hsv2rgb(0,0,0)
    draw.polygon([(0,0),(0,80),(161,0)], fill = color, outline = color)
    draw.polygon([(0,83),(0,163),(161,163)], fill = color, outline = color)
    draw.polygon([(165,0),(325,0),(326,80)], fill = color, outline = color)
    draw.polygon([(326,83),(164,163),(325,163)], fill = color, outline = color)
    
    return img
    
if __name__ == "__main__":
    img = Image.open("Screenreader/test.jpg").convert('RGB')
    #img = paint_minimap_background(img)
    img_opencv = numpy.array(img)
    img_opencv = img_opencv[:, :, ::-1].copy() 
    getminimapscreen(img_opencv)
    """_______________________________________________
    #System.Threading.Thread.Sleep(5000);
    #p = Point(5,5)
    #print(p)
    #print(sys.path)
    #sys.path.append('C:\\Users\\Andres\\Downloads\\pythonnet-master\\src\\runtime\\resources\\clr.py')
    for i in range (0,10):
        t0=time.perf_counter()
        
        array = getscreenasarray(monitor)
        
        #savepicturefromarray(array)
        # The simplest use, save a screen shot of the 1st monitor
       
        # Take pic, get RGB
        #foto = ImageGrab.grab()#.load()
        #print(foto)
        #matrix = getRgbmatrix(0, 0, 5, 5, foto, 1)

        #showRgbmatrix(matrix)
        
        # Detect elements in pixel coordinates
        #getelementcoordinates(matrix)
        
        t1 = time.perf_counter()
        dt = t1-t0
        print(dt)
        #time.sleep(5)
    sct.close()
    """