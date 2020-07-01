#récuper danceability, energy, tempo, id
from lxml import etree
import urllib.request
import json
import sqlite3
import os
import sys
path = os.path.dirname(sys.argv[0])

def read_xml_file():
    """ Get TOP 50 tracks from xml file """
    list_TOP50_URL = []
    tree = etree.parse("https://dlsandboxweu002.blob.core.windows.net/spotify?restype=container&comp=list")
    for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
        if "top_50" in url.text: 
            list_TOP50_URL.append(url.text)  
    for album in list_TOP50_URL:
        print(album)
    return list_TOP50_URL


def read_xml_file2(): 
    """ Get songs tracks from xml file """  
    
    return list_songs_URL

path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify.db")
cur=bdd.cursor()

webURL = urllib.request.urlopen("https://dlsandboxweu002.blob.core.windows.net/spotify/raw/spotify/playlists/2020/06/23/top_50_france.json")
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
dic = json.loads(data.decode(encoding))
i = 0
j = 0


while i < len(dic["items"]):
    nom_artiste=[str(dic["items"][i]["track"]["artists"][j]["name"])]
    cur.execute("""INSERT INTO artiste (nom_artiste) VALUES(?)""",nom_artiste)
    données_titre=[str(dic["items"][i]["track"]["name"]),str(dic["items"][i]["track"]["duration_ms"]),str(dic["items"][i]["track"]["id"])]
    cur.execute("""INSERT INTO titre(nom_titre,durée,id_spotify) VALUES(?,?,?);""",données_titre)
    bdd.commit()
    i += 1
    j = 0

list_songs_URL = []
tree = etree.parse(path + "/spotify.xml")
for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
    if "songs" and "json" in url.text:
         list_songs_URL.append(url.text)


for url in list_songs_URL :
    webURL2 = urllib.request.urlopen(url)    
    data = webURL2.read()
    encoding = webURL2.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))
    i = 0
    j = 0
    if dic["error"] in dic :
        print("error")
    else :
        while i < len(dic["audio_features"]):
            bpmenergintens = [str(dic["audio_features"][i]["tempo"]),str(dic["audio_features"][i]["energy"]),str(dic["audio_features"][i]["loudness"]),str(dic["audio_features"][i]["id"])]
            cur.execute("""UPDATE titre SET bpm = ?, energie = ?, intensité = ? WHERE id_spotify= ?""",bpmenergintens)
            i += 1


cur.execute("""SELECT * from titre;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)
'''cur.execute("""SELECT artiste, COUNT(artiste) AS compte FROM test GROUP BY artiste;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)'''
cur.execute("""SELECT AVG(durée) AS Duree_moyenne FROM titre;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)