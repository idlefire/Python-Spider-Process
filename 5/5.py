import json
import string
from Downloader import Downloader

template_url = 'http://example.webscraping.com/places/ajax/search.json?&search_term=.&page_size=1000&page=0'
countries = set()
D = Downloader()

# for letter in string.lowercase:
#     page = 0
#     while True:
#         html = D(template_url.format(letter, page))
#         try:
#             ajax = json.loads(html)
#         except ValueError as e:
#             print e
#             ajax = None
#         else:
#             for records in ajax['records']:
#                 countries.add(records['country'])
#                 # print countries
#             page += 1
#             if ajax is None or page > ajax['num_pages']:
#                 break
html = D(template_url)
ajax = json.loads(html)
for records in ajax['records']:
    countries.add(records['country'])

# open('countries.txt', 'w').write('\n'.join(sorted(countries)))
