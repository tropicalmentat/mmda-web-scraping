from google.cloud import storage
import os
import logging
import datetime as dt

client = storage.Client.from_service_account_json(os.environ['GCLOUD_STORAGE_CREDS'])

bucket = client.get_bucket('mmda-tv5-scrape-dumps')

# get yesterday's data
yesterday = (dt.datetime.now() - dt.timedelta(1)).strftime("%Y%m%d")

dumps = list(bucket.list_blobs(prefix=yesterday))

for fn in dumps:
	print(fn)