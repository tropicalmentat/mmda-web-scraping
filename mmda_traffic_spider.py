#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import unicodecsv as csv
from datetime import date
import os, re

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

#print tr_soup.prettify()

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
    field_names = ['LINE','SB_STATUS','NB_STATUS','TIME_STAMP']
    writer.writerow(field_names)

    for link in links:
        try:
            tr_line = urllib.urlopen('http://mmdatraffic.interaksyon.com'
                                     +'/'+link).read().decode('utf-8')

            line_soup = BeautifulSoup(tr_line, "lxml")

            print '\n\n'+site+'/'+link+'\n'

            line_tr = line_soup.find("div", class_="line-row1")
            # print line_tr.contents

            """
            for i in line_tr.contents:
                if i == u'\n':
                    pass
                else:
                    print i
            """

            siblings = line_tr.next_siblings

            #print type(siblings)
            for sibling in siblings:
                print sibling.


            line_name = line_soup.find_all('div', class_="line-name")[1:]
            # print line_name  # len(line_name)

            # retrieve traffic status per station
            nb_status = []
            sb_status = []
            tr_status = line_soup.find_all('div', class_="line-status")

            count = 0
            for i in tr_status:
                if i.contents[1]['id'].split('_')[2] == '1':
                    nb_status.insert(count, i.contents[-2].string)
                else:
                    sb_status.insert(count, i.contents[-2].string)

            # retrieve time stamp per traffic status
            nbtime_stamp = line_soup.find_all(string=re.compile("Updated"))
            #print len(time_stamp)

            sbtime_stamp = nbtime_stamp[len(nbtime_stamp)-1:]

            """
            for i in zip(line_name,sb_status,nb_status,time_stamp):
                writer.writerow([i[0].a.string,
                                 i[1].contents[-2].string,
                                 i[2].contents[-2].string,
                                 i[3].split(' ')[1]+i[3].split(' ')[2]])
            """

            # TODO:needs scraper for service roads and accident notifications
        except:
            UnicodeEncodeError

