import sys
#sys.path.insert(0,"C:\\Users\\Andres\\Downloads\\pythonnet-master\\src\\runtime\\resources")
from PIL import ImageGrab, Image
from ctypes import windll
import time
import numpy as np
#import pythonnet
import clr
from System import String
clr.AddReference("System.Drawing")
from System.Drawing import Point
clr.AddReference("C:\\Users\\Andres\\Documents\\Aoe Machine learning\\Reskin Graphics\\pixelgetter.cs")
import pixelgetter

opencv (template matching, segmentierung), numpy array sind schnell weil C.

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
    
    bmp = windll.gdi32.Bitmap
    
    for i in range(0,yn, space):
        for j in range(0,xn, space):
            matrix[i][j] = windll.gdi32.GetPixel(windll.user32.GetDC(0), j, i)
            #matrix[i][j] = foto[j,i]
            #print(matrix[i][j])
    return matrix
    
def showRgbmatrix(matrix):
    img = Image.fromarray(matrix.astype('uint8'))
    img.show()
    
def getelementcoordinates(matrix):
    
    return
    
if __name__ == "__main__":
    #System.Threading.Thread.Sleep(5000);
    p = Point(5,5)
    print(p)
    print(sys.path)
    #sys.path.append('C:\\Users\\Andres\\Downloads\\pythonnet-master\\src\\runtime\\resources\\clr.py')
    for i in range (0,10):
        t0=time.perf_counter()

        # Take pic, get RGB
        foto = ImageGrab.grab().load()
        #matrix = getRgbmatrix(0, 0, 5, 5, foto, 1)

        #showRgbmatrix(matrix)
        
        # Detect elements in pixel coordinates
        #getelementcoordinates(matrix)
        
        t1 = time.perf_counter()
        dt = t1-t0
        print(dt)