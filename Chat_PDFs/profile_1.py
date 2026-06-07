from PyPDF2 import PdfReader

path = 'summary.pdf'
def myprofile(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# profile = myprofile(path)
# print(profile)