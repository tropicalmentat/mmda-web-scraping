from bs4 import BeautifulSoup
import urllib
import csv

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
    
#crawl through links

with open('test.csv', 'wb') as f:
    writer = csv.writer(f,delimiter=',')

    #write field names
    field_names = ['LINE','STATUS','TIME_STAMP']
    writer.writerow(field_names)

    for link in links:
        try:
            tr_line = urllib.urlopen('http://mmdatraffic.interaksyon.com'
                                     +'/'+link).read()

            line_soup = BeautifulSoup(tr_line, "lxml")

            print '\n\n'+site+'/'+link+'\n\n'

            line_tr = line_soup.find_all("div", class_="line-row1")
            
            for element in line_tr:

                #scraping line name
                line_name = element.a.get_text().strip() 

                #scraping traffic status
                line_stat = element.find("div", \
                                         class_="line-status").get_text().\
                                         split('\n')[2].strip()
                
                time_stamp = element.find("div", class_="line-col" \
                                          ).p.get_text().strip('Updated: ')
                
                print line_name, ': ', line_stat, ': ', time_stamp, '\n'
                tr_record = [line_name,line_stat,time_stamp]
                writer.writerow([line_name,
                                  line_stat,
                                 time_stamp])

                ##needs scraper for service roads and accident notifications
        except:
            UnicodeEncodeError
