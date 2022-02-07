import os
import csv
import requests
from bs4 import BeautifulSoup


def request_url():
  os.system("clear")
  alba_url = "http://www.alba.co.kr"
  alba = requests.get(alba_url)
  #print(alba.status_code)
  if alba.status_code == 200:
    alba_html = BeautifulSoup(alba.text, "html.parser")
    selected = alba_html.select('#MainSuperBrand > ul')
    tags = selected[0].find_all('a', {'class':'goodsBox-info'})
 
    urls = []
    for i in range(len(tags)):
      url = tags[i]['href']
      urls.append(f"{url}job/brand/")
    
    url_names = []
    for i in range(len(tags)):
      name = tags[i].find('span', class_='company').string
      if '/' in name:
        name = name.replace('/','')
  
      url_names.append(name)


    print(len(urls))
    print(len(url_names))
    return urls, url_names
    
  else:
    print("error!")


#for url in urls
def get_contents(url):
  
  new_alba = requests.get(url)
  #print(new_alba.status_code)
  new_html = BeautifulSoup(new_alba.text,'html.parser') 
  
  places = new_html.find_all('td', class_='local first')
  print(len(places))

  titles = new_html.find_all('td', class_='title')
  print(len(titles))

  times = new_html.find_all('td', class_="data")
  print(len(times))
  
  pays = new_html.find_all('td', class_="pay")
  print(len(pays))

  dates = new_html.find_all('td',class_="regDate last")
  print(len(dates))
  
  return places, titles, times, pays, dates


#places, titles, times, pays, dates
def get_detail():

  data = []

  for i in range(len(places)):
    place = places[i].get_text().replace('\xa0', ' ')
    title = titles[i].find('span').get_text(strip=True)
    w_time = times[i].get_text(strip = True)
    pay = pays[i].get_text(strip = True)
    update = dates[i].get_text()
    result = {'place':place, 'title':title, 'time':w_time, 'pay':pay, 'date':update}

    #print(result)
    data.append(result)
    
  #print(data)  
  return data
  

#data = get_detail()
def save_to_csv(data, url_name):
  file = open(f"{url_name}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(['place', 'title','time','pay','date'])
  for d in data:
    writer.writerow(list(d.values()))
  return 


#### 실행 ####
urls, url_names = request_url()

for i in range(len(urls)):
  places, titles, times, pays, dates = get_contents(urls[i])
  data = get_detail()
  url_name = url_names[i]
  save_to_csv(data, url_name)


