import os
import time

# intiate scraping every 30 mins.

while True:
    os.system('scrapy crawl theguardian')
    time.sleep(1800)

# fix crontab
# os.system('cat <(crontab -l) <(echo "*       /30       *       *       *      /app/scrapy.sh") | crontab -')
