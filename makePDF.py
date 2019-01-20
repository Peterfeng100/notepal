from pylatex import Document, Figure, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
import os

def fill_page(doc, text, image, image_num):
	print("DEBUG: " + text)
	f = open(text, "r")
	text = f.read()
	image = "../" + image
	print("DEBUG: " + image)
	with doc.create(Subsection("Page " + str(image_num))):
		with doc.create(Figure(position='h!')) as img:
			img.add_image(image, width='300px')
			img.add_caption("Image " + str(image_num))    
		doc.append(text)
	
def makePDF(input_dir, course):
	geometry_options = {"tmargin": "3cm", "lmargin": "3cm", "rmargin":"3cm",  "bmargin":"3cm"}
	doc = Document(course, geometry_options=geometry_options)
    
	doc.preamble.append(Command('title', course))
	doc.preamble.append(Command('author', "notepal"))
	doc.preamble.append(Command('date', NoEscape(r'\today')))
	doc.append(NoEscape(r'\maketitle'))
    
	counter = 1
	big_counter = 1
	for dir in sorted (os.listdir(input_dir,)):
		with doc.create(Section(dir[:4] + str(big_counter))):
			for fname in sorted(os.listdir(os.path.join(input_dir, dir))):
				if fname.endswith(".jpg"):
					fill_page(doc, os.path.join(os.path.join(input_dir, dir), "record" + str(counter) + ".wav.txt"), os.path.join(os.path.join(input_dir, dir), "image" + str(counter) + ".jpg"), counter)
					counter += 1
		counter = 1
	doc.generate_pdf("PDFs/" + course, clean = True, clean_tex=True)
    
if __name__ == "__main__":
	makePDF("Notes/IntroductiontoDatabases", "Introduction to Databases")

