import cv2
import sys
sys.path.insert(0,'caffe/python')
sys.path.insert(0,'caffe/pylayer')
import caffe
import numpy as np
import scipy.io as sio
import argparse
import os
import tqdm
import pandas as pd
import pdb

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filelist', type=str, help='file list')


caffe.set_mode_gpu()
caffe.set_device(0)
net = caffe.Net('models/KITTI/deploy.prototxt', 'models/KITTI/cvpr_kitti.caffemodel', caffe.TEST)
pixel_means = np.array([[[103.0626, 115.9029, 123.1516]]])

def depth_prediction(filename):
    img = cv2.imread(filename, 1)
    img = img.astype(np.float32)
    H = img.shape[0]
    W = img.shape[1]
    img -= pixel_means
    img = cv2.resize(img, (W, 385), interpolation=cv2.INTER_LINEAR)
    ord_score = np.zeros((385, W), dtype=np.float32)
    counts = np.zeros((385, W), dtype=np.float32)
    for i in xrange(4):
        h0 = 0
        h1 = 385
        w0 = int(0 + i*256)
        w1 = w0 + 513
        if w1 > W:
           w0 = W - 513
           w1 = W

        data = img[h0:h1, w0:w1, :]
        data = data[None, :]
        data = data.transpose(0,3,1,2)
        blobs = {}
        blobs['data'] = data
        net.blobs['data'].reshape(*(blobs['data'].shape))
        forward_kwargs = {'data': blobs['data'].astype(np.float32, copy=False)}
        net.forward(**forward_kwargs)
        pred = net.blobs['decode_ord'].data.copy()
        pred = pred[0,0,:,:]
        ord_score[h0:h1,w0:w1] = ord_score[h0:h1, w0:w1] + pred
        counts[h0:h1,w0:w1] = counts[h0:h1, w0:w1] + 1.0

    ord_score = ord_score/counts - 1.0
    ord_score = (ord_score + 40.0)/25.0
    ord_score = np.exp(ord_score)
    ord_score = cv2.resize(ord_score, (W, H), interpolation=cv2.INTER_LINEAR)
    return ord_score
    #ord_score = ord_score*256.0


#------ main ---- 

args = parser.parse_args()

imglist = pd.read_csv(args.filelist) 
N = imglist.shape[0]

for i in tqdm.tqdm(range(N)):
    fname = imglist.iloc[i,0]
    rname = imglist.iloc[i,1]

    depth = depth_prediction(fname)
    depth = depth*256.0
    depth = depth.astype(np.uint16)

    folder = os.path.dirname(rname)
    if not os.path.exists(folder):
        os.makedirs(folder)
    cv2.imwrite(rname, depth)

