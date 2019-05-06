from PIL import Image, ImageDraw, ImageColor
import sys, os, subprocess, colorsys
import math

"""
home/paint.py
home/Folder A
home/Folder A/15002
home/Folder A/15002.slx
home/Folder A/15002_000.png
"""

talk = 1
lines = []
       
def getfolderslist():
    # Return a list with foldernames contained in actual directory
    # Also updates foldercontent.txt
    print("Getting Folder-List...")
    
    slxfolders = []
    os.system("dir /b >foldercontent.txt")
    f = open("foldercontent.txt", "r")
    string = f.read()
    lines = string.split("\n")
    slxfolders = []
    i=0
    for line in lines:
        if lines[i].find(".") == -1:
            slxfolders.append(line)
        i+=1
    slxfolders = slxfolders[:i-3]
    return slxfolders, i-3

def getbitmapnames(slxfolders, amount, gr_data_included = False, mode ="update"):
    # Gets all Bitmap filenames inside all Slxfolders as [['1.1.bmp', '1.2.bmp']['2.1.bmp', '2.2.bmp']]
    print("Getting Bitmap-List...")
    
    bitmaps = []
    gr_data = []
    for i in range (0,amount):
        if mode == "update":
            os.system("dir "+str(slxfolders[i])+" /b > bitmapcontent.txt")
        f = open("bitmapcontent.txt", "r")
        string = f.read()
        lines = string.split("\n")
        bitmapinfile = []
        gr_data_infile = []
        
        for line in lines:
            if (line.find('d') == -1) and (line != 0) and (line.find('.png')!=-1):
                bitmapinfile.append(line)
            elif (gr_data_included == True) and (line.find('d') != -1) and (line != 0) and (line.find('.png')!=-1):
                gr_data_infile.append(line)
                #print("d found")
                
        bitmaps.append(bitmapinfile)
        if gr_data_included == True:
            gr_data.append(gr_data_infile)
        
    return bitmaps, gr_data
    
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
    
def drawframewithcolor(id, color, mode="color", colorseed=0):
    img = Image.open(id).convert('RGB')
    draw = ImageDraw.Draw(img, mode = "RGB")
    
    if mode=="hueseed":
        color = hsv2rgb(colorseed,1,1)
        print(r,g,b)
    
    draw.rectangle([(0,0),img.size], fill = color)
    """
    pixels = img.load() # Create the pixel map
    for o in range(img.size[0]):    # For every pixel:
        for p in range(img.size[1]):
            pixels[o,p] = (o, p, 100) # Set the colour accordingly
    """
    # write to stdout
    img.save(id)
    #img.show()
    
def gatherslps(slxfolders):
    # Get the SLPS out of the SLX Folders
    for name in slxfolders:
        commandstring = "move "+name+"\\"+name+".slp ."
        os.system(commandstring)
    
def func_paintterrains(slxfolders, amount):
    # Get Bitmap-Filenames
    bitmapfiles = []
    bitmapfiles = getbitmapnames(slxfolders, amount)[:-1]
    
    # Loop through all found bitmaps and folders
    j=0
    while j < len(slxfolders):
        k=0
        while k < len(bitmapfiles[j]):
            print(k)
            id = slxfolders[j]+"/"+bitmapfiles[j][k]
            # print(id)
            
            #Generate Colorseed
            if j == 2 or j == 10 or j == 11: #Water
                color = (30,30,200)
            else:   #Land
                color = (30,200,20)
            
            # Open and Paint Bitmap
            drawframewithcolor(id, color)
            
            k+=1
        j+=1
    
def getwhitepixels(img):
    # Gets a picture and returns an array of white pixels [[x1,y1],[x2,y2]]
    size = img.size
    whitepixels = []
    for x in range (0, size[0]):
        for y in range (0,size[1]):
            r,g,b = img.getpixel((x,y))
            if(r==255) and (g==255) and (b==255):
                whitepixels.append((x,y))
    return whitepixels
    
def paintwhitezone_units():
    #Analyzes Data_graphics to find white parts, which are unit color (not background, shadows or color-player)
    #Then paint that zone of the graphics (.png) in a color code
    slxfolders, amount = getfolderslist()
    bitmapfiles, gr_data = getbitmapnames(slxfolders, amount, gr_data_included=True)
    
    whitepixels = []
    
    # Loop through all found bitmaps and folders
    j=0
    while j < len(slxfolders):
        k=0
        #print("Unit Nr.: %d" %j)
        while k < len(gr_data[j]):
        
            # Load Graphic Data, get size      
            gr_data_id = slxfolders[j]+"/"+gr_data[j][k]
            img = Image.open(gr_data_id).convert('RGB')
            
            # Search white Pixels in Graphic Data
            #print("Get white pixels from %s" %gr_data_id)
            whitepixels = getwhitepixels(img)
            
            # Color those Pixels in Graphics, with color code.
            graphic_id = slxfolders[j]+"/"+bitmapfiles[j][k]
            img2 = Image.open(graphic_id).convert('RGB')
            draw = ImageDraw.Draw(img, mode = "RGB")
            
            # Generate Color, Paint and save
            color = hsv2rgb(j,1,1)
            draw.point(whitepixels, color)
            img.save(graphic_id)
            
            #print("Paint them in %s with color:" %graphic_id)
            #print(color)
            k+=1
        print("%d from %d" %(j,len(slxfolders)))
        
        j+=1
    
if __name__ == "__main__":
    #paintwhitezone_units()
    
    img = Image.open("1048_025d.png").convert('RGB')
    draw = ImageDraw.Draw(img, mode = "RGB")
    color = hsv2rgb(120,1,1)
    array = getwhitepixels(img)
    draw.point(array, color)
    img.save("1048_025.png")
    print(array)
    print(img.size)
    
    img2 = Image.open("1048_025.png").convert('RGB')
    print(img2.size)
    