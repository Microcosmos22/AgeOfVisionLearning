from PIL import Image, ImageDraw, ImageColor
import sys, os, subprocess, colorsys
#img = Image.new( 'RGB', (255,255), "black") # Create a new black image

talk = 1
lines = []


def countlines(fname):
    def file_lengthy(fname):
        with open(fname) as f:
                for i, l in enumerate(f):
                        pass
    #print("Number of lines in the file: ",file_lengthy(fname))    
    return file_lengthy(fname)
       
def getfolders(indexlist):
    string = f.read()
    lines = string.split("\n")
    slxfolders = []
    i=0
    for line in lines:
        if lines[i].find(".") == -1:
            slxfolders.append(line)
        i+=1
    slxfolders = slxfolders[:i-4]
    return slxfolders, i-4

def getbitmapnames(slxfolders, amount):
    bitmaps = []
    for i in range (0,amount):
        os.system("dir "+str(slxfolders[i])+" /b > bitmapcontent.txt")
        f = open("bitmapcontent.txt", "r")
        string = f.read()
        lines = string.split("\n")
        bitmapinfile = []
        
        for line in lines:
            if line.find('.bmp') != -1:
                bitmapinfile.append(line)
        i+=1
        bitmaps.append(bitmapinfile)
    #print(bitmaps)
    return bitmaps
    
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    
def drawframewithcolor(id, colorseed):
    img = Image.open(id).convert('RGB')
    draw = ImageDraw.Draw(img, mode = "RGB")
    
    r,g,b = hsv2rgb(colorseed,1,1)
    print(r,g,b)
    draw.rectangle([(0,0),img.size], fill = (r,g,b))
    """
    pixels = img.load() # Create the pixel map
    for o in range(img.size[0]):    # For every pixel:
        for p in range(img.size[1]):
            pixels[o,p] = (o, p, 100) # Set the colour accordingly
    """
    # write to stdout
    img.save(id)
    #img.show()
    
if __name__ == "__main__":
    # Get folders containing (SLX, Bitmaps)
    slxfolders = []
    os.system("dir /b >foldercontent.txt")
    f = open("foldercontent.txt", "r")
    slxfolders, amount = getfolders(f)
    
    # Get Bitmap-Filenames
    bitmapfiles = []
    bitmapfiles = getbitmapnames(slxfolders, amount)
    #print(len(bitmapfiles[0]))
    
    j=0
    while j < len(slxfolders):
        k=0
        while k < len(bitmapfiles[j]):
            id = slxfolders[j]+"/"+bitmapfiles[j][k]
            print(id)
            
            #Generate Colorseed
            colorseed = float(slxfolders[j])/5312.0
            
            # Open and Paint Bitmap
            drawframewithcolor(id, colorseed)
            
            k+=1
        j+=1