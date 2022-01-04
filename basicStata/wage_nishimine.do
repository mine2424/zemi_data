/*
西峰綾汰
8月19日課題
*/

// move reserved file
cd C:\Users\minew\Desktop\zemi_data\basicStata\

// import Wage.xlsx

// •experの２乗とログを作って下さい
replace exper = exper ^ 2 
replace lnexper = log(exper)

// 賃金が平均以上の観測値１それ以下を０として下さい
gen wageMoreAverage = 1 if wage > 5.908992
replace wageMoreAverage = 0 if wage <= 5.908992

// tenureが２０時間以上の観測値だけを残して下さい
keep if tenure >= 20