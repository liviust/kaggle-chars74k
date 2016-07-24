# Kaggle Chars74k

Code for producing a submission for the Kaggle challenge [First steps with Julia](https://www.kaggle.com/c/street-view-getting-started-with-julia). The Chars74k dataset contains images from Google Streetview of 64 characters. The below network achieves an accuracy of 0.76014 on the public test set.

![alt text](https://kaggle2.blob.core.windows.net/competitions/kaggle/3947/media/chars74k.jpg "Source: https://www.kaggle.com/c/street-view-getting-started-with-julia")

Model architecture
------------------

| Layer |   Type            				|
|:-----:|:-------------------------:		|
| Input | 48x48             				|
| 1     | conv 3x3, 128, leaky relu (0.01) 	|
| 2     | conv 3x3, 128, leaky relu (0.01)  |
|       | max 2x2/2, dropout 0.25			| 
| 3     | conv 3x3, 128, relu    			|
| 4     | conv 3x3, 128, relu    			|
|       | max 2x2/2, LR normalization		|
| 5     | conv 3x3, 128, leaky relu (0.01)  |
| 6     | conv 3x3, 128, leaky relu (0.01)  |
|       | max 2x2/2, LR normalization		|
| 7     | conv 3x3, 128, leaky relu (0.01)  |
| 8     | fc 2048, leaky relu (0.01)  		|
|       | droput 0.5 						|
| 10    | fc 2048, leaky relu (0.01)  		|
|       | dropout 0.5 						|
| 11    | fc 62, softmax    				|


Running training
----------------

Create augmented data from original images
```
python gen_train.py ./data/train/ ./data/trainAugmented/ ./data/trainLabels.csv
python gen_test.py ./data/test/ ./data/testAugmented/
```
  
Create database files
``` 
rm -r ~/kaggle/chars74k/train_leveldb/
rm -r ~/kaggle/chars74k/valid_leveldb/

cd ~/caffe/build/tools

./convert_imageset -gray -backend leveldb ~/kaggle/chars74k/data/trainAugmented/ ~/kaggle/chars74k/train.lst ~/kaggle/chars74k/train_leveldb
./convert_imageset -gray -backend leveldb ~/kaggle/chars74k/data/trainAugmented/ ~/kaggle/chars74k/valid.lst ~/kaggle/chars74k/valid_leveldb
```

Compute mean image from training set
```
./compute_image_mean ~/kaggle/chars74k/train_leveldb ~/kaggle/chars74k/mean.binaryproto -backend leveldb`
```

Run CNN training
```
./caffe train --solver=/home/matthias/kaggle/chars74k/networks/vgg_solver.prototxt
```

Make submission
```
cd ~/kaggle/chars74k
python make_submission.py ~/kaggle/chars74k/data/sampleSubmission.csv test.lst out.csv
```
