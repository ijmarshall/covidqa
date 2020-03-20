import pandas as pd

import requests
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

import os 

BASE_URL = "https://www.cebm.net/oxford-covid-19/"

def get_soup(url_):
    page = requests.get(url_)   
    return BeautifulSoup(page.content)


def get_links():
    soup = get_soup(BASE_URL)
    main_div = soup.find("div", id="mainMenu")  
     
    ev_service_div = main_div.find("div", {"class":"content twelve columns"})  

    ps = ev_service_div.find_all("p")
    uls = ev_service_div.find_all("ul")

    links = []
    for ul in uls: 
        for link_elem in ul.find_all("a"):
            links.append(link_elem.get("href"))
    return links 


def fetch_content_for_page(page_url):
    soup = get_soup(page_url)


def get_pdf_from_link(page_url):
    soup = get_soup(page_url)
    ps = soup.find("div", {"class":"content twelve columns"}).find_all("p")
    for p in ps: 
        if "PDF to download" in p.text:
            pdf_url = p.find("a").get("href") 
            fname = os.path.split(pdf_url)[-1]
            path = os.path.join("..", "pdfs/{}".format(fname))
            download_pdf(pdf_url, path)
            return fname 

def download_pdf(pdf_url, out_path):
    r = requests.get(pdf_url, stream = True) 
      
    with open(out_path,"wb") as pdf: 
        for chunk in r.iter_content(chunk_size=1024): 
             if chunk: 
                 pdf.write(chunk)



#links = oxford_cebm.get_links()

'''
<ul>
<li><a href="https://www.cebm.net/rapid-diagnosis-strategy-of-community-acquired-pneumonia-for-clinician/" rel="noopener noreferrer" target="_blank">Rapid diagnosis of community-acquired pneumonia for clinicians</a></li>
<li><a href="https://www.cebm.net/rapidly-managing-pneumonia-in-older-people-during-a-pandemic/" rel="noopener noreferrer" target="_blank">Rapidly managing pneumonia in older people during a pandemic</a></li>
<li><a href="https://www.cebm.net/wp-content/uploads/2020/03/Pneumonia-treatment-in-the-elderly-2.pdf" rel="noopener noreferrer" target="_blank">Pneumonia treatment in the elderly (2)</a> to download</li>
</ul>
'''