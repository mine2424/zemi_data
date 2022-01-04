/*-------------------------------
basicStata2.do
stata第2回勉強会
作成者：　西峰
作成日：　２０２１年８月19日
*/-------------------------------

// move reserved file
cd C:\Users\minew\Desktop\zemi_data\basicStata\

// check current path
pwd

// import Global.xlsx file
import excel "C:\Users\minew\Desktop\zemi_data\basicStata\Global.xlsx", sheet("Sheet1") firstrow

// rename variable
label variable year "Year"
label variable month "Month"
label variable temp "Global Temp vs 1901-2000"

// sort of temp (smaller first)
sort temp

// back previous status
use Global, clear

// before 1970 (the "summarize" can Look at the mean and variance, etc.)
summarize temp if year < 1970

// after 1970
summarize temp if year >= 1970

// Jan, Feb of before 1940 and after 1970
summarize temp if (month == 1 | month == 2) & year >= 1940 & year < 1970

// call Canada.std
use Canada, clear

// generate variable (= gen)
generate gap = flife - mlife

// replace result of calculation
replace pop = pop/100
replace pop = pop*100

sum pop

// multiplication by two 
gen pop2 pop^2

// use log
gen lnmlife = log(mlife)

use Canada, clear
// judgement using popMoreAverage
gen popMoreAverage=1 if pop >=4554.769
replace popMoreAverage=0 if pop < 4554.769
keep if pop >= 4554.769

use Canada, clear
// remove variables
drop mlife flife

use Canada, clear
// use reserved variables
keep place pop unemp


