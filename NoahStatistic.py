from bs4 import BeautifulSoup
import urllib

def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)

class Article:
    def __init__(self, subject, writer, time ,hit):
        self.subject=subject
        self.writer=writer
        self.time=time
        self.hit=hit

    def __str__(self):
        return ", ".join([self.subject, self.writer, self.time, self.hit])

def getInfo() :
    soup = getSoup("http://noah.kaist.ac.kr/Circle/HAJE/seminar/1d1p")
    qmap = {"class": "listlink"}
    max_page = soup.find("a", qmap).text
    max_page = int(max_page)
    list = []
    for page_num in xrange(1,max_page+1):
        print page_num, "="*10
        soup = getSoup("http://noah.kaist.ac.kr/Circle/HAJE/seminar/1d1p?page="+str(page_num))
        rows = soup.find("table").findAll("tr")
        for row in rows[1:]:
            cols = row.findAll('td')
            subject= cols[1].text
            writer= cols[2].text
            time = cols[3].text
            hit = cols[4].text
            article = Article(subject, writer, time, hit)
            list.append(article)
            print  article.__str__().encode('utf8')
        print page_num, "="*10
    print "max_page", max_page

