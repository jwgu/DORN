import os
import glob

path0 = '/lpr/SLAM/7Scenes/'
path1 = '/nfs/data/7Scenes/DORN' 

#path0 = '/data/nyu_depth_v2_raw/'
#path1 = '/nfs/data/nyu_depth_v2_raw/DORN' 


#with open('scanNet_split/scannet_val.txt','r') as f:
#    seqs = f.read().splitlines()
#
#f = open('scannet_val_list.csv','wt')

f = open('7scene_selected_list.csv','wt')
#seqs = ['chess/seq-01']
#seqs = ['office/seq-01']

seqs = ['chess/seq-02', 'chess/seq-03', 'chess/seq-04', 'chess/seq-05', 'chess/seq-06',
        'fire/seq-01', 'fire/seq-02', 'fire/seq-03', 'fire/seq-04',
        'heads/seq-01', 'heads/seq-02',
        'office/seq-02', 'office/seq-03', 'office/seq-04', 'office/seq-05', 'office/seq-06', 'office/seq-07', 'office/seq-08', 'office/seq-09', 'office/seq-10',
        'pumpkin/seq-01', 'pumpkin/seq-02', 'pumpkin/seq-03', 'pumpkin/seq-06', 'pumpkin/seq-07', 'pumpkin/seq-08',
        'redkitchen/seq-01', 'redkitchen/seq-02', 'redkitchen/seq-03', 'redkitchen/seq-04', 'redkitchen/seq-05', 'redkitchen/seq-06', 'redkitchen/seq-07', 'redkitchen/seq-08', 'redkitchen/seq-11', 'redkitchen/seq-12', 'redkitchen/seq-13', 'redkitchen/seq-14',
        'stairs/seq-01', 'stairs/seq-02', 'stairs/seq-03', 'stairs/seq-04', 'stairs/seq-05', 'stairs/seq-06']
        
        
#f = open('nyu_selected_list.csv','wt')
##seqs = ['bedroom_0001']
#seqs = ['kitchen_0001a']


for seq in seqs:
    
    imgfs = glob.glob(os.path.join(path0,seq,'frame*.color.png'))
    #imgfs = glob.glob(os.path.join(path0,seq,'r-*.ppm'))
    imgfs.sort()

    pathr = os.path.join(path1,seq)

    for imgf in imgfs:
        name = os.path.basename(imgf)
    
        fname1 = imgf
        fname2 = os.path.join(pathr,name[:-9]+'depth.pgm')
        f.write(fname1+','+fname2+'\n')

f.close()
