import os
import glob

path0 = '/nfs/data/KITTI/rawdata'
path1 = '/nfs/data/KITTI/val'
#path2 = '/nfs/data/KITTI/val_DORN'
path2 = '/nfs/data/KITTI/val_DORN_nyu'
seqs = os.listdir(path1)

#f = open('kitti_val_list.csv','wt')
f = open('kitti_val_list_nyu.csv','wt')

for seq in seqs:
    folder = seq[:10]
    
    path = os.path.join(path0,folder,seq,'image_02/data')
    imgfs = os.listdir(path)
    imgfs.sort()

    pathr = os.path.join(path2,seq,'image_02')

    for imgf in imgfs:
        fname1 = os.path.join(path,imgf)
        fname2 = os.path.join(pathr,imgf)
        f.write(fname1+','+fname2+'\n')

f.close()
