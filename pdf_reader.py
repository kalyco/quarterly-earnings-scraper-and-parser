import os
from PyPDF2 import PdfFileReader

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
		last_q_count = 0
		for line in f.readlines():
			if total_revenues_this_q_line:
				report_data["total_revenues_this_q"] = line
				total_revenues_this_q_line = False
				total_revenues_last_q_line = True
				
			if "Total revenues" in line:
				total_revenues_this_q_line = True

			if total_revenues_last_q_line:
				if last_q_count != 2:
					last_q_count += 1
				else:
					report_data["total_revenues_last_q"] = line
					last_q_count = 0
					total_revenues_last_q_line = False

		# os.remove("tmp.txt")
		print(report_data)

	total_revenues_this_q = []
	total_revenues_last_q = []
	total_operating_costs_this_q = []
	total_operating_costs_last_q = []
	net_income_this_q = []
	net_income_last_q = []
	change_in_comparable_store_sales = []

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
