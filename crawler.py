"""
  The crawler crawl data from 
  http://iesn.tfri.gov.tw/forestDW/
"""

import urllib2 as ul2
import re
import csv
from lxml import etree

def main():
  url = 'http://iesn.tfri.gov.tw/forestDW/Frog/Listen?frogSpeciesId=&siteId=02&pointId=&startDate=&endDate=&p=1'
  start_page_num = 1
  end_page_num = 152
  species = list()
  places = list()
  
  req = ul2.Request(url)
  response =  ul2.urlopen(req)
  html = response.read()

  page = etree.HTML(html)
  
  # iterate through all pages
  for data in page.xpath("//div[@class='frog-sound-list']"):
    for place, name in zip(data.xpath(u"//h3/text()"),data.xpath(u"//p/text()")):
      name = re.sub('[\n\t, ]', '', name)
      species.append(name)
      places.append(place)

  for ele1, ele2 in zip(species, places):
    # write to a csv file
    print ele1, ele2
if __name__ == '__main__':
  main()
