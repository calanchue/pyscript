import urllib
import urllib2
import sys
import time
import argparse
from os import path
from urlparse import parse_qs, urljoin
from urlparse import urlparse
from urllib2 import URLError
import dns.resolver
from bs4 import BeautifulSoup
from socket import getaddrinfo

ip_count = {}

def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('url', metavar='url', type=str, help='')
    argvs = parser.parse_args()
    str_url = argvs.url
    str_url = "http://www.w3schools.com/xpath/xpath_syntax.asp"
    str_url = "https://www.google.co.kr/maps/@36.3731,127.3888,12z"
    str_url = "https://www.google.co.kr/drive/using-drive/"
    str_url = "https://news.google.com/"
    parsed_uri = urlparse( str_url)
    mianDomain = '{uri.netloc}'.format(uri=parsed_uri)
    
    
    print str_url
    soup = getSoup(str_url)
    #print soup
    images = soup.findAll("img")
    for image in images:

        
        if image.has_attr("src") :
            src = image["src"]
            str_src = str(src)
            src = urljoin(str_url, str_src)
                
            print src
            #print getaddrinfo(src, None)
            
            parsed_uri = urlparse( src)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            for address_type in ['A']:
                try:
                    answers = dns.resolver.query(domain, address_type)
                    ip = ""
                    for rdata in answers:
                        ip = rdata
                    print ip
                    str_ip = str(ip)           
                    if( str_ip in  ip_count):
                        ip_count[str_ip] += 1
                    else : 
                        ip_count[str_ip] = 1
                except dns.resolver.NoAnswer:
                    pass
    
    scripts = soup.findAll("script")
    for script in scripts:                
        if script.has_attr("src"):
            src = script["src"]
            src = urljoin(str_url, str_src)
            
            print src
            parsed_uri = urlparse(src)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            for address_type in ['A']:
                try:
                    answers = dns.resolver.query(domain, address_type)
                    ip = ""
                    for rdata in answers:
                        ip = rdata
                    print ip           
                    str_ip = str(ip)           
                    if( str_ip in  ip_count):
                        ip_count[str_ip] += 1
                    else : 
                        ip_count[str_ip] = 1
                except dns.resolver.NoAnswer:
                    pass
                
    styles = soup.findAll("style")
    for style in styles:                
        if style.has_attr("src"):
            src = style["src"]
            str_src = str(src)
            src = urljoin(str_url, str_src)
            
            print src
            parsed_uri = urlparse(src)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            for address_type in ['A']:
                try:
                    answers = dns.resolver.query(domain, address_type)
                    ip = ""
                    for rdata in answers:
                        ip = rdata
                    print ip           
                    str_ip = str(ip)           
                    if( str_ip in  ip_count):
                        ip_count[str_ip] += 1
                    else : 
                        ip_count[str_ip] = 1
                except dns.resolver.NoAnswer:
                    pass            
    
    print ""
    
    f = open("web_page_ip_count.txt", 'w')
    for x in ip_count:
        print (x) + ", " +str(ip_count[x])
        f.write((x) + ", " +str(ip_count[x])+ "\n")    
    