from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_data(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'}
    url = f'https://www.simplyhired.com/search?q=data+scientist&l=United+States&pn={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='SerpJob-jobCard card')
    for item in divs:
        title = item.find('a', class_='SerpJob-link card-link').text.strip()
        company_location = item.find('div', class_='jobposting-subtitle').text.strip()
        try:
            salary = item.find('div',
                               class_='jobposting-salary SerpJob-salary SerpJob-salary--is-estimate').text.strip()
        except:
            salary = ''

        job = {
            'title': title,
            'company': company_location,
            'salary': salary
        }
        jobs.append(job)

    return


jobs = []
for i in range(1, 91):
    data = get_data(i)
    transform(data)

df = pd.DataFrame(jobs)
df.to_excel("simplyhired.xlsx")
