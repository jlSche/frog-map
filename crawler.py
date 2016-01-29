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
  start_page = 1
  end_page = 152

  df = crawWebsite(start_page, end_page)
  df.to_csv('./frog.csv', encoding='big5', index=False)
  

def crawWebsite(start_page=1, end_page=1, start_date='', end_date='', specie='', place=''):
  main_url = 'http://iesn.tfri.gov.tw/forestDW/Frog/Listen?frogSpeciesId=&siteId=02&pointId=&startDate=&endDate=&p='
  frog = dict()
  frog_list = list()

  for idx in range(start_page, end_page+1):
    url = main_url + str(idx)
    req = ul2.Request(url)
    response =  ul2.urlopen(req)
    html = response.read()
    page = etree.HTML(html)
    
    species = page.xpath(u"//div[@class='frog-sound-item']//p/text()")
    info = page.xpath(u"//div[@class='frog-sound-item']//h3/text()")
    link = page.xpath(u"//div[@class='frog-sound-item']//a[@class='k-button'][2]/@href")

    for idx in range(0, len(species)):
      # if more than 2 frog
      names = re.sub('[\r\n\t ]', '', species[idx])
      names = names.split(',')
      
      for jdx in range(0, len(names)):
        frog = {
          'specie': re.sub('[\r\n\t ]', '', names[jdx]),
          'time': datetime.datetime.strptime(info[idx][:19], '%Y-%m-%d %H:%M:%S'),
          'place': re.sub('[, ]', '', info[idx][21:-3]),
          'link': link[idx]
        }
        '''
        frog['time'] = datetime.datetime.strptime(info[idx][:19], '%Y-%m-%d %H:%M:%S')
        frog['place'] = re.sub('[, ]', '', info[idx][21:-3])
        frog['link'] = link[idx]
        '''
        frog_list.append(frog)

  return pd.DataFrame(frog_list)


if __name__ == '__main__':
  main()
