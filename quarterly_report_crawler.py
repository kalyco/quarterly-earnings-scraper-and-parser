import logging
import os
import pandas as pd
from pathlib import Path
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

'''
1- Spins up a Google Webdriver
2- Collects all public quarterly reports
3- Use request for curling links
4- Saves either PDF or XLS files
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
# directory = '/reports'
directory = '/pdfs'

def setUp():
	options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	driver = webdriver.Chrome(options=options)
	driver.set_window_size(720, 454)
	driver.get(url)

	return driver

def scrape_xls():
	driver = setUp()
	reports = driver.find_elements(By.CLASS_NAME, 'acc-body') # get list of report links
	quarters = driver.find_elements(By.CLASS_NAME, 'acc-title')
	main_window = driver.current_window_handle
	driver.implicitly_wait(15)
	year = 2021
	quarter = 3
	count = 0

	for _ in range(len(reports)):
		print("Opening File %s" % str(count + 1))
		report = reports[count]
		report_button = quarters[count]
		report_button.click() # open dropdown
		
		results_list = report.find_element(By.TAG_NAME, 'ul') # get list of reports
		report_10_q = results_list.find_elements(By.TAG_NAME, 'li')[2] # get 10-Q element
		report_10_q_link = report_10_q.find_elements(By.TAG_NAME, 'a')[0]
		report_10_q_link.send_keys(Keys.COMMAND + Keys.RETURN) # Open in new tab
		driver.switch_to.window(driver.window_handles[-1]) # Switch to tab
		
		xls_report = driver.find_element(By.CLASS_NAME, "doc-group")
		# save xls files
		try:
			xls_report_url = xls_report.find_elements(By.TAG_NAME, 'a')[3].get_attribute('href') # Get url text of report
			if xls_report_url == "Form 10-Q":
				quarter, year, xls_file = get_filename_by_quarter(year, quarter, "_Q", ".xls") # get filename
			elif xls_report_url == "Form 10-K":
				quarter, year, xls_file = get_filename_by_quarter(year, quarter, "_K", ".xls") # get filename	
		except Exception as exc:
			print("Exception found %s" % exc)
			driver.close()
			driver.switch_to.window(main_window) # Return to main tab
			quarter = quarter - 1 if quarter > 1 else 4
			year = year if quarter != 4 else year - 1
			count += 1
			continue
		resp = requests.get(xls_report_url, allow_redirects=True)
		output = open(xls_file, 'wb')
		output.write(resp.content)
		time.sleep(1)
		output.close()

		driver.close()
		driver.switch_to.window(main_window) # Return to main tab
		count += 1
	driver.quit

def scrape_pdfs():
	driver = setUp()
	reports = driver.find_elements(By.CLASS_NAME, 'acc-body') # get list of report links
	quarters = driver.find_elements(By.CLASS_NAME, 'acc-title')
	main_window = driver.current_window_handle
	driver.implicitly_wait(15)
	year = 2021
	quarter = 3
	count = 0

	for _ in range(len(reports)):
		print("Opening File %s" % str(count + 1))
		report = reports[count]
		report_button = quarters[count]
		report_button.click() # open dropdown
		
		results_list = report.find_element(By.TAG_NAME, 'ul') # get list of reports
		financial_results = results_list.find_elements(By.TAG_NAME, 'li')[0] # get 10-Q element
		financial_results_link = financial_results.find_elements(By.TAG_NAME, 'a')[0]
		financial_results_link.send_keys(Keys.COMMAND + Keys.RETURN) # Open in new tab
		driver.switch_to.window(driver.window_handles[-1]) # Switch to tab
		
		pdf_report = driver.find_element(By.ID, "content-area")
		# save pdf files
		try:
			pdf_report_url = pdf_report.find_element(By.CLASS_NAME, 'pdf-file-link')
			pdf_report_url = pdf_report_url.find_element(By.CLASS_NAME, 'file')
			pdf_report_url = pdf_report_url.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
			quarter, year, pdf_file = get_filename_by_quarter(year, quarter, "_Q", ".pdf") # get filename	
		except Exception as exc:
			print("Exception found %s" % exc)
			driver.close()
			driver.switch_to.window(main_window) # Return to main tab
			quarter = quarter - 1 if quarter > 1 else 4
			year = year if quarter != 4 else year - 1
			count += 1
			continue
 
		resp = requests.get(pdf_report_url, allow_redirects=True)
		print("teeeeext!!!!")
		print(resp.url)
		filename = Path(pdf_file)
		filename.write_bytes(resp.content)
		time.sleep(1)

		driver.close()
		driver.switch_to.window(main_window) # Return to main tab
		count += 1
	driver.quit


def get_filename_by_quarter(year, quarter, report_type, suffix):
	filename = os.getcwd() + directory + "/" + "dave_and_busters_earnings_" + str(year) + report_type + str(quarter) + suffix
	quarter = quarter - 1 if quarter > 1 else 4
	year = year if quarter != 4 else year - 1
	return quarter, year, filename

scrape_pdfs()
