import json
from pycocotools import mask
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Ground Truth')
    parser.add_argument('--fname',dest='fname',type=str,help='name of the folder')
    args = parser.parse_args()
    fname = args.fname
    fn = fname + '_gt.json'
    out_json = {'images':[],'categories':[],'annotations':[]}
    
    imgs = json.load(open('image_export_'+fname+'.json','r'))
    anns = json.load(open('annotation_export_'+fname+'.json','r'))
    cats = json.load(open('categories_export.json','r'))

    out_json['info'] = {}
    
    hw = dict()
    for im in imgs:
        out_json['images'].append({'id':im['_id'],
                                   'width':im['width'],
                                   'height':im['height'],
                                   'file_name':im['file_name']})
        hw[im['_id']] = [im['width'], im['height']]

    for ct in cats:
        out_json['categories'].append({'id':int(ct['_id']),
                                       'name':ct['name']})

    for (k,an) in enumerate(anns):
        #print(an['segmentation'])
        #msk = mask.frPyObjects(an['segmentation'],hw[an['image_id']][1],hw[an['image_id']][0])
        #for i in range(len(msk)):
        #    msk[i]['counts'] = msk[i]['counts'].decode('ascii')
        if an['segmentation'] == []:
            continue
        out_json['annotations'].append({'id':k,
                                        'image_id':an['image_id'],
                                        'category_id':int(an['category_id']),
                                        'segmentation':an['segmentation'],
                                        'area':an['area'],
                                        'bbox':an['bbox'],
                                        'iscrowd':0})

    fout = open(fn,'w')
    fout.write(json.dumps(out_json))
    fout.close()
