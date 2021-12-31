import os
from PyPDF2 import PdfFileReader

pdf_files = os.listdir(os.getcwd() + '/pdfs')

def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    
    print(info)
	
    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title


if __name__ == '__main__':
	for i in range(len(pdf_files)):
		path = pdf_files[i]
		get_info(path)
