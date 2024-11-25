import pdfplumber
from typing import Optional
from ai_translator.book import Book, Page, Content, ContentType, TableContent
from ai_translator.translator.exceptions import PageOutOfRangeException
from ai_translator.utils import LOG


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()
                raw_text_chars = pdf_page.chars

                lines = []
                for char in raw_text_chars:
                    char_top = char.get("top", None)
                    matching_line = None
                    for l in lines:
                        lt = l.get("top", None)
                        if lt and (char_top < lt + 5) and (char_top > lt - 5):
                            matching_line = l
                            l['chars'].append(char.get("text", None))
                    if not matching_line:
                        lines.append({'text': ''.join([char.get("text",None)]), 'size': char.get('size', None), 'font': char.get('fontname', 'SimSun')})

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text and lines:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    page.add_detailed_content(lines)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")



                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                book.add_page(page)

        return book