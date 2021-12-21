import requests
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from imdb import IMDb
from requests.api import request

#################
#################
# https://www.geeksforgeeks.org/python-imdbpy-getting-title-from-searched-movie/
# for the movie posters ^
#################
#################



###-Functions-###

def cleanup(id):
    separation = [id[i:i+2] for i in range(0, len(id), 2)]
    date = "/".join([separation[3], separation[2]])
    hour = ":".join(separation[4:6])
    return date, hour




#########################-Prog-#########################
###-Getting the programs part-###
url = "https://xmltv.ch/xmltv/xmltv-complet_1jour.xml"
rawXML = requests.get(url)
root = ET.fromstring(rawXML.content)


channelsDict = {}
channelIcons = {}
progList = []
wantedInfos = ('title', 'sub-title', 'category', 'desc',  'date', 'lenght')



current = []
tonight = []



for child in root:
    ##-Récupère la chaine qui va avec l'ID si on est sur une chaine-##
    if child.get('id') != None:
        channelsDict[child.get('id')] = child[0].text
        channelIcons[child[0].text] = child[1].attrib['src']

    ##-Récupère les infos du programme puis l'ajoute à une liste de programmes-##
    elif child.get("channel") != None:
        ##-Récupère les heures et la chaine du programme-##
        start = cleanup(child.get('start'))
        stop = cleanup(child.get('stop'))
        channel = channelsDict[child.get('channel')]
        channelIcon = channelIcons[channel]
        progDict = {'channel': channel,
                    'icon' : channelIcon,
                    'start' : start,
                    'stop' : stop
                    }
        ###################################################


        ##-Enlève les chaines x-##
        if 'brazzers' in progDict['channel'].lower() or 'XXL' in progDict['channel'].upper():
            continue
        ##########################    


        ##-Récupère les infos qu'on veut sur le programme-##
        for wanted in wantedInfos:
            if child.find(wanted) != None:
                progDict[wanted] = child.find(wanted).text
            else:
                progDict[wanted] = "empty"    
        #####################################################
        
        
        ##-Trie les programmes selon si ils passent maintenant ou ce soir, aurait besoins d'être amélioré pour le maintenant-##
        progHour = int(progDict['start'][1][:2])
        progMinutes = int(progDict['start'][1][3:])
        progEndMins = int(progDict['stop'][1][3:])
        progEndHours = int(progDict['stop'][1][:2])
    
        currentHours = int(datetime.now().strftime("%H"))
        currentMins = int(datetime.now().strftime("%M"))

        if progHour <= currentHours <= progEndHours:
            current.append(progDict)

        if 20 <= progHour and progMinutes > 40 or 23 > progHour >= 21:
            tonight.append(progDict)
        #########################################################################################################################




        progList.append(progDict)   #Rajoute le programme a la liste complete des programmes


##-Récupère l'url du poster du film sur IMDB, si il ne trouve pas le film le poster sera un fond vert. Aurait besoins d'optimisation-##
for movie in current:
    movieInfos = IMDb().search_movie(movie['title'])
    if len(movieInfos) == 0:
        continue
    else: movieInfos = movieInfos[0]
    PosterUrlRequest = "https://api.themoviedb.org/3/find/tt" + movieInfos.movieID + "?api_key=f310b2f9d87f92ebb5f2c1a036cf95be&external_source=imdb_id"

    JsonRequest = urlopen(PosterUrlRequest).read()
    JsonRequest = json.loads(JsonRequest)

    if len(JsonRequest['movie_results']) < 1:
        movie['poster'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/1200px-Solid_green.svg.png"
        continue
    if 'poster_path' in JsonRequest['movie_results'][0] and JsonRequest['movie_results'][0]['poster_path'] != None:
        posterURL = "http://image.tmdb.org/t/p/original" + JsonRequest['movie_results'][0]['poster_path']
        movie['poster'] = posterURL
        print('Getting poster for', movie['title'])
    else:
        movie['poster'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/1200px-Solid_green.svg.png"


for movie in tonight:
    movieInfos = IMDb().search_movie(movie['title'])
    if len(movieInfos) == 0:
        continue
    else: movieInfos = movieInfos[0]
    PosterUrlRequest = "https://api.themoviedb.org/3/find/tt" + movieInfos.movieID + "?api_key=f310b2f9d87f92ebb5f2c1a036cf95be&external_source=imdb_id"

    JsonRequest = urlopen(PosterUrlRequest).read()
    JsonRequest = json.loads(JsonRequest)

    if len(JsonRequest['movie_results']) < 1:
        movie['poster'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/1200px-Solid_green.svg.png"
        continue
    if 'poster_path' in JsonRequest['movie_results'][0] and JsonRequest['movie_results'][0]['poster_path'] != None:
        posterURL = "http://image.tmdb.org/t/p/original" + JsonRequest['movie_results'][0]['poster_path']
        movie['poster'] = posterURL
        print('Getting poster for', movie['title'])
    else:
        movie['poster'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Solid_green.svg/1200px-Solid_green.svg.png"
##########################################################################################################################################



##-A rajouter pour l'instant: mettre les chaines dans l'ordre, pourquoi pas supprimer les chaines "inutiles"-##