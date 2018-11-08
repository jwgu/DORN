import os
import glob

path0 = '/data/data/vkitti/vkitti_1.3.1_rgb'
path1 = '/nfs/data/vkitti/res_DORN'

#seq = '0002/morning'
#seq = '0020/morning'
seqs = ['0001/clone',
       '0001/fog',
       '0001/morning',
       '0001/overcast',
       '0001/rain',
       '0001/sunset',
       '0002/clone',
       '0002/fog',
       '0002/morning',
       '0002/overcast',
       '0002/rain',
       '0002/sunset',
       '0018/clone',
       '0018/fog',
       '0018/morning',
       '0018/overcast',
       '0018/rain',
       '0018/sunset',
       '0020/clone',
       '0020/fog',
       #'0020/morning',
       '0020/overcast',
       '0020/rain',
       '0020/sunset']


#f = open('vkitti_list0.csv','wt')
f = open('vkitti_list_all.csv','wt')

imgfs = []
for seq in seqs:  
    imgfs = glob.glob(os.path.join(path0,seq,'*.png'))
    imgfs.sort()

    pathr = os.path.join(path1,seq)

    for imgf in imgfs:
        fname1 = imgf
        fname2 = os.path.join(pathr, os.path.basename(imgf))
        f.write(fname1+','+fname2+'\n')

f.close()
