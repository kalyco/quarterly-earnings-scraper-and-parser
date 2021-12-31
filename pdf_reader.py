import os
import re
from PyPDF2 import PdfFileReader

numbers = re.compile(r'\d+(?:\.\d+)?')

# # Helper method
# def update_last_count(report_data, key, last_q_count, line):	
# 	if last_q_count != 1:
# 		last_q_count += 1
# 	else:
# 		report_data[key] = ''.join(i for i in line if i.isdigit())
# 		last_q_count = 0
# 	return report_data, last_q_count

def parse_pdf(path, filename):	
	report_data = {
		"report_quarter": filename
	}

	with open(path, 'rb') as f:
		pdf = PdfFileReader(f, strict=False)
		
		number_of_pages = pdf.getNumPages()
		new_file = open("tmp.txt", "a")
		for i in range(number_of_pages):
			page = pdf.getPage(i)
			text = page.extractText()
			new_file.write(text)
		new_file.close()
	
		f = open("tmp.txt", "r")
		total_revenues_this_q_line = False
		total_revenues_last_q_line = False
		total_operating_costs_this_q_line = False
		total_operating_costs_last_q_line = False

		last_q_count = 0
		for line in f.readlines():
			if total_revenues_last_q_line:
				if last_q_count == 0:
					last_q_count += 1
				else:
					report_data["total_revenues_last_q"] = ''.join(i for i in line if i.isdigit())
					last_q_count = 0
					total_revenues_last_q_line = False

			if total_operating_costs_last_q_line:
				if last_q_count == 0:
					last_q_count += 1
				else:
					report_data["total_operating_costs_last_q"] = ''.join(i for i in line if i.isdigit())
					last_q_count = 0
					total_operating_costs_last_q_line = False
			
			if total_revenues_this_q_line:
				report_data["total_revenues_this_q"] = ''.join(i for i in line if i.isdigit())
				total_revenues_this_q_line = False
				total_revenues_last_q_line = True
					
			if total_operating_costs_this_q_line:
				report_data["total_operating_costs_this_q"] = ''.join(i for i in line if i.isdigit())
				total_operating_costs_this_q_line = False
				total_operating_costs_last_q_line = True
			
			if "Total revenues" in line: total_revenues_this_q_line = True
			if "Total operating costs" in line: total_operating_costs_this_q_line = True


		# net_income_last_q_line = False
		# for line in f.readlines():
		# 	if net_income_last_q_line:
		# 		if last_q_count < 2:
		# 			last_q_count += 1
		# 		else:
		# 			report_data["net_income_last_q"] = ''.join(i for i in line if i.isdigit())
		# 			last_q_count = 0
		# 			total_revenues_last_q_line = False
				
		# 	if "Net income" in line:
		# 		# Net income value shows up on first line
		# 		report_data["net_income_this_q"] = ''.join(i for i in line if i.isdigit())
		# 		net_income_last_q_line = True

		os.remove("tmp.txt")
		print(report_data["total_operating_costs_this_q"])
		print(report_data["total_operating_costs_last_q"])
		print(report_data["total_revenues_this_q"])
		print(report_data["total_revenues_last_q"])
		# print(report_data["net_income_this_q"])
		# print(report_data["net_income_last_q"])

	# change_in_comparable_store_sales = []

	return report_data


if __name__ == '__main__':
	# for i in range(len(pdf_files)):
	report_summary = []
	pdf_files = os.listdir(os.getcwd() + '/pdfs')
	for i in range(2):
		filename = pdf_files[i]
		if filename != ".DS_Store":
			# path = os.getcwd() + '/pdfs/' + filename
			path = os.getcwd() + '/pdfs/' + filename
			
			print("Parsing %s" % filename)
			data = parse_pdf(path, filename)
			report_summary.append(data)
