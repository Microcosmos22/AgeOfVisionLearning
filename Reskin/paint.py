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


class SLPGroups:
    trees = [1250,1251,1253,1254,1255,1256,1257,1258,1259,1260,1261,1262,1263,1264,1265,1266,1267,1268,1269,1270,1271,1272,1273,2533,435,2308,1252]
    stone = [1034,4482]
    gold = [2561,4479]
    villager = [1382,1385,1388,1392,1398,1405,1421,1424,1434,3841, 2592, 3483,1431,1427, 3682,3677,3681,3574,1479,1493,2586,1525,1542,1558,1493,1509,3684,1560,1563,1552,3568,1388,1401,2571,1427,1440,1453,1880,1879,1401,1414,1453,2218,3679]
    militia = [987,990,993,997]
    menatarms = [1038,1041,1044,1045,1048]
    archer = [2,5,8,9,12]
    crossbow = [186,189,192,193,196]
    barracks = [133,131,132,130]
    miningcamp = [3495,3493,3494,3492]
    house = [2235,2233,2234,2232,2223]
    lumber = [3507,3505,3506,3504]
    archrange = [24,22,23,21]
    mill = [733,737,741,735,739,732,736,740,730,734,738]
    tc = [889,891,3594,3595,3596,4610,4611,4612]
    pikemen = [873,867,873,877]
    scout = [2079,2085,2089]
    sheepalive = [3629,3634]
    boar = [2555,2556,2557,2558,2559,3577]
    #blacksmith = []
    slpgroup = []
    slpgroup.append(trees)
    slpgroup.append(stone)
    slpgroup.append(gold)
    slpgroup.append(villager)
    slpgroup.append(militia)
    slpgroup.append(menatarms)
    slpgroup.append(archer)
    slpgroup.append(crossbow)
    slpgroup.append(barracks)
    slpgroup.append(miningcamp)
    slpgroup.append(house)
    slpgroup.append(lumber)
    slpgroup.append(archrange)
    slpgroup.append(mill)
    slpgroup.append(tc)
    slpgroup.append(pikemen)
    slpgroup.append(scout)
    slpgroup.append(sheepalive)
    slpgroup.append(boar)
    def __init__(self):
        self.x = 0
    def get_slp_groups(self):
        return self.slpgroup
        
talk = 1
lines = []
       
def getfolderslist(custompath=None):
    # Return a list with SLX-foldernames contained in actual directory
    # Also updates foldercontent.txt
    print("Getting Folder-List...")
    
    slxfolders = []
    if (custompath==None):
        os.system("dir /b >foldercontent.txt")
    else:
        os.system("dir /b "+custompath+" >foldercontent.txt")
        
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
    # Gets all Bitmap filenames inside the specified
    # Slxfolders as [['1.1.bmp', '1.2.bmp']['2.1.bmp', '2.2.bmp']]
    print("Getting Bitmap-List...")
    
    #print(len(slxfolders))
    
    bitmap = [0] * len(slxfolders)
    for i in range(len(slxfolders)):
        bitmap[i] = [0] * len(slxfolders[i])
        #print(len(slxfolders[i]))
        for k in range (0, len(slxfolders[i])):
            bitmap[i][k] = [0] * 200
    
    gr_data = [0] * len(slxfolders)
    for i in range(len(slxfolders)):
        gr_data[i] = [0] * len(slxfolders[i])
        for k in range (0, len(slxfolders[i])):
            gr_data[i][k] = [0] * 200
            
    for i in range (0,amount):
        for j in range (0,len(slxfolders[i])):
            if mode == "update":
                os.system("dir "+str(slxfolders[i][j])+" /b > bitmapcontent.txt")
            f = open("bitmapcontent.txt", "r")
            string = f.read()
            #print( slxfolders[i][j])
            
            lines = string.split("\n")
            k=0
            for line in lines:
                #print(k)
                if (line.find('d') == -1) and (line != 0) and (line.find('.png')!=-1):
                    bitmap[i][j][k] = line
                    #print(line)
                elif (gr_data_included == True) and (line.find('d') != -1) and (line != 0) and (line.find('.png')!=-1):
                    gr_data[i][j][k] = line
                k+=1
                    
    return bitmap, gr_data
    
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
        
def gatherslxfolders(slxfolders):
    for i in range(0, len(slxfolders)):
        for j in range(0, len(slxfolders[i])):
            commandstring = "xcopy /Y "+str(slxfolders[i][j])+" \\results\\"+str(slxfolders[i][j])
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
    
def paintwhitezone_units(slxfolders, amount, bitmap, gr_data):
    #Analyzes Data_graphics to find white parts, which are unit color (not background, shadows or color-player)
    #Then paint that zone of the graphics (.png) in a color code
    count=0
    whitepixels = []
    
    # Loop through all found bitmaps and folders
    for i in range (0,len(slxfolders)):
        for j in range (0,len(slxfolders[i])):
            #print(j)
            #print("Unit Nr.: %d" %j)
            for k in range (0,len(gr_data[i][j])):
                if (gr_data[i][j][k] != 0) and (bitmap[i][j][k-1] != 0):
                
                    # Load Graphic Data, get size 
                    #print(gr_data[i][j][k])
                    #print(slxfolders[i][j])
                    gr_data_id = str(slxfolders[i][j])+"/"+str(gr_data[i][j][k])
                    img = Image.open(gr_data_id).convert('RGB')
                    
                    # Search white Pixels in Graphic Data
                    # print("Get white pixels from %s" %gr_data_id)
                    whitepixels = getwhitepixels(img)
                    
                    # Color those Pixels in Graphics, with color code.
                    graphic_id = str(slxfolders[i][j])+"\\"+str(bitmap[i][j][k-1])
                    img2 = Image.open(graphic_id).convert('RGB')
                    draw = ImageDraw.Draw(img, mode = "RGB")
                    
                    # Generate Color, Paint and save
                    colorseed = count*12
                    color = hsv2rgb(colorseed,1,1)
                    draw.point(whitepixels, color)
                    savepath = "C:\\results\\"+graphic_id
                    img.save(savepath)
                    
                    #print("Paint them in %s with color:" %graphic_id)
                    #print(color)
        print("%d units from 18" %(count))
        count+=1
        print("Colorseed:")
        print(colorseed)
    
if __name__ == "__main__":
    slpcolor = SLPGroups()
    slxfolderlist = slpcolor.get_slp_groups()
    
    #bitmaps, gr_data = getbitmapnames(slxfolderlist, len(slxfolderlist), gr_data_included = True, mode ="update")
    
    #alreadydone = getfolderslist("C:\\results")  
    #print(alreadydone)
    #paintwhitezone_units(slxfolderlist, len(slxfolderlist), bitmaps, gr_data)
    
    gatherslxfolders(slxfolderlist)
    
    """
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
    """