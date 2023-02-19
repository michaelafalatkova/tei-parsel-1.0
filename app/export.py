from abc import ABC

from app.model import *

from jinja2 import Environment, select_autoescape, FileSystemLoader


class Export(ABC):

    def export(self) -> None:
        raise NotImplemented


class HtmlExport(Export):

    def __init__(self, tei_document: TEIDocument) -> None:
        self.tei_document = tei_document

    def export(self):
        env = Environment(
            loader=FileSystemLoader('./app/templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('./index.html')
        return template.render(pages=self.tei_document.text.asdict(), header=self.tei_document.header)


class SqlLiteExport(Export):

    def __init__(self, tei_document: TEIDocument) -> None:
        self.tei_document = tei_document

    def export(self) -> None:
        pass
