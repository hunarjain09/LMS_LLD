from collections import defaultdict
class Book:
    BOOK_DB = {}
    def __init__(self,bookId,title,authors,publishers):
        self.bookId = bookId
        self.title = title
        self.authors = authors
        self.publishers = publishers
        self.bookCopies = [] 
        Book.BOOK_DB[self.bookId] = self

    
