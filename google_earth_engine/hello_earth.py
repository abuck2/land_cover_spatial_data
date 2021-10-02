import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

# Import the MODIS land cover collection.
lc = ee.ImageCollection('MODIS/006/MCD12Q1')

# Import the MODIS land surface temperature collection.
lst = ee.ImageCollection('MODIS/006/MOD11A1')

# Import the USGS ground elevation image.
elv = ee.Image('USGS/SRTMGL1_003')

# Initial date of interest (inclusive).
i_date = '2017-01-01'

# Final date of interest (exclusive).
f_date = '2020-01-21'

# Selection of appropriate bands and dates for LST.
lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)

# Brussels
u_lon = 4.309333
u_lat = 50.872986
u_poi = ee.Geometry.Point(u_lon, u_lat)

# Define a region of interest with a buffer zone of x km around Brussels.
roi = u_poi.buffer(150000)

# Reduce the LST collection by mean.
lst_img = lst.mean()

# Adjust for scale factor.
lst_img = lst_img.select('LST_Day_1km').multiply(0.02)

# Convert Kelvin to Celsius.
lst_img = lst_img.select('LST_Day_1km').add(-273.15)

from IPython.display import Image

# Create a URL to the styled image for a region around Brussels.
url = lst_img.getThumbUrl({
    'min': 10, 'max': 30, 'dimensions': 512, 'region': roi,
    'palette': ['blue', 'yellow', 'orange', 'red']})
print(url)

# Display the thumbnail land surface temperature in Belgium.
print('\nPlease wait while the thumbnail loads, it may take a moment...')
Image(url=url)

# Make pixels with elevation below sea level transparent.
elv_img = elv.updateMask(elv.gt(0))

# Display the thumbnail of styled elevation in Belgium.
Image(url=elv_img.getThumbURL({
    'min': 0, 'max': 2000, 'dimensions': 512, 'region': roi,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}))

# Get a feature collection of administrative boundaries.
countries = ee.FeatureCollection('FAO/GAUL/2015/level0').select('ADM0_NAME')

# Filter the feature collection to subset France.
belgium = countries.filter(ee.Filter.eq('ADM0_NAME', 'Belgium'))

# Clip the image by France.
elv_fr = elv_img.clip(belgium)

# Create the URL associated with the styled image data.
url = elv_fr.getThumbUrl({
    'min': 0, 'max': 2500, 'region': roi, 'dimensions': 512,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']})

# Display a thumbnail of elevation in Belgium.
Image(url=url)

"""
#Export to drive
task = ee.batch.Export.image.toDrive(image=elv_img,
                                     description='elevation',
                                     scale=30,
                                     region=lyon,
                                     fileNamePrefix='my_export_brussels',
                                     crs='EPSG:4326',
                                     fileFormat='GeoTIFF')
task.start()

"""
brussel = roi = u_poi.buffer(1000)
link = lst_img.getDownloadURL({
    'scale': 30,
    'crs': 'EPSG:4326',
    'fileFormat': 'GeoTIFF',
    'region': brussel})
print(link)

