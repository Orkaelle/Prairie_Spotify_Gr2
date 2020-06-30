# CREATION DE LISTE D'ARTISTES
artistes = ["nomartiste1","nomartiste2","nomartiste3","nomartiste4"]
print (artistes)

# FORMATAGE DE LA LISTE ARTISTE POUR L'IMPORT SQLITE
for i in artistes :
    importArtistes = '(' + str(artistes.index(i)+1) + ' , "' + i + '")'
print(importArtistes)



# CREATION DE LISTE DE TITRES
titres = [["Cette année là",1,3.49,9.32,3.54,5.65],["nomtitre2"],["nomtitre3"],["nomtitre4"]]
print (titres)

# FORMATAGE DE LA LISTE ARTISTE POUR L'IMPORT SQLITE
for i in titres :
    importTitres = '(' + str(titres.index(i)+1) + ' , "' + i + '")'
print(importTitres)