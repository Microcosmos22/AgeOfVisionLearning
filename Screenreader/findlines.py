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
    
def getminimapscreen(src):
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image: ' + argv[0])
        return -1
    #cv.imshow("src", src)
    print(type(src))
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    print("Src image:")
    print(gray)
    
    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 100, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 15, -2)
    
    # Show binary image
    #show_wait_destroy("binary", bw)
    
    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)
    
    # Create structure element for extracting lines
    cols = horizontal.shape[1]
    horizontal_size = 1
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (int(horizontal_size), 1))
    
    rows = vertical.shape[0]
    verticalsize = 1
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
    #show_wait_destroy("horizontal", horizontal)
    #show_wait_destroy("vertical", vertical)
    
    
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
    print(type(len(rows)))
    rectangle = []
    for i in range (0,len(rows)-1):
        for j in range (0, len(cols)-1):
            print (i,j)
            if horizontal[i][j] == 0:
                rectangle.append[(i,j)]
                
    print(rectangle)
    print(horizontal[4][3])
    
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])