/*-------------------------------
first.do
stata第一回勉強会
作成者：　西峰
作成日：　２０２１年８月５日
*/-------------------------------

*reserve work file*
cd C:\Users\minew\Desktop\basicStata

*import excel file*
import excel "C:\Users\minew\Desktop\basicStata\Canada.xlsx", sheet("Sheet1")

*clear for overwriting file*
clear

*rename variables*
rename A place
rename B pop

*add labels into variables*
label variable place "Place Name"

*save data set*
label data "Canadian data"

*save .dta*
save Canada

*overwriting .dta*
save, replace

*output correlate*
correlate unemp mlife flife

*output tabulate*
tabulate mlife