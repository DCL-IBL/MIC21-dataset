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

    #f = open('new_cats','r')
    #dsets = f.readlines()
    #f.close()
    dsets = ['accordionist\n']
    
    for d in dsets:
        dname = d[:-1]
        print('Working on '+dname)
        dset = dataset_model.find({'name':dname}).next()
        for c in category_model.find():
            if 'name' in c.keys():
                anns = annotation_model.find({'dataset_id':dset['_id'],'category_id':c['_id']})
                if anns.count() > 0:
                    print('-'+str(c['name'])+' '+str(anns.count()))
                    dataset_model.update({'_id':dset['_id']},{'$addToSet':{'categories':c['_id']}})
                    continue                                                                                                         
            
    quit()
