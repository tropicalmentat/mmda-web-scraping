#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html 
from bs4 import BeautifulSoup
import urllib
from unidecode import unidecode

mmda = unidecode(urllib.urlopen('http://mmdatraffic.interaksyon.com/line-view-edsa.php \
                      ').read().decode('utf-8'))
soup = BeautifulSoup(mmda, "lxml")

#print soup, '\n'

line_tr = soup.find_all("div", class_="line-row1")
print '\n', type(line_tr), '\n'

for element in line_tr:

    line_name = element.a.get_text().strip() #scraping line name

    #scraping traffic status
    line_stat = element.find("div", \
                             class_="line-status").get_text().\
                             split('\n')[2].strip()
    
    time_stamp = element.find("div", class_="line-col" \
                              ).p.get_text().strip('Updated: ')
    
    print line_name, ': ', line_stat, ': ', time_stamp, '\n'
