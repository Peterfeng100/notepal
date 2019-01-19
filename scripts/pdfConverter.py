from fpdf import FPDF
pdf = FPDF()
# imagelist is the list with all image filenames
imagelist = ["scripts/abc.jpg"]
for image in imagelist:
    pdf.add_page()
    pdf.image(image)
pdf.output("yourfile.pdf", "F")