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


def remove_space(l):
    for elm in l:
        if elm == '\n':
            l.remove(elm)
    return l

site = 'http://mmdatraffic.interaksyon.com/line-view-edsa.php'

tr_start = urllib.urlopen(site).read()  #TODO: handle IO error

# website to spider: http://mmdatraffic.interaksyon.com/line-view-edsa.php
# code segment of interest is located from 264:271, div class "lnav"

tr_soup = BeautifulSoup(tr_start, "lxml")

#print tr_soup.prettify()

tr_sites = tr_soup.find("div", class_="lnav")

line_link = tr_sites.find_all("div", class_="row")

# collect line links
links = []

for i in line_link:
    if "http:" in i.a["href"]:
        pass
    else:
        links.append(i.a["href"])
        #print i.a["href"]
    
# crawl through links and write data to csv

with open('test.csv', 'wb') as f:
    writer = csv.writer(f,delimiter=',')

    # write field names
    field_names = ['LINE', 'SB_STATUS', 'NB_STATUS', 'TIME_STAMP']
    writer.writerow(field_names)

    for link in links:
        try:
            tr_line = urllib.urlopen('http://mmdatraffic.interaksyon.com'
                                     +'/'+link).read().decode('utf-8')

            line_soup = BeautifulSoup(tr_line, "lxml")

            print '\n\n'+site+'/'+link+'\n'

            # find first line data
            traffic_status = line_soup.find("div", class_="line-row1").contents
            # the first child is the line name
            # the second child is the southbound status
            # the third child is the northbound status
            # the timestamps of each status is embedded in the p tag

            # remove child spaces
            remove_space(traffic_status)

            line_name = traffic_status[0].a.string
            sb_status = remove_space(traffic_status[1].find('div',
                                                            class_='line-status').
                                     contents)[-1].string
            sb_timestamp = traffic_status[1].p.string
            nb_status = remove_space(traffic_status[2].find('div',
                                                            class_='line-status').
                                     contents)[-1].string
            nb_timestamp = traffic_status[2].p.string
            print "%s|%s|%s|%s|%s" % (line_name,
                                sb_status, sb_timestamp,
                                nb_status, nb_timestamp)

            # find data for each sibling of the first
            line_sib = line_soup.find("div", class_="line-row1").next_siblings
            for sibling in line_sib:
                if sibling == '\n':
                    pass
                else:
                    sibling_status = remove_space(sibling.contents)
                    line_name = sibling_status[0].a.string
                    sb_status = remove_space(sibling_status[1].find('div',
                                                    class_='line-status').
                                             contents)[-1].string
                    sb_timestamp = sibling_status[1].p.string
                    nb_status = remove_space(sibling_status[2].find('div',
                                                    class_='line-status').
                                             contents)[-1].string
                    nb_timestamp = sibling_status[2].p.string
                    print "%s|%s|%s|%s|%s" % (line_name,
                                              sb_status, sb_timestamp,
                                              nb_status, nb_timestamp)



            # loop to inspect the html structure of line status
            # to be used when there is a change in the over structure
            # of the website
            """
            count = 1
            for child in traffic_status.contents:
                if child == '\n':  # ignore the space between tags
                    pass
                else:
                    print "%d.%s" % (count, child)
                    count += 1
            """

            #for i in zip(line_name, sb_status, nb_status):
             #   writer.writerow([i[0].a.string, i[1], i[2]])

            # TODO:needs scraper for service roads and accident notifications
        except:
            UnicodeEncodeError

