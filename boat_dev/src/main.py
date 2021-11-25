# coding: UTF-8
import datetime
import openpyxl
import os

import generate_boat_race
import scraping_boat_data
import util

# =========== main function =============================================


def main(tour_url_list):
    initializedSheet = openpyxl.Workbook()
    exfile = "2018_boat_data"
    excelFile = f'../excel_data/{exfile}.xlsx'
    initializedSheet.save(excelFile)
    book = openpyxl.load_workbook(excelFile)
    sheet = book.worksheets[0]

    # 全体のcolumnCountを管理する変数
    all_column_count = 2
    all_scraping_column_count = 2

    for i, url in enumerate(tour_url_list):

        file_name = url[48:55]

        print(f"{file_name}分のボートデータをexcelに書き込み中")

        pre_tour_count = 2
        if i != 0:
            pre_tour_count = all_column_count

        # txt dataを展開し整理する
        one_day_result_list = generate_boat_race.generate_one_day_race_result_list(
            sheet=sheet,
            name="K"+file_name,
            column_count=all_column_count
        )

        tour_place_list = one_day_result_list[0]
        tour_name_list = one_day_result_list[1]
        all_column_count += one_day_result_list[2]
        round_list_by_day = one_day_result_list[3]

        # 1日に行う全トーナメントのurlの取得
        tour_url_list_by_day = scraping_boat_data.scraping_tournament_url_by_day(
            url,
            round_list_by_day,
        )
        tour_url_list = tour_url_list_by_day[0]
        rank_list = tour_url_list_by_day[1]
        tour_series_list = tour_url_list_by_day[2]
        time_zone_list = tour_url_list_by_day[3]

        # 保存する
        book.save(excelFile)

        ccp = 0
        for index, url in enumerate(tour_url_list):
            all_scraping_column_count = scraping_boat_data.scraping_one_tournament(
                sheet=sheet,
                url=url,
                columnCount=all_scraping_column_count,
            )
            ccp += 1
            book.save(excelFile)
            print(f'スクレイピング進捗 : {ccp}/{len(tour_url_list)}')
            
        # 1日分が重複して記入されている。（1日分ずらすためにカウントが必要かも）
        util.generate_other_boat_data(
            pre_tour_count=pre_tour_count,
            tour_place_list=tour_place_list,
            tour_name_list=tour_name_list,
            reservedRaceRank=rank_list,
            roundIndexList=round_list_by_day,
            time_zone_list=time_zone_list,
            tour_series_list=tour_series_list,
            sheet=sheet,
        )


        # 保存する
        book.save(excelFile)
        print(f"{file_name}分の書き込みが完了しました")
        print("=============================================")
        print(" ")

    util.delete_empty_no_len_rows_in_excel(exfile)


# file nameから日時を取得してくる
folder_name = '../local_boat_data'
file_name_list = os.listdir(folder_name)

file_name_list.sort()

# TODO: 1900年代にも対応できるようにする
start_time = '20' + file_name_list[0][1:-4]
finish_time = '20' + file_name_list[-1][1:-4]

time_list = []


def split_YYMMDD_word(time: list, isFinish: bool):
    figure = ''
    for index, elm in enumerate(list(time)):
        figure += elm

        if index == 3:
            time_list.append(int(figure))
            figure = ''
        elif index == 5:
            time_list.append(int(figure))
            figure = ''
        elif index == len(list(start_time))-1:
            dayFigure = 0
            if isFinish:
                # HACK; macでは「+1」が必要ない？
                dayFigure = int(figure)
            else:
                dayFigure = int(figure)
            time_list.append(dayFigure)
            figure = ''


split_YYMMDD_word(list(start_time), False)
split_YYMMDD_word(list(finish_time), True)

# 指定された日時の「本日のデータ」のurlを取得する
tour_url_list = scraping_boat_data.generate_all_tournament_url(
    datetime.date(time_list[0], time_list[1], time_list[2]),
    datetime.date(time_list[3], time_list[4], time_list[5]),
)

main(tour_url_list)
