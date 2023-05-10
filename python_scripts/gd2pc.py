from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList:
    #print('Title: %s, ID: %s' % (file['title'], file['id']))
    #Get the folder ID that you want
    if(file['title'] == "ExampleData2"):
       fileID = file['id']

query_string = "'" + fileID + "' in parents and trashed=false"
#flist = []
#print(query_string)
fileList_2 = drive.ListFile({'q':query_string}).GetList()
for file in fileList_2:
    print('Title: %s, ID: %s' % (file['title'], file['id']))
    file.GetContentFile(file['title'])
    #flist.append(file['id'])
#print(flist)