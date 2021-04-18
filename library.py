from book import Book
from bookCopy import BookCopy
from user import User
import sys
class Library:
    LIBRARY_DB = {}
    def __init__(self,id,rackCount):
        self.id = id
        self.racks =[]
        for i in range(rackCount):
            self.racks.append('')
        Library.LIBRARY_DB[self.id] = self


    def addBook(self,bookId,title,authors,publishers,copiesDetails):
        if bookId in Book.BOOK_DB:
            print('Book already exist in the DB')
        else:
            book = Book(bookId,title,authors,publishers)
            book.bookCopies=copiesDetails
            self.addCopiesToRacks(copiesDetails,bookId)

        return 

    # TODO: From Different Libraries, Please check that case 
    def addCopiesToRacks(self,copiesDetails,parentBookId):
        placedRacks = []
        # print(copiesDetails,parentBookId,self.racks)
        try:
            for bookCopyId in copiesDetails:
                index = self.racks.index('')
                if bookCopyId not in BookCopy.BOOK_COPY_DB:
                    self.racks[index] = bookCopyId
                    bookCopy = BookCopy(parentBookId,bookCopyId,rackNumber=index,libraryId=self.id)
                    placedRacks.append(index+1)
                else:
                    self.racks[index] = bookCopyId
                    BookCopy.BOOK_COPY_DB[bookCopyId].rackNumber = index
                    placedRacks.append(index+1)

        except:
            print('No racks are available',sys.exc_info()[0])
            return
        
        print('Books added to the racks :: ',",".join(map(str,placedRacks)))

        return

    
    def removeBookCopy(self,bookCopyId):
        try:
            index = self.racks.index(bookCopyId)
            self.racks[index] = ''
            BookCopy.BOOK_COPY_DB[bookCopyId].rackNumber = float('inf')
            print('Removed book copy: ',bookCopyId,' from rack: ',index+1)
        
        except:
            print('Invalid Book Copy ID')
            return float('inf')
        
        return index


    def borrowBook(self,parentBookId,userId,borrowedTill):
        user = User.USER_DB[userId] # TODO: Handle Test Case for Non-Existing User
        if len(user.borrowedBooks) == User.BORROWING_LIMIT:
            print('Overlimit')
            return
        if parentBookId in Book.BOOK_DB:
            parentBook = Book.BOOK_DB[parentBookId]
            sortedBookCopies = sorted(parentBook.bookCopies,key=lambda x : BookCopy.BOOK_COPY_DB[x].rackNumber)

            for bookCopy in sortedBookCopies:
                bookCopyObj = BookCopy.BOOK_COPY_DB[bookCopy]
                if bookCopyObj.rackNumber != float('inf') and bookCopyObj.isBorrowed == False:
                    rackNumber = self.removeBookCopy(bookCopyObj.bookCopyId) # TODO: Check for crash!
                    if rackNumber != float('inf'):
                        bookCopyObj.isBorrowed = True
                        bookCopyObj.borrowedBy = userId
                        bookCopyObj.borrowedTill = borrowedTill
                        user.borrowedBooks.append(bookCopyObj.bookCopyId)
                        print('Borrowed Book from rack: ',rackNumber+1)
                        return
                
            print('Not available')

        else:
            print('Invalid Book Id')
        
        return 

    def borrowBookCopy(self,bookCopyId,userId,borrowedTill):
        user = User.USER_DB[userId]
        if len(user.borrowedBooks) == User.BORROWING_LIMIT:
            print('Overlimit')
            return
        
        rackNumber = self.removeBookCopy(bookCopyId)

        if rackNumber != float('inf'):
            bookCopyObj = BookCopy.BOOK_COPY_DB[bookCopyId]
            bookCopyObj.isBorrowed = True
            bookCopyObj.borrowedBy = userId
            bookCopyObj.borrowedTill = borrowedTill
            user.borrowedBooks.append(bookCopyObj.bookCopyId)
            print('Borrowed Book from rack: ',rackNumber+1)
            return

        print('Not Available because of removal')
        
        return 

    
    def returnBookCopy(self,bookCopyId):
        if bookCopyId in BookCopy.BOOK_COPY_DB:
            bookCopyObj = BookCopy.BOOK_COPY_DB[bookCopyId]
            userId = bookCopyObj.borrowedBy
            try:
                user = User.USER_DB[userId]
                user.borrowedBooks.remove(bookCopyId)
            except:
                print("bookCopyId not present in user's borrowed books")
                return
            bookCopyObj.isBorrowed = False
            bookCopyObj.borrowedBy = None
            bookCopyObj.borrowedTill = None
            self.addCopiesToRacks([bookCopyId],bookCopyObj.parentBookId)
            return
        else:
            print('Invalid Book Copy ID')

        return

    def printBorrowed(self,userId):
        user = User.USER_DB[userId]
        borrowedBooks = map(self.getTuple,sorted(user.borrowedBooks))

        for bookCopyTuple in borrowedBooks:
            print('Book Copy: ',bookCopyTuple[0],' ',bookCopyTuple[1] )
        
        return
            

    def search(self,bookId = None,author = None, publisher = None):
        searchResults = set(BookCopy.BOOK_COPY_DB)
        # TODO: Please check the below code.
        if bookId != None:
            searchResultsBooks = []
            if bookId in Book.BOOK_DB:
                searchResultsBooks = set(Book.BOOK_DB[bookId].bookCopies)
            searchResults.intersection(searchResultsBooks)
   
        if author != None:
            searchResultsAuthor = []
            for bookId in Book.BOOK_DB:
                if author in Book.BOOK_DB[bookId].authors:
                    searchResultsAuthor.extend(Book.BOOK_DB[bookId].bookCopies)
            searchResults.intersection(searchResultsAuthor)

        
        if publisher != None:
            searchResultsPublisher = []
            for bookId in Book.BOOK_DB:
                if author in Book.BOOK_DB[bookId].authors:
                    searchResultsPublisher.extend(Book.BOOK_DB[bookId].bookCopies)
            searchResults.intersection(searchResultsPublisher)

        if len(searchResults) == 0:
            print('No result found !!')
        else:
            sortedBookCopies = sorted(searchResults,key=lambda x : BookCopy.BOOK_COPY_DB[x].rackNumber)
            
            for bookCopyId in sortedBookCopies:
                bookCopyObj = BookCopy.BOOK_COPY_DB[bookCopyId]
                # Copy might belong to different library
                if bookCopyObj.libraryId == self.id:
                    bookId = bookCopyObj.parentBookId
                    book = Book.BOOK_DB[bookId]
                    title = book.title
                    authors = ','.join(book.authors)
                    publishers = ','.join(book.publishers)
                    rackNumber = bookCopyObj.rackNumber
                    borrowedBy = bookCopyObj.borrowedBy
                    dueDate = bookCopyObj.borrowedTill
                    if bookCopyObj.isBorrowed == False:
                        print('Book Copy: ',bookCopyId,' ',bookId,' ',title,' ',authors,' ',publishers,' ',rackNumber)
                    else:
                        rackNumber = -1
                        print('Book Copy: ',bookCopyId,' ',bookId,' ',title,' ',authors,' ',publishers,' ',rackNumber,' ',borrowedBy,' ',dueDate)
                                    
        return


    def getTuple(self,bookCopyId):
        bookCopyObj = BookCopy.BOOK_COPY_DB[bookCopyId]

        return (bookCopyObj.bookCopyId,bookCopyObj.borrowedTill)


