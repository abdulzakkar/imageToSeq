# imageToSeq
Turn any picture into a grid of characters that resembles the original picture.

## Usage
### Required inputs

`python /path/to/imageToSeq.py -i /path/to/inputFile -b /path/to/backgroundFile`

**Input file** (-i) is the image that will be transformed into the character grid.

**Background file** (-b) is the image from which the RGB values for the characters will be taken.

### Optional inputs

`python /path/to/imageToSeq.py -i /path/to/inputFile -b /path/to/backgroundFile -o /path/to/outputFileName -f /path/to/font -n numberOfRows -c characterSize -r random -g backgroundNormalization -w blackOrWhite -s characterSet -t fontSize -e brightness`

**Output File** (-o) is the desired output image name. 
    (default: imageToSeq_output.jpg)
    
**Font** (-f) the font in which the characters will be rendered. 
    (default: C:/Windows/Fonts/BAUHS93.ttf; must be modified on non-Windows computers)
    
**Number of rows** (-n) __INTEGER VALUE__ refers to number of character rows that will be used to generate the final image. 
  *The more rows, the more detail will be visible. Large row counts require more processing time and more hard disk space.*
    (default: 50)
    
**Character Size** (-c)  __INTEGER VALUE__ the number of pixels delineating the width and height of every character.
    (default: 10)
    
**Random** (-r)  __FLOAT VALUE__ allows for more imprecise selection of characters to fit the original image. 
  *Useful for avoiding an overly repetitive look. The higher the number, the more random the characters.*
    (default: 2.0)
    
**Background Normalization** (-g) __FLOAT VALUE__ higher values indicate that the pixels of the image will be brought closer to a specific level of brightness (which can also be modified).
  *essentially, higher values reduce background contrast to allow characters to have a larger visual impact.*
    (default: 1.0; 0 = no normalization)
    
**Black or White** (-w) __BOOLEAN VALUE__ Enter True for a white backdrop, or enter False for a blck backdrop.
    (default: False)
    
**Character set** (-s) __INTEGER VALUE BETWEEN 1 AND 5__ Select the set of characters which the program is allowed to use in generating the image.
  *1: every ASCII character.
  2: All amino acid residues UPPER CASE
  3: All amino acid residues UPPER CASE and lower case
  4: All DNA nitrogenous bases (A,C,G,T) UPPER CASE
  5: All DNA nitrogenous bases (A,C,G,T) UPPER CASE and lower case*
    (default: 1)
    
**Font size** (-t)  __FLOAT VALUE__ Size of font relative to character size.
  *Overly large values will result in characters being cut off and partially visible within their spaces
  Overly small values will result in there being too much backdrop visible.*
    (default: 1.4)
    
**Brightness** (-e) __INTEGER VALUE BETWEEN 0 AND 255__ Set the value of brightness to which all pixels of the background image will be normalized.
    (default: 200)


 
