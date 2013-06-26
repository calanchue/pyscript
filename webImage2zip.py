"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""

from BeautifulSoup import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
import sys,getopt,os
from zipfile import ZipFile
from cStringIO import StringIO
from os import path
import string


class SiteCrawler():
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    def __init__(self, first_page_url):
        self.page_count = 1
        self.first_page_url = first_page_url
        self.curr_page_soup = bs(urlopen(first_page_url))
        self.curr_page_url = first_page_url
        self.parsed = list(urlparse.urlparse(first_page_url))
    
    """must override """
    def _getImageSourceUrl(self):
        pass
    
    """must override """
    def _getNextPageUrl(self):
        pass
    
    """optional override """
    def getTitle(self):
        return ''.join(c for c in self.parsed[2] if c in SiteCrawler.valid_chars)
        
    """return a next page url string. if there are not, return None"""
    def jumpToNextPage(self):
        url = self._getNextPageUrl()
        if not url:
            return None
        self.curr_page_soup = bs(urlopen(url))
        self.curr_page_url = url
        self.page_count += 1
        return self    
    
    def getCurrentPageNumber(self):
        return self.page_count
    
    def getFullImageUrl(self):
        raw_src = self._getImageSourceUrl().lower()
        if raw_src.startswith("http") or raw_src.startswith("https"):
            return raw_src
        else:
            self.parsed[2] = raw_src
            return urlparse.urlunparse(self.parsed)
    def getAllImageUrl(self):
        while(True):
            yield self.getFullImageUrl()
            if not self.jumpToNextPage():
                break

    
class CwNoah(SiteCrawler):
    def _getImageSourceUrl(self):
        pass
    
    def _getNextPageUrl(self):
        pass

class CwH2R(SiteCrawler):
    def _getImageSourceUrl(self):
        pass
        
    def _getNextPageUrl(self):
        pass
class CwEH(SiteCrawler):
    def _getImageSourceUrl(self):
        pass
        
    def _getNextPageUrl(self):
        pass

class CwGM(SiteCrawler):
    def _getImageSourceUrl(self):
        pass
    
    def _getNextPageUrl(self):
        pass

class CwDummy(SiteCrawler):
    def __init__(self):
        SiteCrawler.__init__(self, "http://noah.kaist.ac.kr/Circle/HAJE/seminar/1d1p")
        self.dummyUrl = ["/static/thumbs_desktop/547160/12_0.png",
                         "/static/thumbs_desktop/547160/12_1.png",
                         "/static/thumbs_desktop/547160/12_2.png"
                         ]
    
    def _getImageSourceUrl(self):
        if self.page_count - 1 < self.dummyUrl.__len__():
            return self.dummyUrl[self.page_count - 1]
        
    
    def _getNextPageUrl(self):
        if self.page_count < self.dummyUrl.__len__():
            return self.first_page_url

def crawlImg2Zip(crawler, target_dir):
    buf = StringIO()
    zip_file = ZipFile(buf, mode='w')
    
    for img_url in crawler.getAllImageUrl():
        image = urlopen(img_url)
        print "imgUrl : ", img_url
        ext = img_url.split(".")[-1]
        fname = path.basename("%03d.%s" % (crawler.getCurrentPageNumber(), ext))
        zip_file.writestr(fname, image.read())
    zip_file.close()
    
    zip_file_name = "%s.zip" % crawler.getTitle()
    output = open(os.path.join(target_dir, zip_file_name), 'wb')
    output.write(buf.getvalue())
    output.close()
    buf.close()

def crawlerFactory(first_page_url):
    if first_page_url.find("noah"):
        return CwDummy()    
    else:
        pass
    
    
def main(argv):
    target_urls = argv[0].strip().split(",")
    if len(argv) == 2:
        target_dir = argv[1]
    else:
        target_dir = os.getcwd()
        
    for url in target_urls:
        crawlImg2Zip(crawlerFactory(url), target_dir)
    
    #crawlImg2Zip(CwDummy(), out_folder)  

if __name__ == "__main__":
    main(sys.argv[1:])
