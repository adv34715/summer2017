# To run this code, must have selenium and chrome driver installed.
# please change the chrome_path and path.
# Every time, please change url and new files names
# new file names: change type, and change which expense.
from selenium import webdriver
import os
import shutil
import time

chrome_path = r"/Users/yimengz/dev/chromedriver"
path = '/Users/yimengz/Downloads/'

def downYear(y):
	driver=webdriver.Chrome(chrome_path)
	url = ("http://ohiotreasurer.gov/Transparency/Ohios-Online-Checkbook#State/%s/Agency-Type-is-Any/Agency-is-Any/Expense-Category-is-transfers-and-non-expense(595)/Expense-Class-is-Any/Expense-Type-is-Any/Expense-Code-is-Any/Budget-Line-Item-is-Any/Program-is-Any/Source-of-Money-is-Any/breadcrumbs-is-(0,1,4)/chart-display-is-AccountCode(6)/chart-type-is-pie") %y
	newfilename = y+'-Transfers&NonExpense-Expense-Code.csv'
	newpdfname = y+'-Transfers&NonExpense-Expense-Code-chart.pdf'
	#newfilename = y+'-Transfers&NonExpense-Agency-Type.csv'
	#newpdfname = y+'-Transfers&NonExpense-Agency-Type-chart.pdf'
	driver.get(url)
	time.sleep(5)
	driver.find_element_by_xpath("""//*[@id="divChartActionBar_barChart3"]/div[2]/div/span""").click()
	driver.find_element_by_xpath("""//*[@id="lnkExportSummary"]""").click()

	downloading=True
	while(downloading):
		time.sleep(1)
		if any(file.startswith("State-Transactions_SummaryData_Export") for file in os.listdir(path)):
			downloading=False
    
	for filename in os.listdir(path):

		if filename.startswith("State-Transactions_SummaryData_Export"):
			#print (filename)
			os.rename(os.path.join(path, filename), os.path.join(path, newfilename))
			os.rename(os.path.join(path, 'chart.pdf'), os.path.join(path, newpdfname))
			#os.rename(os.path.join(path, 'chart(1).pdf'), os.path.join(path, newpdfname))
			print(filename,newfilename)
			if any(file.startswith("State-Transactions_SummaryData_Export") for file in os.listdir(path)):
				print(False)
	driver.close();

year=['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']

for y in year:
	downYear(y)