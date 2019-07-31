import sys

from apiclient.http import MediaFileUpload
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()

filename = args.filename
filepath = filename
SCOPES = 'https://www.googleapis.com/auth/drive'
CHUNK_SIZE = 1 #MB
store = file.Storage('python_credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', scope=SCOPES)
    creds = tools.run_flow(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

media_body = MediaFileUpload(filepath, chunksize=CHUNK_SIZE*1024*1024, resumable=True)
metadata = {'name': filename}

req = DRIVE.files().create(body=metadata, media_body=media_body)
res = None
while res is None:
    status, res = req.next_chunk()
    if status:
        progress = round(status.progress()*100)
        print(str(progress))
        sys.stdout.flush()

# print str(res['id'])
# sys.stdout.flush()