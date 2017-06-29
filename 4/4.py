import csv
from zipfile import ZipFile
from StringIO import StringIO
import urllib2


url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
f = urllib2.urlopen(url)
zipped_data = f.read()
with open('csv.zip', 'wb') as code:
    code.write(zipped_data)
# urls = []
# with ZipFile('csv.zip') as zf:
#     csv_filename = zf.namelist()[0]
# for _, website in csv.reader(zf.open(csv_filename)):
#     print "~"
#     urls.append('http://' + website)
# print len(urls)
