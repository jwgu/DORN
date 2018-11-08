import os
import glob

path0 = '/lpr/depth/scanNet-5-frame/scan-net-5-frame'
path1 = '/nfs/data/scanNet-5-frame/val_DORN'

#with open('scanNet_split/scannet_val.txt','r') as f:
#    seqs = f.read().splitlines()
#
#f = open('scannet_val_list.csv','wt')

seqs = ['scene0000_00']
f = open('scannet_selected_list.csv','wt')

for seq in seqs:
    
    imgfs = glob.glob(os.path.join(path0,seq,'frame*.color.jpg'))
    imgfs.sort()

    pathr = os.path.join(path1,seq)

    for imgf in imgfs:
        name = os.path.basename(imgf)
    
        fname1 = imgf
        fname2 = os.path.join(pathr,name[:-9]+'depth.pgm')
        f.write(fname1+','+fname2+'\n')

f.close()
