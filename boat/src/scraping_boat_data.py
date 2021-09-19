# coding: UTF-8
import re
import openpyxl
import requests
from bs4 import BeautifulSoup
import time
import json

def requested_url(reqUrl: str):
  res = requests.get(reqUrl)
  res.encoding = res.apparent_encoding

  return BeautifulSoup(res.text, "lxml")

def raceListByRound(roundTag: str):
  detailRound = requested_url(roundTag)
  roundPage = detailRound.find("ul", class_="tab3_tabs")
  spans = roundPage.find_all("a")

  oddAndInfoUrlList: str = []

  for span in spans:
    spanTag = "https://www.boatrace.jp" + span.get("href")
    oddAndInfoUrlList.append(spanTag)

  oddUrl = oddAndInfoUrlList[0].replace("odds3t","oddstf")

  oddPage = requested_url(oddUrl)
  oddPoints = oddPage.find_all("td" ,class_="oddsPoint")

  oddPointsList = []

  for index,point in enumerate(oddPoints):
    if index < 6:
      oddPointsList.append(point.text)

  detailInfoPage = requested_url(oddAndInfoUrlList[1])
  weightPage = detailInfoPage.find("table",class_="is-w748")
  weightTable = weightPage.find_all("td")

  weightList = []

  for weight in weightTable:
    if "kg" in weight.text:
      weightList.append(weight.text)

  return oddPointsList,weightList

def scrapingOnetournament(sheet ,url: str, columnCount: int, roundCount:int):
  html = requested_url(url)

  table1 = html.find("div", class_="table1")

  roundTagList = []
  resultList = []
  # oddとinfoのurl取得
  for a in table1.find_all('td', class_="is-fs14 is-fBold"):
    roundTag = "https://www.boatrace.jp" + a.find("a").get("href")
    roundTagList.append(roundTag)

  for raceRound in roundTagList:
    resultList.append(raceListByRound(raceRound))
    time.sleep(2)

  # if columnCount != 2:
    # columnCount = columnCount + (2 + (roundCount * 6))
    

  # 1Race、１ループ
  for index,result in enumerate(resultList):
    odds = result[0]
    weights = result[1]

    for odd in odds:
      # その位置の艇番
      sheet.cell(row=columnCount,column=5).value = odd
      columnCount += 1

    columnCount -= 6

    for weight in weights:
      # その位置の艇番
      sheet.cell(row=columnCount,column=6).value = weight[:-2]
      columnCount += 1
  
  return columnCount
