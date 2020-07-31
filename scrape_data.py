#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import csv
import time 
import datetime as dt
import logging
import os
from google.cloud import storage


def current_timestamp():
    return dt.datetime.now()


def new_csv(timestamp):
    """Creates a new csv file with current date and time as suffix"""
    suf = timestamp.strftime("%Y%m%d") + '_' + timestamp.strftime("%H%M%S")
    new_report = "data/trfc_stat_" + suf + ".csv"
    return new_report


def remove_space(l):
    """Removes spaces in the child html code block"""
    for elm in l:
        if elm == '\n':
            l.remove(elm)
    return l


def extract_update_timestamp(s):
    split_time = s.split(' ')
    t = ' '.join(split_time[1:])
    return t

def upload_blob(timestamp,src_name):
    """Upload scrape dump to bucket"""
    current_date = timestamp.strftime("%Y%m%d")
    fn = src_name.split('/')[1]

    storage_client = storage.Client.from_service_account_json(os.environ['GCLOUD_STORAGE_CREDS'])
    bucket = storage_client.bucket(r'mmda-tv5-scrape-dumps')
    blob = bucket.blob(r'{}/{}'.format(current_date,fn))
    blob.upload_from_filename(r'{}'.format(src_name))
    return


def main():

    site = 'http://mmdatraffic.interaksyon.com/line-view-edsa.php'

    now = current_timestamp()

    ########################## LOGGING CONFIG ##########################

    logger = logging.getLogger('mmda_traffic_history')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler('logs/mmda_traffic_history.log')
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    ####################################################################

    dump_name = new_csv(now)

    try:
        tr_start = urllib.request.urlopen(site).read()  #TODO: handle IO error
        logger.info('Accessing {}'.format(site))
    except Exception as e:
        logger.error(e)

    # website to spider: http://mmdatraffic.interaksyon.com/line-view-edsa.php
    # code segment of interest is located from 264:271, div class "lnav"

    tr_soup = BeautifulSoup(tr_start, "lxml")

    tr_sites = tr_soup.find("div", class_="lnav")

    line_link = tr_sites.find_all("div", class_="row")

    links = []

    for i in line_link:
        if "http:" in i.a["href"]:
            pass
        else:
            links.append(i.a["href"])

    with open(dump_name,'w') as f:
        writer = csv.writer(f, delimiter=',')

        # write field names
        field_names = ['LINE', 'SB_STATUS', 'UPDATE_TIMESTAMP',
                       'NB_STATUS', 'UPDATE_TIME_STAMP', 'SCRAPE_TIMESTAMP']
        writer.writerow(field_names)

        for link in links:
            try:
                tr_line = urllib.request.urlopen('http://mmdatraffic.interaksyon.com'
                                         + '/' + link).read().decode('utf-8')
                logger.info('Scraping traffic status for {}'.format(link))
            except Exception as e:
                logger.error(e)

            line_soup = BeautifulSoup(tr_line, "lxml")

            # print('\n\n'+site+'/'+link+'\n')

            # find first line data
            traffic_status = line_soup.find("div", class_="line-row1").contents
            # the first child is the line name
            # the second child is the southbound status
            # the third child is the northbound status
            # the timestamps of each status is embedded in the p tag

            remove_space(traffic_status)

            line_name = traffic_status[0].a.string
            sb_status = remove_space(traffic_status[1].find('div',
                                                            class_='line-status').
                                     contents)[-1].string

            sb_timestamp = extract_update_timestamp(traffic_status[1].p.string)

            nb_status = remove_space(traffic_status[2].find('div',
                                                            class_='line-status').
                                     contents)[-1].string

            nb_timestamp = extract_update_timestamp(traffic_status[2].p.string)


            writer.writerow([line_name, sb_status, sb_timestamp,
                             nb_status, nb_timestamp])


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

                    sb_timestamp = extract_update_timestamp(sibling_status[1].p.string)

                    nb_status = remove_space(sibling_status[2].find('div',
                                                    class_='line-status').
                                             contents)[-1].string

                    nb_timestamp = extract_update_timestamp(sibling_status[2].p.string)

                    # Only get timestamp unti minute precision. Any more detail will bloat
                    # raw data and we want to take advantage of GCS Always Free tier :)
                    writer.writerow([line_name, sb_status, sb_timestamp,
                                     nb_status, nb_timestamp,dt.datetime.now().strftime("%Y-%m-%d %H:%M")])

           # TODO: implement log rotation for when logs get too big
           # TODO: Optimize filenaming convention by removing redunant info
           # TODO: needs scraper for service roads and accident notifications

    # upload_blob(now,dump_name)

if __name__ == '__main__':
    main()
