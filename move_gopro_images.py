from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
 
import urllib2
import requests
from bs4 import BeautifulSoup
import urlparse
import shutil

import re, os

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
    delete_url = "http://10.5.5.9/gp/gpControl/command/storage/delete?p="+delete_filename
    print(delete_url)
    print('Deleting:',delete_filename)
    r = requests.get(delete_url)
    if (r.status_code==200):
        print("Successfully deleted", delete_filename)
    else:
        print("Error occurred deleting", delete_filename)

# config these dudes

base_folder = "100GOPRO" #Where XXX, change it by the directory you want (for instance 100GOPRO)
image_download_dir = "./gopro" #os.path.join(os.path.expanduser("~"),'Pictures', 'gopro')

 
# these should be fine

base_url = "http://10.5.5.9:8080/videos/DCIM/" + base_folder + "/"
content = requests.get(base_url).text
soup = BeautifulSoup(content, "lxml")
 
media_re = re.compile(r'(jpg|jpeg|mp4)$', re.IGNORECASE)

print("Download directory:",image_download_dir)
 
try:
    os.makedirs(image_download_dir)
    print("Created:",image_download_dir)
except (OSError):
    print('Already exists:',image_download_dir)
 
#Run through all the links in the file listing
for a in soup.findAll('a', attrs={'href': media_re}):
    print("Found the URL:", a['href'])
    file_url = urlparse.urljoin(base_url, a['href'])
    file_name = os.path.join(image_download_dir, a['href'].split('/')[-1])

    if(os.path.isfile(file_name)):
        print('Already exists:',file_name)
        delete_filename = a['href'].replace("/videos/DCIM", "")
        delete_image(delete_filename)
        #delete file 
        
    else:
        print("Downloading to:", file_name)
        download_file(file_url, file_name)
        if(os.path.isfile(file_name)):
            print("Downloaded", file_name)
            delete_filename = a['href'].replace("/videos/DCIM", "")
            delete_image(delete_filename)
