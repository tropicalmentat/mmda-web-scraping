from bs4 import BeautifulSoup
import urllib

site = 'http://mmdatraffic.interaksyon.com/line-view-edsa.php'

tr_start = urllib.urlopen(site).read()                      

#website to spider: http://mmdatraffic.interaksyon.com/line-view-edsa.php
#code segment of interest is located from 264:271, div class "lnav"

tr_soup = BeautifulSoup(tr_start, "lxml")

#print type(tr_soup)

tr_sites = tr_soup.find("div", class_="lnav")

line_link = tr_sites.find_all("div", class_="row")

links = []

for i in line_link:
    links.append(i.a["href"])
    if "http" in i.a["href"]:
        pass
    
    print i.a["href"]
    

print links
