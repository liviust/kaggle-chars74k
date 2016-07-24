"""
Generate test images by converting to gray scale and resizing to 56x56 pixels.
"""

import os
import sys
import csv

if len(sys.argv) < 2:
    print "Usage: python gen_test.py input_folder output_folder"
    exit(1)

fi = sys.argv[1]
fo = sys.argv[2]

cmd = "convert -colorspace gray -resize 56x56\! "

img_lst = []

imgs = os.listdir(fi)

# resize original images
print "Resizing images"
for img in imgs:
    basename = os.path.basename(img)
    filename = os.path.splitext(basename)
    img_without_ext = filename[0]
    outFileName = str(img_without_ext) + ".jpg"
    md = ""
    md += cmd
    md += fi + str(img)
    md += " " + fo + outFileName
    img_lst.append((outFileName, 0))
    os.system(md)


fo = csv.writer(open("test.lst", "w"), delimiter='\t', lineterminator='\n')
for item in img_lst:
    fo.writerow(item)



