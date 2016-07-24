"""
Generates text files that contain the filenames for training and test sets.
"""

import csv
import os
import sys
import random

if len(sys.argv) < 4:
    print "Usage: gen_img_list.py train/test sample_submission.csv folder"
    exit(1)

random.seed(888)

task = sys.argv[1]			# train or test (train has subfolders for classes)
fc = csv.reader(file(sys.argv[2]))	# csv containing class list in first column
fi = sys.argv[3]			# path to folder containing class subfolders (train) or images (test)

# make class map (will be used to read subfolders)
head = fc.next()
head = head[1:]

# make image list
img_lst = []
cnt = 0
if task == "train":
    for i in xrange(len(head)):
        path = fi + head[i]
        lst = os.listdir(fi + head[i])
        for img in lst:
            img_lst.append((head[i] + '/' + img, i))
            # img_lst.append((cnt, i, path + '/' + img))
            # cnt += 1
else:
    lst = os.listdir(fi)
    for img in lst:
        img_lst.append((img, 0))
        # img_lst.append((cnt, 0, fi + img))
        # cnt += 1

# shuffle
if task == "train":
    random.shuffle(img_lst)

# in training, 10% of the data are used for validation
if task == "train":
    val_index = int(0.9 * len(img_lst))
    val_lst = img_lst[val_index:]
    img_lst = img_lst[:val_index]

    fo = csv.writer(open("train.lst", "w"), delimiter='\t', lineterminator='\n')
    for item in img_lst:
        fo.writerow(item)

    fo = csv.writer(open("valid.lst", "w"), delimiter='\t', lineterminator='\n')
    for item in val_lst:
        fo.writerow(item)

else:
    fo = csv.writer(open("test.lst", "w"), delimiter='\t', lineterminator='\n')
    for item in img_lst:
        fo.writerow(item)

