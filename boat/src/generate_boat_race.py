# coding: UTF-8
import re


def generate_common_race_list(data: str):
    newList = []
    isPassedCourse = False

    # print(data) => ['7R', '予', '選', '進入固定', 'H1800m', '晴', '風', '東', '5m', '波', '5cm']
    print(data)
    for index, elm in enumerate(data):

        if isPassedCourse == False:
            # 最初を通過してからコースの長さ(H1800m)が出てくるまでスキップ
            if index == 0:
                newList.append(elm)
            else:
                if elm == "進入固定":
                    # 一番初めに挿入する。
                    newList.insert(0, elm)
                if 'H' in elm:
                    newList.append(elm)
                    isPassedCourse = True
        else:
            if not "風" in elm and not "波" in elm:
                if "m" in elm:
                    if "cm" in elm:
                        newList.append(elm.replace("cm", ""))
                    else:
                        newList.append(elm.replace("m", ""))
                else:
                    newList.append(elm)
            elif "無風" in elm:
                newList.append("無")

    return newList


def generate_race_result_list(datalist: list, indexElm: int):
    allList = []
    for counter in range(6):
        resultlist = datalist[indexElm+counter].split()
        generatedResultList = []
        playerName = []

        # 各選手のレース結果と情報(横列)
        # resultlist => ['04', '2', '3441', '土', '屋', '太', '朗', '45', '33', '6.79', '2', '0.19', '1.54.7']
        print(resultlist)
        for dx, result in enumerate(resultlist):
            if is_int(result):
                generatedResultList.append(result)
            elif is_float(result):
                generatedResultList.append(result)
            elif dx == len(resultlist)-1:
                if result == '.':
                    generatedResultList.append(".  .")
                else:
                    generatedResultList.append(result)
            else:
                if result == '.':
                    continue
                elif 'K' in result or 'S' in result or 'F' in result or 'L1' in result:
                    generatedResultList.append(result)
                else:
                    playerName.append(result)

            if dx == 9:
                generatedResultList.insert(0, ''.join(playerName))

        allList.append(generatedResultList)

    return allList


def is_int(s):
    p = '[-+]?\d+'
    return True if re.fullmatch(p, s) else False


def is_float(s):
    p = '[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?'
    return True if re.fullmatch(p, s) else False


def create_Excel_Data_from_Local_data(columnCount: int, index: int, data: str, sheet, txtFile, datalist: list):
    indexElm = 0
    roundDict = {"着順": " ", "艇番": " ", "登録番号": " ", "選手名": " ", "オッズ": " ", "体重": " ", "ﾓｰﾀｰ": " ", "ﾎﾞｰﾄ": " ", "展示": " ", "進入": " ", "ST": " ", "ﾚｰｽﾀｲﾑ": " ", "進入固定": " ",
                 "ラウンド": " ", "コース(m)": " ", "天気": " ", "風向": " ", "風速(m)": " ", "波(cm)": " ", "日付": " ", "開催場所": " ", "大会名": " ", "SG": " ", "G1": " ", "G2": " ", "G3": " ", "一般": " "}
    fixedEnter = 0
    #　①[選手名]までローカル配列から取得、[オッズ][体重]は最初は空のstrを入れておく、（SGより右も同様）
    # これらを配列に挿入してcsvに入れる準備をする。6回回ったら終了
    if 'R' in data and index > 2:
        generatedData = generate_common_race_list(data.split())
        # generatedDataを出力してどの部分に「進入固定」があるか探す。
        # print(generatedData) =>  ['7R', 'H1200m', '雨', '北東', '6', '10']
        print(generatedData)

        if generatedData[0] == "進入固定":
            fixedEnter = 1
            roundDict.update(
                {
                    "ラウンド": int(generatedData[1][:-1]),
                    "コース(m)": generatedData[2][:-1],
                    "天気": generatedData[3],
                    "風向": generatedData[4],
                    "風速(m)": int(generatedData[5]),
                    "波(cm)": int(generatedData[6]),
                    "日付": txtFile[3:],
                }
            )
        else:
            roundDict.update(
                {
                    "ラウンド": int(generatedData[0][:-1]),
                    "コース(m)": generatedData[1][:-1],
                    "天気": generatedData[2],
                    "風向": generatedData[3],
                    "風速(m)": int(generatedData[4]),
                    "波(cm)": int(generatedData[5]),
                    "日付": txtFile[3:],
                }
            )
        indexElm = index + 3

    # データ項目名を取得
    if index == 0:
        # セルへ書き込む
        indexListCount = 1
        for headElm in roundDict.keys():
            sheet.cell(row=1, column=indexListCount).value = headElm
            indexListCount += 1

    # レースの結果分を取得(縦列)
    if indexElm != 0:
        columnCountMin = columnCount
        # １レース（6回分、for文が動く）
        for raceResult in generate_race_result_list(datalist=datalist, indexElm=indexElm):
            intrusion = ".  ."
            st = ".  ."
            raceTime = ".  ."

            # indexが7以降要素があるかどうか分岐する
            if raceResult[7:8]:
                intrusion = raceResult[7]
            if raceResult[8:9]:
                st = raceResult[8]
            if raceResult[9:10]:
                raceTime = raceResult[9]

            roundDict.update(
                {
                    "着順": raceResult[1],
                    "艇番": int(raceResult[2]),
                    "登録番号": int(raceResult[3]),
                    "選手名": raceResult[0],
                    "ﾓｰﾀｰ": int(raceResult[4]),
                    "ﾎﾞｰﾄ": raceResult[5],
                    "展示": raceResult[6],
                    "進入": intrusion,
                    "ST": st,
                    "ﾚｰｽﾀｲﾑ": raceTime,
                    "進入固定": fixedEnter,
                }
            )

            # 横列のindex
            cellIndex = 1
            # columnCountを固定させて、roundDictから艇番を取得して、艇番順に並び替える
            boatNumber = columnCountMin + int(roundDict["艇番"]) - 1

            for cellValue in roundDict.values():
                sheet.cell(row=boatNumber, column=cellIndex).value = cellValue
                cellIndex += 1
            columnCount += 1

    return columnCount


def generate_one_day_race_result_list(sheet, jsonData):
    txtFile = f'../local_boat_data/{jsonData["txtFile"]}.TXT'
    f = open(txtFile, 'r', encoding='shift_jis')
    datalist = f.readlines()
    f.close()

    placeTour = []
    # 現在のcolumnの行数
    columnCount = 2

    for index, data in enumerate(datalist):
        if '［成績］' in data:
            c = data.find("［")
            placeTour.append(re.sub(r"[\u3000 \t \n]", "", data[:c]))
            placeTour.append(re.sub(r"[\u3000 \t \n]", "", datalist[index+4]))

        columnCount = create_Excel_Data_from_Local_data(
            columnCount=columnCount,
            index=index,
            data=data,
            sheet=sheet,
            txtFile=jsonData["txtFile"],
            datalist=datalist
        )

    return placeTour
