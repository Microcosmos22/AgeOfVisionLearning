"""
@file morph_lines_detection.py
@brief Use morphology transformations for extracting horizontal and vertical lines sample code
"""
import numpy as np
import sys
import cv2 as cv
np.set_printoptions(threshold=sys.maxsize)

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)
    
def imagetogray(src):
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    
    #show_wait_destroy("binary", gray)
    return gray
        
def imagetobinary(src, show = 0):
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
        
    # Apply Threshold to get binary
    bw, binary = cv.threshold(gray, 225, 255, cv.THRESH_BINARY)
    
    if show == 1:
        show_wait_destroy("gray", gray)
        show_wait_destroy("binary", binary)
    
    return binary
    
def check_upperleft(i, j, binary):
    whitepixel = True
    
    for di in range (0, 10):
        if binary[i+di][j] == 0: #unten
            whitepixel = False
            
    for dj in range (0, 10):
        if binary[i][j+dj] == 0: #rechts
            whitepixel = False
            
    return whitepixel
    
def check_upperright(i, j, binary):
    whitepixel = True
    
    for di in range (0, 10):
        if binary[i+di][j] == 0: #unten
            whitepixel = False
            
    for dj in range (0, 10):
        if binary[i][j-dj] == 0: #rechts
            whitepixel = False
            
    return whitepixel
    
def check_bottomleft(i, j, binary):
    whitepixel = True
    
    for di in range (0, 10):
        if binary[i-di][j] == 0: #oben
            whitepixel = False
            
    for dj in range (0, 10):
        if binary[i][j+dj] == 0: #rechts
            whitepixel = False
            
    return whitepixel
    
def check_bottomright(i, j, binary):
    whitepixel = True
    
    for di in range (0, 10):
        if binary[i-di][j] == 0: #oben
            whitepixel = False
            
    for dj in range (0, 10):
        if binary[i][j-dj] == 0: #links
            whitepixel = False
            
    return whitepixel
    
def getscreenposition(minimap_img):
    """
    Get screen position (center of rectangle) in pixel coordinates relative 
    to the upper-left corner of the Minimap-Cut
    """
    xradius = 29.5
    yradius = 14
    
    cornertype, x, y = getcorners(minimap_img)
    screenpos = (0,0)
    print(x,y)
    
    if cornertype == "upperleft":
        print("UL Detected")
        screenpos = (x+xradius, y+yradius)
    elif cornertype == "upperright":
        print("UR Detected")
        screenpos = (x-xradius, y+yradius)
    elif cornertype == "bottomleft":
        print("BL Detected")
        screenpos = (x+xradius, y-yradius)
    elif cornertype == "bottomright":
        print("BR Detected")
        screenpos = (x-xradius, y-yradius)
    
    return screenpos
    
def getcorners(img):
    """
    Finds any corner of the screen rectangle in the minimap and return as
    ("which corner" pixel-x, pixel-y)
    """
    # Convert to grayscale
    binary = imagetobinary(img, 0)
    counti = 0
    countj = 0
    foundcorner = ("none", 0,0)
    
    for j in range (0, binary.shape[0]):
        for i in range (0, binary.shape[1]):
            if binary[j][i] == 255 and j>10 and j<154 and i>10 and i<316:
            
                if(check_upperleft(j,i, binary) == True):
                    foundcorner = ("upperleft",i,j)
                    return foundcorner
                elif(check_upperright(j,i, binary) == True):
                    foundcorner = ("upperright",i,j)
                    return foundcorner
                elif(check_bottomleft(j,i, binary) == True):
                    foundcorner = ("bottomleft",i,j)
                    return foundcorner
                elif(check_bottomright(j,i, binary) == True):
                    foundcorner = ("bottomright",i,j)
                    return foundcorner
            """
                if(check_upperleft(j, i, binary) == True):
                    foundcorner = ("upperleft",i,j)
                elif()
            """
    #print(foundcorner)
    
def getminimapscreen(src):
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image: ' + argv[0])
        return -1
        
    bw = imagetobinary(src)
    
    # Show binary image
    #show_wait_destroy("binary", bw)
    
    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)
    
    # Create structure element for extracting lines
    cols = horizontal.shape[1]
    horizontal_size = cols/5
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (int(horizontal_size), 1))
    
    rows = vertical.shape[0]
    verticalsize = rows/5
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, int(verticalsize)))
    
    # Apply morphology operations
    horizontal = cv.erode(horizontal, horizontalStructure)
    print("Output:")
    #print(horizontal)
    horizontal = cv.dilate(horizontal, horizontalStructure)
    
    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)
    #print(vertical)
    # Show extracted horizontal lines
    show_wait_destroy("horizontal", horizontal)
    show_wait_destroy("vertical", vertical)
    
    
    # Inverse vertical image
    vertical = cv.bitwise_not(vertical)
    #show_wait_destroy("vertical_bit", vertical)
    '''
    Extract edges and smooth image according to the logic
    1. extract edges
    2. dilate(edges)
    3. src.copyTo(smooth)
    4. blur smooth img
    5. smooth.copyTo(src, edges)
    '''
    # Step 1
    edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 3, -2)
    #show_wait_destroy("edges", edges)
    # Step 2
    kernel = np.ones((2, 2), np.uint8)
    edges = cv.dilate(edges, kernel)
    #show_wait_destroy("dilate", edges)
    # Step 3
    smooth = np.copy(vertical)
    # Step 4
    smooth = cv.blur(smooth, (2, 2))
    # Step 5
    (rows, cols) = np.where(edges != 0)
    vertical[rows, cols] = smooth[rows, cols]
    # Show final result
    #show_wait_destroy("smooth - final", vertical)
    # [smooth]
    
    """______________________________________________________
    Find Coordinates of Rectangle:
    """
    rectangle = []
    count=0
    #print(len(rows), len(cols))
    for i in range (0, horizontal.shape[0]):
        for j in range (0, horizontal.shape[1]):
            rectangle.append((j,i))
            if horizontal[i][j] == 0:
                print (j, i)
                print(horizontal[i][j])
                if count == 0:
                    upperleft = (j,i)
                    #print("count: %d" %count)
                    count = count+1
                    break
                
    
    i = horizontal.shape[0] - 1
    j = horizontal.shape[1] - 1
    count = 0
    #print(len(horizontal))
    
    while i >= 0:
        j = horizontal.shape[1] - 1
        while j >= 0:
            #print (j,i)
            if horizontal[i][j] == 0 and count==0:
                downright = (j,i)
                #print("count: %d" %count)
                count = count+1
                break
            j = j-1
        i = i-1
    
    print(downright)
    print(upperleft)
    #print(rectangle)
    
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])