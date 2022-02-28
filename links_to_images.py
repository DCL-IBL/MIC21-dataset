import pymongo
import json

if __name__ == '__main__':
    client = pymongo.MongoClient('172.19.0.2',27017)
    db = client.flask
    dataset_model = db.dataset_model
    annotation_model = db.annotation_model
    image_model = db.image_model
    category_model = db.category_model
    user_model = db.user_model

    names = ['elbow pad','motorcyclist','collared shirt','pressure suit','zebra crossing','dog','ship','clubs','diving suit','car wndshield','bus','ribbon','uneven bars','truck','motorcycle','trampoline','car1 headlight','bottle','climbing backpack','roller skater cap','car1 wheel','stop sign','searchlight','hoop','camera tripod','horizontal bar','skateboard helmet','street sign','scoreboard','swimming trunks','traffic light','sweatshirt','handbag','bikini','car1','body of water','baton','tennis net','swimsuit','pen','cyclist','cameraman','balance\xa0beam','photographer','rings','jammers','open-wheel','trainer','cylinder','ball','tennis cap','cap','beach volleyball hat','skateboard hat','legging','bicycle','leggings','visor','golf bag','rhythmic gymnast','maillot','catcher\'s helmet','backpack','goal','skis','girl']

    categ_names = ['gymnastics','rhythmic_gymnast','figure_skating','chess','skiing','weightlifting','climbing','cricket','flying','hockey','soccer','volleyball','tennis','skateboarding','swimming','roller_skating','horse_racing','steeplechase','jogging','golf','diving','car_racing','boxing','bowling','billiard','beach_volleyball','basketball','baseball','jumping','running','acrobatics']
    
    f = open('list_of_images.html','w')
    f.write('<html><head></head><body>')
    for d in dataset_model.find({}):
        print(d['name'])
        f.write('<p>'+d['name']+'</p>')
        for im in image_model.find({'dataset_id':d['_id']}):
            f.write('<p><a href=\'http://dcl.bas.bg:5000/#/annotate/'+str(im['_id'])+'\'>'+im['file_name']+'</a></p>')
    f.close()
    quit()
        
    for n in names:
        print(n)
        f.write('<p>'+n+'</p>')
        cat_id = category_model.find({'name':n}).next()['_id']
        imgs = []
        for ann in annotation_model.find({'category_id':cat_id}):
            try:
                dset = dataset_model.find({'_id':ann['dataset_id']}).next()
            except:
                print('Dataset '+str(ann['dataset_id'])+' not found')
                continue
            if ann['image_id'] not in imgs and dset['name'] in categ_names:
                imgs.append(ann['image_id'])
                try:
                    im = image_model.find({'_id':ann['image_id']}).next()
                    f.write('<p>('+dset['name']+')<a href=\'http://dcl.bas.bg:5000/#/annotate/'+str(ann['image_id'])+'\'>'+im['file_name']+'</a></p>')
                except:
                    f.write('<p>Image id: ' + str(ann['image_id']) +' not found</p>')
    f.close()
