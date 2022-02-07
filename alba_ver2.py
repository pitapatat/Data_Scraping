import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

## alba_url 넣고 브랜드별 url 얻기
def get_brand_urls(url):
  r_alba = requests.get(url)
  soup = BeautifulSoup(r_alba.text, 'html.parser')
  soup_brands = soup.find(id ="MainSuperBrand").find_all('a', class_ = 'goodsBox-info')

  name_list = []
  brand_url_list =[]
  for brand in soup_brands:
    name = brand.find('span', class_ = 'company').string.strip()
    href = brand['href']
    name_list.append(name)
    brand_url_list.append(href)

    brands = {name: href for name, href in zip(name_list, brand_url_list)}
   
  return brands


## page_num 찾기
def get_page_num(url):
  url = url + 'job/brand/'
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  job_table = soup.find(id = 'NormalInfo')
  num = job_table.find('p', class_='jobCount').find('strong').text
  if ',' in num:
    num = num.replace(',','')
  page = int(num)//50 +1
  #print(page)
  return page


## brand url 넣고, range(1, page+1) 에 대해 column별 데이터 추출
def get_table(url, page):  
  for i in range(1,page+1):
    url = url + f'?page={page}'
    #print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    job_table = soup.find(id = 'NormalInfo').find('tbody').find_all('tr', class_='')
    #print(job_table)
    return job_table

def get_contents(job_table):
  job_list = []
  for jobs in job_table:
    local = jobs.find(class_='local first').string
    company = jobs.find('span', class_='company').get_text().strip()
    working_time = jobs.find('td', class_='data').string
    pay= jobs.find('td', class_='pay').get_text()
    reg_date = jobs.find('td', class_='regDate last').string.strip()
    wanted_jobs = {'local':local, 'company': company, 'working_time':working_time, 'pay':pay, 'reg_date':reg_date}
    job_list.append(list(wanted_jobs.values()))
    #print(wanted_jobs)
  print(job_list)
  return job_list


#############################
url_dict = get_brand_urls(alba_url)
#print(url_dict)

urls = list(url_dict.values())
name = list(url_dict.keys())

for name, url in zip(name, urls):
  page = get_page_num(url)
  table = get_table(url,page)
  jobs = get_contents(table)
  print(jobs)

  #file = open(f"{name}.csv", "w")
  #writer = csv.writer(file)
  #writer.writerow(jobs)

## 결과물 보고 다시 ##