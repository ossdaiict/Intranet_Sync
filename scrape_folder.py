import requests, os, threading, time
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join, exists

# Setting Constants
DIR_URLS = [
    'http://intranet.daiict.ac.in/~daiict_nt01/Academic/B%20Tech%20Students-Groups/',
    'http://intranet.daiict.ac.in/~daiict_nt01/Academic/Archives/Holidays/'
]

DEST_PATH = '/Users/meetpatel/Documents/Code/Miscellaneous/PythonSync/target_folder'

IGNORE_LIST = [
    '.DS_Store', 'Thumbs.db'
]
DOWNLOAD_TIMEOUT = 10 # In seconds
CHUNK_SIZE = 1024


def scrape_dir(url, dest):  # url is single string, not a list, points to a remote directory # dest points to local download destination
    if not exists(dest):
        os.makedirs(dest)

    response = requests.get(url)
    webpage = BeautifulSoup(response.text, 'lxml')
    table_row = webpage.find_all('tr')
    dirs_list = []
    dirs_links = []
    files_list = []
    files_links = []
    for item in table_row:
        file_name = item.find('a')
        if(file_name and file_name.text!="Name" and file_name.text!="Parent Directory"):     #TODO: make list of items to be ignored
            if file_name.text[-1] == '/': #If the row-item is Directory 
                dirs_list.append(file_name.text)
                dirs_links.append(url + file_name.get('href'))
            else:
                files_links.append(url + file_name.get('href'))
                files_list.append(file_name.text)

    # compare current directory file list with remote here
    check_current_dir(files_list, files_links, dest)
    
    # check subdirectories
    for j in range(len(dirs_links)): 
        scrape_dir(dirs_links[j], join(dest,dirs_list[j]))

def check_current_dir(fileslist, fileslinks, local_dest):
    ls = listdir(local_dest)
    available_files = []
    for f in ls:
        if isfile(join(local_dest, f)) and f not in IGNORE_LIST:
            available_files.append(f)
    
    thread_list=[]
    for i in range(len(fileslist)):
        if (fileslist[i] not in available_files) and (fileslist[i] not in IGNORE_LIST):
            t = threading.Thread(target=download_file_to_curr_dir, args=(fileslinks[i], local_dest))
            t.start()
            thread_list.append(t)
    for thread in thread_list:
        thread.join()

def download_file_to_curr_dir(link, dest):
    download(link, join(dest,link.split('/')[-1]))

def download(url, file_name):
    file_name = file_name.replace('%20', ' ')
    try:
        response = requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT)
        print("downloading...")
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    file.write(chunk)
    except:
        os.remove(file_name)
        print("\n**Couldn't download file**: " + file_name)
        print("Download Manually at: " + url + '\n')


# EXECUTE
def main():
    threadslist = []
    for dirurl in DIR_URLS:
        newdirname = dirurl.split('/')[-2].replace('%20', ' ')
        newdirname = join(DEST_PATH, newdirname)
        if not exists(newdirname):
            os.makedirs(newdirname)
            print("this")
        t = threading.Thread(target=scrape_dir, args=(dirurl, newdirname))
        t.start()
        threadslist.append(t)
        # threading.join()
        # scrape_dir(dirurl, newdirname)
    for thread in threadslist:
        thread.join()

starttime = time.time()
main()
print("\nFINAL Execution Time: " + str(time.time() - starttime))