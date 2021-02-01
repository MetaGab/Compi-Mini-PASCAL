from node import Node
class Lexicon:
    def __init__(self, filename, print_result=True):
        self.error_found = False
        self.head = None
        p = None
        state = 0
        column = None
        tm_value = None
        row_number = 1
        character = 0
        lexeme = ""

        matrix = [ #   L    D    +    -    *    =    <    >    :    .    ,    ;    (    )    {    }    "    %   EB  EOL   NL  TAB  EOF   oc
                   #   0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23
                   [   1,   2, 103, 104, 105, 106,   5,   6,   7, 113, 114, 115, 117, 118,   8, 503,   9, 120,   0,   0,   0,   0,   0, 504], # 0
                   [   1,   1, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], # 1
                   [ 101,   2, 101, 101, 101, 101, 101, 101, 101,   3, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101 ,101], # 2
                   [ 500,   4, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], # 3
                   [ 102,   4, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102], # 4
                   [ 108, 108, 108, 108, 108, 109, 108, 107, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108], # 5
                   [ 110, 110, 110, 110, 110, 111, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110], # 6
                   [ 116, 116, 116, 116, 116, 112, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116], # 7
                   [   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   0,   8,   8,   8,   8,   8,   8, 501,   8], # 8
                   [   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9,   9, 119,   9,   9, 502,   9,   9, 501,   9]  # 9
        ]

        self.reserved_words = {
            'or':200, 'and':201, 'not':202, 'while':203, 'do':204, 'if':205,
            'then':206, 'else':207, 'begin':208, 'end':209, 'div':210,
            'read':211, 'write':212, 'true':213, 'false':214, 'var':215,
            'integer':216, 'real':217, 'string':218,'program':219, 'bool':220,
            'for':221, 'to':222, 'repeat':223, 'until':224 , "writeln":225,
            "break": 226, "continue":227, "clrscr":228
        }

        self.errors = {
            500: "Se esperaba dígito",
            501: "EOF inesperado",
            502: "EOL inesperado",
            503: "Comentario no iniciado",
            504: "Símbolo no válido"
        }

        column_characters = {
            '+':2, '-':3, '*':4, '=':5, '<':6, '>':7, ':':8, '.':9,
            ',':10, ';':11, '(':12, ')':13, '{':14, '}':15, '"':16,
            '%':17, ' ':18, '\r':19, '\n':20,'\t':21,
        }

        try:
            file = open(filename, 'r', newline='\r\n')
            character = True
            while character:
                character = file.read(1)
                if not character:
                    column = 22
                elif character.isalpha():
                    column = 0
                elif character.isdigit():
                    column = 1
                elif character in column_characters:
                    column = column_characters[character]
                    if ord(character) == 10:
                        row_number +=1
                else:
                    column = 23

                tm_value = matrix[state][column]

                if tm_value < 100:
                    state = tm_value
                    if state == 0:
                        lexeme = ""
                    else:
                        lexeme = lexeme + character
                elif tm_value >= 100 and tm_value < 500:
                    if tm_value == 100:
                        tm_value = self.validateReservedWord(lexeme, tm_value)
                    if tm_value in [100,101,102,108,110,116] or tm_value >= 200:
                        file.seek(file.tell()-1)
                    else:
                        lexeme = lexeme + character
                
                    p = self.insertNode(lexeme, tm_value, row_number, self.head, p)
                    state = 0
                    lexeme = ""
                else:
                    self.printErrorMessage(tm_value, character, row_number) 
                    self.error_found = True
                    break
            if print_result:
                self.printNodes(self.head)
        except Exception as e:
            print(e)
        finally:
            try:
                if file:
                    file.close()
            except Exception as e:
                print(e) 

    def printNodes(self, p):
        print("-----------------------+-------+----------")
        print("  {0:20} | {1:5} | {2:5}".format("Lexema", "Token", "Renglon"))
        print("-----------------------+-------+----------")
        while p:
            print("  {0:20} | {1:5} | {2:5}".format(p.lexeme,p.token,p.row))
            p = p.next
        print("-----------------------+-------+----------")

    def validateReservedWord(self, lexeme, token):
        if lexeme in self.reserved_words:
            return self.reserved_words[lexeme]
        return token

    def insertNode(self, lexeme, token, row, head, p):
        node = Node(lexeme, token, row)
        if self.head:
            p.next = node
        else:
            self.head = node
        return node
    
    def printErrorMessage(self, token, character, row):
        if token in self.errors:
            print(" !!! ERROR !!!")
            if character and ord(character) not in [10,13]:
                print('  El error encontrado es: "'+self.errors[token]+'", error',
                token,"caracter '"+character+"' en el renglon", row)
            else:
                print('  El error encontrado es: "'+self.errors[token]+'", error',
                token, "en el renglon", row)

