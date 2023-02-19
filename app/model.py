class LineBlock(object):
    number: int
    text: str
    type: str

    def __init__(self, number, text, type):
        self.number = number
        self.text = text
        self.type = type


class LineBlockText(LineBlock):
    pass


class Quote(LineBlock):
    pass


class Note(LineBlock):
    number_in_page: int

    def __init__(self, number, text, type):
        super().__init__(number, text, type)
        self.number_in_page = 0


class Reference(LineBlock):
    internal: bool
    link: str

    def __init__(self, number, text, type, content):
        super().__init__(number, text, type)

        if len(content.attrs) != 0:
            self.link = content.attrs['target']
            self.text = content.contents[0]
            self.internal = False

        else:
            for i in content.children:
                if i.name == 'name':
                    self.text = i.contents[0]
            self.internal = True


class Line(object):
    number: int
    line_blocks: list[LineBlock]

    def __init__(self, number, line_blocks):
        self.number = number
        self.line_blocks = line_blocks

    def asdict(self):
        return self.line_blocks


class Page(object):
    number: int
    lines: list[Line]
    link: str
    mark: str
    notes: list[object]

    def __init__(self, number, link, mark):
        self.number = number
        self.lines = []
        self.link = link
        self.mark = mark
        self.notes = []

    def asdict(self):
        d = {'number': self.number,
             'lines': [line.asdict() for line in self.lines],
             'link': self.link,
             'mark': self.mark,
             'notes': [notes.asdict() for notes in self.notes]}
        return d


class NoteLink(object):
    note: Note

    def __init__(self, note):
        self.note = note

    def asdict(self):
        return {'number_in_page': self.note.number_in_page, 'text': self.note.text}


class TEItext(object):
    pages: list

    def __init__(self):
        self.pages = []

    def asdict(self):
        return [page.asdict() for page in self.pages]


class TEIHeader(object):
    title: str
    author: str
    editor: str
    date_translated: str
    pub_authority: str
    license: Reference
    witness: str
    declaration: str

    def __init__(self):
        self.title = None
        self.author = None
        self.editor = None
        self.date_translated = None
        self.pub_authority = None
        self.license = None
        self.witness = None
        self.declaration = None


class TEIDocument(object):
    header: TEIHeader
    text: TEItext

    def __init__(self):
        self.header = TEIHeader()
        self.text = TEItext()

    def asdict(self):
        return {'header': self.header, 'text': self.text.asdict()}
