import requests
from bs4 import BeautifulSoup
from urllib import parse

def main():

    support = parse.quote('장학')
    education = parse.quote('교육')

    origin = "https://www.jbnu.ac.kr/kor/"
    url = origin + f"?menuID=139&category={support}"
    web = requests.get(url)
    soup = BeautifulSoup(web.content, 'html.parser')

    notion = soup.table.find_all('a')

    href = []
    for i in notion:
        if '신청' in i.text:
            href.append(origin + i.attrs['href'])
            notion_pages = requests.get(href[-1])
            notion_soup = BeautifulSoup(notion_pages.content, 'html.parser')
            content = notion_soup.find_all('p', class_="0")
            for c in content:
                print(c.text)


    # for h in href:
    #     origin



if __name__ == '__main__':
    main()
