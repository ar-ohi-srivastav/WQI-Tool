import ee
import sys
import pprint
import geetools
from geetools import tools, composite, cloud_mask, algorithms
import geedatasets
#import ipygee as ui

if (len(sys.argv) < 3):
    print('\nUSAGE: ee2gd.py start_date[yyyy_mm_dd] end_date[yyyy_mm_dd]\n')
    exit(1)

start_date = sys.argv[1]
end_date = sys.argv[2]

#ee.Authenticate()
ee.Initialize()

pp = pprint.PrettyPrinter(depth=4)

#defining the image collection with filters
collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').\
    filter(ee.Filter.eq('WRS_PATH',145)).\
    filter(ee.Filter.eq('WRS_ROW',50)).\
    filterDate(start_date,end_date).\
    filter(ee.Filter.lessThan('CLOUD_COVER',10));
#sun_ele = collection.get("SUN_ELEVATION").getInfo()
#sunStats = collection.aggregate_stats('SUN_ELEVATION')
#pp.pprint(str(collection.getInfo()[['id']]))
num = collection.size().getInfo()
imglist = collection.toList(collection.size())
imglist_id = imglist.map(lambda img: ee.String(ee.Image(img).get('system:id')))
#date = ee.Date(collection.first().get('system:time_start')).format('yyyy-MM-dd').getInfo()
#pp.pprint(str(imglist))
#print(sunStats.getInfo())
print('\nThere are '+str(num)+' image collections with cloud cover < 10% between '+start_date+' and '+end_date) 
imgid_str = ""
for i in range(num):
    imgid = imglist_id.getInfo()[i].split('/')
    imgid_str = imgid_str+" "+str(imgid[-1])
    #print(imgid[-1])
    #imgid = imglist_id.getInfo()[i]
    #print('\t'+str(i+1)+'\t'+imgid)
print(imgid_str+" ")


## Export
#folder = 'ExampleData2'
folder = 'test_image'
scale = 30
#var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_168037_20210918').select('SR_B2')
for i in range(num):
    imgid = imglist_id.getInfo()[i].split('/')
    img_filename = imgid[-1]
    imgb = (ee.Image(imglist.get(i))).select([2,3,4,5])
    #imgb = ee.Image((ee.Image(imglist.get(i))).select('SR_B3'))
    #pp.pprint(imgb.getInfo())
    # Export
    task = ee.batch.Export.image.toDrive(
            image=imgb,
            description=img_filename,
            folder=folder,
            #scale=scale
            maxPixels= 1e10,
            crs='EPSG:32643',
            crsTransform= imgb.projection().getInfo()['transform'],
            )
    # task = ee.Export.image.toDrive(
            # image=imgb,
            # description=img_filename,
            # folder=folder,
            # #scale=scale
            # maxPixels= 1e10,
            # crs='EPSG:32638',
            # crsTransform= image.projection().getInfo().transform,
            # )
    task.start()
    print('Requested download of '+img_filename+' to '+folder+' on GoogleDrive... ')


#parameters for constructing the export task
#bands = ['B2', 'B3', 'B6']
#scale = 30
#name_pattern = '{id}'
## the keywords between curly brackets can be {system_date} for the date of the
## image (formatted using `date_pattern` arg), {id} for the id of the image
## and/or any image property. You can also pass extra keywords using the `extra`
## argument. Also, numeric values can be formatted using a format string (as
## shown in {WRS_PATH:%d} (%d means it will be converted to integer)
#date_pattern = '' # dd: day, MMM: month (JAN), y: year
#folder = 'ExampleData2'
#data_type = 'uint32'
#extra = dict(sat='L8SR')
#region = site

#authentication failed; 

## Export
# task = geetools.batch.Export.imagecollection.toDrive(
            # collection=collection,
            # folder=folder,
            # namePattern=name_pattern,
            # scale=scale,
            # verbose=True,
            # #dataType=data_type,
            # #datePattern=date_pattern,
            # #extra=extra,
            # #region=region,
            # maxPixels=int(1e13)
        # )
# print('Request to download the images to GoogleDrive is submitted!')


#Converting DN to SR 
#_______________TBD___________________
# info = collection.getInfo()
# info
#sun_ele = collection.get("SUN_ELEVATION").getInfo()
# sunStats = collection.aggregate_stats('SUN_ELEVATION')
# print(sunStats.getInfo())