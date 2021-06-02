from selenium import webdriver
import random
import numpy as np
import time
from termcolor import colored
import discord_notify as dn
from datetime import datetime
import pyfiglet

ascii_banner = pyfiglet.figlet_format("MonitorFnac!", font = "slant")
print(colored(ascii_banner, "cyan"))

print("Veuillez entrer le webhook du chanel Discord concerné.")
notifier = dn.Notifier(str(input()))

def main (): 
  driver = webdriver.Chrome("./chromedriver")

  print("Veuillez entrer le PRID du produit que vous recherchez : (Exemple : 14119961 -> PS5 Digital // 14119956 -> PS5 Disc")
  prid = str(input())

  print("C'est partit\n")
  incrementation = 1

  heureOuverture = 8
  heureFermeture = 21

  pauseFermetureOuverture = heureOuverture + 24 - heureFermeture


  try:
    while True:
      now = datetime.now()
      date_time = now.strftime("%H")
      if(int(date_time) < heureFermeture  and int(date_time) >= heureOuverture):

        #Print l'itération dans laquelle nous sommes.
        print(colored("Nombre de ping : " + str(incrementation), "blue"))
        
        # 1 : Zone Paris
        get_info_on_fnac(driver, prid, "48.857187671206425", "2.348435546835592", 10, 20, "Paris")
        # 2 : Zone Lyon
        get_info_on_fnac(driver, prid, "45.75616798575563", "4.842348965490211", 10, 20, "Lyon")
        # 3 : Zone Marseille
        get_info_on_fnac(driver, prid, "43.28730182457255", "5.370048916331154", 10, 20, "Marseille")
        # 4 : Zone Toulouse
        get_info_on_fnac(driver, prid, "43.550575890617694", "1.3709180166120705", 10, 20, "Toulouse")
        #5 : Zone Bordeaux
        get_info_on_fnac(driver, prid, "44.7892784777663", "-0.5669863492124971", 10, 20, "Bordeaux")
        # 6 : Zone Rennes
        get_info_on_fnac(driver, prid, "48.064427729891605", "-1.6413239430975057", 10, 20, "Rennes")
        # 7 : Zone Le Havre
        get_info_on_fnac(driver, prid, "49.47893939669166", "0.15773592711100015", 10, 20, "Le Havre")
        #8 : Zone Reims
        get_info_on_fnac(driver, prid, "49.262266860598345", "3.9992169365206465", 10, 20, "Reims")
        # 9 : Zone Strasbourg
        get_info_on_fnac(driver, prid, "48.58704745769136", "7.722671973071056", 10, 20, "Strasbourg")
        # 10 : Zone Metz
        get_info_on_fnac(driver, prid, "49.100224923823035", "6.2259022369219075", 10, 20, "Metz")
        # 11 : Zone Dijon
        get_info_on_fnac(driver, prid, "47.34112542421955", "5.061042646922895", 10, 20, "Dijon")
        # 12 : Zone Lille
        get_info_on_fnac(driver, prid, "50.56866455968465", "3.1227685532252902", 10, 20, "Lille")
        # 13 : Zone Montpellier
        get_info_on_fnac(driver, prid, "43.58636668834572", "3.854646980812513", 10, 20, "Montpellier")
        # 14 : Zone Tours
        get_info_on_fnac(driver, prid, "47.40812805985102", "0.7185524954498579", 10, 20, "Tours")
        

        incrementation += 1 
      else : 
        notifier.send("Scipt en pause car Fnac fermé", print_message=True)
        time.sleep(60*60)


  except KeyboardInterrupt:
    notifier.send("Arrêt du script", print_message=True)
    pass
  

def mise_en_forme_string(prid, boutique):
  return "\n@everyone\nProduit qui a pour prid : " + prid + "\nDisponible à la boutique : " + boutique + "\nhttps://www.fnac.com/a" + prid + "\n"

def temps_dattente_aleatoire(minTemps, maxTemps):
  sleepTime = random.uniform(minTemps, maxTemps)
  time.sleep(sleepTime)

def get_info_on_fnac(driver, prid, latitudeVille, longitudeVille, minTemps, maxTemps, zone):  
  # Lien d'URL dynamique avec le PRID, la latitude et longitude. 
  link = 'https://www.fnac.com/Nav/API/KissRetreatStore/SearchStore?InputValue=.&Latitude=' + latitudeVille + '&Longitude=' + longitudeVille + '&Prid=' + prid + '&FnacPlusPrid=0&OnShlef=false&IsRetreatOneHour=false'

  driver.get(link)

  elementBody = driver.find_element_by_tag_name("body")

  # Si le produit est disponible dans la réponse reçue, nous allons noter quels magasins le propose. 
  if "En rayon" in elementBody.text :
    listDeLi = elementBody.find_elements_by_tag_name("li")
    for magasin in listDeLi:
      if "En rayon" in magasin.text :
        nomStore = magasin.find_element_by_class_name('storeName')
        notifier.send(mise_en_forme_string(prid, nomStore.text), print_message=True)
        time.sleep(0.1)
        

    print(colored("Produit disponible", "green"))

  # Cas où le produit est indisponible dans aucuns magasins renvoyés.  
  else : 
    print(colored("Produit NON disponible", "red"))

  print("Fin du scan de la zone : " + zone)
  temps_dattente_aleatoire(minTemps,maxTemps)
  
if __name__ == "__main__":
    main()