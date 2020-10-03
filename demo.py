from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import config

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

fileId = ''
def upload(filename, filepath):

    file1 = drive.CreateFile({'title' : filename,"parents": [{"kind": "drive#fileLink", "id": config.root_id}]})
    file1.SetContentFile(filepath)
    # print('Uploaded!')
    file1.Upload()
    global fileId
    fileId = file1['id']
    return fileId

def getfile(id):
	source = drive.CreateFile({'id': id})
	return source

def delete(id):
    file = getfile(id)
    file.Delete()

def list(id):
    file = getfile(id)
    print('title: %s\n',(file['title']))
