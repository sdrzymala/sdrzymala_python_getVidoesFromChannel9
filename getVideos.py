import requests
from clint.textui import progress
import os.path
import sys
import datetime


# configuration
noFilesToDwonload = 1
fileWithLinksToDownload = "E:\\downloads_ch9\\myoutputfile.txt"
outputDirectory = "E:\\downloads_ch9\\"
log_file_path = "E:\\downloads_ch9\\log.txt"


# function to download file
def download(url, file_name):

    r = requests.get(url, stream=True)
    path = file_name
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()


def log(message_to_log):
    with open(log_file_path, "a") as myfile:
        myfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message_to_log + '\n')




# get links from file
with open(fileWithLinksToDownload) as f:
    allFilesToDownload = f.read().splitlines()


# download links
i = 0 #iterate file
j = 0 #iterate downloaded file
while j < noFilesToDwonload:

    currentFileToDownload = str(allFilesToDownload[i]).split('  :  ')[1].strip()
    currentFileName = currentFileToDownload[currentFileToDownload.rfind("/")+1:]
    currentFilePath = outputDirectory + currentFileName

    if os.path.isfile(currentFilePath) == False:
        try:
            download(currentFileToDownload, currentFilePath)
            log(currentFileToDownload + ": downloaded succesful")
            j = j + 1
        except:
            log(currentFileToDownload + ": error downloading file")
    else:
        log("File " + currentFileToDownload + " already downloaded: " + currentFilePath)

    i = i + 1