#!/usr/bin/env python3

from m3u import parse_radios
from browser import get_radio
import json
from time import sleep
import os
import uuid

def write_to_file(file, data):
    f = open(file, "w")
    if isinstance(data, list) or isinstance(data, dict):
        str_data = json.dumps(data)
    elif isinstance(data, str):
        str_data = data
    else:
        str_data = str(data)
    f.write(str_data)
    f.close()

def read_file(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data

def m3u_to_json(file):
    data = parse_radios("file.m3u")
    tab = []
    for i in data:
        if i["uuid"] != "":
            radio = get_radio(i["uuid"])
            sleep(0.5)
            if not isinstance(radio, str):
                tab.append(radio)
            else:
                print(radio)
    return tab

def codec_content(codec):
    if codec == "MP3":
        return "audio/mpeg"
    elif "AAC" in codec:
        return "audio/aac"
    else:
        return ""

def create_collection(path, file):
    data = json.loads(read_file(file))
    prefix = "file:///storage/emulated/0/Android/data/org.y20k.transistor/files/images/"
    new = {
        "modificationDate": "4/2/24 10:47 PM",
        "stations": [],
        "version": 0
    }
    os.mkdir(path)
    os.mkdir(f"{path}/images")
    os.mkdir(f"{path}/collection")
    for j in data:
        i = j[0]
        uid = str(uuid.uuid4())
        new["stations"].append({})
        new["stations"][-1] = {
            "homepage": i["homepage"],
            "image": prefix+uid+"/station-image.jpg",
            "imageColor": -1007576,
            "imageManuallySet": False,
            "isPlaying": False,
            "modificationDate": "4/2/24 10:46 PM",
            "name": i["name"],
            "nameManuallySet": False,
            "radioBrowserChangeUuid": i["changeuuid"],
            "radioBrowserStationUuid": i["stationuuid"],
            "remoteImageLocation": i["favicon"],
            "remoteStationLocation": i["url"],
            "smallImage": prefix+uid+"/station-image-small.jpg",
            "starred": False,
            "stream": 0,
            "streamContent": codec_content(i["codec"]),
            "streamUris": [i["url"]],
            "uuid": uid
        }
        os.mkdir(f"{path}/images/{uid}")
    write_to_file(f"{path}/collection/collection.json", new)

def collection_to_m3u(collection, file):
    f = open(collection, "r")
    data = json.loads(f.read())
    f.close()
    f = open(file, "a")
    f.write("#EXTM3U")
    for i in data["stations"]:
        f.write("\n")
        uid = i["radioBrowserStationUuid"]
        f.write(f"#RADIOBROWSERUUID:{uid}\n")
        name = i["name"]
        f.write(f"#EXTINF:-1,{name}\n")
        url = i["remoteStationLocation"]
        f.write(f"{url}\n")
    f.close()

if __name__ == "__main__":
    """
    json_raw = json.dumps(m3u_to_json("file.m3u"))
    f = open("file.json", "w")
    f.write(json_raw)
    f.close()
    """
    #create_collection("fold3", "browser.json")
    collection_to_m3u("folder/collection/collection.json", "file2.m3u")
