class User:
    USER_DB = {}
    BORROWING_LIMIT = 5
    def __init__(self,id):
        self.id = id
        self.borrowedBooks = []
        User.USER_DB[id] = self