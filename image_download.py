from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, sys, time

# config - FileckrAPI APIKey 
key = "ABCDEF"
secret = "xyz"

# config - search keyword
keywords = ['rose', 'sunflower', 'lilium']

# config - number of images to search
image_count = 20

# config - save image filepath
dataset_dir = "./dataset/"

def search_image(keyword):
  flickr = FlickrAPI(key, secret, format='parsed-json')
  res = flickr.photos.search(
    text = keyword,
    per_page = image_count, 
    media = 'photos',
    sort = "relevance",
    safe_search = 1,
    extras = 'url_q,license'
  )
  return res

def download_image(photos, savedir):  
  try:
    for i, photo in enumerate(photos['photo']):
      url_q = photo['url_q']
      filepath = savedir+'/'+photo['id']+'.jpg'
      print("file",str( i+1 ), "= ", url_q)
      urlretrieve(url_q, filepath)
      time.sleep(2)
  except:
    import traceback
    traceback.print_exc()

# download images from Flickr
# [https://www.flickr.com/]
for keyword in keywords:
    print("download now ...",  keyword)
    
    # create a directory to save images
    traindir = dataset_dir + keyword
    if not os.path.exists(traindir):
      os.mkdir(traindir)

    # search images
    res = search_image(keyword)
    photos = res['photos']
    
    # download images
    download_image(photos, traindir)
    
