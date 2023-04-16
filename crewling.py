import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

now = datetime.now()
today = now.date()
datetime_format = "%Y/%m/%d"

output_dir = "output/"
output_file = 'output/projects.xlsx'


def main():
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
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

    origin = "https://icals.snu.ac.kr"

    # 처음 실행할 떄
    if not os.path.exists(output_file):
        for i in range(1, 5):
            url = origin + f"/board/subject/page/{i}?pmove=1"
            web = requests.get(url)
            soup = BeautifulSoup(web.content, 'html.parser')

            # 테이블 행 마다 가져오기(컬럼 행 제외)
            notion = soup.table.find_all('tr')[1:]
            for i in notion:
                # 오늘 날짜와 신청기간 비교 (신청날짜와 같거나 더 나중에 있는 것 가져오기)
                date = i.select_one("td:nth-of-type(3)").text.split('-')
                date_result = datetime.strptime(date[-1], datetime_format)
                if date_result.date() >= today:
                    content = i.find_all('td', class_="alignLeft")
                    # 상세페이지 들어가서 정보 가져오기
                    for x in content:
                        link = x.find('a')['href']
                        notion_pages = requests.get(origin + link)
                        notion_soup = BeautifulSoup(notion_pages.content, 'html.parser')  # 상세페이지 들어가기

                        title_c = notion_soup.find('dl', class_='cHeader')  # 제목 가져오기
                        title.append(title_c.find('dt').text)
                        data = notion_soup.find_all('li', class_='custom_text')  # 신청기간, 지원기관, URL 가져오기 (같은 태그임)
                        for z in data:
                            con = z.text.replace('\t', '').split('\n')  # 분류, 공백 정리
                            if con[0] == '신청기간':
                                app.append(con[1])
                            elif con[0] == '지원기관':
                                agency.append(con[1])
                            else:
                                site.append(con[1])

        df = pd.DataFrame({'제목': title, '신청기간': app, '지원기관': agency, 'URL': site})
        df.to_excel('output\projects.xlsx')

    # 2회 이상 실행할 때 (새글 알림)
    else:
        df = pd.read_excel('output\projects.xlsx')
        url = origin + f"/board/subject/page/1?pmove=1"
        web = requests.get(url)
        soup = BeautifulSoup(web.content, 'html.parser')

        # 테이블 행 마다 가져오기(컬럼 행 제외)
        notion = soup.table.find_all('tr')[1:]
        for i in notion:
            content = i.find_all('td', class_="alignLeft")
            for q in content:
                link = q.find('a')['href']
                notion_pages = requests.get(origin + link)
                notion_soup = BeautifulSoup(notion_pages.content, 'html.parser')
                title_c = notion_soup.find('dl', class_='cHeader')  # 제목 가져오기
                if title_c in df['제목']:
                    pass
                else:
                    # 크롤링 했을 때 엑셀파일에 중복되지 않은 공지가 있으면 알림, 새로 저장
                    title.append(title_c.find('dt').text)
                    data = notion_soup.find_all('li', class_='custom_text')  # 신청기간, 지원기관, URL 가져오기 (같은 태그임)
                    for z in data:
                        con = z.text.replace('\t', '').split('\n')  # 분류, 공백 정리
                        if con[0] == '신청기간':
                            app.append(con[1])
                        elif con[0] == '지원기관':
                            agency.append(con[1])
                        else:
                            site.append(con[1])

            if len(title) > 0:
                # 새로운 연구과제 공지 알림
                requests.post("https://ntfy.sh/re_project_SF",
                              data=f'연구과제공모 새 글 공지 :{title}'.encode(encoding='utf-8'))
                df2 = pd.DataFrame({'제목': title, '신청기간': app, '지원기관': agency, 'URL': site})
                df3 = pd.concat([df2, df])
                df3.to_excel('output/projects.xlsx')
            else:
                pass


if __name__ == '__main__':
    main()
