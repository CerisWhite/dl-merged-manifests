# Dragalia Lost Manifest Parser to download the essential latest (2.0) assets for Private Server purposes, made with love by Ceris

# This version relies solely on the asset name, and ignores any older versions of the same asset.


import sys
import os
import hashlib
import json
import requests
import threading
import time
# from git import Repo

from io import BytesIO
import zipfile

### VARIABLES HERE. Set these to "1" to process the localization manifests. ###

Download_EN = 0
Download_CN = 0
Download_TW = 0

# The app platform doesn't make much a difference other than iOS not having V1 files. Options are "iOS/" or "Android/". Yes, the trailing slash is necessary.
App_Platform = "Android/"
Master_URL = "http://dragalialost.akamaized.net/dl/assetbundles/" + App_Platform
UserAgent = "Dragalia/174 CFNetwork/1209 Darwin/20.2.0"

# Clone dl-datamine repo to local directory
scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
if os.path.exists(scriptDir + "/manifest"):
    os.rename(scriptDir + "/manifest", scriptDir + "/_manifest")
if not os.path.exists(scriptDir + "/_manifest"):
    ## print("Cloning the dl-datamine repo. This is over 3GB in size.")
    ## Repo.clone_from("https://github.com/CerisWhite/dl-datamine", scriptDir + "/_manifest", depth=1)
    print("Getting the manifests. This is over 3GB in size.")
    zipdata = requests.get("https://github.com/CerisWhite/dl-merged-manifests/archive/refs/heads/master.zip")
    zip2 = zipfile.ZipFile(BytesIO(zipdata.content))
    zip2.extractall(scriptDir + "/./")
    os.rename(scriptDir + "/dl-datamine-master", scriptDir + "/_manifest")
    
# Define the download function to allow for threading
def DownloadData(Manifest_json, manifest_date, assetname, assethash, DownloadURL, DownloadPath):
    tick = 0
    while tick <= 2:
        try:
            if assetname not in Manifest_json:
                Manifest_json[assetname] = []
                DataStream = requests.get(DownloadURL, stream=True, headers={"user-agent":UserAgent})
                DataFile = open(DownloadPath, "wb")
                for chunk in DataStream.iter_content(chunk_size=8192):
                    DataFile.write(chunk)
                Manifest_json[assetname].append({"hash": assethash, "date": manifest_date})
                tick = 3
            else:
                pass
        except:
            print("File " + assethash + " from manifest " + manifest_date + " failed to download.")
            time.sleep(0.5)
            tick += 1

# Prepare
JPManifest = open(scriptDir + "/master_manifest.json", "w+")
JPManifest_json = {}
os.makedirs(scriptDir + "/masterassets/latest")
if Download_EN == 1:
    ENManifest = open(scriptDir + "/master_enmanifest.json", "w+")
    ENManifest_json = {}
    os.makedirs(scriptDir + "/enassets/latest")
if Download_CN == 1:
    CNManifest = open(scriptDir + "/master_cnmanifest.json", "w+")
    CNManifest_json = {}
    os.makedirs(scriptDir + "/cnassets/latest")
if Download_TW == 1:
    TWManifest = open(scriptDir + "/master_twmanifest.json", "w+")
    TWManifest_json = {}
    os.makedirs(scriptDir + "/twassets/latest")

manifest_subdirectory = [x for x in sorted(os.listdir(scriptDir + "/_manifest/manifest/"),reverse=True)]
manifest_subdirectory_length = len(manifest_subdirectory)

def ManifestParser(current_manifest_json, Manifest_json, assetpath, manifest_date):
    master_assetdata = current_manifest_json['categories'][0]['assets']
    other_assetdata = current_manifest_json['categories'][1]['assets']
    raw_assetdata = current_manifest_json['rawAssets']
    for ix in master_assetdata:
        assetname = ix['name']
        assethash = ix['hash']
        HashIdentifier = assethash[:2]
        AssetPredictedPath = scriptDir + assetpath + "/latest/" + HashIdentifier + "/"
            
        if assetname in Manifest_json:
            pass
        else:
            if not os.path.exists(AssetPredictedPath):
                os.makedirs(AssetPredictedPath)
            DownloadURL = Master_URL + HashIdentifier + "/" + assethash
            DownloadPath = AssetPredictedPath + assethash
            while threading.active_count() >= 5:
                pass
            DownloadThread = threading.Thread(target=DownloadData, args=(Manifest_json, manifest_date, assetname, assethash, DownloadURL, DownloadPath))
            DownloadThread.start()     
    for ix in other_assetdata:
        assetname = ix['name']
        assethash = ix['hash']
        HashIdentifier = assethash[:2]
        AssetPredictedPath = scriptDir + assetpath + "latest/" + HashIdentifier + "/"
        if not os.path.exists(AssetPredictedPath):
            os.makedirs(AssetPredictedPath)
        if assetname in Manifest_json:
            pass
        else:
            if not os.path.exists(AssetPredictedPath):
                os.makedirs(AssetPredictedPath)
            DownloadURL = Master_URL + HashIdentifier + "/" + assethash
            DownloadPath = AssetPredictedPath + assethash
            while threading.active_count() >= 5:
                pass
            DownloadThread = threading.Thread(target=DownloadData, args=(Manifest_json, manifest_date, assetname, assethash, DownloadURL, DownloadPath))
            DownloadThread.start()
    for ix in raw_assetdata:
        assetname = ix['name']
        assethash = ix['hash']
        HashIdentifier = assethash[:2]
        AssetPredictedPath = scriptDir + assetpath + "/latest/" + HashIdentifier + "/"
        if assetname in Manifest_json:
            pass
        else:
            if not os.path.exists(AssetPredictedPath):
                os.makedirs(AssetPredictedPath)
            DownloadURL = Master_URL + HashIdentifier + "/" + assethash
            DownloadPath = AssetPredictedPath + assethash
            while threading.active_count() >= 5:
                pass
            DownloadThread = threading.Thread(target=DownloadData, args=(Manifest_json, manifest_date, assetname, assethash, DownloadURL, DownloadPath))
            DownloadThread.start()

# Process
iterator = 0
while iterator < manifest_subdirectory_length:
    currentName = manifest_subdirectory[iterator]
    manifest_date = currentName[:8]
    manifest_directory = scriptDir + "/_manifest/manifest/" + currentName
    
    JPcurrent_manifest = open(manifest_directory + "/assetbundle.manifest.json", "r")
    JPcurrent_manifest_json = json.load(JPcurrent_manifest)
    assetpath = "/masterassets/"
    ManifestParser(JPcurrent_manifest_json, JPManifest_json, assetpath, manifest_date)
    
    if Download_EN == 1:
        try:
            ENcurrent_manifest = open(manifest_directory + "/assetbundle.en_us.manifest.json", "r")
        except:
            print("The specified en_us manifest does not exist.")
            break
        ENcurrent_manifest_json = json.load(ENcurrent_manifest)
        assetpath = "/enassets/"
        ManifestParser(ENcurrent_manifest_json, ENManifest_json, assetpath, manifest_date)
    if Download_CN == 1:
        try:
            CNcurrent_manifest = open(manifest_directory + "/assetbundle.zh_cn.manifest.json", "r")
        except:
            print("The specified zh_cn manifest does not exist.")
            break
        CNcurrent_manifest_json = json.load(CNcurrent_manifest)
        assetpath = "/cnassets/"
        ManifestParser(CNcurrent_manifest_json, CNManifest_json, assetpath, manifest_date)
    if Download_TW == 1:
        try:
            TWcurrent_manifest = open(manifest_directory + "/assetbundle.zh_tw.manifest.json", "r")
        except:
            print("The specified zh_tw manifest does not exist.")
            break
        TWcurrent_manifest_json = json.load(TWcurrent_manifest)
        assetpath = "/twassets/"
        ManifestParser(TWcurrent_manifest_json, TWManifest_json, assetpath, manifest_date)
    print("Manifest " + currentName + " finished.")
    iterator += 1
    
New_JPManifest = json.dumps(JPManifest_json)
JPManifest.write(New_JPManifest)
if Download_EN == 1:
        New_ENManifest = json.dumps(ENManifest_json)
        ENManifest.write(New_ENManifest)
if Download_CN == 1:
        New_CNManifest = json.dumps(CNManifest_json)
        CNManifest.write(New_CNManifest)
if Download_TW == 1:
        New_TWManifest = json.dumps(TWManifest_json)
        TWManifest.write(New_TWManifest)
exit

# Enjoy!
#  - Ceris
