import config as cfg
import json
import logging 
import time

from recogito.recogito_client import RecogitoAPI

root = logging.getLogger()
root.setLevel(logging.INFO)

#####
# Stores the JSON-LD annotations to a file named according to the document title
#####
def store_annotations_json(filename_stem, annotations):
  with open(f'{cfg.DOWNLOAD_ANNOTATIONS_TO}/{filename_stem}.json', 'w') as outfile:
    json.dump(annotations, outfile, indent=2)

#####
# Stores the CSV annotations to a file named according to the document title
#####
def store_annotations_csv(filename_stem, annotations):
  with open(f'{cfg.DOWNLOAD_ANNOTATIONS_TO}/{filename_stem}.csv', 'w') as outfile:
    outfile.write(annotations)

###############################
#
# Download process starts here
#
###############################
try:
  client = RecogitoAPI.login({
    'username': cfg.RECOGITO_USER,
    'password': cfg.RECOGITO_PW, 
    'server_url': cfg.RECOGITO_URL
  })
  
  items = [ i for i in client.list_directory(cfg.DOWNLOAD_FOLDER)['items'] if i['type'] == 'DOCUMENT' ]
  logging.info(f'Downloading data for {len(items)} documents')

  for item in items:
    doc_id = item['id']
    logging.info(f'Downloading data for {item["title"]} ({item["id"]})')

    annotations_json = client.get_annotations(doc_id)
    annotations_csv = client.get_annotations(doc_id, 'csv')

    logging.info(f'  Document has {len(annotations_json)} annotations')

    filename_stem = cfg.FILENAME_TEMPLATE.format_map(item)
    store_annotations_json(filename_stem, annotations_json)
    store_annotations_csv(filename_stem, annotations_csv)

    time.sleep(0.2)

except Exception as e:
  logging.error(f'Error: {str(e)}')
