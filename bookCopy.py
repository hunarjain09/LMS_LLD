class BookCopy:
    BOOK_COPY_DB ={}

    def __init__(self,parentBookId,bookCopyId,isBorrowed = False,rackNumber = float('inf'),borrowedBy=None,borrowedTill=None,libraryId = None):
        self.parentBookId = parentBookId
        self.bookCopyId = bookCopyId
        self.isBorrowed = isBorrowed
        self.rackNumber = rackNumber
        self.borrowedBy = borrowedBy
        self.borrowedTill = borrowedTill
        self.libraryId = libraryId

        BookCopy.BOOK_COPY_DB[self.bookCopyId] = self
        