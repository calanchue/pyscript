"""
webImage2zip.py
    Downloads all the images on the supplied URL which is the first page of manga, comic. 
    and saves them to the specified directory as zip file. 

Usage:
    first argument : the url of the first page you want to downlaod. 
    comma separated input will be resolved as multiple input.   
    second argument : target directory.  
    python "www.abcd.com/some_comic_or_manga/1, www.abcd.com/other_comic_or_manga/1" "c://mangaOrComic/" 
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
        """it can be that constructor throw exception, if the given url is uncomphrensible"""
        self.page_count = 1
        self.first_page_url = first_page_url
        self.curr_page_soup = bs(urlopen(first_page_url))
        self.curr_page_url = first_page_url
        self.parsed = list(urlparse.urlparse(first_page_url))
    
    
    def _getImageSourceUrl(self):
        """must override """
        pass
    
    
    def _getNextPageUrl(self):
        """must override """
        pass
       
    
    def getTitle(self):
        """optional override """
        return ''.join(c for c in self.parsed[2] if c in SiteCrawler.valid_chars)
        
    
    def jumpToNextPage(self):
        """return a next page url string. if there are not, return None"""
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
    
    def getTitle(self):
        return "_".join(self.curr_page_url.split("/")[-3,-2])
    
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
    
from Tkinter import Tk
from tkFileDialog import askdirectory
import thread

def main(argv):
    if len(argv) == 0:
        Tk().withdraw()
        print "interactive mode"
        target_dir = askdirectory()
        print "directory : ",  target_dir
        while True :
            url = raw_input("give me url : ")
            thread.start_new_thread(crawlImg2Zip, (crawlerFactory(url),target_dir) )    
        
        
    else:
        target_urls = argv[0].strip().split(",")
        if len(argv) == 2:
            target_dir = argv[1]
        else:
            target_dir = os.getcwd()
            
        for url in target_urls:
            try:
                crawlImg2Zip(crawlerFactory(url), target_dir)
            except Exception as e:
                print "FAIL : ", url
                print e
            
    
    #crawlImg2Zip(CwDummy(), out_folder)  

if __name__ == "__main__":
    main(sys.argv[1:])
