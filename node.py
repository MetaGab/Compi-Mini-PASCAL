class Node:
    def __init__(self, lexeme, token, row):
        self.lexeme = lexeme
        self.token = token
        self.row = row
        self.next = None

    def __str__(self):
        return self.lexeme

    
    def __repr__(self):
        return self.lexeme