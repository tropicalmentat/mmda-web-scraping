#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import unicodecsv as csv
from datetime import date
import os

def newCSV(f):
    """Creates a new csv file with current date and time as suffix"""
    if os.path.exists(f):
        new_csv = f.split('_')
        new_csv[1] += '_'+date.today()

        return new_csv


site = 'http://mmdatraffic.interaksyon.com/line-view-edsa.php'

tr_start = urllib.urlopen(site).read()

#website to spider: http://mmdatraffic.interaksyon.com/line-view-edsa.php
#code segment of interest is located from 264:271, div class "lnav"

tr_soup = BeautifulSoup(tr_start, "lxml")

#print type(tr_soup)

tr_sites = tr_soup.find("div", class_="lnav")

line_link = tr_sites.find_all("div", class_="row")

#collect line links
links = []

for i in line_link:
    if "http:" in i.a["href"]:
        pass
    else:
        links.append(i.a["href"])
        #print i.a["href"]
    
#crawl through links and write data to csv

with open('test.csv', 'wb') as f:
    writer = csv.writer(f,delimiter=',')

    #write field names
    field_names = ['LINE','NB_STATUS','TIME_STAMP']
    writer.writerow(field_names)

    for link in links:
        try:
            tr_line = urllib.urlopen('http://mmdatraffic.interaksyon.com'
                                     +'/'+link).read().decode('utf-8')

            line_soup = BeautifulSoup(tr_line, "lxml")

            print '\n\n'+site+'/'+link+'\n\n'

            line_tr = line_soup.find_all("div", class_="line-row1")
            
            for element in line_tr:

                #scraping line name
                line_name = element.a.get_text().strip()

                #scraping north bound traffic status
                nb_stat = element.find("div", \
                                         class_="line-status").get_text().\
                                         split('\n')[2].strip()
                
                time_stamp = element.find("div", class_="line-col" \
                                          ).p.get_text().strip('Updated: ')

                #scraping south bound traffic status
                sb_stat = element.find("div",
                                       class_="line-status")

                tr_record = [line_name.decode,nb_stat,time_stamp]
                writer.writerow([line_name,nb_stat,time_stamp])

                print sb_stat
                #print line_name, ': ', nb_stat, ': ', time_stamp, '\n'

                ##needs scraper for service roads and accident notifications
        except:
            UnicodeEncodeError

