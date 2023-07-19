from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


def reset_crawl():
    global game_dates
    global game_infos

    global teams_hm
    global teams_aw

    global pitcher_hm
    global pitcher_aw
    
    game_dates = []
    game_infos = []

    teams_hm = []
    teams_aw = []

    pitcher_hm = []
    pitcher_aw = []


game_dates = []
game_infos = []

teams_hm = []
teams_aw = []

pitcher_hm = []
pitcher_aw = []

hit_cols = ['hitman_hm_1','hitman_hm_2',
            'hitman_hm_3','hitman_hm_4','hitman_hm_5',
            'hitman_hm_6','hitman_hm_7','hitman_hm_8',
            'hitman_hm_9',
            
            'hitman_aw_1','hitman_aw_2',
            'hitman_aw_3','hitman_aw_4','hitman_aw_5',
            'hitman_aw_6','hitman_aw_7','hitman_aw_8',
            'hitman_aw_9']

home = ['hitman_hm_1','hitman_hm_2',
            'hitman_hm_3','hitman_hm_4','hitman_hm_5',
            'hitman_hm_6','hitman_hm_7','hitman_hm_8',
            'hitman_hm_9']

away = ['hitman_aw_1','hitman_aw_2',
            'hitman_aw_3','hitman_aw_4','hitman_aw_5',
            'hitman_aw_6','hitman_aw_7','hitman_aw_8',
            'hitman_aw_9']

def get_lineup(url):

    lineup_url = 'https://api-gw.sports.naver.com/schedule/games/' + url + '/preview' # 라인업
    result_url = 'https://api-gw.sports.naver.com/schedule/games/' +  url             # 결과

    response = requests.get(lineup_url).json()

    game_date = response['result']['previewData']['gameInfo']['gdate']
    team_hm = response['result']['previewData']['gameInfo']['hFullName']
    team_aw = response['result']['previewData']['gameInfo']['aFullName']
    players_hm = response['result']['previewData']['homeTeamLineUp']['fullLineUp']
    players_aw = response['result']['previewData']['awayTeamLineUp']['fullLineUp']

    game_info = requests.get(result_url).json()['result']['game']

    return game_info, game_date, team_hm, team_aw, players_aw, players_hm


def get_lineup(url):

    lineup_url = 'https://api-gw.sports.naver.com/schedule/games/' + url + '/preview' # 라인업
    result_url = 'https://api-gw.sports.naver.com/schedule/games/' +  url             # 결과

    response = requests.get(lineup_url).json()

    game_date = response['result']['previewData']['gameInfo']['gdate']
    team_hm = response['result']['previewData']['gameInfo']['hCode']
    team_aw = response['result']['previewData']['gameInfo']['aCode']
    pit_hm = response['result']['previewData']['gameInfo']['hPCode']
    pit_aw = response['result']['previewData']['gameInfo']['aPCode']


    return game_date, team_hm, team_aw, pit_hm, pit_aw
    
def start_crawl(urls):

    for url in urls:
        game_date, team_hm, team_aw, pit_hm, pit_aw = get_lineup(url)
    
        game_dates.append(str(game_date))

        teams_hm.append(team_hm)
        teams_aw.append(team_aw)
        
        pitcher_hm.append(str(pit_hm))
        pitcher_aw.append(str(pit_aw))



today_datetime = datetime.now()
today_date = today_datetime.strftime("%Y%m%d")

#today_datetime = (datetime.now() + timedelta(days=30))
#today_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")



today_year = int(today_date[:4])
today_month = int(today_date[4:6])
today_day = int(today_date[6:])

# return할 리스트
urls = []

all_url = f'https://sports.news.naver.com/kbaseball/schedule/index?month={today_month}&year={today_year}&teamCode='

response = requests.get(all_url)
soup = BeautifulSoup(response.text, 'html.parser')
x = soup.find_all('span', class_ = 'td_btn')


for line in x:
    url = line.find('a')['href'][6:-7]

    if int(url[:8]) == int(today_date):
        if not url in urls:
            urls.append(url)



if len(urls) == 0:
    tomorrow = (today_datetime + timedelta(days=1)).strftime("%Y%m%d")
    for line in x:
        url = line.find('a')['href'][6:-7]

        if int(url[:8]) == int(tomorrow):
            if not url in urls:
                urls.append(url)    



if not len(urls) == 0:
    reset_crawl()
    start_crawl(urls)
    
    col_names = ['game_dates', 'teams_hw', 'teams_aw', 'pitcher_hm', 'pitcher_aw']
    
    df = pd.DataFrame(list(zip(game_dates, teams_hm , teams_aw, pitcher_hm, pitcher_aw)),columns = col_names)
    
    for i in hit_cols:
        df[i] = 0
    
    lineup = pd.read_csv('BASE_lineup.csv')
    lineup = lineup.sort_values('game_dates', ascending=False).reset_index()
    
    ALL_TRUE = {'SK' : False, 'LG' : False, 'HH' : False, 'WO' : False, 'SS' : False, 'HT' : False, 'KT' : False, 'LT' : False, 'NC' : False, 'OB' : False}
    
    i = 0
    
    while not all(value for value in ALL_TRUE.values()):
        
        if lineup.iloc[i]['homeTeamCode'] in ALL_TRUE.keys():
            if ALL_TRUE[lineup.iloc[i]['homeTeamCode']] == False:
    
            
                indices = df.loc[(df['teams_hw'] == lineup.iloc[i]['homeTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], home] = list(lineup.iloc[i]['hitman_hm_1':'hitman_hm_9'])
                    ALL_TRUE[lineup.iloc[i]['homeTeamCode']] = True
        
        
                    
                indices = df.loc[(df['teams_aw'] == lineup.iloc[i]['homeTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], away] = list(lineup.iloc[i]['hitman_hm_1':'hitman_hm_9'])
                    ALL_TRUE[lineup.iloc[i]['homeTeamCode']] = True
                    
        
        if lineup.iloc[i]['awayTeamCode'] in ALL_TRUE.keys():
            if ALL_TRUE[lineup.iloc[i]['awayTeamCode']] == False:
                
                indices = df.loc[(df['teams_hw'] == lineup.iloc[i]['awayTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], home] = list(lineup.iloc[i]['hitman_aw_1':'hitman_aw_9'])
                    ALL_TRUE[lineup.iloc[i]['awayTeamCode']] = True
    
    
                    
                indices = df.loc[(df['teams_aw'] == lineup.iloc[i]['awayTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], away] = list(lineup.iloc[i]['hitman_aw_1':'hitman_aw_9'])
                    ALL_TRUE[lineup.iloc[i]['awayTeamCode']] = True
        i += 1
    
    
    


else:
    df = pd.DataFrame(columns = ['game_dates', 'teams_hw', 'teams_aw', 'pitcher_hm', 'pitcher_aw',
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9'])


if df['pitcher_aw'].iloc[0] == '':
    df = pd.DataFrame( columns = ['game_dates', 'teams_hw', 'teams_aw', 'pitcher_hm', 'pitcher_aw',
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9'])


df.to_csv('tomorrow_lineup.csv')
df = pd.read_csv('tomorrow_lineup.csv')
df.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
df.to_csv('tomorrow_lineup.csv',index = False)


df = pd.read_csv('tomorrow_lineup.csv')
hit = df[[
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9']]

pit = df[['pitcher_hm', 'pitcher_aw']]

hit_code = list(set(hit.values.flatten().tolist()))
pit_code = list(set(pit.values.flatten().tolist()))

Basedf_pit = pd.read_csv('DB_pit.csv')
Basedf_hit = pd.read_csv('DB_hit.csv')

Basedf_pit = Basedf_pit.groupby('code').tail(5).reset_index(drop=True)
Basedf_pit = Basedf_pit.groupby('code').filter(lambda x: x['code'].iloc[0] in pit_code)

Basedf_hit = Basedf_hit.groupby('code').tail(5).reset_index(drop=True)
Basedf_hit = Basedf_hit.groupby('code').filter(lambda x: x['code'].iloc[0] in hit_code)

Basedf_pit = Basedf_pit.drop(['idx'], axis = 1)
Basedf_hit = Basedf_hit.drop(['idx'], axis = 1)

Basedf_pit['out'] = Basedf_pit['ip'].apply(int) *3 + (Basedf_pit['ip'] - Basedf_pit['ip'].apply(int))*10

pit_5days = Basedf_pit.groupby(['code']).sum()
pit_5days['count'] = list(Basedf_pit.groupby(['code']).size().reset_index()[0])

pit_5days['bbb'] = pit_5days['bb'].replace(0,1) 


pit_5days['era'] = round(pit_5days['er'] * 9 / (pit_5days['out'] / 3), 2)
pit_5days['k/pit'] = round(pit_5days['k'] / pit_5days['pit'], 3)
pit_5days['k/bb'] = round(pit_5days['k'] / pit_5days['bbb'], 3)
pit_5days['whip'] = round( (pit_5days['hit'] + pit_5days['ibb']+ pit_5days['hbp']+ pit_5days['bb']) /  (pit_5days['out'] / 3),3)
pit_5days['wpa'] = round(pit_5days['wpa'],3) 
pit_5days['re24'] = round(pit_5days['re24'],3)

pit_5days = pit_5days.reset_index()
pit_5days = pit_5days[['code','era', 'k/pit', 'k/bb', 'whip', 'wpa', 're24']]

pit_5days.to_csv('pit_5days.csv')
pit_5days = pd.read_csv('pit_5days.csv')
pit_5days.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
pit_5days.to_csv('pit_5days.csv',index = False)

hit_5days = Basedf_hit.groupby(['code']).sum()
hit_5days['count'] = list(Basedf_hit.groupby(['code']).size().reset_index()[0])

hit_5days['ab'] = hit_5days['pa']
hit_5days['pa'] = hit_5days['ab'] + hit_5days['bb'] + hit_5days['hbp'] + hit_5days['ibb'] + hit_5days['sh'] + hit_5days['sf']
hit_5days['kk'] = hit_5days['k'].replace(0,1)


hit_5days['avg'] = round(hit_5days['hit'] / hit_5days['ab'], 3)
hit_5days['slg'] = round( (hit_5days['hit'] + hit_5days['second'] + hit_5days['third']*2 +hit_5days['homerun']*3) / hit_5days['ab'], 3)
hit_5days['obp'] = round( ( (hit_5days['hit'] + hit_5days['bb'] + hit_5days['ibb'] + hit_5days['hbp']) / hit_5days['pa'] ), 3)
hit_5days['bb/k'] = round( hit_5days['bb'] / hit_5days['kk'] , 3)
hit_5days['wpa'] = round(hit_5days['wpa'],3)
hit_5days['re24'] = round(hit_5days['re24'],3)

hit_5days = hit_5days.reset_index()
hit_5days = hit_5days[['code','avg', 'slg', 'obp', 'bb/k', 'wpa', 're24']]

hit_5days.to_csv('hit_5days.csv')
hit_5days = pd.read_csv('hit_5days.csv')
hit_5days.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
hit_5days.to_csv('hit_5days.csv',index = False)