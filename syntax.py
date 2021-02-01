from node import Node
class Syntax:
    def __init__(self, head, print_result=True):
        self.error_found = False
        self.errors = {
            505: 'Se esperaba "program"',
            506: 'Se esperaba identificador',
            507: 'Se esperaba ";"',
            508: 'Se esperaba "."',
            509: 'Se esperaba ":"',
            510: 'Se esperaba "string", "real" o "integer"',
            511: 'Se esperaba "begin"',
            512: 'Se esperaba "end"',
            513: 'No es una sentencia',
            514: 'Se esperaba ":="',
            515: 'Se esperaba "("',
            516: 'Se esperaba ")"',
            517: 'Se esperaba "then"',
            518: 'Se esperaba "do"',
            519: 'Se esperaba identificador, cadena o número',
            520: 'Código después de punto final',
            521: 'Variable ya declarada',
            522: 'Variable no puede declararse con mismo identificador que el programa',
            523: 'Variable no declarada',
            524: 'Identificador de programa no puede ser usado como variable',
            525: 'Incompatibilidad de tipos',
            526: 'Se esperaba condición booleana',
            527: 'Se esperaba asignación',
            528: 'Se esperaba "to"',
            529: 'Se esperaba limite numérico',
            530: 'Se esperaba contador numérico',
            531: 'Se esperaba "until"',
            532: '"break" debe encontrarse dentro de estructura de repetición',
            533: '"continue" debe encontrarse dentro de estructura de repetición',
        }
        self.vars = {}
        self.program_id = ""
        self.polish = []
        self.if_level = 0
        self.while_level = 0
        self.for_level = 0
        self.repeat_level = 0
        self.last_control = ["",""]
        self.operators = []
        self.polish_code = []
        self.priority = {":=":0, "or":1, "and":2, "not":3, "<":4, 
                        ">":4, "<=":4, ">=":4, "=":4, "<>":4, "+":5, 
                        "-":5, "*":6, "div":6, "%":6, "s+":7, "s-":7}
        self.type_id = {"integer": 0, "real":1, "string":2, "bool": 3}
        self.token_vars = {101: "integer", 102:"real", 119:"string", 213:"bool", 214:"bool"}
        self.type_system = {
            "+": [['integer', 'real', 'string', 'error'],
                 ['real', 'real', 'string', 'error'],
                 ['string', 'string', 'string', 'error'],
                 ['error', 'error', 'error', 'error']],
            "-": [['integer', 'real', 'error', 'error'],
                 ['real', 'real', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "*": [['integer', 'real', 'error', 'error'],
                 ['real', 'real', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "%": [['integer', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "div":[['integer', 'real', 'error', 'error'],
                 ['real', 'real', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            ":=":[['integer', 'real', 'error', 'error'],
                 ['integer', 'real', 'error', 'error'],
                 ['error', 'error', 'string', 'error'],
                 ['error', 'error', 'error', 'bool']],
            ">":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "<":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            ">=":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "<=":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error']],
            "=":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'bool', 'error'],
                 ['error', 'error', 'error', 'bool']],
            "<>":[['bool', 'bool', 'error', 'error'],
                 ['bool', 'bool', 'error', 'error'],
                 ['error', 'error', 'bool', 'error'],
                 ['error', 'error', 'error', 'bool']],
            "and":[['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'bool']],
            "or":[['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'error'],
                 ['error', 'error', 'error', 'bool']],
            "not":['error', 'error', 'error', 'bool'],
            "s+":['integer', 'real', 'error', 'bool'],
            "s-":['integer', 'real', 'error', 'bool']
        }
        p, code = self.program(head)
        if code:
            self.error_found = True
            if code == 525:
                print(p[0])
                return
            print(" !!! ERROR !!!")
            print_error = '  El error encontrado es: '+self.errors[code]+', error '+str(code)
            self.error_found = True
            if p:
                print_error += " en la fila " + str(p.row)
            print(print_error)
            return
        if print_result:
            self.print_variables()


    def print_variables(self):
        print("+--------------------------------------+")
        print("| Identificador de programa            |")
        print("+--------------------------------------+")
        print("| {0:36} |".format(self.program_id))
        print("+--------------------------------------+\n")
        
        print("+--------------------------------------+")
        print("| Lista de variables                   |")
        print("+--------------------------------------+")
        print("| ID de variable    | Tipo de dato     |")
        print("+--------------------------------------+")
        for v in self.vars:
            print("| {0:17} | {1:16} |".format(v,self.vars[v]["type"]))
        print("+--------------------------------------+")

        for v in self.vars:
            if not self.vars[v]["used"]: 
                print('ALERTA: Variable "%s" no utilizada' % v) 

    def add_operator(self, operator):
        if operator.lexeme == "(":
            self.operators.append(operator)
            return
        if operator.lexeme == ")":
            while self.operators[-1].lexeme != "(":
                self.polish.append(self.operators.pop())
            self.operators.pop()
            return
        elif self.operators and self.operators[-1].lexeme != "(" and \
            self.priority[self.operators[-1].lexeme] >= self.priority[operator.lexeme]:
            self.polish.append(self.operators.pop())
            self.add_operator(operator)
            return
        self.operators.append(operator)

    def check_error_polish(self, row):
        for p in self.operators[::-1]:
            self.polish.append(p)
        types = []
        result = ""
        for p in self.polish:
            if p.lexeme in self.vars:
                types.append(self.vars[p.lexeme]["type"])
            elif p.token in [101, 102, 119, 213, 214]:
                types.append(self.token_vars[p.token])
            else:
                type_1 = types.pop()
                if p.lexeme in ["not", "s+", "s-"]:
                    result = self.type_system[p.lexeme][self.type_id[type_1]]
                    if result == "error":
                        return '  El error encontrado es: Incompatibilidad de tipos, operador "'+ \
                            p.lexeme+'" incompatible con tipo "'  +type_1+'", error 525 en la fila '+ \
                            str(row), 525
                else:
                    type_2 = types.pop()
                    result = self.type_system[p.lexeme][self.type_id[type_1]][self.type_id[type_2]]
                    if result == "error":
                        return '  El error encontrado es: Incompatibilidad de tipos, operador "'+ \
                            p.lexeme+'" incompatible con tipos "' + type_2+'" y "'+ type_1 + \
                            '", error 525 en la fila ' + str(row), 525
                types.append(result)
        self.polish_code += self.polish
        self.polish = []
        self.operators = []
        return types.pop(), 0

    def program(self, p):
        if not p or p.token != 219:                
            return p, 505
        p = p.next
        if not p or p.token != 100:              
            return p, 506
        self.program_id = p.lexeme    
        p = p.next
        if not p or p.token != 115:            
            return p, 507
        p = p.next
        p, code = self.block(p)                   
        if code:
            return p, code
        if not p or p.token != 113:            
            return p, 508
        p = p.next
        if p:
            return p, 520
        return p, 0
            
    def block(self, p):
        p, code = self.var_declaration_part(p)    
        if code:
            return p, code
        p, code = self.compound_statement(p)     
        if code:
            return p, code
        return p, 0

    def var_declaration_part(self, p):
        if not p or p.token != 215:               
            return p, 0
        p = p.next
        p, code = self.variable_declaration(p)      
        if code:
            return p, code
        if not p or p.token != 115:              
            return p, 507 
        p = p.next
        while p and p.token == 100:                 
            p, code = self.variable_declaration(p)  
            if code:
                return p, code
            if not p or p.token != 115:           
                return p, 507 
            p = p.next
        return p, code
    
    def variable_declaration(self, p):
        if not p or p.token != 100:              
            return p, 506
        ids = [p]
        p = p.next
        while p and p.token == 114:             
            p = p.next
            if not p or p.token != 100:           
                return p, 506
            ids.append(p)
            p = p.next
        if not p or p.token != 116:                
            return p, 509
        p = p.next
        p, code, var_type = self.type(p)
        if code:
            return p, code
        for i in ids:
            if i.lexeme in self.vars:
                return i, 521
            elif i.lexeme == self.program_id:
                return i, 522
            self.vars[i.lexeme] = {"type": var_type, "used": False}
        return p, 0

    def type(self, p):
        if not p or not p.token in [216, 217, 218, 220]: 
            return p, 510, "error"
        var_type = p.lexeme
        p = p.next
        return p, 0, var_type
    
    def compound_statement(self, p):
        if not p or p.token != 208:                
            return p, 511
        p = p.next
        p, code = self.statement(p)
        if code:
            return p, code
        while p and p.token == 115:                
            p = p.next
            p, code = self.statement(p)          
            if code:
                return p, code
        if not p or p.token != 209:                 
            return p, 512
        p = p.next
        return p, 0

    def statement(self, p):
        p, code = self.assign_statement(p)
        if code != 1:
            return p, code
        p, code = self.read_statement(p)
        if code != 1:
            return p, code
        p, code = self.write_statement(p)        
        if code != 1:
            return p, code   
        p, code = self.routine_statement(p)        
        if code != 1:
            return p, code   
        p, code = self.while_statement(p)   
        if code != 1:
            return p, code
        p, code = self.if_statement(p)        
        if code != 1:
            return p, code
        p, code = self.for_statement(p)        
        if code != 1:
            return p, code
        p, code = self.repeat_statement(p)        
        if code != 1:
            return p, code
        p, code = self.compound_statement(p)   
        if code == 511:         
            return p, 513
        return p, code
    
    def assign_statement(self, p, called_in_for=False):
        if not p or p.token != 100:
            return p, 1
        if p.lexeme == self.program_id:
            return p, 524
        if p.lexeme not in self.vars:
            return p, 523
        self.vars[p.lexeme]["used"] = True
        self.polish.append(p)
        p = p.next
        if not p or p.token != 112:
            return p, 514
        self.add_operator(p)
        p = p.next
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op
        if called_in_for and not op[0] in ["integer", "real"]:
            return p, 530
        return p, 0
    def routine_statement(self, p):
        if not p or p.token not in [226, 227, 228]:
            return p, 1
        if p.token == 226:
            if self.last_control[0] == "while":
                self.polish_code.append("BRI-C"+str(self.last_control[1]))
            elif self.last_control[0] == "for":
                self.polish_code.append("BRI-F"+str(self.last_control[1]))
            elif self.last_control[0] == "repeat":
                self.polish_code.append("BRI-H"+str(self.last_control[1]))
            else:
                return p, 532
        elif p.token == 227:
            if self.last_control[0] == "while":
                self.polish_code.append("BRI-D"+str(self.last_control[1]))
            elif self.last_control[0] == "for":
                self.polish_code.append("BRI-I"+str(self.last_control[1]))
            elif self.last_control[0] == "repeat":
                self.polish_code.append("BRI-J"+str(self.last_control[1]))
            else:
                return p, 533
        elif p.token == 228:
            self.polish_code.append(p)
        p = p.next
        return p,0

    def read_statement(self, p):
        if not p or p.token != 211:
            return p, 1
        p_read = p
        p = p.next
        if not p or p.token != 117:
            return p, 515
        p = p.next
        if not p or p.token != 100:
            return p, 506
        if p.lexeme == self.program_id:
            return p, 524
        if p.lexeme not in self.vars:
            return p, 523
        self.vars[p.lexeme]["used"] = True
        self.polish_code.append(p)
        self.polish_code.append(p_read)
        p = p.next
        while p and p.token == 114:
            p = p.next
            if not p or p.token != 100:
                return p, 506
            if p.lexeme not in self.vars:
                return p, 523
            self.polish_code.append(p)
            self.polish_code.append(p_read)
            p = p.next
        if not p or p.token != 118:
            return p, 516
        p = p.next
        return p, 0

    def write_statement(self, p):
        if not p or p.token not in [212, 225]:
            return p, 1
        p_write = p
        p = p.next
        if not p or p.token != 117:
            return p, 515
        p = p.next
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op, 525
        self.polish_code.append(Node("write",212,p.row))
        while p and p.token == 114:
            p = p.next
            p, code = self.expression(p)
            if code:
                return p, code
            op = self.check_error_polish(p.row)
            if op[1]:
                return op, 525
            self.polish_code.append(Node("write",212,p.row))
        if not p or p.token != 118:
            return p, 516
        p = p.next
        if p_write.token == 225:
            self.polish_code.append("writeln")
        return p, 0

    def if_statement(self, p):
        if not p or p.token != 205:
            return p, 1
        p = p.next
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op
        if op[0] != "bool":
            return p, 526
        level = self.if_level
        self.if_level += 1
        self.polish_code.append("BRF-A"+str(level))
        if not p or p.token != 206:
            return p, 517
        p = p.next
        p, code = self.statement(p)
        if code:
            return p, code
        self.polish_code.append("BRI-B"+str(level))
        self.polish_code.append("A"+str(level)+":")
        if p and p.token == 207:
            p = p.next
            p, code = self.statement(p)
            if code:
                return p, code
        self.polish_code.append("B"+str(level)+":")
        return p, 0
    
    def while_statement(self, p):
        if not p or p.token != 203:
            return p, 1
        p = p.next
        level = self.while_level
        self.while_level += 1
        self.polish_code.append("D"+str(level)+":")
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op
        if op[0] != "bool":
            return p, 526
        self.polish_code.append("BRF-C"+str(level))
        if not p or p.token != 204:
            return p, 518
        p = p.next
        self.last_control = ["while",level]
        p, code = self.statement(p)
        self.last_control =  ["while",level]
        if code:
            return p, code
        self.polish_code.append("BRI-D"+str(level))
        self.polish_code.append("C"+str(level)+":")
        self.last_control =["",""]
        return p, 0

    def for_statement(self, p):
        if not p or p.token != 221:
            return p, 1
        p = p.next
        p_counter = p
        p, code = self.assign_statement(p, True)
        if code:
            if code == 1:
                return p, 527
            return p, code 
        level = self.for_level
        self.for_level += 1
        self.polish_code.append("G"+str(level)+":")
        self.polish_code.append(p_counter)
        if not p or p.token != 222:
            return p, 528
        p = p.next
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op
        if not op[0] in ["integer", "real"]:
            return p, 529
        self.polish_code.append(Node("<=", 109, p.row))
        self.polish_code.append("BRF-F"+str(level))
        if not p or p.token != 204:
            return p, 518
        p = p.next
        self.last_control = ["for",level]
        p, code = self.statement(p)
        self.last_control = ["for",level]
        if code:
            return p, code
        self.polish_code.append("I"+str(level)+":")
        self.polish_code.append(p_counter)
        self.polish_code.append(p_counter)
        self.polish_code.append(Node("1",101,p_counter.row))
        self.polish_code.append(Node("+",103,p_counter.row))
        self.polish_code.append(Node(":=",112,p_counter.row))
        self.polish_code.append("BRI-G"+str(level))
        self.polish_code.append("F"+str(level)+":")
        self.last_control = ["",""]
        return p, 0

    def repeat_statement(self, p):
        if not p or p.token != 223:
            return p, 1
        p = p.next
        level = self.repeat_level
        self.repeat_level += 1
        self.polish_code.append("E"+str(level)+":")
        self.last_control=["repeat", level]
        p, code = self.statement(p)
        self.last_control=["repeat", level]
        if code:
            return p, code
        if not p or p.token != 224:
            return p, 531
        self.polish_code.append("J"+str(level)+":")
        p = p.next
        p, code = self.expression(p)
        if code:
            return p, code
        op = self.check_error_polish(p.row)
        if op[1]:
            return op
        if op[0] != "bool":
            return p, 526
        self.polish_code.append("BRF-E"+str(level))
        self.polish_code.append("H"+str(level)+":")
        self.last_control=["",""]
        return p, 0

    def expression(self, p):
        p, code = self.simple_expression(p)
        if code:
            return p, code
        p, code = self.relational_operator(p)
        if code:
            p, code = self.simple_expression(p)
            if code:
                return p, code
        return p, 0
    
    def relational_operator(self, p):
        if p and p.token in [106, 107, 108, 109, 110, 111]:
            self.add_operator(p)
            p = p.next
            return p, 1
        return p, 0
        
    def simple_expression(self, p):
        p = self.sign(p)
        p, code = self.term(p)
        if code:
            return p, code
        while p and p.token in [103, 104, 200]:
            p = self.adding_operator(p) 
            p, code = self.term(p)
            if code:
                return p, code
        return p, 0
    
    def sign(self, p):
        if p and p.token in [103, 104]:
            n = Node("s"+p.lexeme, p.token, p.row)
            self.add_operator(n)
            p = p.next
        return p
    
    def adding_operator(self, p):
        if p and p.token in [103, 104, 200]:
            self.add_operator(p)
            p = p.next
        return p
    
    def term(self, p):
        p, code = self.factor(p)
        if code:
            return p, code
        while p and p.token in [105, 120, 210, 201]:
            p = self.multiplying_operator(p)
            p, code = self.factor(p)
            if code:
                return p, code
        return p, 0
    
    def multiplying_operator(self, p):
        if p and p.token in [105, 120, 210, 201]:
            self.add_operator(p)
            p = p.next
        return p
    
    def factor(self, p):
        if p and p.token in [100, 101, 102, 119, 213, 214]:
            if p.token == 100:
                if p.lexeme == self.program_id:
                    return p, 524
                if p.lexeme not in self.vars:
                    return p, 523
                self.vars[p.lexeme]["used"] = True
            self.polish.append(p)
            p = p.next
            return p, 0
        if p and p.token == 202:
            self.add_operator(p)
            p = p.next
            p, code = self.factor(p)
            if code:
                return p, code
            return p, 0
        if p and p.token == 117:
            self.add_operator(p)
            p = p.next
            p, code = self.expression(p)
            if code:
                return p, code
            if not p or p.token != 118:
                return p, 516
            self.add_operator(p)
            p = p.next
            return p, 0
        return p, 519