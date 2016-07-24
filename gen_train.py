"""
Create training and validation images by converting to gray scale, resizing to 56x56 pixels and applying
data augmentation by random scaling and shearing.
"""

import os
import sys
import csv
import random
import numpy as np
import pandas as pd
from sklearn import preprocessing

random.seed(0)
np.random.seed(0)

if len(sys.argv) < 3:
    print "Usage: python gen_train.py input_folder output_folder label_file"
    exit(1)

fi = sys.argv[1]
fo = sys.argv[2]
fc = pd.read_csv(sys.argv[3])

labels = fc.Class.values
lbl_enc = preprocessing.LabelEncoder()
labels = lbl_enc.fit_transform(labels)
imgs = fc.ID.values

p = np.random.permutation(len(imgs))
imgs = imgs[p]
labels = labels[p]

val_index = int(0.9 * len(imgs))
val_imgs = imgs[val_index:]
val_labels = labels[val_index:]

imgs = imgs[:val_index]
labels = labels[:val_index]

cmd = "convert -colorspace gray -resize 56x56\! "

img_lst = []

# resize original images
print "Resizing training images"
for i, img in enumerate(imgs):
    outFileName = str(img) + ".jpg"
    outLabel = labels[i]
    md = ""
    md += cmd
    md += fi + str(img) + ".Bmp"
    md += " " + fo + outFileName
    img_lst.append((outFileName, outLabel))
    os.system(md)

print "Inverting training images"
for i, img in enumerate(imgs):
    outFileName = str(img) + "_inverted.jpg"
    outLabel = labels[i]
    md = ""
    md += cmd
    md += " -negate "
    md += fi + str(img) + ".Bmp"
    md += " " + fo + outFileName
    img_lst.append((outFileName, outLabel))
    os.system(md)

print "Creating scaled training images"
for i, img in enumerate(imgs):
    for nRep in range(3):
        scale_factor = random.randint(44, 68)
        outFileName = str(img) + "_scaled_" + str(scale_factor) + ".jpg"
        outLabel = labels[i]
        md = "convert -colorspace gray -resize " + str(scale_factor) + "x" + str(scale_factor) + "\! -gravity center -background white -extent 56x56 "
        md += " -gravity center -crop 56x56+0+0 +repage "
        md += fi + str(img) + ".Bmp"
        md += " " + fo + outFileName
        img_lst.append((outFileName, outLabel))
        os.system(md)

print "Creating scaled sheared training images"
for i, img in enumerate(imgs):
    for nRep in range(3):
        scale_factor = random.randint(58, 70)
        shear_x = random.randint(-15, 15)
        shear_y = random.randint(-15, 15)
        outFileName = str(img) + "_scaled_" + str(scale_factor) + "_" + str(shear_x) + "x" + str(shear_y) + "shear.jpg"
        outLabel = labels[i]
        md = "convert -colorspace gray -resize " + str(scale_factor) + "x" + str(scale_factor) + "\! -gravity center -background white -extent 56x56 "
        md += "-shear " + str(shear_x) + "x" + str(shear_y)
        md += " -gravity center -crop 56x56+0+0 +repage "
        md += fi + str(img) + ".Bmp"
        md += " " + fo + outFileName
        img_lst.append((outFileName, outLabel))
        os.system(md)

random.shuffle(img_lst)

train_list_writer = csv.writer(open("train.lst", "w"), delimiter='\t', lineterminator='\n')
for item in img_lst:
    train_list_writer.writerow(item)

val_lst = []

# resize original images
print "Resizing validation images"
for i, img in enumerate(val_imgs):
    outFileName = str(img) + ".jpg"
    outLabel = val_labels[i]
    md = ""
    md += cmd
    md += fi + str(img) + ".Bmp"
    md += " " + fo + outFileName
    val_lst.append((outFileName, outLabel))
    os.system(md)

print "Inverting validation images"
for i, img in enumerate(val_imgs):
    outFileName = str(img) + "_inverted.jpg"
    outLabel = val_labels[i]
    md = ""
    md += cmd
    md += " -negate "
    md += fi + str(img) + ".Bmp"
    md += " " + fo + outFileName
    val_lst.append((outFileName, outLabel))
    os.system(md)

print "Creating scaled validation images"
for i, img in enumerate(val_imgs):
    for nRep in range(3):
        scale_factor = random.randint(44, 68)
        outFileName = str(img) + "_scaled_" + str(scale_factor) + ".jpg"
        outLabel = val_labels[i]
        md = "convert -colorspace gray -resize " + str(scale_factor) + "x" + str(scale_factor) + "\! -gravity center -background white -extent 56x56 "
        md += " -gravity center -crop 56x56+0+0 +repage "
        md += fi + str(img) + ".Bmp"
        md += " " + fo + outFileName
        val_lst.append((outFileName, outLabel))
        os.system(md)

print "Creating scaled sheared validation images"
for i, img in enumerate(val_imgs):
    for nRep in range(3):
        scale_factor = random.randint(58, 70)
        shear_x = random.randint(-15, 15)
        shear_y = random.randint(-15, 15)
        outFileName = str(img) + "_scaled_" + str(scale_factor) + "_" + str(shear_x) + "x" + str(shear_y) + "shear.jpg"
        outLabel = val_labels[i]
        md = "convert -colorspace gray -resize " + str(scale_factor) + "x" + str(scale_factor) + "\! -gravity center -background white -extent 56x56 "
        md += "-shear " + str(shear_x) + "x" + str(shear_y)
        md += " -gravity center -crop 56x56+0+0 +repage "
        md += fi + str(img) + ".Bmp"
        md += " " + fo + outFileName
        val_lst.append((outFileName, outLabel))
        os.system(md)


val_list_writer = csv.writer(open("valid.lst", "w"), delimiter='\t', lineterminator='\n')
for item in val_lst:
    val_list_writer.writerow(item)


