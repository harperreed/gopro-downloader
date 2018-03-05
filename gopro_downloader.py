from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
 
import urllib2
import requests
from bs4 import BeautifulSoup
import urlparse
import shutil
import yaml

import sys, re, os

# handle logging

import logging
# create logger with 'spam_application'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

#let's do it


def gopro_wifi_on():
    url = "http://" + gopro_host +"/gp/gpMediaList"
    try:
        r = requests.get(url, timeout=0.1)
        return True
    except:
        logger.info(gopro_host + ' is not up')
        return False

def download_file(url, local_filename):
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def delete_image(delete_filename):
    delete_url = "http://" + gopro_host + "/gp/gpControl/command/storage/delete?p="+delete_filename
    #print(delete_url)
    logger.info('Deleting: ' + delete_filename)
    r = requests.get(delete_url)
    if (r.status_code==200):
        logger.debug("Successfully deleted: " + delete_filename)
    else:
        logger.error("Error occurred deleting: " + delete_filename)

# config these dudes


try:
    config_file = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml" 
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
except:
    logger.error("config file not found: "+ config_file)
    sys.exit(0)

base_folder = cfg['gopro']['sd_dir']
image_download_dir = cfg['images']['save_dir'] #os.path.join(os.path.expanduser("~"),'Pictures', 'gopro')
gopro_host = cfg['gopro']['host']
delete_images = cfg['gopro']['delete_images']
 
# these should be fine

if gopro_wifi_on():

    base_url = "http://" + gopro_host + "/videos/DCIM/" + base_folder + "/"
    content = requests.get(base_url).text
    soup = BeautifulSoup(content, "lxml")
     
    media_re = re.compile(r'(jpg|jpeg|mp4)$', re.IGNORECASE)

    logger.info("Download directory:",image_download_dir)
     
    try:
        os.makedirs(image_download_dir)
        logger.debug("Created: " + image_download_dir)
    except (OSError):
        logger.debug('Already exists: ' + image_download_dir)
     
    #Run through all the links in the file listing
    for a in soup.findAll('a', attrs={'href': media_re}):
        logger.debug("Found the URL: " +  a['href'])
        file_url = urlparse.urljoin(base_url, a['href'])
        file_name = os.path.join(image_download_dir, a['href'].split('/')[-1])

        if(os.path.isfile(file_name)):
            logger.debug('Already exists: ' + file_name)
            if delete_images:
                delete_filename = a['href'].replace("/videos/DCIM", "")
                delete_image(delete_filename)
                #delete file 
            
        else:
            print("Downloading to:", file_name)
            download_file(file_url, file_name)
            if(os.path.isfile(file_name)):
                logger.info("Downloaded" + file_name)
                if delete_images:
                    delete_filename = a['href'].replace("/videos/DCIM", "")
                    delete_image(delete_filename)
