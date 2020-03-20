"""

scrapes content from NHS Covid information

"""
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
from urllib.parse import urljoin, urlparse
import datetime
from tika import parser
import uuid
import os
from readability import Document
import re
import pandas as pd
import tqdm



def sstrip(raw):
    if not isinstance(raw, str):
        return ""
    st = re.sub("\s\s+", "\n", raw)
    return st.strip()

def get_title(parsed):
    try:
        return parsed['metadata']['title']
    except:
        return ""
    

def get_file(url, out_path):
    r = requests.get(url, stream=True) 
    with open(out_path, "wb") as f: 
        for chunk in r.iter_content(chunk_size=1024): 
             if chunk: 
                 f.write(chunk)


def is_html(parsed):
    try:
        assert (parsed['metadata']['Content-Type'].startswith('text/html') or parsed['metadata']['Content-Type'].startswith('application/xhtml'))
        return True
    except:
        return False

def is_covid(parsed):
    try:
        assert(any((s in parsed['content'].lower() for s in ['covid', 'coronavirus'])))
        return True
    except:
        return False


def scrape(start_url, whitelist, outfile, datapath, depth=2):
    
    encountered = set()

    dataset = []

    stack = set([(start_url, "Main index", 0)])

    with tqdm.tqdm() as pbar:


        while stack:
            pbar.update(1)

                
            url, link_title, level = stack.pop()    
            stem, ext = os.path.splitext(url)    
            filename = f"{uuid.uuid4()}{ext}"
            try:  
                get_file(url, os.path.join(datapath, filename))    
            except (requests.exceptions.InvalidSchema, requests.exceptions.SSLError):
                continue
            parsed = parser.from_file(os.path.join(datapath, filename))

            if not is_covid(parsed):
                os.remove(os.path.join(datapath, filename))
                continue
                
            dataset.append(OrderedDict([("date", datetime.datetime.now().strftime("%Y-%m-%d")),
                                        ("url", url),
                                        ("title", get_title(parsed)),
                                        ("format", parsed['metadata']['Content-Type']),
                                        ("text", sstrip(parsed['content'])),
                                        ("filename", filename)
                                        ]))
            
            
            if is_html(parsed):
                
                with open(os.path.join(datapath, filename), 'r') as f:
                    soup = BeautifulSoup(f, features="lxml")
                links = soup.find_all('a')


                for link in links:

                    href = link.get('href')            
                    href = urljoin(url, href) # calculate relative references

                    domain = urlparse(href).netloc
                    if whitelist and not any((domain.endswith(urlend) for urlend in whitelist)):
                        continue


                    if href is None:
                        continue
                    elif href in encountered:
                        continue

                    encountered.add(href)



                    if href.startswith("#"):
                        continue
                    else:            
                        if level < depth:
                            stack.add((href, link.get('text'), level+1))


    df = pd.DataFrame(dataset)
    df.to_csv(outfile)
