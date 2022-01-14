# 랭킹 아이디 1~100위까지 크롤링
import requests
from bs4 import BeautifulSoup

# 데이터 저장
df = []
# 사용자 지정 함수 만들기
def get_data(info):
    if info is None:
        return 'None'
    else:
        return info.get_text().strip()

# 1위~5위 데이터 가져오기
headers= {'User-Agent' : 'Mozilla/5.0'}
url = f'https://www.op.gg/ranking/ladder/page=1'
res = requests.get(url, headers = headers)
res.text
soup = BeautifulSoup(res.text)

table = soup.find('div', class_='ranking-highest')
rows = soup.find_all('li', attrs ={'class':'ranking-highest__item'})

for row in rows:
    rank = get_data(row.find('div', class_='ranking-highest__rank'))
    name = get_data(row.find('a', class_='ranking-highest__name'))
    tier = get_data(row.find('div', class_='ranking-highest__tierrank').find('span'))
    lp = get_data(row.find('div', class_='ranking-highest__tierrank').find('b'))
    win = get_data(row.find('div', class_='winratio-graph__text--left'))
    lose = get_data(row.find('div', class_='winratio-graph__text--right'))
    win_ratio = get_data(row.find('span', class_='winratio__text'))
    df.append([rank, name, tier, lp, win, lose, win_ratio])

# 6위~100위 데이터 가져오기
headers= {'User-Agent' : 'Mozilla/5.0'}
url = 'https://www.op.gg/ranking/ladder/'
res = requests.get(url, headers = headers)
res.text
soup = BeautifulSoup(res.text)

# 테이블 태그 불러오기
table = soup.find('table', class_ = 'ranking-table')
rows = table.find_all('tr', class_='ranking-table__row')
for row in rows:
    rank = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--rank'))
    name = get_data(row.find('span'))
    tier = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--tier'))
    lp = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--lp'))
    win = get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--left'))
    lose = get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--right'))
    win_ratio = get_data(row.find('span', class_='winratio__text'))
    df.append([rank, name, tier, lp, win, lose, win_ratio])

# 여러 페이지 추출
for cur_page in range(2,100):
    headers= {'User-Agent' : 'Mozilla/5.0'}
    url = f'https://www.op.gg/ranking/ladder/page={cur_page}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text)
    table = soup.find('table', class_ = 'ranking-table')
    rows = table.find_all('tr', class_='ranking-table__row')
    
    for row in rows:
        rank = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--rank'))
        name = get_data(row.find('span'))
        tier = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--tier'))
        lp = get_data(row.find('td', class_='ranking-table__cell ranking-table__cell--lp'))
        win = get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--left'))
        lose = get_data(row.find('div', class_='winratio-graph__text winratio-graph__text--right'))
        win_ratio = get_data(row.find('span', class_='winratio__text'))
        df.append([rank, name, tier, lp, win, lose, win_ratio])
    
#csv 파일로 저장
fields = ['rank','name','tier','lp','win','lose','win_ratio']
# 데이터는 df
df
# 데이터 붙이기
import csv
with open('./lol_userid.csv','w', encoding = 'utf-8', newline='\n') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(df)

