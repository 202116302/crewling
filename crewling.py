import requests
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
from datetime import datetime

now = datetime.now()

date_now = now.strftime('%Y/%m/%d')


def main():
    origin = "https://icals.snu.ac.kr"
    url = origin + f"/board/subject/page/1?pmove=1"
    web = requests.get(url)
    soup = BeautifulSoup(web.content, 'html.parser')

    notion = soup.table.find_all('tr')[1:]

    href = []
    title = []
    app = []
    agency = []
    site = []
    for i in notion:
        date = i.select_one("td:nth-of-type(3)").text.split('-')
        if date[1] == date_now:
            content = i.find_all('td', class_="alignLeft")
            for x in content:
                link = x.find('a')['href']
                href.append(origin + link)
                notion_pages = requests.get(href[-1])
                notion_soup = BeautifulSoup(notion_pages.content, 'html.parser')
                title_c = notion_soup.find('dl', class_='cHeader')
                title.append(title_c.find('dt').text)
                data = notion_soup.find_all('li', class_='custom_text')
                for z in data:
                    con = z.text.replace('\t', '').split('\n')
                    if con[0] == '신청기간':
                        app.append(con[1])
                    elif con[0] == '지원기관':
                        agency.append(con[1])
                    else:
                        site.append(con[1])

    # print(title)
    # print(app)
    # print(agency)
    # print(site)

    df = pd.DataFrame({'제목': title, '신청기간': app, '지원기관': agency, 'URL': site})
    # print(df.head())



if __name__ == '__main__':
    main()
