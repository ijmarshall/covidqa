import string
import os 

import pandas as pd

import requests
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

import tika
from tika import parser

BASE_URL = "https://www.cebm.net/oxford-covid-19/"

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

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
    return soup.title.text

def get_pdf_from_link(page_url):
    soup = get_soup(page_url)
    ps = soup.find("div", {"class":"content twelve columns"}).find_all("p")
    for p in ps: 
        if "PDF to download" in p.text:
            pdf_url = p.find("a").get("href") 
            fname = os.path.split(pdf_url)[-1]
            path = os.path.join("..", "pdfs/{}".format(fname))
            download_pdf(pdf_url, path)
            return fname, path 

def download_pdf(pdf_url, out_path):
    r = requests.get(pdf_url, stream = True) 
      
    with open(out_path,"wb") as pdf: 
        for chunk in r.iter_content(chunk_size=1024): 
             if chunk: 
                 pdf.write(chunk)


def download_html(url, out_path):
    raw_html = requests.get(url).text
    with open(out_path, "w") as html_f:
        #import pdb; pdb.set_trace()
        html_f.write(str(raw_html))


def pull_all():

    links = get_links()
    print ("processing {} links".format(len(links)))
    dates, urls, titles, formats, pdfs, texts = [], [], [], [], [], []

    for link in links: 
        failed = False
        format_ = "pdf"
        print("\non link: {}".format(link))

        if link.endswith(".pdf"):
            print ("direct pdf")
            title = os.path.split(link)[-1].split(".pdf")[0]
            pdf_name = title + ".pdf"
            saved_pdf_path = "../pdfs/{}".format(pdf_name)
            download_pdf(link, saved_pdf_path)
        else:
            print("trying to pull pdf from webpage...")
            title = get_soup(link).title.text
            try:
                pdf_name, saved_pdf_path = get_pdf_from_link(link)
            except: 
                print("failed to get pdf for {}".format(link))
                print("attempting to pull html...")
                try: 
                    pdf_name = title + ".html"
                    saved_pdf_path = "../pdfs/{}".format(pdf_name)
                    download_html(link, saved_pdf_path)
                    format_ = "html"
                except:
                    print("no dice.")
                    failed = True 


        if not failed: 
            urls.append(link)
            titles.append(title)
            dates.append(today)
            formats.append(format_)
            pdfs.append(pdf_name)

            pdf_text = parser.from_file(saved_pdf_path)
            texts.append(pdf_text)

    return pd.DataFrame({"date":dates, "url":urls, "title":titles, "format": formats, "pdf":pdfs, "text":texts})

'''
Example use: 

> import oxford_cebm
> df = oxford_cebm.pull_all()
> df.head()

'''
