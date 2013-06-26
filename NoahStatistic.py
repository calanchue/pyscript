from bs4 import BeautifulSoup
import urllib
from collections import Counter
import csv

def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)

class Article:
    def __init__(self, subject, reply, writer, time ,hit):
        self.subject=subject
        self.reply = reply
        self.writer=writer
        self.time=time
        self.hit=hit

    def __str__(self):
        return ", ".join([self.subject, self.reply, self.writer, self.time, self.hit])

def getInfo() :
    soup = getSoup("http://noah.kaist.ac.kr/Circle/HAJE/seminar/1d1p")
    qmap = {"class": "listlink"}
    max_page = soup.find("a", qmap).text 
    max_page = int(max_page)+1 #listlink+1 page is exact page.  
    
    list = []
    user_count = {}
    
    for page_num in xrange(1,max_page+1):
        print page_num, "="*10
        soup = getSoup("http://noah.kaist.ac.kr/Circle/HAJE/seminar/1d1p?page="+str(page_num))
        rows = soup.find("table").findAll("tr")
        
        currName = None
        currHit = 0
        currDate = None
        maxName = 0
        maxHit = 0
        
        for row in rows[1:]:
            cols = row.findAll('td')
            subject= cols[1].text
            subject= subject.split('\n')
            
            if currName is not subject[1]:
                if maxHit < currHit:
                    maxHit=currHit
                    maxName=currName
                currName = subject[1]
                currHit = 1
                
            writer= cols[2].text
            time = cols[3].text
            
            hit = cols[4].text
            article = Article(subject[1],subject[4][1:-1], writer, time, hit)
            list.append(article)
            print  article.__str__().encode('utf8')
        print page_num, "="*10
    print "max_page", max_page
    
    o = open("NS.csv", "wb")
    c = csv.writer(o)
    count_list = []
    c.writerow(["subject", "reply", "writer", "time", "hit"])
    for a in list:
        count_list.append(a.writer)
        c.writerow([a.subject.encode('ms949'), a.reply, a.writer, a.time, a.hit])
    print Counter(count_list)
    o.close()

getInfo()
