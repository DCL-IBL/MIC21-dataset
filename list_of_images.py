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

    f = open('list_of_categories_by_dataset.csv','w')
    f.write('dataset,name,count,images\n')
    dnames = dataset_model.aggregate([{'$match':{'deleted':False}},{'$group':{'_id':1,'names':{'$addToSet':'$name'}}}]).next()['names']

    for n in dnames:
        print(n)
        dset = db.dataset_model.find({'name':n}).next()
        ids = db.annotation_model.aggregate([{'$match':{'dataset_id':dset['_id']}},{'$group':{'_id':1,'ids':{'$addToSet':'$category_id'}}}]).next()['ids']
        for ct in ids:
            anns = annotation_model.find({'dataset_id':dset['_id'],'category_id':ct})
            #anns = annotation_model.find({'dataset_id':dset['_id'],'category_id':ct,'creator':'system','events':[]})
            cat = category_model.find({'_id':ct}).next()
            print('-'+cat['name'])
            try:
                f.write(dset['name']+','+cat['name']+','+str(anns.count())+',')
                for an in anns:
                    f.write(str(an['image_id'])+';')
                f.write('\n')
            except:
                print(error)
    f.close()

    quit()

    f = open('list_of_categories.csv','w')
    f.write('name,count,datasets\n')
    cats = []
    for cat in category_model.find({'deleted':False}):
        cats.append(cat)
        
    for cat in cats:
        client = pymongo.MongoClient('172.19.0.2',27017)
        db = client.flask
        #dataset_model = db.dataset_model
        annotation_model = db.annotation_model
        #image_model = db.image_model
        #category_model = db.category_model
        #user_model = db.user_model
        cat_id = cat['_id']
        cnt = annotation_model.find({'category_id':cat_id}).count()
        names = ''
        if 'name' not in cat.keys():
            print('No name for '+str(cat['_id']))
            continue
        print(cat['name'])
        for dset in dataset_model.find({'deleted':False}):
            print('dset = '+dset['name'])
            if annotation_model.find({'category_id':cat_id,'dataset_id':dset['_id']}).count() > 0:
                names = names + ';'+dset['name']
        f.write(cat['name']+','+str(cnt)+','+names+'\n')
    f.close()
    quit()

'''
    sport  = ['chess','skiing','weightlifting','climbing','cricket','flying','hockey','soccer','volleyball','tennis','skateboarding','swimming','rowing','roller_skating','horse_racing','steeplechase','jogger','gymnastics','golf','diving','car_racing','boxing','bowling','billiard','beach_volleyball','basketball','baseball','jumping','running','acrobatics','figure_skating','motorcyclist-cross','motorcycle racing','fisherman','hunter','hang_gliding','rhythmic gymnastics','racing_bicycle','sleigh','handball']
    transport = ['airplane','glider','helicopter','hot-air_balloon','bicycle','camper','convertible','jeep','limousine','sedan','taxi','wagon','carriage','motorcycle','bus','minibus','tram','trolleybus','boat','ferry','gondola','motorboat','sailing_vessel','ship','yacht','astronaut','rocket','spaceship','train','car_transporter','dumper','garbage_truck','lorry','pickup','tow_truck','truck','van','bulldozer','digger','forklift','tractor','baby_carriage','wheelchair','horse_sleigh','dog sleigh','double-decker','road_sign','zebra_crossing','rickshaw','scooter']
    art = ['artist','sculptor','accordionist','piper','cellist','clarinetist','conductor','flute_player','guitar_player','opera_singer','percussionist','piano player','rapper','saxophonist','singer','trombonist','trumpeter','violin person','ballet_dancer','cameraman','clown','dancer','makeup_artist','photographer','writer']
    security = ['traffic_police','fire engine','fireman','police car','police helicopter','mounted police','policeman','tank','ambulance','military helicopter','military_truck_NEW','police boat','motorized police','soldier','APC_NEW']

    f = open('list_of_images.csv','w')
    f.write('dataset,file_name\n')
    cnt = 0;
    for im in image_model.find({'deleted':False}):
        dset_id = im['dataset_id']
        dset = dataset_model.find({'_id':dset_id})
        if dset.count() > 0:
            m = dset.next()
            if m['deleted'] == False:
                cnt = cnt + 1
                f.write(m['name']+','+im['file_name']+'\n')
    f.close()
    print('Total count: '+str(cnt))
    quit()
    
    f = open('statistic_security.csv','w')
    f.write('name,images,annotations\n')
    tot_im = 0
    tot_an = 0
    for n in security:
        print(n)
        dset = dataset_model.find({'name':n}).next()
        dset_id = dset['_id']
        im_cnt = image_model.find({'dataset_id':dset_id}).count()
        an_cnt = annotation_model.find({'dataset_id':dset_id}).count()
        f.write(n+','+str(im_cnt)+','+str(an_cnt)+'\n')
        tot_im = tot_im + im_cnt
        tot_an = tot_an + an_cnt
    f.write('Total,'+str(tot_im)+','+str(tot_an)+'\n')
    f.close()

    quit()
    
    #print('Prepare categories')
    #f = open('list_of_categories.csv','w')
    #f.write('id,name,count\n');
    #for ct in category_model.find({}):
    #    print(ct['name'])
    #    anns = annotation_model.find({'category_id':ct['_id']})
    #    f.write(str(ct['_id'])+','+ct['name']+','+str(anns.count())+'\n')
    #f.close()

    print('Prepare datasets')
    names = ['airplane','glider','helicopter','bicycle','camper','convertible','jeep','limousine','sedan','taxi','wagon','horse-drawn_vehicle','motorcycle','bus','minibus','tram','trolleybus','road_sign','traffic_cop','zebra_crossing','boat','ferry','gondola','motorboat','yacht','sleigh','astronaut','rocket','spaceship','train','car_transporter','dumper','garbage_truck','lorry','pickup','tow_truck','truck','van','bulldozer','digger','forklift','steamroller','tractor','airplane_1','bus_1','dumper_1','jeep_1','motorcyclist-cross','rocket_1','steamroller_1','trolleybus_1','astronaut_1','carriage_1','ferry_1','limousine_1','motorcyclist-racing','sailing_boat_1','taxi_1','truck_1','boat_1','car_transporter_1','garbage_truck_1','minibus_1','motorcycle-transport_1','sleigh_1','tow_truck_1','van_1','bulldozer_1','digger_1','gondolla_1','motorboat_1','road_sign_1','spacecraft_1','tractor_1','yacht_1','ambulance_NEW_1','baby_carriage_NEW_1','wheelchair_NEW_1']

    users = ['dcl','Cveti','Hrisi','Iva','Maria','Svetla','Valya','Viki','Zara']
    
    f = open('list_of_images.txt','w')
    a = open('list_of_annotations.txt','w')
    for n in names:
        print(n)
        dset_id = dataset_model.find({'name':n}).next()['_id']
        f.write('\nDataset: '+n+'\n\n')
        a.write('\nDataset: '+n+'\n\n')
        for im in image_model.find({'dataset_id':dset_id}):
            if 'file_name' in im.keys():
                f.write(im['file_name']+'\n')
        cats_ids = annotation_model.aggregate([{'$match':{'dataset_id':dset_id}},{'$group':{'_id':1,'ids':{'$addToSet':'$category_id'}}}]).next()['ids']
        a.write('(category_name,total)\n')
        for c_id in cats_ids:
            a.write(category_model.find({'_id':c_id}).next()['name']+',')
            total_n = int(annotation_model.find({'dataset_id':dset_id,'category_id':c_id}).count())
            a.write(str(total_n)+'\n')
            
    f.close()
    a.close()
'''
