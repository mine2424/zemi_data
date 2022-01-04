/*
Regpractice.do
name: Ryota Nishimine
2020/9/29
*/

/// regression.do

// income(y) yeduc(x)の散布図
scatter income yeduc

// level-level
reg income yeduc	

// log-level
gen lnincome = log(income)
reg lnincome yeduc

// level-log
gen lnyeduc = log(yeduc)
reg income lnyeduc

// log-log
reg lnincome lnyeduc

// incomeの単位を１０００円にする(level-levelだと単位合わせが重要)
gen income1000 = income*10
reg income1000 yeduc

// income1000のログレベルの推定値βとincomeのログレベルの推定値βを比較してください
gen lnincome1000 = log(income1000)
reg lnincome1000 yeduc


/// IceCream2.do

// 被説明変数をIcecream説明変数をIncomeにして散布図と書いて回帰分析してください。(外れ値等を確認)
scatter icecream income
reg icecream income

// icecream=b0+b1income+b2u15+U(t値が1.64(10%)より大きくないと優位ではない)
reg icecream income u15

// extra

//東日本は1それ以外は0のダミー変数作成
gen dummy=1 in 1/25
replace dummy=0 if dummy==. 

reg icecream income u15 dummy


// 推計結果をwordに書き出し
outreg2 using title.doc,replace ctitle(model1)
outreg2 using title.doc,append ctitle(model2)

// 記述統計の書き出し
outreg2 using title2.doc,replace sum(log)
