import urllib, json

def get_schema():
    url = "https://raw.githubusercontent.com/overture-stack/SONG/develop/song-server/src/main/resources/schemas/sequencingRead.json"
    response = urllib.urlopen(url)
    return  json.loads(response.read())