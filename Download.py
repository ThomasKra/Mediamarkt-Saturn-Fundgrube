import requests
import json
import csv
numElements = 99 # nicht über 100 gehen!

angebote = []
maerkte = ['mediamarkt', 'saturn']

for markt in maerkte:
  request_cookie = requests.get(f'https://www.{markt}.de/de/data/fundgrube')

  headers = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'referer': f'https://www.{markt}.de/de/data/fundgrube',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"', 
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }

  url = f'https://www.{markt}.de/de/data/fundgrube/api/postings?limit=10&offset=0'

  request_categories = requests.post(url, headers=headers, cookies=request_cookie.cookies)
  category = json.loads(request_categories.content)['categories']


  start = 0

  numQuery = 1

  while True:
    url = f'https://www.{markt}.de/de/data/fundgrube/api/postings?limit={numElements}&offset={start}'

    r = requests.post(url, headers=headers, cookies=request_cookie.cookies)

    json_content = json.loads(r.content)
    angebote.extend(json_content['postings'])
    start = start + numElements
    len_postings = len(json_content['postings'])
    morePostingsAvailable = json_content['morePostingsAvailable']
    print(f'NumQuery: {numQuery}')
    if not morePostingsAvailable or len_postings < numElements:
      break
    numQuery = numQuery + 1


for elem in angebote:
  elem['outlet_id'] = elem['outlet']['id']
  elem['outlet'] = elem['outlet']['name']
  elem['markt'] = ('saturn' if 'SAT' in elem['top_level_catalog_id'] else 'mediamarkt')
  elem['brand_id'] = elem['brand']['id']
  elem['brand'] = elem['brand']['name']
  elem.pop('eek')


keys = angebote[0].keys()

with open('angebote_all.csv', 'w', newline='') as output_file:
  dict_writer = csv.DictWriter(output_file, keys)
  dict_writer.writeheader()
  dict_writer.writerows(angebote)

with open('angebote_all.js', 'w') as output_file:
  output_file.write('let data = ')
  output_file.write(json.dumps(angebote))
  