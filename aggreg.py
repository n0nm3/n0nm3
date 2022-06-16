import feedparser as fp
import sys 
import time as tm

def charge_urls(liste_url):
    flux = []
    for element in liste_url:
        nv_flux = None      
        nv_flux = fp.parse("http://"+element+'/rss.xml')        
        verif = False
        if nv_flux["bozo"] == 0:
            verif = True
        if verif == False:
            flux.append(None)
        else:
            flux.append(nv_flux)
    return flux


def fusion_flux(liste_url, liste_flux):
    liste_retour = []
    url = 0
    for flux_rss in liste_flux:
        if flux_rss == None:
            print("None")
        else:
            for i in flux_rss.keys():
                if i == "entries":
                    for liste in flux_rss[i]:
                        dico = {}
                        for element in liste:
                            if element == "title":
                                v = liste[element]
                                dico["titre"] = v
                            elif element == "link":
                                v = liste[element]
                                dico["lien"] = v
                            elif element == "summary":
                                v = liste[element]
                                dico["description"] = v
                            elif element == "published":
                                v = liste[element]
                                dico["date_publi"] = v
                            elif element == "tags":
                                for tag in liste[element]:
                                    for key in tag.keys():
                                        if key == "term":
                                            v = tag[key]
                                            dico["categorie"] = v
                                            dico["serveur"] = liste_url[url]
                        liste_retour.append(dico)
        url+=1
    print(liste_url)
    return liste_retour

def genere_html(liste_evenements, chemin_html):
    page_element = ""
    time = tm.strftime("%A %B, %y")
    for element in liste_evenements:
        uid = element["lien"]
        guid = ""
        for i in uid[20:]:
            guid = guid + i
        p_el = '<article>\n <header>\n <h2>'+ element["titre"] + '</h2>\n </header>\n  <p>from:' + element["serveur"] + '</p> <p>'+ element["date_publi"]+'</p><p>' + element["categorie"] + '</p> <p>' + guid +'</p> <p><a href="' + element["lien"] + '">' + element["lien"] + '</a></p><p>' + element["description"] + '</p>'
        page_element = page_element + p_el
    page = '<html>\n <head>\n <meta charset="utf-8">\n <meta name="viewport" content="width=device-width, initial-scale=1">\n <title>Event log </title>\n <link rel="stylesheet" href="css/feed.css" type="text/css"> </head> <body> <article>\n <header>\n <h1>Events log</h1>\n </header>\n <p>'+time+'</p>\n'+ page_element +'</article>\n</body></html>'
    x = open(chemin_html,"w")
    x.write(page)
    x.close()
    return x


def main():
    """liste_url = ["serveur1.net","toto.net"]"""
    liste_url = sys.argv[1:] 
    x = charge_urls(liste_url)
    r = fusion_flux(liste_url, x)
    h = genere_html(r,"/var/www/html/index.html")

if __name__ == "__main__":
    main()


