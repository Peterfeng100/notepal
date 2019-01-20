from pylatex import Document, Figure, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
import os


def fill_page(doc, section, text, image, image_num):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    print("DEBUG: " + text)
    print("DEBUG: " + image)
    f = open(text, "r")
    text = f.read()
    with doc.create(Section(section)):
		with doc.create(Subsection("Page " + str(image_num))):
			with doc.create(Figure(position='h!')) as img:
				img.add_image(image, width='300px')
                img.add_caption("Image " + str(image_num))    
		doc.append(text)
	
def makePDF(input_dir, course):
	doc = Document(course)

	doc.preamble.append(Command('title', course))
	doc.preamble.append(Command('author', "Notepal"))
	doc.preamble.append(Command('date', NoEscape(r'\today')))
	doc.append(NoEscape(r'\maketitle'))
    
	counter = 1
	for dir in sorted (os.listdir(input_dir,)):
		for fname in sorted(os.listdir(os.path.join(input_dir, dir))):
			if fname.endswith(".jpg"):
				fill_page(doc, dir, os.path.join(os.path.join(input_dir, dir), record + ".wav.txt"), os.path.join(os.path.join(input_dir, dir), fname), counter)
				counter += 1
		counter = 1
	doc.generate_pdf(os.path.join("PDFs", course), clean_tex=False)
    
if __name__ == "__main__":
	makePDF("Notes/Algorithms and Data Structures", "Algorithms and Data Structures")

