import pandas as pd

import requests
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup


BASE_URL = "https://www.cebm.net/oxford-covid-19/"

def get_links():
    page = requests.get(BASE_URL)   
    soup = BeautifulSoup(page.content)
 
    main_div = soup.find("div", id="mainMenu")  
     
    ev_service_div = main_div.find("div", {"class":"content twelve columns"})  

    ps = ev_service_div.find_all("p")
    uls = ev_service_div.find_all("ul")

    links = []
    for ul in uls: 
        for link_elem in ul.find_all("a"):
            links.append(link_elem.get("href"))
    return links 


links = oxford_cebm.get_links()

'''
<ul>
<li><a href="https://www.cebm.net/rapid-diagnosis-strategy-of-community-acquired-pneumonia-for-clinician/" rel="noopener noreferrer" target="_blank">Rapid diagnosis of community-acquired pneumonia for clinicians</a></li>
<li><a href="https://www.cebm.net/rapidly-managing-pneumonia-in-older-people-during-a-pandemic/" rel="noopener noreferrer" target="_blank">Rapidly managing pneumonia in older people during a pandemic</a></li>
<li><a href="https://www.cebm.net/wp-content/uploads/2020/03/Pneumonia-treatment-in-the-elderly-2.pdf" rel="noopener noreferrer" target="_blank">Pneumonia treatment in the elderly (2)</a> to download</li>
</ul>
'''