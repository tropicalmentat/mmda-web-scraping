from bs4 import BeautifulSoup
import urllib

tr_start = urllib.urlopen('http://mmdatraffic.interaksyon.com/line-view-edsa.php' \
                          ).read()                      

#website to spider: http://mmdatraffic.interaksyon.com/line-view-edsa.php
#code segment of interest is located from 264:271, div class "lnav"

tr_soup = BeautifulSoup(tr_start, "lxml")

#print type(tr_soup)

tr_sites = tr_soup.find("div", class_="lnav")

print tr_sites

#tr_link = tr_sites.find_all("a")

#print tr_link
