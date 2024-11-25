from .content import Content

class Page:
    def __init__(self):
        self.contents = []
        self.detailed_contents = []

    def add_content(self, content: Content):
        self.contents.append(content)

    def add_detailed_content(self, content: list):
        """
        a list of dict items as {'text': '', 'size': '', 'font': ''}
        """
        self.detailed_contents.extend(content)