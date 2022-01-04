/*
learning stata part3
Ryota Nishimine
2021/9/2
*/

rename A place
rename B population
rename C unemployment
rename D mammylife
rename E daddylife
rename F type

label variable place "Place Name"
label variable population "Population in 1995"
label variable unemployment "Poluation unemployed, 1995"
label variable mammylife "Male life expectancy, years"
label variable daddylife "Female life expectancy, years" 
label variable type "Random type"

*comfirm 3 tyspes*
tabulate type

*???*
*error : factor-variable and time-series operators not allowed*
tabulate type, generate(type)

*summarize without type3 in type variables*
sum unemployment if type != "type3"

*Find out if unemployment value is above or below average.* 
gen popMoreAverageUnemployment = 1 if unemployment >=  12.10909
replace popMoreAverageUnemployment = 0 if unemployment <  12.10909


/*~~~~~~using Wage.dta~~~~~~*/


replace exper exper^3

* log of exper plus 1* 
gen lnexper1 = log(exper) + 1

*comfirm median*
tabstat wage, stat(mean, median, min, max, sd)

*Find out if wage value is above or below average.* 
gen popMoreAverageWage = 1 if wage >= 4.7
replace popMoreAverageWage = 0 if wage < 4.7

*leave tenure value above 25 hours*
replace tenure =. if tenure < 25 


/*~~~~~~using auto.dta~~~~~~*/


*相関係数*
correlate weight length

*相対分布表 of price*
ta price

sum


/*~~~~~~using nations.dta~~~~~~*/


*histogram of each countries*
histogram adfert, frequency start(0) width(15) by(country)


/*~~~~~~using global.dta~~~~~~*/

*毎年の平均気温のデータセットになおす*
collapse (mean) temp, by(year)


*extra*
generate gdp1000=gdp/1000
summarize gdp gdp1000