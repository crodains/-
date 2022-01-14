#사용할 라이브러리--------------------------------------
from pandas.core.indexes.base import Index
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver #셀레니움 웹드라이버
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import csv
#-----------------------------------------------------------


#사용할 함수-------------------------------------------------
def get_data(info):
        if info is None:
            return 'None'
        else:
            return info.get_text().strip()
#------------------------------------------------------------


# 스크래핑한 랭킹 csv에서 id만 추출

df = pd.read_csv("./lol_userid.csv")
# 이름만 따로 추출하고 리스트로 저장

name = df['name']
name = list(name)

#최종적으로 결과값 넣어줄 DataFrame 미리 생성
columns = ['id','champion','result','kills','deaths','assists','time','timestamp','win_top','win_jungle','win_mid','win_onedeal','win_support','lose_top','lose_jungle','lose_mid','lose_onedeal','lose_support']
result = pd.DataFrame(columns= columns)



# url 확인 결과 띄어쓰기 할 때 +가 붙고 영문이나 한글이나 동일하게 표기됨.
# 예를 들어 http://www.op.gg/summoner/userName=Hide+on+bush 와 같이 표기됨
# for문을 사용하고 띄어쓰기는 split으로 나눠서 + 사이 사이에 각각 넣는 코드를 작성

for id in name:
    try:
        
        url = 'https://www.op.gg/summoner/userName='+id

        #-------------------------------------솔로랭크 클릭파트-------------------
        
        headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        options = webdriver.ChromeOptions()
        # options.add_argument("--start-maximized")
        options.add_argument('lang=ko_KR')
        options.add_argument('disable-gpu')
        options.add_argument('headless')
        browser = webdriver.Chrome('./chromedriver.exe', options=options)
        browser.get(url)
        time.sleep(2)
        solorank_button = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/div[1]/div/ul/li[2]")
        solorank_button.click()
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source , "html.parser")

        #-------------------------------------솔로랭크 클릭파트 end-------------------


            
        # 미리 가져올 리스트 생성
        recent_id = []
        recent_champions=[]
        recent_kills=[]
        recent_deaths=[]
        recent_assists=[]
        recent_results=[]
        recent_times=[]
        recent_timestamp=[]
        recent_champions_union=[]

        win_champion1 = []
        win_champion2 = []
        win_champion3 = []
        win_champion4 = []
        win_champion5 = []

        lose_champion1 = []
        lose_champion2 = []
        lose_champion3 = []
        lose_champion4 = []
        lose_champion5 = []

        recent_games_html = soup.select('div.GameItemList div.GameItemWrap') #GameItemWrap의 html 가져와서 저장
        # recent_games_html = soup.find_all('div',attrs={'class':'GameItemWrap'}) # 안되면 이걸로 실행하면 잘 됨
        recent_game_len = len(recent_games_html)
        print(recent_game_len)

        for i in range(recent_game_len): #반복문 사용해서 리스트에 원하는 데이터 넣기
            
            recent_id.append(id)
            recent_champions.append(''.join(list(recent_games_html[i].select('div.ChampionName')[0].stripped_strings)))
            recent_kills.append(list(recent_games_html[i].select('div.KDA div.KDA span.Kill')[0].stripped_strings)[0])
            recent_deaths.append(list(recent_games_html[i].select_one('div.KDA div.KDA span.Death').stripped_strings)[0])
            recent_assists.append(list(recent_games_html[i].select('div.KDA div.KDA span.Assist')[0].stripped_strings)[0])
            recent_results.append(recent_games_html[i].select_one('div.GameItem')['data-game-result'])
            recent_times.append(recent_games_html[i].find('div', attrs={'class':'GameLength'}).get_text())
            recent_timestamp.append(recent_games_html[i].find('div', attrs={'class':'TimeStamp'}).span['title'])
            
            
            #------------------승패 챔피언 ------------
            my_champion = recent_games_html[i].select('div.GameSettingInfo div.ChampionName a')[0].text
            all_champions = recent_games_html[i].find_all('div', class_='ChampionImage')
            win_or_lose = recent_games_html[i].find('div', class_='GameResult').text
            win_or_lose1=win_or_lose.replace('\n','').replace('\t','')
            
            
            team_all = []
            for each_champion in all_champions: #ㄷㅁㄴㅇㄹㅇㅁㄴㄹㅇ라요릭21213421244!@!!!
                team=get_data(each_champion) # 요릭\n\요릭
                team_all.append(team) 
            
            team_all = team_all[1::] #[',', '요릭요릭', '몰가몰가']
            
            
            team_final = []
            for team_append in team_all:
                a= team_append.split('\n')
                team_final.append(a[0]) # ['요릭','몰가' x]
                
            
            team1 = team_final[0:5] 
            team2 = team_final[5::]
            
            
            if my_champion in team1 and win_or_lose == "승리" or 'Victory':
                win_champion1.append(team1[0])
                win_champion2.append(team1[1])
                win_champion3.append(team1[2])
                win_champion4.append(team1[3])
                win_champion5.append(team1[4])
                
                lose_champion1.append(team2[0])
                lose_champion2.append(team2[1])
                lose_champion3.append(team2[2])
                lose_champion4.append(team2[3])
                lose_champion5.append(team2[4])
                
                
            
            elif my_champion in team2 and win_or_lose == "승리" or 'Victory':
                win_champion1.append(team2[0])
                win_champion2.append(team2[1])
                win_champion3.append(team2[2])
                win_champion4.append(team2[3])
                win_champion5.append(team2[4])
                
                lose_champion1.append(team1[0])
                lose_champion2.append(team1[1])
                lose_champion3.append(team1[2])
                lose_champion4.append(team1[3])
                lose_champion5.append(team1[4])
                
            elif my_champion in team1 and win_or_lose == "패배" or 'Defeat':
                win_champion1.append(team2[0])
                win_champion2.append(team2[1])
                win_champion3.append(team2[2])
                win_champion4.append(team2[3])
                win_champion5.append(team2[4])
                
                lose_champion1.append(team1[0])
                lose_champion2.append(team1[1])
                lose_champion3.append(team1[2])
                lose_champion4.append(team1[3])
                lose_champion5.append(team1[4])
                
            elif my_champion in team2 and win_or_lose == "패배" or 'Deafeat':
                win_champion1.append(team1[0])
                win_champion2.append(team1[1])
                win_champion3.append(team1[2])
                win_champion4.append(team1[3])
                win_champion5.append(team1[4])
                
                lose_champion1.append(team2[0])
                lose_champion2.append(team2[1])
                lose_champion3.append(team2[2])
                lose_champion4.append(team2[3])
                lose_champion5.append(team2[4])
            else:
                print('error 발생')
    
        print(id)
        middle_df = pd.DataFrame(data = list(zip(recent_id, recent_champions, recent_results, recent_kills, recent_deaths, recent_assists, recent_times, recent_timestamp, win_champion1,win_champion2,win_champion3,win_champion4,win_champion5, lose_champion1,lose_champion2,lose_champion3,lose_champion4,lose_champion5)), columns = columns)
        print(middle_df)
        result = result.append(middle_df, ignore_index=True)
        
        
    except:
        print("에러발생")
print(result)
print(lose_champion1)
#데이터 프레임으로 만들어주기

result.to_csv('롤2.csv',sep=',',encoding='utf-8')
# result.to_excel('롤csv.xlsx')
