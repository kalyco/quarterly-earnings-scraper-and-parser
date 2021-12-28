import logging
import os
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
# from xlrd import open_workbook
# from xlutils.save import save

'''
1- Spins up a Google Webdriver
2- Collects all public quarterly reports
3- Use request for curling links
4- Converts each file to XLS saveable format and saves
'''

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'
}
logging.basicConfig(filename='output.log',level=logging.INFO)

url = 'https://ir.daveandbusters.com/quarterly-results'
directory = '/reports'

def setUp():
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	driver = webdriver.Chrome(options=options)
	driver.set_window_size(720, 454)
	driver.get(url)

	return driver

def scrape():
	driver = setUp()
	reports = driver.find_elements(By.CLASS_NAME, 'acc-body') # get list of report links
	quarters = driver.find_elements(By.CLASS_NAME, 'acc-title')
	main_window = driver.current_window_handle
	driver.implicitly_wait(15)
	# wait = WebDriverWait(driver, 10)
	year = 2021
	quarter = 3
	count = 0

	for _ in range(len(reports)):
		print("Opening File %s" % str(count + 1))
		report = reports[count]
		report_button = quarters[count]
		report_button.click() # open dropdown
		
		quarter, year, xls_file = get_filename_by_quarter(year, quarter) # get filename
		results_list = report.find_element(By.TAG_NAME, 'ul') # get list of reports
		report_10_q = results_list.find_elements(By.TAG_NAME, 'li')[2] # get 10-Q element 
		report_10_q_link = report_10_q.find_elements(By.TAG_NAME, 'a')[0]
		report_10_q_link.send_keys(Keys.COMMAND + Keys.RETURN) # Open in new tab
		driver.switch_to.window(driver.window_handles[-1]) # Switch to tab
		
		xls_report = driver.find_element(By.CLASS_NAME, "doc-group")
		xls_report_url = xls_report.find_elements(By.TAG_NAME, 'a')[3].get_attribute('href') # Get url text of report
		# request_=urllib.request.Request(xls_report_url,None,headers) # Use curl to obtain the assembled request
		# response = urllib.request.urlretrieve(xls_report_url, xls_file) # Store the response

		resp = requests.get(xls_report_url, allow_redirects=True)
		# print(resp.headers.get('content-type'))
		output = open(xls_file, 'wb')
		output.write(resp.content)
		time.sleep(1)
		output.close()
		# wb = open_workbook(xls_file)
		# save(wb,os.path.join(resp.content,xls_file))
		# os.listdir(os.cw)
		

		# time.sleep(2)
		
		# request_=urllib.request.Request(xls_report_url,None,headers) # Use curl to obtain the assembled request
		# response = urllib.request.urlopen(request_) # Store the response
		# data = pd.read_excel(response.read())
		# f = open(xls_file, 'wb') # Create file location
		# f.write(response.read()) # Write to file

		driver.close()
		driver.switch_to.window(main_window) # Return to main tab
		count += 1
	driver.quit

def get_filename_by_quarter(year, quarter):
	filename = os.getcwd() + directory + "/" + "dave_and_busters_earnings_" + str(year) + "_Q" + str(quarter) + ".xls"
	quarter = quarter - 1 if quarter > 1 else 4
	year = year if quarter != 4 else year - 1
	return quarter, year, filename

scrape()
