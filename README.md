# kaggle-chars74k
Classification of characters from Google Street View images

# create augmented data from original images
python gen_train.py ./data/train/ ./data/trainAugmented/ ./data/trainLabels.csv

python gen_test.py ./data/test/ ./data/testAugmented/

# create database files
rm -r ~/kaggle/chars74k/train_leveldb/
rm -r ~/kaggle/chars74k/valid_leveldb/

cd ~/caffe/build/tools

./convert_imageset -gray -backend leveldb ~/kaggle/chars74k/data/trainAugmented/ ~/kaggle/chars74k/train.lst ~/kaggle/chars74k/train_leveldb

./convert_imageset -gray -backend leveldb ~/kaggle/chars74k/data/trainAugmented/ ~/kaggle/chars74k/valid.lst ~/kaggle/chars74k/valid_leveldb

# compute mean image from training set
./compute_image_mean ~/kaggle/chars74k/train_leveldb ~/kaggle/chars74k/mean.binaryproto -backend leveldb

# run ConvNet training
./caffe train --solver=/home/matthias/kaggle/chars74k/networks/vgg_solver.prototxt

# make submission
cd ~/kaggle/chars74k
python make_submission.py ~/kaggle/chars74k/data/sampleSubmission.csv test.lst out.csv
