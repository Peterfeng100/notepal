from PyPDF2 import PdfFileMerger

pdfs = ['scripts/test.pdf', 'scripts/yourfile.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")