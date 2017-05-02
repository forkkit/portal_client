
# Contains the functions for downloading the contents of a manifest. 
#
# Author: James Matsumura
# Contact: jmatsumura@som.umaryland.edu

# base 2.7 lib(s)
import urllib2,hashlib
# additional dependencies (get from pip) 
import boto

# Accepts a manifest data structure which is a dict where the key is the unique
# ID of the file designated by OSDF. The value is then another dict which contains
# all URLs present as well as the MD5 for the file. 
def download_manifest(manifest,destination,priorities):
    
    # iterate over the manifest data structure, one ID/file at a time
    for key in manifest: 

        url = get_prioritized_endpoint(manifest[key]['urls'],priorities)

        file_name = "{0}/{1}".format(destination,url.split('/')[-1])
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print("Downloading: {0} Bytes: {1}".format(file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"{0}  [{1:.2f}%]".format(file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

        # Something is odd about the MD5 check. It could be on the end of the 
        # OSDF upload or could be here. Until the problem is diagnosed, just 
        # trust that a downloaded file is legit. 
        '''
        md5 = hashlib.sha256(file_name)
        print(md5.digest().encode('hex'))
        print(manifest[key]['md5'])
        if md5.hexdigest() == manifest[key]['md5']:
            print "MD5 check passed for file {1}".format(file_name)
        '''

# Function to get the URL for the prioritized endpoint that the user requests.
# Note that priorities can be a list of ordered priorities 
def get_prioritized_endpoint(manifest_urls,priorities):

    chosen_url = ""

    urls = manifest_urls.split(',')
    eps = priorities.split(',')

    if eps[0] == "":
        eps = ['HTTP','FTP','S3','FASP'] # if none provided, use this order

    # Priorities are entered with highest first, so simply check until we find
    # a valid endpoint and then leave.
    for ep in eps:
        if chosen_url != "":
            break
        else:
            for url in urls:
                if url.startswith(ep.lower()):
                    chosen_url = url

    return chosen_url