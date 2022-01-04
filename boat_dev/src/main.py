# coding: UTF-8
import datetime
import openpyxl
import os

import generate_boat_race
import scraping_boat_data
import util

# 解消すべき問題点
# TODO: oddとweightが一致しない時、欠場等があるのにそれを無視して次の選手のデータが挿入されていることがある
# TODO: 必要のない謎文字が最後の位置れるに入っていることがある。（１が起因しているかも）

# 今後のタスク
# TODO: そのレースが予選なのか優勝戦なのかをダミー年数でまとめる
# TODO: 2012年のデータが取れればとる

# やるべきこと
# TODO: 大会名やそれに関するダミー変数が空白で一気に抜けることがあるのでインデックスやカウントの飛びがないかを確認する
# TODO: tour_place_listで中止となった大会の他にその周辺の大会もスキップされていることがある。
# TODO: round_list_by_dayに-1が挿入されていたらそのレース分は中止となっているのでごっそり消すかどうか検討する
# TODO: len(tour_place_list): 10, len(roundIndexList): 11　特に中止となったレースがある大会はこのようになっている。

# =========== main function =============================================


def main(all_tour_url_list):
    for x, tour_url_list in enumerate(all_tour_url_list):
        if x == 0:
            initializedSheet = openpyxl.Workbook()
            exfile = f"{tour_url_list[0][-6:-2]}_boat_data"
            excelFile = f'../excel_data/{exfile}.xlsx'
            initializedSheet.save(excelFile)
            book = openpyxl.load_workbook(excelFile)
            sheet = book.worksheets[0]

            # 全体のcolumnCountを管理する変数
            all_column_count = 2
            all_scraping_column_count = 2

            print(f"{exfile}の書き込み中")

            for i, url in enumerate(tour_url_list):

                file_name = url[48:55]

                print(f"{file_name}分のボートデータをexcelに書き込み")

                pre_tour_count = 2
                if i != 0:
                    pre_tour_count = all_column_count

                # txt dataを展開し整理する
                # TODO: 取得数の確認をすること
                one_day_result_list = generate_boat_race.generate_one_day_race_result_list(
                    sheet=sheet,
                    time=tour_url_list[0][-6:-2],
                    name="K" + file_name,
                    column_count=all_column_count,
                )
                tour_place_list = one_day_result_list[0]
                tour_name_list = one_day_result_list[1]
                all_column_count = one_day_result_list[2]
                round_list_by_day = one_day_result_list[3]

                # 1日に行う全トーナメントのurlの取得
                # TODO: 取得数の確認をすること
                tour_url_list_by_day = scraping_boat_data.scraping_tournament_url_by_day(
                    url=url,
                    round_list_by_day=round_list_by_day,
                )
                tour_url_list = tour_url_list_by_day[0]
                rank_list = tour_url_list_by_day[1]
                tour_series_list = tour_url_list_by_day[2]
                time_zone_list = tour_url_list_by_day[3]

                # 保存する
                book.save(excelFile)

                # TODO: データ取得後に仮に欠場等で空白となっている選手の箇所を空文字として開ける。
                # ccp = 0
                # for url in tour_url_list:
                #     # TODO: all_scraping_column_countの記録をとる
                #     all_scraping_column_count = scraping_boat_data.write_odd_and_weight_for_excel(
                #         sheet=sheet,
                #         url=url,
                #         columnCount=all_scraping_column_count,
                #         exfile=exfile,
                #     )
                #     ccp += 1
                #     book.save(excelFile)
                #     print(f'スクレイピング進捗 : {ccp}/{len(tour_url_list)}')

                # 他の変数を書き込み
                # TODO: 何かしらのカウント、インデックスの影響で大会名等が飛ぶことがあるので確認する
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
                print(" ")

            # TODO: 空白行を削除
            util.delete_empty_rows_in_excel(exfile)
            # util.delete_empty_no_len_rows_in_excel(exfile)

            # 保存する
            book.save(excelFile)
            print(f"{exfile}の書き込み完了")
            pre_tour_url = tour_url_list


# file nameから日時を取得してくる
folder_name = '../local_boat_data'
file_name_list = os.listdir(folder_name)

file_name_list.sort()

# TODO: 1900年代にも対応できるようにする
start_time = '20' + file_name_list[1][1:-4]
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
        elif index == len(list(start_time)) - 1:
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
all_tour_url_list = scraping_boat_data.generate_all_tournament_url(
    datetime.date(time_list[0], time_list[1], time_list[2]),
    datetime.date(time_list[3], time_list[4], time_list[5]),
)

main(all_tour_url_list)
