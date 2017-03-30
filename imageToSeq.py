from PIL import Image, ImageDraw, ImageFont
import math
import random
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-i","--infile", help = "input file.")
parser.add_argument("-b","--bgfile", help = "file to be used as the background/character color.")
parser.add_argument("-o","--outfile", help = "output file name.", default = "imageToSeq_output.jpg", nargs='?')
parser.add_argument("-n","--nrows", help = "number of rows used from the image used to generate characters.", default = 50, nargs='?', type = int)
parser.add_argument("-c","--charsize", help = "number of pixels of width and height of characters.", default = 10, nargs='?', type = int)
parser.add_argument("-r","--random", help = "How non-exact character choices are with respect to pixel brightness.", default = 2.0, nargs='?', type = float)
parser.add_argument("-g","--bgnormal", help = "controls how much normalizing there is for the background colors. Higher number means values are more similar.", default = 1.0, nargs='?', type = float)
parser.add_argument("-w","--borw", help = "enter [True] for white background. Enter [False] for black background.", default = False, nargs='?', type = bool)
parser.add_argument("-s","--set", help = "choose element set. 1: all ASCII; 2: all amino acids (UPPERCASE); 3: all amino acids (UPPER and lowercase); 4: all nucleotides (UPPERCASE); 5: all nucleotides (UPPER and lowercase)", default = 1, nargs='?', type = int)
parser.add_argument("-f","--font", help = "path to font file for characters.", default = "C:/Windows/Fonts/BAUHS93.ttf", nargs='?')
parser.add_argument("-t","--fontsize", help = "size of letter within each 'pixel.'", default = 1.4, nargs='?', type = float)
parser.add_argument("-e","--brightness", help = "the value to which the pixels are normalized to.", default = 200, nargs='?', type = int)
args = vars(parser.parse_args())

def normalize(s):
    n = min(s)
    x = max(s)
    output = []
    for i in range(len(s)):
        output.append((s[i] - n) / (x - n)) #formula
    return output

def AdjustInputImagePixelsSize(filename,M):
    imageIn = Image.open(filename)
    width,height = imageIn.size
    Mw = int((width / float(height))*M)
    imageIn = imageIn.resize((Mw,M), Image.ANTIALIAS)
    allPixels = list(imageIn.getdata())
    width,height = imageIn.size
    return imageIn,allPixels,width,height

def AdjustBgImagePixelsSize(filename,width,height,N,blackOnWhite,n,brightness):
    imageBg = Image.open(filename)
    imageBg = imageBg.resize((width*N,height*N), Image.ANTIALIAS)
    bgData = list(imageBg.getdata())
    bgPixels = imageBg.load()
    nPixels = len(bgData)
    sys.stdout.write("Progress:\n--------------------------------------------------\n")
    for i in range(nPixels):
        if i%(nPixels / 50) == 0:
            sys.stdout.write("#")
        R = bgData[i][0]
        if R == 0:
            R = 1
        G = bgData[i][1]
        if G == 0:
            G = 1
        B = bgData[i][2]
        if B == 0:
            B = 1
        avg = (float(R) + float(G) + float(B)) / float(3)
        if blackOnWhite:
            avg = float(brightness * n + avg) / float(avg * (n + 1))
        else:
            avg = float(brightness * n + avg) / float(avg * (n + 1))
        bgPixels[i%(width*N),int(math.floor(i/float(width*N)))] = (int(R * avg), int(G * avg), int(B * avg))
    bgData = list(imageBg.getdata())
    return bgData, bgPixels

def generateElementValuesPics(elementSets,elements,blackOnWhite,font,fontsize,N):
    elementValues = []
    elementPics = []
    for e in elementSets[elements-1]:
        if blackOnWhite:
            letterImage = Image.new("RGB", (N,N), "white")
        else:
            letterImage = Image.new("RGB", (N,N), "black")
        fnt = ImageFont.truetype(font, int(float(N) * fontsize))
        d = ImageDraw.Draw(letterImage)
        if blackOnWhite:
            d.text(((int(float(N)/12)),-(int(float(N)/5))), e, font=fnt, fill=(0,0,0))
        else:
            d.text(((int(float(N)/12)),-(int(float(N)/5))), e, font=fnt, fill=(255,255,255))
        letterPixels = list(letterImage.getdata())
        elementPics.append(letterPixels)
        nPixels = len(letterPixels)
        elementValue = 0
        for i in range(nPixels):
            elementValue += ((float(letterPixels[i][0]) + float(letterPixels[i][1]) + float(letterPixels[i][2]))
            / float(3)) / float(255)
        elementValue /= nPixels
        elementValues.append(elementValue)
    elementValues = normalize(elementValues)
    return elementValues, elementPics

def generateAndSaveOutputFile(width,height,N,allPixels,elementValues,blackOnWhite,elementPics,bgData,outputFile,r):
    imageOut = Image.new("RGB", (width*N,height*N), "black")
    pixels = imageOut.load()
    nPixels = len(allPixels)
    sys.stdout.write("Progress:\n--------------------------------------------------\n")
    for i in range(nPixels):
        if i%(nPixels / 50) == 0:
            sys.stdout.write("#")
        avg = ((float(allPixels[i][0]) + float(allPixels[i][1]) + float(allPixels[i][2]))
        / float(3)) / float(255) + float(random.randint(-r,r)) / float(10)
        bestDiff = 1.0
        bestIndex = 0
        for j in range(len(elementValues)):
            diff = abs(elementValues[j] - avg)
            if diff < bestDiff:
                bestDiff = diff
                bestIndex = j
        for m in range(N):
            for n in range(N):
                if blackOnWhite:
                    value = 1.0 - (float(elementPics[bestIndex][m * N + n][0]) / float(255))
                    adj = elementPics[bestIndex][m * N + n][0]
                else:
                    value = (float(elementPics[bestIndex][m * N + n][0]) / float(255))
                    adj = 0
                pixels[((i)%width)*N+n,(math.floor(i/width))*N+m] = (
                    int(bgData[int((((i)%width)*N+n) + ((math.floor(i/width))*N+m)*width*N)][0] * value + adj),
                    int(bgData[int((((i)%width)*N+n) + ((math.floor(i/width))*N+m)*width*N)][1] * value + adj),
                    int(bgData[int((((i)%width)*N+n) + ((math.floor(i/width))*N+m)*width*N)][2] * value + adj))
    imageOut.save(outputFile)

def main():
    elementSets = [
    [chr(x) for x in range(33,127)],
    ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y'],
    ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y','a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y'],
    ['A','C','G','T'],
    ['A','C','G','T','a','c','g','t']
    ]


    ###PARAMETERS
        ###REQUIRED
    inputFile = args["infile"] #input file
    bgFile = args["bgfile"] #file to be used for colors
        ###OPTIONAL
    outputFile = args["outfile"] #output file
    M = args["nrows"] #number of rows used from the image used to generate characters.
    N = args["charsize"] #number of pixels of width and height of characters.
    r = args["random"] #controls how much randomness there is for picking elements.
    n = args["bgnormal"] #controls how much normalizing there is for the background colors.
    #Higher n means values are more similar.
    blackOnWhite = args["borw"] #if true, then bg is white, else it's black.
    elements = args["set"] #which letters can be used in image generation.
    font = args["font"]
    fontsize = args["fontsize"] #size of letter within each 'pixel.'
    brightness = args["brightness"] #the value to which the pixels are normalized to.

    sys.stdout.write("\nAdjusting input image.\n\n")
    imageIn,allPixels,width,height = AdjustInputImagePixelsSize(inputFile,M)
    sys.stdout.write("Adjusting background image:\n")
    bgData,bgPixels = AdjustBgImagePixelsSize(bgFile,width,height,N,blackOnWhite,n,brightness)
    sys.stdout.write("\nDone.\n\n")
    sys.stdout.write("Generating character images and values.\n\n")
    elementValues,elementPics = generateElementValuesPics(elementSets,elements,blackOnWhite,font,fontsize,N)
    sys.stdout.write("Rendering final image:\n")
    generateAndSaveOutputFile(width,height,N,allPixels,elementValues,blackOnWhite,elementPics,bgData,outputFile,r)
    sys.stdout.write("\nDone! Image is ready :)")


main()
