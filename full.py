#!/usr/bin/python
"""
This example demonstrates several features of PyLaTeX.

It includes plain equations, tables, equations using numpy objects, tikz plots,
and figures.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
import os

if __name__ == '__main__':
    image_filename = os.path.join(os.path.dirname(__file__), 'image 1.jpg')

    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('The simple stuff')):
        doc.append('Some regular text and some')
        doc.append(italic('italic text. '))
        doc.append('\nAlso some crazy characters: $&#{}')
        with doc.create(Subsection('Math that is incorrect')):
            doc.append(Math(data=['2*3', '=', 9]))

        with doc.create(Subsection('Cute kitten pictures')):
            with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(image_filename, width='120px')
                kitten_pic.add_caption('Look it\'s on its back')

    doc.generate_pdf('full', clean_tex=False)
