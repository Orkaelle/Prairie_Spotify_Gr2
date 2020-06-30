def read_xml_file():
    """ Get TOP 50 tracks from xml file """
    list_TOP50_URL = []
    tree = etree.parse("https://dlsandboxweu002.blob.core.windows.net/spotify?restype=container&comp=list")
    for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
        if "top_50" in url.text:
            list_TOP50_URL.append(url.text)
        if "songs" in url.text:
            list_songs_URL.append(url.text)
    for album in list_TOP50_URL:
        print(album)
    for songs in list_songs_URL :
        print(songs)
    return list_TOP50_URL




#récuper danceability, energy, tempo, id
from lxml import etree
import urllib.request
import json
import sqlite3
import os

bdd=sqlite3.connect("exemple.sqlite")
bdd.close()
os.remove("exemple.sqlite")
bdd=sqlite3.connect("exemple.sqlite")
cur=bdd.cursor()
cur.execute("""CREATE TABLE test( id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT, duration_ms INTEGER, artiste TEXT);""")
bdd.commit()

webURL = urllib.request.urlopen("https://dlsandboxweu002.blob.core.windows.net/spotify/raw/spotify/playlists/2020/06/23/top_50_france.json")
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
dic = json.loads(data.decode(encoding))
i = 0
j = 0


while i < len(dic["items"]):
    test=[str(dic["items"][i]["track"]["name"]),str(dic["items"][i]["track"]["duration_ms"]),str(dic["items"][i]["track"]["artists"][j]["name"])]
    cur.execute("""INSERT INTO test (titre,duration_ms,artiste) VALUES(?,?,?)""",test)
    bdd.commit
    i += 1
    j = 0

    
cur.execute("""SELECT * from test;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)
cur.execute("""SELECT artiste, COUNT(artiste) AS compte FROM test GROUP BY artiste;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)
cur.execute("""SELECT AVG(duration_ms) AS Duree_moyenne FROM test;""")
affichages=cur.fetchall()
for affichage in affichages :
     print(affichage)


    
'''webURL2 = urllib.request.urlopen("https://dlsandboxweu002.blob.core.windows.net/spotify/raw/spotify/songs/2020/06/23/06s3QtMJVXw1AJX3UfvZG1.json")    
data = webURL2.read()
encoding = webURL2.info().get_content_charset('utf-8')
dic = json.loads(data.decode(encoding))
i = 0
j = 0


while i < len(dic["audio_features"]):
    print("**")
    print(i)
    print(dic["audio_features"][i]["tempo"])
    i += 1
'''