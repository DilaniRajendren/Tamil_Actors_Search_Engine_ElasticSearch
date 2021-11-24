import requests
import numpy as np
import pandas as pd
import json
from bs4 import BeautifulSoup
import codecs
import unicodedata

url = 'https://en.wikipedia.org/wiki/List_of_Tamil_film_actors'
movies = []
r = requests.get(url)
content = r.content
soup = BeautifulSoup(content)
detail_content = soup.find('table', attrs = {'class': 'standard mb-50px'})

tablecontent = detail_content.find_all('tr')
print("num_movies:",len(tablecontent))

for tr in tablecontent[1:]:
    actor = {}
    a_tags = tr.find_all('a')
    td_tags = tr.find_all('td')
    
    actor["actor_url"] = a_tags[0].get('href')
    actor["வருடம்"] = td_tags[1].get_text()
    actor["அறிமுகஆண்டு"] = td_tags[2].get_text()
    actor["நடிகர்"] = td_tags[3].get_text()
    movies.append(actor)

print(len(movies))
print(movies[0])

actors_data = []
def crawl_actor_url(movie):
  # print(movie)
  r = requests.get(movie["actor_url"])
  content = r.content
  soup = BeautifulSoup(content)

  detail_content = soup.find('table', attrs = {'class': 'standard'})

  td_tags = detail_content.find_all('td')
  # print(tablecontent)
  movie["திரைப்படம்"]= td_tags[2].get_text()

  actor_div = soup.find('div', attrs = {'class': 'tab-content clearfix', 'id': 'tab_1'})
  actor_li_tags =actor_div.find_all('li')
  
  for actor_li in actor_li_tags:
    actor ={}
    actor["திரைப்படம்"] = movie["திரைப்படம்"]
    s = actor_li.find('a').get_text().split('(')
    actor["அறிமுகதிரைபடம்"]= s[1][:-3].strip('\n')
    actor["அறிமுகஆண்டு"] = movie["அறிமுகஆண்டு"]
    actor["வருடம்"] = movie["வருடம்"]
    actor["நடிகர்கள்"] = movie["நடிகர்கள்"]
    actor["actor_url"]= actor_li.find('a').get('href')
    actors_data.append(actor)
    
i=0
for movie in movies:
  if(i%500==0):
    print(i)
  crawl_actor_url(movie)
  i+=1

print(len(actors_data))
print(actors_data[0])

final_data = []
def crawl_actor_url(actor):
  r = requests.get(actor["actor_url"])
  content = r.content
  soup = BeautifulSoup(content)
  detail_content = soup.find('table', attrs = {'class': 'standard mb-10px'})
  tablecontent =detail_content.find_all('td')
  # print(tablecontent)
  actor["பாலினம்"]= tablecontent[4].get_text()

  # print(actor)
  actor_content = soup.find('div', attrs = {'class': 'info-box white-bg'})

  actor["அறிமுகஆண்டு"]= (actor_content.get_text()).strip()
  del actor["actor_url"]
  final_data.append(actor)
  # print(actor)
    
i=0
for actor in actors_data:
  if(i%500==0):
    print(i)
  try:
    crawl_actor_url(actor)
  except Exception as e:
    print("Error in")
    print(actor)
    print(e)
  i+=1

print(len(final_data))
print(final_data[0])



f = codecs.open('scraped_actors.csv', 'w', encoding='utf-8')
i=1
for line in final_data:
  # if(i%500==0):
  #   print(i)
  try:
      actor_json = str(line).replace("\'", "\"")
      # actor_json["பாடல்வரிகள்"] = unicodedata.normalize("NFKD",actor_json["பாடல்வரிகள்"])

      # json.dump(actor_json, f, ensure_ascii=False)
      f.write(actor_json)
      f.write('\n')
  except Exception as e:
      print(i)
      print("Error in")
      print(line)
      print(e)
  i += 1
