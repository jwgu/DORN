import cv2
import sys
sys.path.insert(0,'caffe/python')
sys.path.insert(0,'caffe/pylayer')
import caffe
import numpy as np
import scipy.io as sio
import argparse
import os
import pdb
import pandas as pd
import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filelist', type=str, help='csv file of image list')

caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Net('models/KITTI/deploy.prototxt', 'models/KITTI/cvpr_kitti.caffemodel', caffe.TEST)
pixel_means = np.array([[[103.0626, 115.9029, 123.1516]]])

def depth_prediction(filename):
    img = cv2.imread(filename, 1)
    img = img.astype(np.float32)

    #--- resize to 640x480 for comparison, Jinwei ---
    img = cv2.resize(img,(640,480), interpolation=cv2.INTER_LINEAR)

    H = img.shape[0]
    W = img.shape[1]

    img -= pixel_means
    #img = cv2.resize(img, (353, 257), interpolation=cv2.INTER_LINEAR)
    img = cv2.resize(img, (513, 385), interpolation=cv2.INTER_LINEAR)
    data = img.copy()
    data = data[None, :]
    data = data.transpose(0,3,1,2)
    blobs = {}
    blobs['data'] = data
    net.blobs['data'].reshape(*(blobs['data'].shape))
    forward_kwargs = {'data': blobs['data'].astype(np.float32, copy=False)}
    net.forward(**forward_kwargs)
    pred = net.blobs['decode_ord'].data.copy()
    pred = pred[0,0,:,:] - 1.0
    #pred = pred/25.0 - 0.36
    pred = (pred + 40.0)/25.0
    pred = np.exp(pred)
    ord_score = cv2.resize(pred, (W, H), interpolation=cv2.INTER_LINEAR)
    return ord_score
    #ord_score = ord_score*256.0

args = parser.parse_args()

imglist = pd.read_csv(args.filelist,skiprows=0)
N = imglist.shape[0]

for i in tqdm.tqdm(range(N)):
    fname = imglist.iloc[i,0]
    rname = imglist.iloc[i,1]

    depth = depth_prediction(fname) 

    #depth = depth/10.0
    #depth = depth*255.0
    #depth = depth.astype(np.uint8)

    depth = depth*256.0
    depth = depth.astype(np.uint16)

    folder = os.path.dirname(rname)
    folder = folder.replace('val_DORN','val_DORN_kitti')
    if not os.path.exists(folder):
        os.makedirs(folder)
    rname = rname.replace('val_DORN','val_DORN_kitti')
    cv2.imwrite(rname, depth)
