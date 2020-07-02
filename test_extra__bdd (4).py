#Libraries import
import urllib.request
import json
import sqlite3
import os
import sys
from lxml import etree


#Ouverture de la BDD
path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify.db") 
cur=bdd.cursor()


#Récupération des URL contenant "TOP_50"
list_TOP50_URL = []
tree = etree.parse(path + "/spotify.xml")
for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
    if "top_50" in url.text: 
        list_TOP50_URL.append(url.text) 
print("Récupération URL TOP50 OK")


#Lecture des données contenues dans les JSON
for top50 in list_TOP50_URL :
    webURL = urllib.request.urlopen(top50)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))
    i = 0
    j = 0
    if "error" in dic.keys() :
        print("lecture impossible")
    else :
        #Ecriture des données dans la BDD
        while i < len(dic["items"]):
            nom_artiste=[str(dic["items"][i]["track"]["artists"][j]["name"])]
            cur.execute("""INSERT OR IGNORE INTO artiste (nom_artiste) VALUES(?)""",nom_artiste)
            données_titre=[str(dic["items"][i]["track"]["name"]),str(dic["items"][i]["track"]["duration_ms"]),dic["items"][i]["track"]["id"]]
            cur.execute("""INSERT OR IGNORE INTO titre(nom_titre,durée,id_spotify) VALUES(?,?,?);""",données_titre)
            bdd.commit()
            i += 1
            j = 0
    

#Récupération des URL contenant "songs" et "json"
list_songs_URL = []
tree = etree.parse(path + "/spotify.xml")
for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
    if "songs" in url.text and "json" in url.text:
         list_songs_URL.append(url.text)
        

#Lecture des données contenues dans les JSON
for songs in list_songs_URL :
    webURL2 = urllib.request.urlopen(songs)    
    data = webURL2.read()
    encoding = webURL2.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))
    i = 0
    j = 0
    if "error" in dic.keys() :
        print("lecture impossible")
    else :
        #Ecriture des données dans la BDD
        while i < len(dic["audio_features"]):
            bpmenergintens = [str(dic["audio_features"][i]["tempo"]),str(dic["audio_features"][i]["energy"]),str(dic["audio_features"][i]["loudness"]),str(dic["audio_features"][i]["danceability"]),str(dic["audio_features"][i]["speechiness"]),str(dic["audio_features"][i]["liveness"]),str(dic["audio_features"][i]["valence"]),str(dic["audio_features"][i]["id"])]
            cur.execute("""UPDATE titre SET bpm = ?, energie = ?, intensité = ?, danceability = ?, speechiness = ? , liveness = ? , valence = ? WHERE id_spotify= ?""",bpmenergintens)
            bdd.commit()
            i += 1
