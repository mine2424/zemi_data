/*-------------------------------------------------
Regression.do
目的：実用的な分析
作成者：高倉詩織
作成日：2021年9月26日（更新日：2021年9月29日）
-------------------------------------------------*/

*作業フォルダの指定*
cd C:\Users\Ma43H\Downloads\shio\shigezemi\Tool\Stata\計量経済学演習\Data


*現在の作業フォルダの確認*
pwd


/*-------------------------------------------------*/
*単回帰分析*
*計量経済学演習5 問題2 P34*
*Excelファイル（Income）のインポート*
. import excel "C:\Users\Ma43H\Downloads\shio\shigezemi\Tool\Stata\計量経済学演習\Data\income.xlsx", sheet("Sheet1") firstrow clear


*income=β0+β1yeduc+U*

*散布図*
scatter income yeduc

*レベル-レベル*
reg income yeduc
*A.修学年数が1年増えれば、年収が24万円増える*

*ログ-レベル*
gen lnincome = log(income)
reg lnincome yeduc
*A.修学年数が1年増えれば、年収が7％増加する*


*レベル-ログ*
gen lnyeduc = log(yeduc)
reg income lnyeduc
*A.修学年数が1％増えれば、年収が311万円増加する*


*ログ-ログ*
reg lnincome lnyeduc
*A.修学年数が1％増えれば、年収が89％増加する*


*incomeの単位を万円→千円に変更。推定値を比較*
gen income1000 = income*10
reg income1000 yeduc
*万単位と比べて推定値も10倍となっている*


*income1000のログレベルとincomeのログレベルの推定値を比較*
gen lnincome1000 = log(income1000)
reg lnincome1000 yeduc
*万単位と比べても推定値は変わらない*




/*-------------------------------------------------*/
*重回帰分析-自由度調整決定係数-*
*計量経済学演習6 問題1 P15*
*Excelファイル（IceCream2）のインポート*
. import excel "C:\Users\Ma43H\Downloads\shio\shigezemi\Tool\Stata\計量経済学演習\Data\IceCream2.xlsx", sheet("Sheet1") firstrow clear


*1. icecream=β0+β1income+U*
*散布図*
scatter icecream income

*回帰分析*
reg icecream income


*2. icecream=β0+β1income+β2u15+U*
reg icecream income u15


*東日本なら1、西日本なら0を取るダミー変数*
gen dummy =1 in 1/25
replace dummy =0 if dummy==.

reg icecream income u15 dummy



/*-------------------------------------------------*/




*推計結果をwordに書き出す*
outreg2 using title.doc,replace ctitle(model1)
outreg2 using title.doc,append ctitle(model2)

*記述統計をwordに書き出す*
outreg2 using title2.doc, replace sum(log)




exit,clear


