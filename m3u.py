#!/usr/bin/env python3

def append_radio(file, name, url, uuid):
    new_content = ""
    f = open(file, "r")
    content = f.readlines()
    for i in content:
        if i == "#RADIOBROWSERUUID:"+uuid+"\n":
            return False

    if content[-1] != "\n":
        new_content += "\n"
    f.close()
    f = open(file, "a")
    new_content += f"#RADIOBROWSERUUID:{uuid}\n#EXTINF:-1,{name}\n{url}\n"
    f.write(new_content)
    f.close()
    return True

def remove_radio(file, uuid):
    new_content = ""
    f = open(file, "r")
    content = f.readlines()
    radio_delete = False
    for i in content:
        if i == "#RADIOBROWSERUUID:"+uuid+"\n":
            radio_delete = True
        elif i == "\n" and radio_delete:
            radio_delete = False
        elif not radio_delete:
            new_content += i
    f.close()
    f = open(file, "w")
    f.write(new_content)


def parse_radios(file):
    radios = []
    f = open(file, "r")
    for i in f.read().split("\n\n"):
        data = i.split("\n")
        uuid = ""
        name = ""
        url  = ""
        for j in data:
            if j.startswith("#RADIOBROWSERUUID"):
                uuid = j.split(":")[-1]
            if j.startswith("#EXTINF:-1,"):
                name = j.replace("#EXTINF:-1,", "")
            elif j != "" and j != None:
                url = j
        radios.append({
            "uuid": uuid,
            "name": name,
            "url": url
        })
    return radios



if __name__ == "__main__":
    uuid = "f1db7f30-672c-4406-9419-22ccc6fda025"
    name = "KUTX 98.9 FM"
    url = "https://kut.streamguys1.com/kutx-free.aac"
    file = "file2.m3u"
    uuid = "5b9ceedf-eb85-11e9-a96c-52543be04c81"
    #print(append_radio(file, name, url, uuid))
    #remove_radio(file, uuid)
    print(parse_radios("file.m3u"))
