#라이브러리 활성화
from selenium import webdriver #셀레니움 웹드라이버
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time #대기시간
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.indexes.base import Index
from selenium.common.exceptions import NoSuchElementException 
import csv

#녹화 버튼 유무 판단하는 함수
def check_exists_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# headers= {'User-Agent' : 'Mozilla/5.0'}
# for문으로 앞서 작성한 id를 넣고 돌릴 예정
# lol_userid 가져오기(csv파일로)


df = pd.read_csv("./lol_userid.csv")
# 이름만 따로 추출하고 리스트로 저장
name = df['name']
name = list(name)


#셀레니움 동작 준비
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
browser = webdriver.Chrome('C:/study/indusry_project_3/python/chromedriver.exe', options=options)

# for id in name:
#     id.replace(' ','+')
id = '코스요릭'
url = 'https://www.op.gg/summoner/userName='+id

#솔로랭크 클릭 파트
browser.get(url)
time.sleep(2)
solorank_button = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/div[1]/div/ul/li[2]")
solorank_button.click()
time.sleep(2)

#더보기 버튼 클릭 파트    
while True:
    try:
    
        showmore_button = browser.find_element_by_css_selector("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content > div.GameMoreButton.Box > a").send_keys(Keys.ENTER)
        time.sleep(1)
    
    except:
        print("더보기 버튼 클릭 완료")
        break
    
#상세게임 버튼 클릭 파트
start = 3
while True:
    try:
        for num in range(1,21):
            
            xpath_saved = f'/html/body/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/div[2]/div[{start}]/div[{num}]/div/div[1]/div[7]/div/div[2]/a'
            
            if check_exists_by_xpath(xpath_saved) == True:
        
                detail = browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/div[2]/div[{start}]/div[{num}]/div/div[1]/div[7]/div/div[2]/a')
                detail.click()
        
            else:
                    
                detail = browser.find_element_by_xpath(f'/html/body/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/div[2]/div[{start}]/div[{num}]/div/div[1]/div[7]/div/div[1]/a')
                detail.click()
                
            
            if num == 20:
                start += 1
                    
    except:
        print("상세내역 검색 완료")
        break
time.sleep(2)    
#동적 작동 완료 후 파싱
soup = BeautifulSoup(browser.page_source , "html.parser")

#-----------------------------------------------#
recent_champions=[] # 미리 가져올 리스트 지정
recent_kills=[]
recent_deaths=[]
recent_assists=[]
recent_results=[]
recent_times=[]
recent_timestamp=[] 
recent_games_html = soup.select('div.GameItemList div.GameItemWrap') #GameItemWrap의 html 가져와서 저장
# recent_games_html = soup.find_all('div',attrs={'class':'GameItemWrap'}) # 안되면 이걸로 실행하면 잘 됨
recent_game_len = len(recent_games_html)
print(recent_game_len)
for i in range(recent_game_len): #반복문 사용해서 리스트에 원하는 데이터 넣기
    recent_champions.append(''.join(list(recent_games_html[i].select('div.ChampionName')[0].stripped_strings)))
    recent_kills.append(list(recent_games_html[i].select('div.KDA div.KDA span.Kill')[0].stripped_strings)[0])
    recent_deaths.append(list(recent_games_html[i].select_one('div.KDA div.KDA span.Death').stripped_strings)[0])
    recent_assists.append(list(recent_games_html[i].select('div.KDA div.KDA span.Assist')[0].stripped_strings)[0])
    recent_results.append(recent_games_html[i].select_one('div.GameItem')['data-game-result'])
    recent_times.append(recent_games_html[i].find('div', attrs={'class':'GameLength'}).get_text())
    recent_timestamp.append(recent_games_html[i].find('div', attrs={'class':'TimeStamp'}).get_text())
    

#-----------------#

#전체 경기 수 수집
recent_games_html = soup.select('div.GameDetail div.GameDetailTableWrap')

# 이긴팀 데이터 수집
winner_games_html = soup.find_all('table',attrs={'class':'GameDetailTable Result-WIN'})

# 진 팀 데이터 수집
loser_games_html = soup.find_all('table',attrs={'class':'GameDetailTable Result-LOSE'})



winner_game_len = len(winner_games_html)
loser_game_len = len(loser_games_html)
print("winner_game_len :", winner_game_len)
print('loser_game_len :',loser_game_len)

winner_companion_champion1 = []
winner_companion_champion2 = []
winner_companion_champion3 = []
winner_companion_champion4 = []
winner_companion_champion5 = []

loser_companion_champion1 = []
loser_companion_champion2 = []
loser_companion_champion3 = []
loser_companion_champion4 = []
loser_companion_champion5 = []

winner_team_color = []
loser_team_color= []

# 반복문 사용하여 리스트에 이긴 팀 데이터 넣기
for i in range(winner_game_len):
    winner_companion_champion1.append(winner_games_html[i].select('table div[title]')[0].string)
    winner_companion_champion2.append(winner_games_html[i].select('table div[title]')[1].string)
    winner_companion_champion3.append(winner_games_html[i].select('table div[title]')[2].string)
    winner_companion_champion4.append(winner_games_html[i].select('table div[title]')[3].string)
    winner_companion_champion5.append(winner_games_html[i].select('table div[title]')[4].string)
    winner_team_color.append((winner_games_html[i].find(class_="HeaderCell").text).replace("\t","").replace("\n","").replace("\r",""))
    loser_team_color.append((loser_games_html[i].find(class_="HeaderCell").text).replace("\t","").replace("\n","").replace("\r",""))
    
    
# 반복문 사용하여 리스트에 진 팀 데이터 넣기

for i in range(loser_game_len):
    loser_companion_champion1.append(loser_games_html[i].select('table div[title]')[0].string)
    loser_companion_champion2.append(loser_games_html[i].select('table div[title]')[1].string)
    loser_companion_champion3.append(loser_games_html[i].select('table div[title]')[2].string)
    loser_companion_champion4.append(loser_games_html[i].select('table div[title]')[3].string)
    loser_companion_champion5.append(loser_games_html[i].select('table div[title]')[4].string)
    
# print(winner_team_color)
# print(winner_companion_champion1)
# print(winner_companion_champion2)
# print(winner_companion_champion3)
# print(winner_companion_champion4)
# print(winner_companion_champion5)

# print(loser_companion_champion1)
# print(loser_companion_champion2) 
# print(loser_companion_champion3) 
# print(loser_companion_champion4) 
# print(loser_companion_champion5) 
# print(winner_team_color)
# print(loser_team_color)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#데이터 프레임으로 만들어주기
recent_df = pd.DataFrame([recent_champions,
                        recent_results,
                        recent_kills,
                        recent_deaths,
                        recent_assists,
                        recent_times,
                        recent_timestamp,
                        
                        winner_team_color,
                        winner_companion_champion1,
                        winner_companion_champion2,
                        winner_companion_champion3,
                        winner_companion_champion4,
                        winner_companion_champion5,
                        
                        loser_team_color,
                        loser_companion_champion1,
                        loser_companion_champion2,
                        loser_companion_champion3,
                        loser_companion_champion4,
                        loser_companion_champion5],
                        index = ['champion','result','kills','deaths','assists','time','timestamp',
                                'winner_teamcolor','winner_companion_champion1(top)',
                                'winner_companion_champion2(jungle)','winner_companion_champion3(mid)','winner_companion_champion4(onedeal)',
                                'winner_companion_champion5(support)',
                                'loser_team_color','loser_companion_champion1(top)','loser_companion_champion2(jungle)',
                                'loser_companion_champion3(mid)','loser_companion_champion4(onedeal)','loser_companion_champion5(support)']).T
recent_df
print('-----------------------------------------------------------------')
lol=[]
lol.append([id,recent_champions, recent_results, recent_kills, recent_deaths, recent_assists, recent_times,   recent_timestamp, 
            winner_team_color, winner_companion_champion1, winner_companion_champion2, winner_companion_champion3, winner_companion_champion4, winner_companion_champion5,
            loser_team_color, loser_companion_champion1, loser_companion_champion2, loser_companion_champion3, loser_companion_champion4, loser_companion_champion5])
            

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

recent_df.to_csv("test2")

#csv파일로 저장
import csv
#필드값 지정
fields = ['id','recent_champions', 'recent_results', 'recent_kills', 'recent_deaths', 'recent_assists', 'recent_times', 'recent_timestamp', 
                'winner_team_color', 'winner_companion_champion1', 'winner_companion_champion2', 'winner_companion_champion3', 'winner_companion_champion4',
                'winner_companion_champion5', 'loser_team_color', 'loser_companion_champion1', 'loser_companion_champion2', 'loser_companion_champion3',
                'loser_companion_champion4', 'loser_companion_champion5']

with open('./ex02.csv', 'w', encoding = 'utf-8', newline='\n') as f:
    write = csv.writer(f)
    write.writerow(fields)
    for i in range(2):
        for j in range(0,7):
            for k in range(0,19):
                f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {},{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n"
                        .format(lol[i][0],lol[i][1][k],lol[i][2][k],lol[i][3][k],lol[i][4][k],lol[i][5][k],lol[i][6][k],        lol[i][7][k],lol[i][8][k],lol[i][9][k],lol[i][10][k],
                                lol[i][11][k],lol[i][12][k],lol[i][13][k],lol[i][14][k],lol[i][15][k],lol[i][16][k],lol[i][17][k],lol[i][18][k],lol[i][19][k]))




