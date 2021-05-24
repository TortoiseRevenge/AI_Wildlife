import logging
import requests
import json
import azure.functions as func
from PIL import Image
from PIL.ExifTags import TAGS
from urllib.request import urlopen
from io import BytesIO
from PIL.ExifTags import GPSTAGS

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)
       

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

            name = req.params.get('name')
   
    imagename = req.params.get('imagename')
    if not imagename:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            imagename = req_body.get('imagename')


    #url = "https://storageaccountrgbiraaaf.blob.core.windows.net/wildlife/IMG_1175.jpg"
    #url2 = "https://storageaccountrgbiraaaf.blob.core.windows.net/wildlife/" + imagename
    url2 = "https://" + name +"/" + imagename
    response = requests.get(url2)
    img = Image.open(BytesIO(response.content))
    exif = img._getexif()
    geotags = get_geotagging(exif)

    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

     


    if name:
        
        
        #return func.HttpResponse(f"Here are the geotags: {lat}, {lon} for {imagename} at location {url2}")
        
         return func.HttpResponse (
            json.dumps({
            'lat': lat,
            'lon': lon
 
            }) 
         )

    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )import logging
import requests
import json
import azure.functions as func
from PIL import Image
from PIL.ExifTags import TAGS
from urllib.request import urlopen
from io import BytesIO
from PIL.ExifTags import GPSTAGS

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)
       

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

            name = req.params.get('name')
   
    imagename = req.params.get('imagename')
    if not imagename:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            imagename = req_body.get('imagename')


    #url = "https://storageaccountrgbiraaaf.blob.core.windows.net/wildlife/IMG_1175.jpg"
    #url2 = "https://storageaccountrgbiraaaf.blob.core.windows.net/wildlife/" + imagename
    url2 = "https://" + name +"/" + imagename
    response = requests.get(url2)
    img = Image.open(BytesIO(response.content))
    exif = img._getexif()
    geotags = get_geotagging(exif)

    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

     


    if name:
        
        
        #return func.HttpResponse(f"Here are the geotags: {lat}, {lon} for {imagename} at location {url2}")
        
         return func.HttpResponse (
            json.dumps({
            'lat': lat,
            'lon': lon
 
            }) 
         )

    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
