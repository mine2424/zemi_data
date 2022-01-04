# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import datetime
from time import sleep
from urllib.error import HTTPError
from urllib.error import URLError

def requested_url(reqUrl: str):
    stand_by_sec = 5
    try:
        res = requests.get(reqUrl, timeout=3.5)
    except HTTPError as e:
        #エラーの場合の処理
        print(f'an error ocurred: {e}')
        
    except URLError:
        #エラーの場合の処理
        print("URLに接続するが処理できない")
        
    except ConnectionError:
        print("通信エラーです。再接続します。")
        requested_url(reqUrl)
        
    except ConnectionResetError:
        # TODO: 該当エラー年月（190222 8/13, 190622 9/13）
        print("強制的にssl接続が切断されました。再接続します。")
        requested_url(reqUrl)
        
    except requests.exceptions.ConnectTimeout:
        print(f"\rタイムアウトしました...\n再接続待機中...{stand_by_sec}秒後に再実行します", end="", flush=True)
        sleep(stand_by_sec)
        requested_url(reqUrl)
    else:
        return BeautifulSoup(res.text, "lxml")

def request_url_test_by_round(url: str, i: int):
    round_url = requested_url(url)
    data_index_list = round_url.find("ul", class_="tab3_tabs")
    if data_index_list is None:
        print('タブリストがありません')
    else:
        data_index_list.find_all("a")
        print(f'現在のスクレイピングのカウントは「{i}」です')

def scraping_odd_weight_data_by_round(roundTag: str):
    detailRound = requested_url(roundTag)
    roundPage = detailRound.find("ul", class_="tab3_tabs")
    if roundPage is None:
        print(f'round page: {roundPage}')
    else:
        spans = roundPage.find_all("a")

    oddAndInfoUrlList: str = []

    for span in spans:
        spanTag = "https://www.boatrace.jp" + span.get("href")
        oddAndInfoUrlList.append(spanTag)

    oddUrl = oddAndInfoUrlList[0].replace("odds3t", "oddstf")

    oddPage = requested_url(oddUrl)
    oddPoints = oddPage.find_all("td", class_="oddsPoint")

    oddPointsList = []

    for index, point in enumerate(oddPoints):
        if index < 6:
            oddPointsList.append(point.text)

    detailInfoPage = requested_url(oddAndInfoUrlList[1])
    weightPage = detailInfoPage.find("table", class_="is-w748")
    # TODO: 該当のエラー年月(180320 8/12, 180721 3/13, 200222 7/14, 201121 4/15)
    if weightPage is None:
        print(f'weight page: {weightPage}')
    else:
        weightTable = weightPage.find_all("td")

    weightList = []

    for weight in weightTable:
        if "kg" in weight.text:
            weightList.append(weight.text)

    return oddPointsList, weightList


# １トーナメント単位でoddとweightをexcelに記入する
def scraping_one_tournament(sheet, url: str, columnCount: int):
    html = requested_url(url)

    # HACK: そもそもfindでtable1が見つかっていないのでその続きのfind_allがエラーを返してしまう。
    table1 = html.find("div", class_="table1")

    roundTagList = []
    odd_weight_data_list = []
    # find_allでNoneだったらその分スキップさせる
    if table1 == None or table1 == 0:
        print('this round is none')
    else:
        round_url_list = table1.find_all('td', class_="is-fs14 is-fBold")
        for a in round_url_list:
            roundTag = "https://www.boatrace.jp" + a.find("a").get("href")
            roundTagList.append(roundTag)

        # oddとinfoのurl取得
        for raceRound in roundTagList:
            odd_weight_data = scraping_odd_weight_data_by_round(raceRound)
            odd_weight_data_list.append(odd_weight_data)

        # 1Race、１ループ
        for result in odd_weight_data_list:
            odds = result[0]
            weights = result[1]

            for odd in odds:
                # その位置の艇番
                sheet.cell(row=columnCount, column=5).value = odd
                columnCount += 1

            columnCount -= 6

            for weight in weights:
                # その位置の艇番
                sheet.cell(row=columnCount, column=6).value = weight[:-2]
                columnCount += 1

    return columnCount


def generate_all_tournament_url(start: datetime.date, end: datetime.date):
    # 各レースのurlを取得し、最後に配列として返す
    tour_url_list = []

    # 最初の取得日時と最後に取得する日時
    current_time = datetime.date(start.year, start.month, start.day)

    # 「本日のレース」の指定日時分のurlを取得
    while True:
        url = "https://www.boatrace.jp/owpc/pc/race/index?hd=" + \
            str(current_time.year) + \
            str(current_time.month).zfill(2) + \
            str(current_time.day).zfill(2)
        tour_url_list.append(url)

        if current_time == end:
            break
        current_time += datetime.timedelta(days=1)
    
    all_tour_url_list_by_month = []
    tour_url_list_by_month = []
    
    preMonth = tour_url_list[0][-4:-2]
    
    for i in range(len(tour_url_list)):
        if tour_url_list[i][-4:-2] != preMonth:
            all_tour_url_list_by_month.append(tour_url_list_by_month)
            
            tour_url_list_by_month = []
            tour_url_list_by_month.append(tour_url_list[i])
        elif i == len(tour_url_list)-1:
            tour_url_list_by_month.append(tour_url_list[len(tour_url_list)-1])
            all_tour_url_list_by_month.append(tour_url_list_by_month)
        else:
            tour_url_list_by_month.append(tour_url_list[i])

        preMonth = tour_url_list[i][-4:-2]

    return all_tour_url_list_by_month


def scraping_tournament_rank(tbody):
    # <tbody>をfind_allした後に先頭(find)から検索をかけて順番通りにランクを並べる
    if tbody.find('td', class_='is-G1b') != None:
        return 'G1'
    if tbody.find('td', class_='is-G2b') != None:
        return 'G2'
    if tbody.find('td', class_='is-G3b') != None:
        return 'G3'
    if tbody.find('td', class_='is-SGa') != None:
        return 'SG'
    if tbody.find('td', class_='is-ippan') != None:
        return 'GE'


def scraping_tournament_series(tbody):
    # <tbody>をfind_allした後に先頭(find)から検索をかけて順番通りにトーナメントシリーズを並べる
    if tbody.find('td', class_='is-venus') != None:
        return 'venus'
    elif tbody.find('td', class_='is-lady') != None:
        return 'lady'
    elif tbody.find('td', class_='is-rookie__3rdadd') != None:
        return 'rookie'
    else:
        return 'none'


def scraping_tournament_time_zone(tbody):
    # <tbody>をfind_allした後に先頭(find)から検索をかけて順番通りにトーナメントの時間帯を並べる
    if tbody.find('td', class_='is-nighter') != None:
        return 'nighter'
    elif tbody.find('td', class_='is-summer') != None:
        return 'summer'
    elif tbody.find('td', class_='is-morning') != None:
        return 'morning'
    else:
        return 'none'


def scraping_tournament_url_by_day(url: str, round_list_by_day: list):
    html = requested_url(url)
    table1 = html.find("div", class_="table1")

    tour_url_list = []
    rank_list = []
    tour_series_list = []
    time_zone_list = []

    # tourのurl取得
    for a in table1.find_all('td', class_='is-alignL is-fBold is-p10-7'):
        tour_url = 'https://www.boatrace.jp' + a.find('a').get('href')
        tour_url_list.append(tour_url)

    tbodys = table1.find_all('tbody')
    for tbody in tbodys:
        # 全トーナメントのランクを取得 (class=is-G1b, is-G2b, is-G3b, is-SGa, is-ippan)
        current_rank = scraping_tournament_rank(tbody)
        rank_list.append(current_rank)

        # 全トーナメントのシリーズ(ルーキ、オールレディース、ヴィナース)を取得 (class=is-nighter, is-summer, is-morning)
        current_tour_series = scraping_tournament_series(tbody)
        tour_series_list.append(current_tour_series)

        # 全トーナメントの時間帯を取得（モーニング、サマータイム、ナイター） (is-venus or is-lady or is-rookie__3rdadd)
        current_time_zone = scraping_tournament_time_zone(tbody)
        time_zone_list.append(current_time_zone)

    tour_url_list.reverse()
    rank_list.reverse()
    tour_series_list.reverse()
    time_zone_list.reverse()

    pop_elm_count = 0
    print(f'round_list_by_day: {round_list_by_day}')
    print(f'tour_url_list: {tour_url_list}')
    # TODO: 中止になったデータだけurlがないか、飛ばされているので、中止となったレース分の時間帯、シリーズの要素を消すようにする(tour_series_list, time_zone_list)
    for i, round_index in enumerate(round_list_by_day):
        if round_index == -1:
            tour_url_list.pop(i - pop_elm_count)
            rank_list.pop(i - pop_elm_count)
            tour_series_list.pop(i - pop_elm_count)
            time_zone_list.pop(i - pop_elm_count)
            pop_elm_count += 1
    
    return tour_url_list, rank_list, tour_series_list, time_zone_list
