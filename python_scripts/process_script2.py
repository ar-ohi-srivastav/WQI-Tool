########
## This code was designed to process the landsat images to get various parameters
## such as MNWDI, ....
##    @ authored by Ananya Amancherla (IIIT)
########
import os
import sys
import glob
import numpy as np
import geetools
from geetools import tools, composite, cloud_mask, algorithms
import geedatasets
import rasterio
from rasterio.features import shapes
from rasterio.plot import show
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import pandas as pd
import datetime
import time as NameTimeVar
from time import strftime
import matplotlib.patches as mpatches
from datetime import *
from shapely.geometry import box
from fiona.crs import from_epsg
import json
from rasterio.mask import mask
import warnings
import shapely
from shapely.geometry import Point, Polygon

def crop_image(img_file):

    warnings.simplefilter('ignore')

    #img_file = 'LC08_145049_20200203.tif'
    cropped_img_file = img_file.split('.')[0]+'_crop.tif'

    data = rasterio.open(img_file)
    #show((data,3),cmap='terrain')

    # Bounding box for clipped region in lat / long that works for all seasons
    minx,miny=75.82,15.05
    maxx,maxy=76.45,15.35
    bbox=box(minx,miny,maxx,maxy)
    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

    # Project the Polygon into same CRS as the grid
    geo = geo.to_crs(crs=data.crs.data)
    coords = [json.loads(geo.to_json())['features'][0]['geometry']]
    # Clip the raster with Polygon
    out_img, out_transform = mask(dataset=data, shapes=coords, crop=True)
    # Copy the metadata
    out_meta = data.meta.copy()
    # Parse EPSG code
    epsg_code = int(data.crs.data['init'][5:])
    out_meta.update({"driver": "GTiff","height": out_img.shape[1],"width": out_img.shape[2],"transform": out_transform,"crs": epsg_code})

    # Write image file
    with rasterio.open(cropped_img_file, "w", **out_meta) as dest:
        dest.write(out_img)
    dest.close()
    # Open the clipped raster file
    cropped = rasterio.open(cropped_img_file)

    # Visualize
    #show((cropped, 3), cmap='terrain')
#end crop_image()

# For normalizing bands into 0.0 - 1.0 scale 
def normalize(array):
    '''
    normalize: normalize a numpy array so all value are between 0 and 1
    '''
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)
# end normalize()

# Normalize bands into -1.0 - 1.0 scale
def _normalize(array):
    '''
    normalize: normalize a numpy array so all value are between -1 and 1
    '''
    array_min, array_max = array.min(), array.max()
    return 2*((array - array_min) / (array_max - array_min)) - 1
    #return  1 - 2*((array - array_min) / (array_max - array_min))
# end _normalize()

def log_writer(my_string,LOG):
    my_string = '[%s]: %s' % (NameTimeVar.strftime('%d%b%Y %H:%M:%S'), my_string)
    print(my_string)
    logfile = open(LOG, "a")
    logfile.write(my_string+"\n")
    logfile.close()

def GenTiffFile(img_array,new_tif_file,meta):

    kwargs = meta
    kwargs.update(
        driver = "GTiff",
        dtype = rasterio.float32,
        compress='lzw',
        count = 1
    )
    new_dataset = rasterio.open(
        new_tif_file, "w", **kwargs
    )
    new_dataset.write(img_array,1)
    new_dataset.close()
#end GenTiffFile()

#RECLASSIFICATION of Image (e.g. MNDWI/NDTI images)
def reclassifyImage(img_array,class_bins):
    #class_bins = [-1, 0, 1]
    img_class = np.digitize(img_array, class_bins)

    # Apply the nodata mask to the newly classified image data
    img_class = np.ma.masked_where(
        np.ma.getmask(img_array), img_class
    )
    np.unique(img_class)
    return img_class
# end reclassifyImage()

# Calculate surface reflectance
def CalcSurfReflectance(img_sr):
    sr_const = -0.2
    # tmp_sr = 0.0000275*img_sr + sr_const 

    # tmp_sr = np.ma.masked_where(tmp_sr<0,tmp_sr)
    # tmp_sr = np.ma.masked_where(tmp_sr>1,tmp_sr)
    # min_sr = tmp_sr.min()
    # max_sr = tmp_sr.max()
    # del tmp_sr
    
    img_srf = 0.0000275*img_sr + sr_const
    img_srf = np.where(img_srf<0.,0.,img_srf)
    img_srf = np.where(img_srf>1.,1.,img_srf)
    
    return(img_srf)
# end CalcSurfReflectance()

# Mask image to shape file
def maskImage(shp_f, img_f):
    # Use fiona to open shape file and extract geometry into geoms object
    with fiona.open(shp_f, "r") as shapefile:
        geoms = [feature["geometry"] for feature in shapefile]

    # Use Rasterio to open the tif file and do the masking using mask function (from Rasterio)
    with rasterio.open(img_f) as src:
        out_image, out_transform = rasterio.mask.mask(src, geoms, crop=True)
        #out_image, out_transform = rasterio.mask.mask(src, geoms, invert=True)
        out_meta = src.meta.copy()

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    masked_img_file = img_f.split('.')[0]+'_masked.tif'

    with rasterio.open(masked_img_file, 'w', **out_meta) as dest:
        dest.write(out_image)
# end maskImage()

#Extracting bands as .tifs to local storage
def extractBands(IMG_FILE_HDR):
    LOG = "..\log.txt"
    #band_list = ['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7','SR_QA_AEROSOL','ST_B10','ST_ATRAN','ST_CDIST','ST_DRAD','ST_EMIS','ST_EMSD','ST_QA','ST_TRAD','ST_URAD','QA_PIXEL','QA_RADSAT']
    band_list = ['SR_B3','SR_B4','SR_B5','SR_B6']

    img = rasterio.open(IMG_FILE_HDR+'.tif')
    out_meta = img.meta.copy()
    
    for i,band in enumerate(band_list):
        if ( (band=='SR_B3') or (band=='SR_B4') or (band=='SR_B5') or (band=='SR_B6') ):
            img_band_file = IMG_FILE_HDR + '_' + str(band_list[i]) + str('.tif')
            dst = img.read(i+1)
            GenTiffFile(dst,img_band_file,out_meta)
            out_str = '    Generated Band - ' + str(band_list[i]) +' ... '
            log_writer(out_str,LOG)
            #print('Generated Band - ' + str(band_list[i]) +' ... ')        
        else:
            continue

    # Delete objects to free memory
    del img
    del dst
# end extractBands()
    
# Make a new tif file with stacked bands to DISPLAY FALSE COLOUR COMPOSITE
def stack_and_generate_rgb_composite(IMG_FILE_HDR):
    #files = glob(os.path.join(IMG_FILE_HDR+"*SR_B[3-5].tif"))
    #files.sort()
    files = [IMG_FILE_HDR+'_SR_B3.tif',IMG_FILE_HDR+'_SR_B4.tif',IMG_FILE_HDR+'_SR_B5.tif']
    # Plot a rgb composite image
    img = rasterio.open(files[2])
    nir_np = img.read(1)
    img = rasterio.open(files[1])
    r_np = img.read(1)
    img = rasterio.open(files[0])
    g_np = img.read(1)

    rgb = np.dstack((normalize(nir_np),normalize(r_np),normalize(g_np)))
    #rgb_crop = rgb[5500:7000,1700:4300]
    #GenTiffFile(rgb,IMG_FILE_HDR+'_rgb_b5b4b3.tif',outmeta)
    
    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('RGB Composite Image (b5+b4+b3)')
    plt.imshow(rgb)
    plt.savefig(IMG_FILE_HDR+'_rgb_b5b4b3.jpg')

    del img 
    del nir_np 
    del r_np 
    del g_np
# end stack_and_generate_rgb_composite()

# Modified Normalized Difference Water Index (MNDWI)
def MNDWI(IMG_FILE_HDR):
    LOG = "..\log.txt"
    out_meta = rasterio.open(IMG_FILE_HDR+'.tif').meta.copy()
    g_file = IMG_FILE_HDR+'_SR_B3.tif'
    s_file = IMG_FILE_HDR+'_SR_B6.tif'
    
    g_img = rasterio.open(g_file).read(1)
    s_img = rasterio.open(s_file).read(1)

    g_SR = CalcSurfReflectance(g_img)
    s_SR = CalcSurfReflectance(s_img)

    out_str = f"{'    Surface Reflectance values from green band (min, max): %.5f %.5f ... '%(g_SR.min(), g_SR.max())}"
    log_writer(out_str,LOG)
    out_str = f"{'    Surface Reflectance values from SWIR-1 band (min, max): %.5f %.5f ... '%(s_SR.min(), s_SR.max())}"
    log_writer(out_str,LOG)
    
    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    mndwi = es.normalized_diff(g_SR, s_SR) #normalize to scale down SR values to 0 to 1
    #ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(12, 10))
    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('MNDWI')
    mndwi_plot = plt.imshow(mndwi)
    cbar = ep.colorbar(mndwi_plot)
    plt.savefig(IMG_FILE_HDR+'_mndwi.jpg')
    out_str = '    Saved MNDWI image ... '
    log_writer(out_str,LOG)
    #print('Saving MNDWI image ... ')

    # # Need a zoom that is OK for all seasons?
    # #mndwi_zoom = mndwi[6050:6500,3200:3700]
    # mndwi_zoom = mndwi[5500:7000,1700:4300]
    # #ep.plot_bands(mndwi_zoom, cols=1, vmin=-1, vmax=1, figsize=(12, 10))
    # fig, ax = plt.subplots(1,figsize=(12,10))
    # ax.set_title('MNDWI')
    # mndwi_zoom_plot = plt.imshow(mndwi_zoom)
    # cbar = ep.colorbar(mndwi_zoom_plot)
    # plt.savefig(IMG_FILE_HDR+'_mndwi_zoom.jpg')
    # out_str = '    Saved zoomed section of MNDWI as image ... '
    # log_writer(out_str,LOG)

    ep.hist(mndwi,bins='auto',figsize=(12,10))
    plt.savefig(IMG_FILE_HDR+'_mndwi_histogram.jpg')
    out_str = '    Saved MNDWI histogram ... '
    log_writer(out_str,LOG)

    GenTiffFile(mndwi,IMG_FILE_HDR+'_mndwi.tif',out_meta)
    #GenTiffFile(mndwi_zoom,IMG_FILE_HDR+'_mndwi_zoom.tif',out_meta)
    out_str = '    Generated mndwi tif file ... '
    log_writer(out_str,LOG)

    #Getting the threshold value from the histogram
    array = np.histogram(mndwi, bins='auto', range=(-1,1), normed=None, weights=None, density=None)
    min_val = 1000000
    arr_val = 0.01
    no_of_cols = len(array[0])
    for i in range(no_of_cols):
        if( (array[1][i] >= 0) and (array[1][i]<=0.01)):
            if(array[0][i] < min_val):
                min_val = array[0][i]
                arr_val = array[1][i]                                              
    #mndwi_class_bins = [mndwi_zoom.min(),arr_val,mndwi_zoom.max()]
    mndwi_class_bins = [mndwi.min(),0,mndwi.max()]

    #out_str = f"{'    MNDWI reclass bins: %f %f %f... '%(mndwi_zoom.min(), arr_val, mndwi_zoom.max())}"
    out_str = f"{'    MNDWI reclass bins: %f %f %f... '%(mndwi.min(), arr_val, mndwi.max())}"
    log_writer(out_str,LOG)
    
    #mndwi_reclass = reclassifyImage(mndwi_zoom,mndwi_class_bins)
    mndwi_reclass = reclassifyImage(mndwi, mndwi_class_bins)
    #mndwi_reclass = np.ma.masked_where(mndwi_reclass==0.0,mndwi_reclass)
    mndwi_reclass_file = IMG_FILE_HDR+'_mndwi_reclass.tif'
    GenTiffFile(mndwi_reclass,mndwi_reclass_file,out_meta)
    out_str = '    Generated mndwi reclass file ... '
    log_writer(out_str,LOG)

    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('Reclassified MNDWI')
    # Plot data using nicer colors
    colors=['linen','blue']
    class_bins = [0.5,1.5,2.5]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(class_bins,len(colors))
    land = mpatches.Patch(color='linen', label='Land')
    water = mpatches.Patch(color='blue', label='Water')
    plt.legend(handles=[land, water])
    mndwi_plot = ax.imshow(mndwi_reclass,cmap=cmap, norm=norm)
    #cbar = ep.colorbar(mndwi_zoom_plot)
    plt.savefig(IMG_FILE_HDR+'_mndwi_reclass.jpg',bbox_inches='tight')
    out_str = '    Saved MNDWI reclassified plot as image ... '
    log_writer(out_str,LOG)
    # Create a list of labels to use for your legend
    #ep.draw_legend(mndwi_zoom_plot,titles=['Land','Water','nature'])
    
    del g_SR 
    del s_SR
    del mndwi
    #del mndwi_zoom
    del mndwi_reclass
# end MNDWI()

#POLYGONIZATION for getting the largest water body
def polygonize(IMG_FILE_HDR,CRS_v):
    LOG = "..\log.txt"
    mask = None
    reclass_file = IMG_FILE_HDR+'_mndwi_reclass.tif'
    #mndwi_file = IMG_FILE_HDR+'_mndwi.tif'
    with rasterio.Env():
        with rasterio.open(reclass_file) as src:
            out_meta = src.meta.copy()
            image = src.read(1) # first band
            results = (
                {'properties': {'raster_val': v}, 'geometry': s}
                for i, (s, v) in enumerate(shapes(image, mask=mask, transform=src.transform))
            )
            geoms = list(results)
            

    #Create geopandas Dataframe and enable easy to use functionalities of spatial join, plotting, save as geojson, ESRI shapefile etc.
    #geoms = list(results)
    gdf  = gpd.GeoDataFrame.from_features(geoms)
    gdf.set_crs(epsg=CRS_v, inplace=True)
    gdf = gdf.to_crs(epsg=CRS_v)
    gdf.set_geometry(col='geometry', inplace=True)
    
    # FINDING POLYGON WITH LARGEST AREA    
    # convert CRS to equal-area projection
    # the length unit is now `meter`
    eqArea_gdf = gdf.to_crs(epsg=6933)

    # compute areas in sq meters
    areas = eqArea_gdf.area

    # set the area units to sq Km.
    # and add it as a new column to geodataframe
    eqArea_gdf['area_sqKm'] = areas.values/1e6
    ea_gdf_sorted = eqArea_gdf.sort_values('area_sqKm',ascending=False)
    gdf['area']=gdf.area
    gdf_sorted = gdf.sort_values('area',ascending=False)

    # # Get Largest Polygon which is the water body
    # poly_area = int(ea_gdf_sorted.iloc[1]['area_sqKm'])
    # areas = [122,123,124,125]
    # if poly_area not in areas:
        # largest_polygon = ea_gdf_sorted.head().index[1]
    # else:
        # largest_polygon = ea_gdf_sorted.head().index[2]
        
    # largest_polygon_area = ea_gdf_sorted['area_sqKm'][largest_polygon]
    
    # Get the water body polygon by identifying point inside it
    p = Point(7.364e6,1.9235e6)
    ea_new = ea_gdf_sorted.reset_index(drop=True)
    the_poly = ea_new[ea_new['geometry'].contains(p)]
    the_poly.set_crs(epsg=CRS_v, allow_override=True)
    the_poly = the_poly.to_crs(epsg=CRS_v)
    water_body_polygon_area = the_poly['area_sqKm']
    
    # Save the image name, date and polygon area into list
    poly = []
    poly.append(IMG_FILE_HDR)
    poly.append(water_body_polygon_area)
    poly.append('sq KM')

    # print area of largest polygon
    out_str = f"{'    Water body polygon area: %.4f sq KM ... '%water_body_polygon_area}"
    log_writer(out_str,LOG)

    # CREATING SHAPEFILE OF LARGEST POLYGON    
    #g=gpd.GeoSeries(gdf_sorted['geometry'][largest_polygon], crs=CRS_v)
    #g.to_file(IMG_FILE_HDR+'_mndwi_poly_shape.shp')
    the_poly.to_file(IMG_FILE_HDR+'_mndwi_poly_shape.shp')

    # Save the polygon image
    #g=gpd.GeoSeries(ea_gdf_sorted['geometry'][largest_polygon], crs=CRS_v)
    fig, ax = plt.subplots(figsize = (10,10))
    #gdf.plot(ax=ax, facecolor="none", edgecolor="black", markersize=15, categorical=True)
    the_poly.plot()
    polygon_img_file = reclass_file.split('.')[0]+'_water_body_polygon.jpg'
    plt.savefig(polygon_img_file)

    out_str = '    Saved image of water body polygon ... '
    log_writer(out_str,LOG)

    return poly
# end polygonize()

# Normalized Difference Turbidity Index (NDTI)
def NDTI(IMG_FILE_HDR):
    LOG = "..\log.txt"
    out_meta = rasterio.open(IMG_FILE_HDR+'.tif').meta.copy()
    r_file = IMG_FILE_HDR+'_SR_B4.tif'
    g_file = IMG_FILE_HDR+'_SR_B3.tif'

    r_img = rasterio.open(r_file).read(1)
    #r_img = r_img[5500:7000,1700:4300]
    r_SR = CalcSurfReflectance(r_img)
    
    g_img = rasterio.open(g_file).read(1)
    #g_img = g_img[5500:7000,1700:4300]
    g_SR = CalcSurfReflectance(g_img)
    
    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')
    
    # Calculate NDTI
    ndti = es.normalized_diff((r_SR), (g_SR))
    
    # Plot NDTI
    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('NDTI')
    ndti_plot = plt.imshow(ndti, cmap='viridis')
    cbar = ep.colorbar(ndti_plot)
    plt.savefig(IMG_FILE_HDR+'_ndti.jpg',bbox_inches='tight')
    out_str = '    Saved NDTI plot as image ... '
    log_writer(out_str,LOG)
    ndti_file = IMG_FILE_HDR+'_ndti.tif'
    GenTiffFile(ndti,ndti_file,out_meta)   
    out_str = '    Generated turbidity tif file for future reference ... '
    log_writer(out_str,LOG)
    
    # Select polygon for calculation
    shp_f = IMG_FILE_HDR+'_mndwi_poly_shape.shp'
    maskImage(shp_f,ndti_file)
    
    out_str = '    Saved masked (polygon) NDTI as tif ... '
    log_writer(out_str,LOG)

    # Plot masked image
    ndti_mask = rasterio.open(IMG_FILE_HDR+'_ndti_masked.tif').read(1) 
    ndti_mask = np.ma.masked_where(ndti_mask==0.0,ndti_mask)
    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('NDTI - Polygon section')
    ndti_mask_plot = plt.imshow(ndti_mask, cmap='viridis')
    cbar = ep.colorbar(ndti_mask_plot)
    plt.savefig(IMG_FILE_HDR+'_ndti_masked.jpg',bbox_inches='tight')
    out_str = '    Saved polygon section of NDTI as image ... '
    log_writer(out_str,LOG)

    # Reclassify the NDTI polygon as low, medium and high turbidity index
    nmin = ndti_mask.min()
    nmax = ndti_mask.max()
    nmean = ndti_mask.mean()
    nstd = ndti_mask.std()
    nmms = nmean - nstd
    nmps = nmean + nstd
    ndti_class_bins = [nmin,nmean-nstd,nmean+nstd,nmax]
    out_str = f"{'    NDTI reclass bins: %f %f %f %f ... '%(nmin,nmms,nmps,nmax)}"
    log_writer(out_str,LOG)

    ndti_reclass = reclassifyImage(ndti_mask,ndti_class_bins)
    ndti_reclass_file = IMG_FILE_HDR+'_ndti_reclass.tif'
    GenTiffFile(ndti_reclass,ndti_reclass_file,out_meta)
    out_str = '    Saved reclassified NDTI as tif ... '
    log_writer(out_str,LOG)
    
    # Plot reclassified NDTI
    fig, ax = plt.subplots(1,figsize=(12,10))
    ax.set_title('Reclassified NDTI')
    # Plot data using nicer colors
    colors=['aqua','lightgreen','green']
    class_bins = [0.5,1.5,2.5,3.5]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(class_bins,len(colors))
    low_turb = mpatches.Patch(color='aqua', label='Low Turbidity')
    moderate_turb = mpatches.Patch(color='lightgreen', label='Moderate Turbidity')
    high_turb = mpatches.Patch(color='green', label='High Turbidity')
    plt.legend(handles=[low_turb, moderate_turb, high_turb])
    ndti_reclass_plot = ax.imshow(ndti_reclass,cmap=cmap, norm=norm)
    #cbar = ep.colorbar(ndti_reclass_plot)
    plt.savefig(IMG_FILE_HDR+'_ndti_reclass.jpg',bbox_inches='tight')
    out_str = '    Saved reclassified NDTI plot as image ... '
    log_writer(out_str,LOG)
    
    # Save the image name, ndti min & max into list
    turb = []
    turb.append(IMG_FILE_HDR)
    turb.append(nmin)
    turb.append(nmax)
    
    del r_SR 
    del g_SR
    del ndti
    del ndti_mask
    
    return turb
# end NDTI()

# If exec_flag = 0 --> all the calculations are done
# Extract bands, RGB Image, MNDWI, Polygonization, NDTI
def calcAll(flist):
    # Tunga Origin = (536535.0,1873305.0)
    # Badra Origin = (468705.0,1553715.0)
    # Preserving the origin (info from the collection meta - "$ gdalinfo -norat Imagefilename") 
    #new_transform = rasterio.transform.from_origin(536535.0, 1873305.0, 30, 30)
    #new_transform = rasterio.transform.from_origin(537225.000,  1873425.000, 30, 30)
    #new_transform = rasterio.transform.from_origin(501885.000, 1713915.000, 30, 30)
    CRS_v = 32643
    LOG = "log.txt"
    out_str = 'Calculate all: RGB false composite, MNDWI, Polygonization, NDTI ... '
    log_writer(out_str,LOG)
    
    polygons = pd.DataFrame(columns = ['Image Description','Area of Water Body','Units'])
    turbidity = pd.DataFrame(columns = ['Image Description','Turbidity (NDTI) min','Turbidity (NDTI) max'])
    
    for i in range(len(flist)):
        IMG_FILE = flist[i]
        IMG_FILE_HDR = IMG_FILE.split('.')[0]
        out_str = 'Working on IMG: '+IMG_FILE+' ... '
        log_writer(out_str,LOG)
        
        # Make a new directory with image collection (file)name
        # Move the image collection (file) to new directory
        # Change directory to newly created one
        os.system('md '+IMG_FILE_HDR)
        os.system('move '+IMG_FILE+' '+IMG_FILE_HDR)

        out_str = 'Moved '+IMG_FILE+' to '+IMG_FILE_HDR+' directory ... '
        log_writer(out_str,LOG)

        os.chdir(IMG_FILE_HDR)
        LOG1 = "..\log.txt"
        out_str = 'Current working directory: '+IMG_FILE_HDR+' ... '
        log_writer(out_str,LOG1)
        
        # Crop tif 
        crop_image(IMG_FILE)
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        out_str = 'Cropped image '+IMG_FILE+' ... '
        log_writer(out_str,LOG1)
        
        # Extract bands from the image collection and save them as individual tif files
        out_str = 'Extracting bands from '+CROPPED_IMG_FILE+' ... '
        log_writer(out_str,LOG1)
        extractBands(CROPPED_IMG_FILE_HDR)
        
        # Make the RGB composite image and save as jpg file
        stack_and_generate_rgb_composite(CROPPED_IMG_FILE_HDR)
        out_str = 'Generated RGB composite image ... '
        log_writer(out_str,LOG1)
        
        # Calculate MNDWI (re-classification is done as part of MNDWI function
        out_str = 'Calculate MNDWI ... '
        log_writer(out_str,LOG1)
        MNDWI(CROPPED_IMG_FILE_HDR)

        # Polygonize the zoom section of MNDWI image
        out_str = 'Polygonize MNDWI reclass file ... '
        log_writer(out_str,LOG1)
        polygon_area = polygonize(CROPPED_IMG_FILE_HDR,CRS_v)
        polygons.loc[len(polygons)] = polygon_area

        # Calculate NDTI
        out_str = 'Calculate NDTI ... '
        log_writer(out_str,LOG1)
        ndti_range = NDTI(CROPPED_IMG_FILE_HDR)
        turbidity.loc[(len(turbidity))] = ndti_range
        
        # Change directory to parent
        os.chdir('../')
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        plt.close('all')
        
    # write the polygon areas and ndti range to excel
    polygons.index = polygons.index+1
    turbidity.index = turbidity.index+1
    tnow = datetime.now()
    sname = tnow.strftime('%Y%b%d_%H%M')
    poly_xcel_name = 'Areas_of_WaterBody_'+sname+'.xlsx'
    turb_xcel_name = 'NDTI_of_WaterBody_'+sname+'.xlsx'
    with pd.ExcelWriter(poly_xcel_name) as writer:
        polygons.to_excel(writer,sheet_name=sname,float_format='%.2f')
    out_str = 'Wrote the water body areas to '+poly_xcel_name+' ...'
    log_writer(out_str,LOG)
    with pd.ExcelWriter(turb_xcel_name) as writer:
        turbidity.to_excel(writer,sheet_name=sname,float_format='%.2f')
    out_str = 'Wrote the min and max turbidity indices to '+turb_xcel_name+' ...'
    log_writer(out_str,LOG)
#end calcAll()

def calcRGB(flist,dlist):

    LOG = "log.txt"
    logfile = open(LOG, "w")
    logfile.write('Image Processing for producing false composite RGB image from LandSAT band Images\n')
    logfile.close()

    # Tunga Origin = (536535.0,1873305.0)
    # Badra Origin = (468705.0,1553715.0)
    # Preserving the origin (info from the collection meta - "$ gdalinfo -norat Imagefilename") 
    #new_transform = rasterio.transform.from_origin(536535.0, 1873305.0, 30, 30)
    #new_transform = rasterio.transform.from_origin(501885.000, 1713915.000, 30, 30)
                                                   
    CRS_v = 32643

    # Iterate with a list of tif files and go through the process for each file
    for i in range(len(flist)):
        IMG_FILE = flist[i]
        IMG_FILE_HDR = IMG_FILE.split('.')[0]
        out_str = 'Working on IMG: '+IMG_FILE+' ... '
        log_writer(out_str,LOG)
        
        # Make a new directory with image collection (file)name
        # Move the image collection (file) to new directory
        # Change directory to newly created one
        os.system('md '+IMG_FILE_HDR)
        os.system('move '+IMG_FILE+' '+IMG_FILE_HDR)
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)
        
        # Crop tif 
        crop_image(IMG_FILE)
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        out_str = 'Cropped image '+IMG_FILE+' ... '
        log_writer(out_str,LOG)
        
        # Extract bands from the image collection and save them as individual tif files
        out_str = 'Extracting bands from '+CROPPED_IMG_FILE+' ... '
        log_writer(out_str,LOG)
        extractBands(CROPPED_IMG_FILE_HDR)
        
        # Make the RGB composite image and save as jpg file
        out_str = 'Generating RGB composite image ... '
        log_writer(out_str,LOG)
        stack_and_generate_rgb_composite(CROPPED_IMG_FILE_HDR)
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        
    for i in range (len(dlist)):
        IMG_DIR = dlist[i]
        IMG_FILE_HDR = IMG_DIR
        LOG = "log.txt"
        out_str = 'Working on IMG: '+IMG_DIR+' ... '
        log_writer(out_str,LOG)
                
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        # Change directory to IMG_FILE
        # Look for bands;
        #   if bands --> generate RGB image after checking that RGB is not already there
        #   if not look for image collection.
        #      if image collection --> generate bands and RGB after checking that RGB is not already there  
        #      if no collection --> exit
        
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)

        files = glob.glob(os.path.join(CROPPED_IMG_FILE_HDR+"*SR_B[3-5].tif"))
        files.sort()
        if (len(files)!=3):
            out_str = 'Individual band images are not found, looking for collection ... '
            log_writer(out_str,LOG)
            if (os.path.exists(IMG_FILE_HDR+'.tif')):
                    
                # Crop tif 
                crop_image(IMG_FILE_HDR+'.tif')
                CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
                CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
                out_str = 'Cropped image '+IMG_FILE_HDR+' ... '
                log_writer(out_str,LOG)
        
                # Extract bands from the image collection and save them as individual tif files
                out_str = 'Extracting bands from '+IMG_DIR+' ... '
                log_writer(out_str,LOG)
                extractBands(CROPPED_IMG_FILE_HDR)
            else:
                out_str = 'Did not find the image collection file, exiting ... '
                log_writer(out_str,LOG)
                # Change directory to parent
                os.chdir('../')
                LOG = "log.txt"
                out_str = 'Changed working directory to: '+os.getcwd()+' ...'
                log_writer(out_str,LOG)
                continue
        #else:
        #    continue
        #check if rgb already exists and exit if i does
        if (os.path.exists(CROPPED_IMG_FILE_HDR+"_rgb_b5b4b3.jpg")):
            out_str = 'RGB cpmosite already exists, exiting ... '
            log_writer(out_str,LOG)
            # Change directory to parent
            os.chdir('../')
            LOG = "log.txt"
            out_str = 'Changed working directory to: '+os.getcwd()+' ...'
            log_writer(out_str,LOG)
            continue   
            
        # Make the RGB composite image and save as jpg file
        out_str = 'Generating RGB composite image ... '
        log_writer(out_str,LOG)
        stack_and_generate_rgb_composite(CROPPED_IMG_FILE_HDR)
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
# end calcRGB()

def calcMNDWI(flist,dlist):
    LOG = "log.txt"
    out_str = 'Only MNDWI calculation and polygonisation ... '
    log_writer(out_str,LOG)
    
    # Tunga Origin = (536535.0,1873305.0)
    # Badra Origin = (468705.0,1553715.0)
    # Preserving the origin (info from the collection meta - "$ gdalinfo -norat Imagefilename") 
    #new_transform = rasterio.transform.from_origin(536535.0, 1873305.0, 30, 30)
    #new_transform = rasterio.transform.from_origin(501885.000, 1713915.000, 30, 30)
    CRS_v = 32643
    polygons = pd.DataFrame(columns = ['Image Description','Area of Water Body','Units'])
    
    # Iterate with a list of tif files and go through the process for each file
    for i in range(len(flist)):
        IMG_FILE = flist[i]
        IMG_FILE_HDR = IMG_FILE.split('.')[0]
        out_str = 'Working on IMG: '+IMG_FILE+' ... '
        log_writer(out_str,LOG)
        
        # Make a new directory with image collection (file)name
        # Move the image collection (file) to new directory
        # Change directory to newly created one
        os.system('md '+IMG_FILE_HDR)
        os.system('move '+IMG_FILE+' '+IMG_FILE_HDR)
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)
     
        # Crop tif 
        crop_image(IMG_FILE_HDR+'.tif')
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        out_str = 'Cropped image '+IMG_FILE_HDR+' ... '
        log_writer(out_str,LOG)
        
        # Extract bands from the image collection and save them as individual tif files
        out_str = 'Extracting bands from '+CROPPED_IMG_FILE+' ... '
        log_writer(out_str,LOG)
        extractBands(CROPPED_IMG_FILE_HDR)
        
        # Calculate MNDWI (re-classification is done as part of MNDWI function
        out_str = 'Calculate MNDWI ... '
        log_writer(out_str,LOG)
        MNDWI(CROPPED_IMG_FILE_HDR)

        # Polygonize the zoom section of MNDWI image
        out_str = 'Polygonize MNDWI reclass file ... '
        log_writer(out_str,LOG)
        polygon_area = polygonize(CROPPED_IMG_FILE_HDR,CRS_v)
        polygons.loc[len(polygons)] = polygon_area
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        
    for i in range (len(dlist)):
        IMG_DIR = dlist[i]
        IMG_FILE_HDR = IMG_DIR
        LOG = "log.txt"
        out_str = 'Working on IMG: '+IMG_DIR+' ... '
        log_writer(out_str,LOG)
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        # Change directory to IMG_FILE
        # Look for bands;
        #   if bands --> generate MNDWI and assorted images
        #   if not look for image collection.
        #      if image collection --> generate bands and MNDWI and assorted images
        #      if no collection --> exit
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)

        files = glob.glob(os.path.join(CROPPED_IMG_FILE_HDR+"*SR_B[3-5].tif"))
        files.sort()
        if (len(files)!=3):
            out_str = 'Individual band images are not found, looking for collection ... '
            log_writer(out_str,LOG)
            if (os.path.exists(IMG_FILE_HDR+'.tif')):
                
                # Crop tif 
                crop_image(IMG_FILE_HDR+'.tif')
                CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
                CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
                out_str = 'Cropped image '+IMG_FILE_HDR+' ... '
                log_writer(out_str,LOG)
        
                # Extract bands from the image collection and save them as individual tif files
                out_str = 'Extracting bands from '+IMG_DIR+' ... '
                log_writer(out_str,LOG)
                extractBands(CROPPED_IMG_FILE_HDR)
            else:
                out_str = 'Did not find the image collection file, exiting ... '
                log_writer(out_str,LOG)
                # Change directory to parent
                os.chdir('../')
                LOG = "log.txt"
                out_str = 'Changed working directory to: '+os.getcwd()+' ...'
                log_writer(out_str,LOG)
                continue
        #else:
        #    continue
        #check if mndwi already exists
        if (os.path.exists(CROPPED_IMG_FILE_HDR+"_mndwi.tif")):
            out_str = 'MNDWI already exists, exiting ... '
            log_writer(out_str,LOG)
            # Change directory to parent
            os.chdir('../')
            LOG = "log.txt"
            out_str = 'Changed working directory to: '+os.getcwd()+' ...'
            log_writer(out_str,LOG)
            continue  
            
        # Calculate MNDWI (re-classification is done as part of MNDWI function
        out_str = 'Calculate MNDWI ... '
        log_writer(out_str,LOG)
        MNDWI(CROPPED_IMG_FILE_HDR)

        # Polygonize the zoom section of MNDWI image
        out_str = 'Polygonize MNDWI reclass file ... '
        log_writer(out_str,LOG)
        polygon_area = polygonize(CROPPED_IMG_FILE_HDR,CRS_v)
        polygons.loc[len(polygons)] = polygon_area
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        
    # write the polygon areas and ndti range to excel
    polygons.index = polygons.index+1
    
    tnow = datetime.now()
    sname = tnow.strftime('%Y%b%d_%H%M')
    poly_xcel_name = 'Areas_of_WaterBody_'+sname+'.xlsx'
    
    with pd.ExcelWriter(poly_xcel_name) as writer:
        polygons.to_excel(writer,sheet_name=sname,float_format='%.2f')
    out_str = 'Wrote the water body areas to '+poly_xcel_name+' ...'
    log_writer(out_str,LOG)
    
# end calcMNDWI()

def calcNDTI(flist,dlist):
    LOG = "log.txt"
    out_str = 'Only NDTI calculation ... '
    log_writer(out_str,LOG)
    
    # Tunga Origin = (536535.0,1873305.0)
    # Badra Origin = (468705.0,1553715.0)
    # Preserving the origin (info from the collection meta - "$ gdalinfo -norat Imagefilename") 
    #new_transform = rasterio.transform.from_origin(536535.0, 1873305.0, 30, 30)
    #new_transform = rasterio.transform.from_origin(501885.000, 1713915.000, 30, 30)
    CRS_v = 32643
    polygons = pd.DataFrame(columns = ['Image Description','Area of Water Body','Units'])
    turbidity = pd.DataFrame(columns = ['Image Description','Turbidity (NDTI) min','Turbidity (NDTI) max'])
    
    # Iterate with a list of tif files and go through the process for each file
    for i in range(len(flist)):
        IMG_FILE = flist[i]
        IMG_FILE_HDR = IMG_FILE.split('.')[0]
        out_str = 'Working on IMG: '+IMG_FILE+' ... '
        log_writer(out_str,LOG)
        
        # Make a new directory with image collection (file)name
        # Move the image collection (file) to new directory
        # Change directory to newly created one
        os.system('md '+IMG_FILE_HDR)
        os.system('move '+IMG_FILE+' '+IMG_FILE_HDR)
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)
     
        # Crop tif 
        crop_image(IMG_FILE_HDR+'.tif')
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        out_str = 'Cropped image '+IMG_FILE_HDR+' ... '
        log_writer(out_str,LOG)
        
        # Extract bands from the image collection and save them as individual tif files
        out_str = 'Extracting bands from '+CROPPED_IMG_FILE+' ... '
        log_writer(out_str,LOG)
        extractBands(CROPPED_IMG_FILE_HDR)
        
        # Calculate MNDWI (re-classification is done as part of MNDWI function
        out_str = 'Calculate MNDWI ... '
        log_writer(out_str,LOG)
        MNDWI(CROPPED_IMG_FILE_HDR)

        # Polygonize the zoom section of MNDWI image
        out_str = 'Polygonize MNDWI reclass file ... '
        log_writer(out_str,LOG)
        polygon_area = polygonize(CROPPED_IMG_FILE_HDR,CRS_v)
        polygons.loc[len(polygons)] = polygon_area
        
        # Calculate NDTI
        out_str = 'Calculate NDTI ... '
        log_writer(out_str,LOG)
        ndti_range = NDTI(CROPPED_IMG_FILE_HDR)
        turbidity.loc[(len(turbidity))] = ndti_range
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        
    for i in range (len(dlist)):
        IMG_DIR = dlist[i]
        IMG_FILE_HDR = IMG_DIR
        LOG = "log.txt"
        out_str = 'Working on IMG: '+IMG_DIR+' ... '
        log_writer(out_str,LOG)
        
        # Change directory to IMG_FILE
        # Look for bands;
        #   if bands --> generate NDTI and assorted images
        #   if not look for image collection.
        #      if image collection --> generate bands and NDTI and assorted images
        #      if no collection --> exit
        os.chdir(IMG_FILE_HDR)
        LOG = "../log.txt"
        out_str = 'Current working directory: '+os.getcwd()+' ... '
        log_writer(out_str,LOG)
        CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
        CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
        files = glob.glob(os.path.join(CROPPED_IMG_FILE_HDR+"*SR_B[3-5].tif"))
        files.sort()
        if (len(files)!=3):
            out_str = 'Individual band images are not found, looking for collection ... '
            log_writer(out_str,LOG)
            if (os.path.exists(IMG_FILE_HDR+'.tif')):    
                # Crop tif 
                crop_image(IMG_FILE_HDR+'.tif')
                CROPPED_IMG_FILE = IMG_FILE_HDR+'_crop.tif'
                CROPPED_IMG_FILE_HDR = IMG_FILE_HDR+'_crop'
                out_str = 'Cropped image '+IMG_FILE_HDR+' ... '
                log_writer(out_str,LOG)
        
                # Extract bands from the image collection and save them as individual tif files
                out_str = 'Extracting bands from '+IMG_DIR+' ... '
                log_writer(out_str,LOG)
                extractBands(CROPPED_IMG_FILE_HDR)
            else:
                out_str = 'Did not find the image collection file, exiting ... '
                log_writer(out_str,LOG)
                 # Change directory to parent
                os.chdir('../')
                LOG = "log.txt"
                out_str = 'Changed working directory to: '+os.getcwd()+' ...'
                log_writer(out_str,LOG)
                continue
        #else:
        #    continue
        #check if ndti already exists
        if (os.path.exists(CROPPED_IMG_FILE_HDR+"_ndti.tif")):
            out_str = 'NDTI already exists, exiting ... '
            log_writer(out_str,LOG)
             # Change directory to parent
            os.chdir('../')
            LOG = "log.txt"
            out_str = 'Changed working directory to: '+os.getcwd()+' ...'
            log_writer(out_str,LOG)
            continue 
        # Ndti needs mndwi, so if mndwi doesn't exist, calculate first
        if (os.path.exists(CROPPED_IMG_FILE_HDR+"_mndwi.tif")==False):
            # Calculate MNDWI (re-classification is done as part of MNDWI function
            out_str = 'Calculate MNDWI ... '
            log_writer(out_str,LOG)
            MNDWI(CROPPED_IMG_FILE_HDR)

            # Polygonize the zoom section of MNDWI image
            out_str = 'Polygonize MNDWI reclass file ... '
            log_writer(out_str,LOG)
            polygon_area = polygonize(CROPPED_IMG_FILE_HDR,CRS_v)
            polygons.loc[len(polygons)] = polygon_area
        
        # Calculate NDTI
        out_str = 'Calculate NDTI ... '
        log_writer(out_str,LOG)
        ndti_range = NDTI(CROPPED_IMG_FILE_HDR)
        turbidity.loc[(len(turbidity))] = ndti_range
        
        # Change directory to parent
        os.chdir('../')
        LOG = "log.txt"
        out_str = 'Changed working directory to: '+os.getcwd()+' ...'
        log_writer(out_str,LOG)
        
    # write the polygon areas and ndti range to excel
    turbidity.index = turbidity.index+1
    tnow = datetime.now()
    sname = tnow.strftime('%Y%b%d_%H%M')
    turb_xcel_name = 'NDTI_of_WaterBody_'+sname+'.xlsx'
    polygons.index = polygons.index+1
    poly_xcel_name = 'Areas_of_WaterBody_'+sname+'.xlsx'
    
    with pd.ExcelWriter(turb_xcel_name) as writer:
        turbidity.to_excel(writer,sheet_name=sname,float_format='%.2f')
    out_str = 'Wrote the min and max turbidity indices to '+turb_xcel_name+' ...'
    log_writer(out_str,LOG)
    
    with pd.ExcelWriter(poly_xcel_name) as writer:
        polygons.to_excel(writer,sheet_name=sname,float_format='%.2f')
    out_str = 'Wrote the water body areas to '+poly_xcel_name+' ...'
    log_writer(out_str,LOG)
# end calcNDTI()

def main():
    LOG = "log.txt"
    logfile = open(LOG, "w")
    logfile.write('\nImage Processing for MNDWI and NDTI calculation of LandSAT Images\n')
    logfile.close()
    if (len(sys.argv) != 4):
        out_str = 'USAGE: python anu_btp2.py start_date end_date exec_flag ... \n'
        log_writer(out_str,LOG)
        exit(1)

    exec_flag = int(sys.argv[3])
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    if ( (exec_flag < 0) or (exec_flag > 3) ):
        out_str = '\nUSAGE: python anu_btp2.py exec_flag ... \nexec_flag has to be between 0 and 3 ... \n'
        log_writer(out_str,LOG)
        exit(1)

    # If exec_flag = 0 --> calculate All
    # If exec_flag = 1 --> calculate RGB
    # If exec_flag = 2 --> calculate MNDWI and polygonize
    # If exec_flag = 3 --> calculate NDTI

    
    flist = glob.glob('*[0-9][0-9][0-9].tif')
    dlist = glob.glob('*[0-9][0-9][0-9]')
    #print(flist)
    
    #add date filter here. 
    #i.e. startdate enddate are inputs, add files and directories between those dates to flist nd dlist
    y1, m1, d1 = [int(x) for x in start_date.split('-')]
    sdt = date(y1, m1, d1)
    y2, m2, d2 = [int(x) for x in end_date.split('-')]
    edt = date(y2, m2, d2)
    
    flist_new = []
    for i in range(len(flist)):
        ye = int(flist[i][12: 16])
        mo = int(flist[i][16: 18])
        da = int(flist[i][18: 20])
        dt = date(ye, mo, da)
       
        if ((dt >= sdt) and (dt <= edt)):
            flist_new.append(flist[i])

    #print(flist_new)
    dlist_new = []
    for i in range(len(dlist)):
        ye = int(dlist[i][12: 16])
        mo = int(dlist[i][16: 18])
        da = int(dlist[i][18: 20])
        dt = date(ye, mo, da)
        if ((dt >= sdt) and (dt <= edt)):
            dlist_new.append(dlist[i])
    #print(dlist_new)
    
    if (exec_flag == 0):
        if (len(flist_new)==0):
            out_str = 'There are no image files between date range ... \n'
            log_writer(out_str,LOG)  
            exit(1)
        calcAll(flist_new)

    if (exec_flag == 1):
        if (len(flist_new)==0 and len(dlist_new)==0):
            out_str = 'There are no image files or directories downloaded between date range ... \n'
            log_writer(out_str,LOG)
            exit(1)
        calcRGB(flist_new,dlist_new)
        
    if (exec_flag == 2):
        if (len(flist_new)==0 and len(dlist_new)==0):
            out_str = 'There are no image files or directories downloaded between date range ... \n'
            log_writer(out_str,LOG)
            exit(1)
        calcMNDWI(flist_new,dlist_new)

    if (exec_flag == 3):
        if (len(flist_new)==0 and len(dlist_new)==0):
            out_str = 'There are no image files or directories downloaded between date range ... \n'
            log_writer(out_str,LOG)
            exit(1)
        calcNDTI(flist_new,dlist_new)

# end main()

if __name__ == "__main__":
    main()