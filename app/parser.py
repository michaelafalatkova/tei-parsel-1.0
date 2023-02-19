from abc import ABC

from bs4 import BeautifulSoup, NavigableString, Tag

from app.model import *


class Parser(ABC):

    def parse(self):
        raise NotImplemented


def extract_lines(content) -> list:
    lines = []
    for ix, i in enumerate(content):
        if not isinstance(i, NavigableString):
            if isinstance(i, Tag):
                lines.append(i)
            else:
                lines.append(i.contents)
    return lines


def parse_header(tag: Tag) -> TEIHeader:

    tei_header = TEIHeader()

    for i in tag:
        if i.name == 'titlestmt':
            tei_header.title = i.title.contents[0]
            tei_header.author = i.author.contents[0]
            tei_header.editor = i.editor.contents[0]
        elif i.name == 'editionstmt':
            tei_header.date_translated = i.edition.date.contents[0]
        elif i.name == 'publicationstmt':
            tei_header.pub_authority = i.authority.ref.contents[0]
            tei_header.license = Reference(1, i.availability.p.ref.contents[0], i.availability.p.ref.name,
                                           i.availability.p.ref)
        elif i.name == 'listwit':
            tei_header.witness = i.witness.contents[0]
        elif i.name == 'encodingdesc':
            tei_header.declaration = i.editorialdecl.p.contents[0]
    return tei_header


def create_line_block(ix: int, tag: Tag):
    if tag.name is None:
        return LineBlockText(ix, tag, 'p')

    blocks = {
        "p": LineBlockText(ix, tag.contents[0], tag.name),
        "quote": Quote(ix, tag.contents[0], tag.name),
        "note": Note(ix, tag.contents[0], tag.name),
        "ref": Reference(ix, tag.contents[0], tag.name, tag),
        "s": LineBlock(ix, 'TODO', tag.name),
        "ahe": LineBlock(ix, 'TODO', tag.name),
    }

    return blocks[tag.name]


def parse_multiblock_line(ix: int, i: Tag) -> list:
    ix_line = ix
    ln_blocks = []
    for ix, x in enumerate(i):
        if isinstance(x, NavigableString):
            line_block = create_line_block(ix_line, x)
        elif isinstance(x, Tag):
            if len(x.contents) != 0:
                line_block = create_line_block(ix_line, x)

        ln_blocks.append(line_block)

    return ln_blocks


def create_line(ix: int, i: Tag) -> Line:
    if isinstance(i, Tag):
        if i.name == 'p':
            if len(i) == 1:
                return Line(ix, [create_line_block(ix, i)])
            else:
                # create correct substructures
                return Line(ix, parse_multiblock_line(ix, i))
        else:
            print(i)


def parse_body(tag: Tag) -> list[Page]:

    body_lines = extract_lines(tag)

    pages = []
    page = None
    page_n = 0
    page_l = []
    for ix, i in enumerate(body_lines):
        if i.name == 'pb':
            if page:
                pages.append(page)
                page.lines = page_l
                page_l = []
                page_n = page_n + 1

            page = Page(page_n, i.attrs['facs'], i.attrs['n'])
        else:
            line = create_line(ix, i)
            if line is not None:
                page_l.append(line)
    pages.append(page)
    page.lines = page_l
    return pages


class BeautifulSoupParser(Parser):

    def __init__(self, file_path):
        self.file_path = file_path
        self.tei_document = TEIDocument()
        self.parse()
        self.note_to_page_link()

    def parse(self) -> None:
        with open(self.file_path, 'r') as tei:
            soup = BeautifulSoup(tei, 'lxml')

        d = {i.name: i for i in soup.html.body.tei.children if isinstance(i, Tag)}

        self.tei_document.header = parse_header(d['teiheader'].children)
        self.tei_document.text.pages = parse_body(d['text'].div.children)

    def get_teidocument(self) -> TEIDocument:
        return self.tei_document

    def note_to_page_link(self) -> None:
        for page in self.tei_document.text.pages:
            n = 1
            notes = []
            for line in page.lines:
                for block in line.line_blocks:
                    if isinstance(block, Note):
                        block.number_in_page = n
                        n = n + 1
                        note_link = NoteLink(block)

                        notes.append(note_link)
            page.notes = notes
