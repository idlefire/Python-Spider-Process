import csv
import json
from Downloader import Downloader

FIELDS = ('area', 'population', 'iso', 'country',)

writer = csv.writer(open('countries.csv', 'w'))
writer.writerow(FIELDS)
D = Downloader()
html = D('http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0')
ajax = json.loads(html)
for records in ajax['records']:
    # row = [records[field] for field in FIELDS]
    row = records['country']
    writer.writerow(row)
