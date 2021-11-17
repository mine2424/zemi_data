# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import time
import datetime


def requested_url(reqUrl: str):
    res = requests.get(reqUrl)
    res.encoding = res.apparent_encoding

    return BeautifulSoup(res.text, "lxml")


def scrapingRaceListByRound(roundTag: str):
    detailRound = requested_url(roundTag)
    roundPage = detailRound.find("ul", class_="tab3_tabs")
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
    weightTable = weightPage.find_all("td")

    weightList = []

    for weight in weightTable:
        if "kg" in weight.text:
            weightList.append(weight.text)

    return oddPointsList, weightList


def scrapingOnetournament(sheet, url: str, columnCount: int, roundCount: int):
    html = requested_url(url)

    table1 = html.find("div", class_="table1")

    roundTagList = []
    resultList = []
    # oddとinfoのurl取得
    for a in table1.find_all('td', class_="is-fs14 is-fBold"):
        roundTag = "https://www.boatrace.jp" + a.find("a").get("href")
        roundTagList.append(roundTag)

    for raceRound in roundTagList:
        resultList.append(scrapingRaceListByRound(raceRound))
        time.sleep(2)

    # if columnCount != 2:
        # columnCount = columnCount + (2 + (roundCount * 6))

    # 1Race、１ループ
    for result in resultList:
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

# TODO: 本日のレースから取得する（https://www.boatrace.jp/owpc/pc/race/index?hd=20200615の「hd=」以降を変更すればデータが取得できる）
# TODO: <td class=is-alignL is-fBold is-p10-7>の中にaタグがあるのでそこから各レースを取得する
# TODO: 今の実装と結合できるように調整する
# TODO: raceRankListとroundIndexListを取得できるようにする
# 中止の場合は取得しない（スクレイピング時にラウンド数を取得するようにする（進行状況欄））
# その他順延等もあるので随時確認する
# nR以降中止
# モーニングサマータイムナイタールーキーシリーズオールレディースヴィーナスシリーズも考慮に入れる（ダミー変数）
# 払戻金を除外する機能を実装する

# TODO: jsonは使用せずにlocal_boat_dataだけで日時をカウントするようにする


def generate_all_tournament_url(start: datetime.date, end: datetime.date):
    # 各レースのurlを取得し、最後に配列として返す
    tour_url_list = []

    # 最初の取得日時と最後に取得する日時
    current_time = datetime.date(start.year, start.month, start.day)
    print(current_time)

    # 「本日のレース」の指定日時分のurlを取得
    while True:
        if current_time == end:
            break

        url = "https://www.boatrace.jp/owpc/pc/race/index?hd=" + \
            str(current_time.year) + \
            str(current_time.month).zfill(2) + \
            str(current_time.day).zfill(2)
        tour_url_list.append(url)
        print(url)
        current_time += datetime.timedelta(days=1)
