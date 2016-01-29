"""
  The crawler crawl data from 
  http://iesn.tfri.gov.tw/forestDW/
"""

import urllib2 as ul2
import re
import csv
import datetime
import pandas as pd
from lxml import etree

def main():
  url = 'http://iesn.tfri.gov.tw/forestDW/Frog/Listen?frogSpeciesId=&siteId=02&pointId=&startDate=&endDate=&p=1'
  start_page_num = 1
  end_page_num = 152
  frog = dict()
  frog_list = list()
  
  req = ul2.Request(url)
  response =  ul2.urlopen(req)
  html = response.read()

  page = etree.HTML(html)
  
  species = page.xpath(u"//div[@class='frog-sound-item']//p/text()")
  info = page.xpath(u"//div[@class='frog-sound-item']//h3/text()")
  audio_source = page.xpath(u"//div[@class='frog-sound-item']//a[@class='k-button'][2]/@href")
  
  for idx in range(0, len(species)):
    # if more than 2 frog
    names = re.sub('[\r\n\t ]', '', species[idx])
    names = names.split(',')
    
    for jdx in range(0, len(names)):
      frog = {
        'specie': re.sub('[\r\n\t ]', '', names[jdx]),
        'time': datetime.datetime.strptime(info[idx][:19], '%Y-%m-%d %H:%M:%S'),
        'place': re.sub('[, ]', '', info[idx][21:-3]),
        'audio_record': audio_source[idx]
      }
    
      frog['time'] = datetime.datetime.strptime(info[idx][:19], '%Y-%m-%d %H:%M:%S')
      frog['place'] = re.sub('[, ]', '', info[idx][21:-3])
      frog['audio_record'] = audio_source[idx]
      frog_list.append(frog)

  df = pd.DataFrame(frog_list)
  print df


if __name__ == '__main__':
  main()
