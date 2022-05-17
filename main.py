import urllib.request
from bs4 import BeautifulSoup
from time import time, sleep
from queue import Queue
from urllib.parse import urlparse

class time_past_connection: 
    time = time()

rate_limt = 10 

def rate_limit(link):
    retention = time_past_connection.time - time() + 60 / rate_limt
    if (retention>0):
        sleep(retention)
    stranitsa = urllib.request.urlopen(link).read()
    time_past_connection.time = time()
    return stranitsa
    
def extract_language (link):
    raspars_link=urlparse(link)
    return raspars_link.hostname[0:1]

def poisk(start_link, end_link, max_len):
    spisok_poseh_link=[]
    queue = Queue()
    queue.put([start_link])
    while queue:
        marshrut = queue.get()
        try:
            stranitsa = rate_limit(marshrut[-1])
        except Exception:
            continue
        pasr=BeautifulSoup(stranitsa,'html.parser')
        osn_content = pasr.find('div',id='bodyContent')
        spisok_doch_link = osn_content.findAll('a')
        for doch_link in spisok_doch_link:
            link_sting=doch_link.get('href')
            if (not link_sting):
                continue
            if (link_sting[0] == '#'):
                continue
            if (link_sting[0] == '/'):
                temp = link_sting
                link_sting= 'https://en.wikipedia.org' + temp
            if (link_sting.find('wikipedia.org') == -1):
                continue
            if (extract_language(link_sting)!= extract_language(start_link)):
                continue
            if (link_sting in spisok_poseh_link or len(marshrut)>= max_len-1):
                continue
            spisok_poseh_link.append(link_sting)
            queue.put(marshrut+[link_sting])
            if (link_sting == end_link):
                marshrut=marshrut+[link_sting]
                return marshrut
    return []
        
            

def main ():
    start_link = input('Input start URL:')
    end_link = input ('Input end URL:')
    if(extract_language(start_link)!= extract_language(end_link)):
        print ('Different language')
        exit(1)
    rate_limt = int(input('Input rate limit:'))
    result=poisk(start_link, end_link, 5)
    print (*result,sep=" => ")
    

main()
