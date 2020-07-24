# Web-scraping of TV5-MMDA traffic monitoring system

The script will be set as a cron job in a GCS F1-micro instance, scheduled to run every 15-minutes. Scraped data will be dumped in the Cloud storage for later analysis.

## Process flow
![process flow](/docs/mmda-data-scrape-archi.png)

### References

There's some related web-scraping work done by like-minded individuals in the past. The goal of this project is to build upon what they have done under a data engineering mindset: as a deployable and sustained data pipeline.

- https://panjib.wixsite.com/blog/single-post/2018/07/25/Building-my-First-Python-Web-Scraper-Part-1---The-Code
- https://panjib.wixsite.com/blog/single-post/2018/10/03/MMDA-Twitter-Analysis-One-Month-of-Traffic-Incidents-in-Manila
- https://www.kaggle.com/esparko/mmda-traffic-incident-data
- https://erikafille.wordpress.com/2015/09/01/web-scraping-with-urllib2-and-beautifulsoup/
- https://business.inquirer.net/6043/mmda-launches-traffic-monitoring-website
