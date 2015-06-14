import csv
import os
import numpy as np
from sklearn import preprocessing
import pandas as pd
import caffe

fc = pd.read_csv('/home/matthias/kaggle/chars74k/data/trainLabels.csv')

labels = fc.Class.values
lbl_enc = preprocessing.LabelEncoder()
labels = lbl_enc.fit_transform(labels)


mean_image = np.load('/home/matthias/kaggle/chars74k/mean.npy')
print np.shape(mean_image)
mean_image = mean_image[:, 4:52, 4:52]
print np.shape(mean_image)
mean_image = np.reshape(mean_image, (1, 48, 48))

net = caffe.Classifier('/home/matthias/kaggle/chars74k/networks/vgg_test.prototxt',
                       '/home/matthias/kaggle/chars74k/models/vgg_train_valid_iter_20000.caffemodel',
                       image_dims=(56, 56), raw_scale=255, mean=mean_image)

caffe.set_mode_gpu()

imgs = os.listdir('/home/matthias/kaggle/chars74k/data/testAugmented/')
fo = csv.writer(open('out.csv', "w"), lineterminator='\n')

fo.writerow(['ID', 'Class'])

for i, img in enumerate(imgs):
    print str(i)
    im = caffe.io.load_image('/home/matthias/kaggle/chars74k/data/testAugmented/' + img, color=False)
    scores = net.predict([im], oversample=True)
    predLabel = np.argmax(scores)
    predClass = lbl_enc.inverse_transform(predLabel)
    fileName, fileExtension = os.path.splitext(img)
    fo.writerow([str(fileName), predClass])



    

