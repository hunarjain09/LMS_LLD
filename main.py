from library import Library
from user import User

myLibrary = Library(1,9)

myLibrary.addBook('1','Hunar',['a','b','c'],['d','e','f'],['1-1','1-2','1-3'])
# myLibrary.removeBookCopy('1-1')
print(myLibrary.racks)

user1 = User('1')

myLibrary.borrowBook('1','1','2020-12-31')
myLibrary.borrowBook('1','1','2020-12-31')
myLibrary.borrowBookCopy('1-3','1','2020-12-31')

print(myLibrary.racks)

# myLibrary.returnBookCopy('1-1')

# print(myLibrary.racks)
print(user1.borrowedBooks)
myLibrary.printBorrowed('1')
myLibrary.search(bookId='1')