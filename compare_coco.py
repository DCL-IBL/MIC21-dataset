from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
import numpy as np
import argparse
import json
import os

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Compare')
    #parser.add_argument('--fname',dest='fname',type=str,help='name of the folder')
    #args = parser.parse_args()
    #dsets = json.load(open('current_datasets.json','r'))
    dsets = [{'name':'figure_skating_1','id':1004}]
    for ds in dsets:
        fname = ds['name']
        if not os.path.isfile(fname+'_yolact.json'):
            continue
        print('Evaluation of '+fname)
        cocoGt = COCO(fname+'_gt.json')
        ids = list(cocoGt.imgs.keys())
        #print(cocoGt.getImgIds())
        #try:
        cocoDt = cocoGt.loadRes(fname+'_yolact.json')
        #print(cocoDt.getImgIds())
        #except:
        #    continue
        cocoEval = COCOeval(cocoGt,cocoDt)
        cocoEval.params.useCats = 0
        #cocoEval.params.imgIds=ids[0]
        #cocoEval.params.iouType = 'bbox'
        #cocoEval.params.iouThrs = [0]
        cocoEval.evaluate()
        #print(cocoEval.evalImgs)
        cocoEval.accumulate()
        cocoEval.summarize()
