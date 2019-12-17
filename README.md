# Intranet_Sync
Python Script to scrape and synchronize entire directories from Intranet - an Apache RedHat HTTP server

[![GitHub issues](https://img.shields.io/github/issues/meet59patel/Intranet_Sync?color=important)](https://github.com/meet59patel/Intranet_Sync/issues)
[![GitHub forks](https://img.shields.io/github/forks/meet59patel/Intranet_Sync)](https://github.com/meet59patel/Intranet_Sync/network)
[![GitHub license](https://img.shields.io/github/license/meet59patel/Intranet_Sync)](https://github.com/meet59patel/Intranet_Sync/blob/master/LICENSE)

This script...
1. Scrapes the remote directories *(from DIR_URLS list)*
2. Compares with locally available files
3. Asynchronously downloads missing files

## Usage
> Make sure you have Python 3 installed. *Commands may vary for Windows environment.*

#### 1. Clone the project:

```bash
git clone https://github.com/meet59patel/Intranet_Sync.git
```

#### 2. Install Dependencies:
Open terminal in Intranet_Sync directory.
```bash
pip install -r requirements.txt
```


#### 3. Add links to the directories you want to synchronize:

Update **DIR_URLS** list inside **main.py**
Also update **DEST_PATH**


#### 4. Run:

```bash
python3 main.py
```



## Development
- [x] Asynchronous GET requests for files
- [ ] GUI
