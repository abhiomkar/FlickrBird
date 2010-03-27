#!/usr/bin/python
import urllib, os, flickrapi

# Flickr User's NSID - use idgettr.com
_userId = '31945977@N04'

# 's'	small square 75x75
# 't'	thumbnail, 100 on longest side
# 'm'	small, 240 on longest side
# ''	medium, 500 on longest side
# 'b'	large, 1024 on longest side (only exists for very large original images)
# 'o'	original image, either a jpg, gif or png, depending on source format (Pro Account Only)
_photoSize = 'b'

api_key = '9ef09d14ab74f2c204b5c4ceea060b4a'
flickr = flickrapi.FlickrAPI(api_key)

# get his all public photos
publicPhotos = flickr.people_getPublicPhotos(api_key=api_key, user_id = _userId, per_page = 500)
photos = []
for photo in publicPhotos.getiterator('photo'):
	photos.append(photo.attrib['id'])

totalPhotos=len(photos)
flog = open('.'+_userId+'-photos','a+'); flog.seek(0); log = flog.read().split(';')

# removing downloaded photos (log) from the download list (photos)
photos = set([p+_photoSize for p in photos])-set(log)
photos = [p.replace(_photoSize,'') for p in photos]
if totalPhotos-len(photos):
	print "Skipping "+str(totalPhotos-len(photos))+" photos. They are already downloaded."
print "--> Started downloading "+str(len(photos))+" photos"

if len(_photoSize.strip()):
	# if the photoSize is not blank
	__photoSize = '_'+_photoSize
else:
	__photoSize = _photoSize
	
# ok, start download one-by-one
for photo in photos:
	photoInfo = flickr.photos_getInfo(photo_id=photo)
	photoTag = photoInfo.find('photo')
	photoTitle = photoTag.find('title').text
	photoDownload = "http://farm%s.static.flickr.com/%s/%s_%s%s.jpg" % (photoTag.attrib['farm'], photoTag.attrib['server'], photoTag.attrib['id'], photoTag.attrib['secret'], __photoSize)
	print "Downloading: " + photoTitle
	# unix doesn't accept '/' in a file name, try $ touch 'foo/bar'
	photoTitle = photoTitle.replace('/','_')
	if photoTitle.startswith('.'):
	# The filename which starts with '.' is a hidden file
		photoTitle = photoTitle.replace('.', '_', 1)
	# actually, downloading now...
	urllib.urlretrieve(photoDownload, os.path.join(os.getcwd(), photoTitle+' ('+_photoSize+')'+'.jpg'))
	flog.write(photo+_photoSize+';')

print "--> Downloaded "+str(len(photos))+" photos of "+photoInfo.find('photo/owner').attrib['username']+" !"
flog.close()
# You have awesome photos! :)
