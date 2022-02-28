import json
import os

keep_labels = ['baseball']
fname = 'baseball'

f = open(fname+'.json','r')
data_in = json.loads(f.read())
f.close()

data_out = {'images':[],'categories':[],'annotations':[]}
data_out['images'] = data_in['images']

keep_ids = []
for ct in data_in['categories']:
    if ct['name'] in keep_labels:
        data_out['categories'].append(ct)
        keep_ids.append(ct['id'])
for ann in data_in['annotations']:
    if ann['category_id'] in keep_ids:
        print('Added '+str(ann['id']))
        data_out['annotations'].append(ann)
f = open(fname+'_out.json','w')
f.write(json.dumps(data_out))
f.close()
