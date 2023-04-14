import requests
from bs4 import BeautifulSoup
from urllib import parse
import pandas as pd
from datetime import datetime

now = datetime.now()
today = now.date()

# date_now = now.strftime('%Y/%m/%d')


datetime_format = "%Y/%m/%d"


def main():
    origin = "https://icals.snu.ac.kr"
    url = origin + f"/board/subject/page/4?pmove=1"
    web = requests.get(url)
    soup = BeautifulSoup(web.content, 'html.parser')

    # 테이블 행 마다 가져오기(컬럼 행 제외)
    notion = soup.table.find_all('tr')[1:]

    # 상세페이지 URL
    href = []
    # 제목
    title = []
    # 신청기간
    app = []
    # 지원기관
    agency = []
    # URL
    site = []

    for i in notion:
        # 오늘 날짜와 신청기간 비교 (신청날짜와 같거나 더 나중에 있는 것 가져오기)
        date = i.select_one("td:nth-of-type(3)").text.split('-')
        date_result = datetime.strptime(date[1], datetime_format)
        if date_result > today:
            content = i.find_all('td', class_="alignLeft")
            # 상세페이지 들어가서 정보 가져오기
            for x in content:
                link = x.find('a')['href']
                notion_pages = requests.get(origin + link)
                notion_soup = BeautifulSoup(notion_pages.content, 'html.parser') # 상세페이지 들어가기

                title_c = notion_soup.find('dl', class_='cHeader') # 제목 가져오기
                title.append(title_c.find('dt').text)
                data = notion_soup.find_all('li', class_='custom_text') # 신청기간, 지원기관, URL 가져오기 (같은 태그임)
                for z in data:
                    con = z.text.replace('\t', '').split('\n') # 분류, 공백 정리
                    if con[0] == '신청기간':
                        app.append(con[1])
                    elif con[0] == '지원기관':
                        agency.append(con[1])
                    else:
                        site.append(con[1])

    rpitnI

    # print(title)
    # print(app)
    # print(agency)
    # print(site)

    df = pd.DataFrame({'제목': title, '신청기간': app, '지원기관': agency, 'URL': site})
    print(df.head())


if __name__ == '__main__':
    main()
