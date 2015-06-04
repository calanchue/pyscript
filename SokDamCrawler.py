from bs4 import BeautifulSoup
import urllib
from collections import Counter
import csv
import sys
reload(sys)
#sys.setdefaultencoding('utf-8')

f = None

#-*- coding: utf-8 -*-
def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)


def crawlPage(letter,group,page):
    url = "http://krdic.naver.com/list.nhn?letter={0}&group={1}&kind=proverb&page={2}".format(letter, group, page)
    print url
    soup = getSoup(url);  
    qmap = {"class": "lst3"}
    rows = soup.find("ul", qmap).findAll("li", recursive = False)
    for row in rows:
        content = row.div.a.text
        print content
        f.write(content + "\n")


if __name__ == '__main__':
    f = open("sokdam.txt", 'w')
    
    orignalURL = "http://krdic.naver.com"
    soup = getSoup("http://krdic.naver.com/list.nhn?kind=proverb")

    
    #letter search
    letterList = []
    lList= soup.find("ul", {"class" : "tab_index2"}).findAll("li")
    for li in lList :
        s = li.a.text
        letterList.append(s)
        print str(unicode(s))
    

    
    for letter in letterList :
        #group search
        groupList = [];  
        soup = getSoup("http://krdic.naver.com/list.nhn?letter={0}&kind=proverb".format(letter));
        gList= soup.find("ul", {"class" : "lst_result "}).findAll("li")
        for li in gList :
            group = li.a.text[0:1]
            print str(unicode(group))
            
            pageSearchSoup = getSoup("http://krdic.naver.com/list.nhn?letter={0}&group={1}&kind=proverb".format(letter, group));
            lastPage = None
            #page number search
            paginate = pageSearchSoup.find("div", {"class" : "paginate"})
            if len(paginate.findAll("a")) == 0 : 
                continue
            while(True):
                paginate = pageSearchSoup.find("div", {"class" : "paginate"})
                nextButton = paginate.find("a", {"class" : "next"})
                if(nextButton is None):
                    lastPage = paginate.findAll(True, recursive = False)[-1].text
                    break;
                else :
                    pageSearchSoup = getSoup(orignalURL + nextButton["href"])
                    pass
            
            print "last page :  " + lastPage;
            
            for page in range(1, int(lastPage)+1):
                crawlPage(letter, group, page)
                
    
    
        
      
    
    f.close()    
    sys.exit();
    
    
        
    
    
    
    
    pass