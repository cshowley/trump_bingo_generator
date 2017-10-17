import random
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.colors import lightgrey, black
from reportlab.lib.units import cm
import string
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from StringIO import StringIO
import os


quoteList = [
'Build a wall',

'The best\n'+
'people',

"They're good\n"+
"friends of\n"+
"mine",

'Crooked\n'+
'Hillary',

'Muslim ban',

'Kill terror-\n'+
'ist families',

'*Adjusts\n'+
'microphone*',

'HYYUUUGE',

'The best\n'+
'words',

'I know more\n'+
'than the\n'+
'generals',

"I won't re-\n"+
"lease my tax\n"+
"returns",

'Bankruptcy',

'Fake tan line',

'Obama is a\n'+
'Muslim',

'Encourages\n'+
'supporters\n'+
'to violence',

"Doesn't an-\n"+
"swer a\n"+
"question",

"MAKE AMERICA\n"+
"GREAT AGAIN",

'Gets mad at\n'+
'moderators',

'Calls the\n'+
'system\n'+
'rigged',

'Gets caught\n'+
'in a lie',

'I love the\n'+
'uneducated',

'I love the\n'+
'blacks',

'I never\n'+
'said that',

'4 more years\n'+
'of Obama',

"Why shouldn't\n"+
"we use nukes?",

'References\n'+
'Twitter',

'References\n'+
'Bernie\n'+
'Sanders',

'I know X\n'+
'better than\n'+
'anyone',

'Deport all\n'+
'illegal aliens',

'Prevent Syrian\n'+
'refugees from\n'+
'immigrating',

'Bring the jobs\n'+
'back',

'Mexico will pay\n'+
'for the wall',

'Big beautiful\n'+
'door',

"I'm a succ-\n"+
"essful bus-\n"+
"iness man",

'Putin will\n'+
'listen to me',

'I will lead\n'+
'the fight\n'+
'against ISIS',

"They've got\n"+
"the best ...",

'Crowd claps for\n'+
'something awful',

'SAD!',

"Brings up\n"+
"Clinton's\n"+
"health",

"Brings up\n"+
"Dr. Oz show\n"+
"appearance",

"Brings up\n"+
"the Apprentice",

"You're fired",

"Brings up God",

'Makes fun of\n'+
'Clinton',

'References\n'+
'victories in\n'+
'primaries',

'References\n'+
'how close the\n'+
'polls are',

"References\n"+
"Clinton's su-\n"+
"per delegates",

'BONUS\n'+
'SQUARE:\n'+
'UNSTUMP-\n'+
'ABLE',

'BONUS\n'+
'SQUARE:\n'+
'LOOK AT\n'+
 'THAT HAIR',

"Says, 'The\n"+
"blacks",

"Says, 'The\n"+
"gays'",

"No one\n"+
"thought I'd\n"+
"get here",

"I love our\n"+
"veterans",

"References\n"+
"Clinton's email\n"+
"server",

"Let's execute\n"+
"Snowden",

'Bomb ISIS',

'I oppose\n'+
'the Supreme\n'+
'Court judge',

'References\n'+
'Gold Star\n'+
'family',

"We're going\n"+
"to win again",

"Says, 'Massive'",

'Does an\n'+
'impression',

'CHINA',

'Takes side\n'+
'of Charlotte\n'+
'protestors',

'Takes side\n'+
'of Charlotte\n'+
'police',

'I hate\n'+
'racism',

"I'm mis-\n"+
"understood",

'Crime all\n'+
'over the\n'+
'place',

'My supporters\n'+
'are better\n'+
'than yours',

'Repeal\n'+
'Obamacare',

'I love\n'+
'gold',

'Trump\n'+
'Vodka/steaks',

"I've never\n"+
"had a bus-\n"+
"iness fail",

"I've done\n"+
"so much",

"I'm worth\n"+
"$10 billion",

'IRS audit'
]

random.shuffle(quoteList)
quoteList = quoteList[:76]

def list_of_columns(
    numbers=range(1, 76),
    num_of_columns=5,
    num_of_rows=5
):
    slice_length = len(numbers) // num_of_columns
    return [
        sorted(
            random.sample(
                numbers[i * slice_length: (i + 1) * slice_length],
                num_of_rows
            )
        )
        for i in range(num_of_columns)
    ]


def list_of_rows(list_of_columns):
    tmp = [list(row) for row in zip(*list_of_columns)]
    for i,_ in enumerate(tmp):
        for j,num in enumerate(row):
            tmp[i][j] = quoteList[tmp[i][j]]
    return tmp


def insert_free_spaces(numbers, coords=[(2, 2)]):
    return [
        [
            n if not (x, y) in coords else None
            for x, n in enumerate(numbers[y])
        ]
        for y in range(len(numbers))
    ]


def prepend_title_row(numbers):
    return [['T', 'R', 'U', 'M', 'P']] + numbers


def card_data():
    return prepend_title_row(
        insert_free_spaces(
            list_of_rows(
                list_of_columns()
            )
        )
    )


def stylesheet():
    return {
        'bingo': TableStyle(
            [
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEADING', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                ('BOX', (0, 0), (-1, 0), 2.0, black),
                ('BOX', (0, 1), (-1, -1), 2.0, black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (2, 3), (2, 3), lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), lightgrey),
            ]
        ),
    }


def pages(number_of_pages, stylesheet):
    pages = zip(
        [
            Table(
                card_data(),
                5 * [2.5 * cm],  # column widths
                6 * [2.5 * cm],  # row heights
                style=stylesheet['bingo']
            )
            for i in range(number_of_pages)
        ],
        [
            PageBreak()
        ] * number_of_pages
    )
    return [e for p in pages for e in p]


def build_pdf(filename, pages):
    doc = BaseDocTemplate(filename)
    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )
    doc.build(pages)


if __name__ == '__main__':
    n = raw_input('Generate how many bingo cards? ')
    build_pdf('bingo_cards.pdf', pages(int(n), stylesheet()))


    # Using ReportLab to insert image into PDF
    imgTemp1 = StringIO()
    imgDoc1 = canvas.Canvas(imgTemp1)

    # Draw image on Canvas and save PDF in buffer
    imgPath1 = "trump.jpg"
    imgDoc1.drawImage(imgPath1, 262, 481, 71, 71)    ## at (399,760) with size 160x160
    imgDoc1.save()

    # Do the same w/ second image
    imgTemp2 = StringIO()
    imgDoc2 = canvas.Canvas(imgTemp2)

    imgPath2 = "logo.jpg"
    imgDoc2.drawImage(imgPath2, 120, 693, 356, 71)    ## at (399,760) with size 160x160
    imgDoc2.save()



    if os.path.exists('Trump Bingo Cards'):
        pass
    else:
        os.makedirs('Trump Bingo Cards')


    for i in range(int(n)):
        print i
        # Use PyPDF to merge the image-PDF into the template
        page = PdfFileReader(file("bingo_cards.pdf","rb")).getPage(i)
        overlay = PdfFileReader(StringIO(imgTemp1.getvalue())).getPage(0)
        page.mergePage(overlay)

        overlay = PdfFileReader(StringIO(imgTemp2.getvalue())).getPage(0)
        page.mergePage(overlay)

        #Save the result
        output = PdfFileWriter()
        output.addPage(page)
        output.write(file("Trump Bingo Cards/card%s.pdf" % i,"w"))


# Sources:
# http://matthiaseisen.com/articles/bingo/
# http://stackoverflow.com/questions/2925484/place-image-over-pdf
